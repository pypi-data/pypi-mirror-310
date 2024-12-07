from datamax.parser import DatamaxProgram
from enum import Enum
import pathlib
import os
import pendulum
import hashlib
from datamax.types import (
    Annotation,
    BaseStep,
    Descriptor,
    ImageManifest,
    MediaType,
    RunStep,
    StepType,
    IngestStep,
    StepWithSource,
    OCILayout,
    IndexJSON,
)
from datamax.console import console
import duckdb
import tempfile
from typing import List
from datamax.utils import (
    get_file_digest,
    make_tarfile,
    generate_name,
    move_file_to_blobs,
)
from datamax.config import CONFIG
from pathlib import Path
import subprocess


class SupportedExtensions(Enum):
    CSV = ".csv"


class Builder:
    layers: List[Descriptor]

    def __init__(self, program: DatamaxProgram, image_name: str = "", tag: str = ""):
        self.program = program
        self.layers = []
        self.name = generate_name(image_name, 2)
        self.tag = tag if tag else "latest"
        self.build_home = CONFIG.datamax_home / "images" / self.name / self.tag
        self.build_home.mkdir(parents=True, exist_ok=True)
        self.index_json = IndexJSON(annotations={Annotation.IMAGE_VERSION.value: self.tag})
        self.init_build_dir()

    def init_build_dir(self):
        oci_layout_path = self.build_home / "oci-layout"
        oci_layout = OCILayout()
        with open(oci_layout_path, "w") as f:
            f.write(oci_layout.model_dump_json(by_alias=True))

    def finish(self):
        manifest_digest = self.write_manifest()
        manifest_descriptor = Descriptor(
            media_type=self.manifest.media_type,
            digest=manifest_digest["digest"],
            size=manifest_digest["size"],
            annotations=self.manifest.annotations,
        )
        self.index_json.manifests.append(manifest_descriptor)
        index_json_path = self.build_home / "index.json"
        with open(index_json_path, "w") as f:
            f.write(self.index_json.model_dump_json(by_alias=True))

    @classmethod
    def list_images(cls):
        images = []
        datamax_home = CONFIG.datamax_home
        build_dir = datamax_home / "images"
        try:
            image_dirs = os.listdir(build_dir)
        except FileNotFoundError:
            return images
        tag = "latest"
        digest = "UNKNOWN"
        created = "UNKNOWN"
        for directory in build_dir.iterdir():
            for tag_dir in directory.iterdir():
                image_path = build_dir / directory / tag_dir
                index_file = image_path / "index.json"
                with open(index_file, "r") as f:
                    index_json = IndexJSON.model_validate_json(f.read())
                for manifest in index_json.manifests:
                    if manifest.media_type == MediaType.IMAGE_MANIFEST:
                        tag = (
                            manifest.annotations.get(Annotation.IMAGE_VERSION.value)
                            if manifest.annotations
                            else tag_dir.stem
                        )
                        created = pendulum.parse(
                            manifest.annotations.get(Annotation.CREATED.value, "")
                            if manifest.annotations
                            else ""
                        )
                        created_duration = (pendulum.now() - created).in_words()
                        digest = manifest.digest.split(":")[1][-12:]
                        break
                images.append(
                    {
                        "name": directory.stem,
                        "tag": tag,
                        "created": f"{created_duration} ago",
                        "digest": digest,
                    }
                )
        return images

    @classmethod
    def from_file(cls, filepath, image_name: str = "", tag: str = ""):
        program = DatamaxProgram.from_file(filepath)
        return cls(program, image_name, tag)

    def write_manifest(self):
        manifest_json = self.manifest.model_dump_json(by_alias=True)
        manifest_bytes = manifest_json.encode()
        digest = hashlib.sha256(manifest_bytes).hexdigest()
        with open(self.build_home / "blobs" / "sha256" / digest, "wb") as f:
            f.write(manifest_bytes)
        digest = {"digest": f"sha256:{digest}", "size": len(manifest_bytes)}
        return digest

    def run_program(self):
        with tempfile.TemporaryDirectory() as tempdir:
            parsed_path = pathlib.Path(tempdir)
            for stmt in self.program.steps:
                self.process_build_step(parsed_path, stmt)
        self.finish()

    def process_build_step(self, tempdir: pathlib.Path, stmt: BaseStep):
        match stmt.type:
            case StepType.INGEST:
                assert isinstance(stmt, IngestStep)
                self.process_ingest_step(tempdir, stmt)
            case StepType.EXTEND:
                assert isinstance(stmt, StepWithSource)
                self.process_extend_step(stmt)
            case StepType.RUN:
                assert isinstance(stmt, RunStep)
                self.process_run_step(stmt)
            case _:
                raise ValueError(f"Unknown statement type: {stmt['type']}")

    def process_run_step(self, stmt: RunStep):
        console.log(f"Running command: {stmt.command}")
        with tempfile.TemporaryDirectory() as tempdir:
            process = subprocess.run(
                stmt.command,
                env={
                    **os.environ,
                    "OUT_DIR": Path(tempdir).resolve().as_posix()
                }
            )
            for output in Path(tempdir).iterdir():
                ingest_step = IngestStep(type=StepType.INGEST, source=output, destination=output.stem, source_extensions=output.suffixes)
                self.process_ingest_step(Path(tempdir), ingest_step)

    def process_ingest_step(self, tempdir: pathlib.Path, stmt: IngestStep):
        filetypes = stmt.source_extensions
        full_extension = "".join(filetypes)
        match full_extension:
            case SupportedExtensions.CSV.value:
                console.log("CSV file detected")
                result = self.process_csv_ingest(tempdir, stmt)
            case _:
                raise ValueError(
                    f"Unsupported file type: {stmt.source} - detected {full_extension}"
                )
        self.add_to_layers(tempdir, result)

    def add_to_layers(self, tempdir: pathlib.Path, result: pathlib.Path):
        blobs_dir = self.build_home / "blobs"
        blobs_dir.mkdir(parents=True, exist_ok=True)
        tarfile = make_tarfile(tempdir / f"{result.name}.tar", result)
        digest = get_file_digest(tarfile)
        layer = Descriptor(media_type=MediaType.IMAGE_TAR_GZIP, **digest)
        move_file_to_blobs(blobs_dir, tarfile, digest["digest"])
        self.layers.append(layer)

    def process_extend_step(self, stmt: StepWithSource): ...

    def process_csv_ingest(self, tempdir: pathlib.Path, stmt: IngestStep):
        conn = duckdb.connect(":memory:")
        conn.execute(
            f"CREATE TABLE {stmt.destination} AS SELECT * FROM read_csv_auto('{stmt.source}')"
        )
        conn.execute(f"""EXPORT DATABASE '{tempdir / stmt.destination}' (
            FORMAT PARQUET,
            COMPRESSION ZSTD,
            ROW_GROUP_SIZE 100_000
        );""")
        return tempdir / stmt.destination

    @property
    def manifest(self) -> ImageManifest:
        return ImageManifest(
            schema_version=2,
            media_type=MediaType.IMAGE_MANIFEST,
            config=Descriptor(media_type=MediaType.EMPTY_JSON, **get_file_digest()),
            layers=self.layers,
            annotations={
                Annotation.IMAGE_VERSION.value: self.tag,
                Annotation.CREATED.value: pendulum.now().isoformat(),
            },
        )
