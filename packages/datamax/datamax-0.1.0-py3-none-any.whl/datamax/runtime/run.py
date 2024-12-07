import hashlib
import io
import tarfile
import tempfile
from pathlib import Path
from typing import Literal

from pyarrow import parquet

from datamax.config import CONFIG
from datamax.console import console
from datamax.types import Descriptor, ImageManifest, IndexJSON, MediaType


class Runner:
    def __init__(self, image_ref: str):
        self.image_ref = image_ref
        self.working_dir = CONFIG.datamax_home / "images" / self.image_name / self.tag

    @property
    def tag(self):
        image_parts = self.image_ref.split(":")
        return image_parts[1] if len(image_parts) > 1 else "latest"

    @property
    def image_name(self):
        return self.image_ref.split(":")[0]

    def read_manifest(self, blobs_dir, manifest_algo: str, manifest_name: str):
        with open(blobs_dir / manifest_algo / manifest_name) as f:
            manifest_json = ImageManifest.model_validate_json(f.read())
        return manifest_json

    def run(self, runtime: Literal["duckdb", "postgresql"] = "duckdb"):
        console.log(f"Running image {self.image_name} with tag {self.tag}...")
        blobs_dir = self.working_dir / "blobs"
        with open(self.working_dir / "index.json") as f:
            index_json = IndexJSON.model_validate_json(f.read())
        with tempfile.TemporaryDirectory() as tempdir:
            for manifest in index_json.manifests:
                blob_algo, blob_name = manifest.digest.split(":")
                manifest = self.read_manifest(blobs_dir, blob_algo, blob_name)
                for layer in manifest.layers:
                    self.handle_layer(tempdir, layer)
            match runtime:
                case "duckdb":
                    import duckdb

                    conn = duckdb.connect(":memory:")
                    for directory in Path(tempdir).iterdir():
                        conn.execute(f"IMPORT DATABASE '{directory}'")
                    console.log("Running DuckDB...")
                    breakpoint()
                    return conn
                case "postgresql":
                    import psycopg

                    conn = psycopg.connect("dbname=postgres", autocommit=True)
                    for directory in Path(tempdir).iterdir():
                        with psycopg.connect("dbname=postgres") as inner_conn:
                            inner_cur = inner_conn.cursor()
                            with open(directory / "schema.sql", "r") as f:
                                schema = f.readlines()
                                statements = [
                                    line.strip() for line in schema if line.strip()
                                ]
                                for stmt in statements:
                                    inner_cur.execute(stmt)
                            parquet_files = [
                                file
                                for file in directory.iterdir()
                                if file.suffix == ".parquet"
                            ]
                            for file in parquet_files:
                                table_name = file.stem
                                table = parquet.read_table(file)
                                keys = table.to_pydict().keys()
                                values_stmt = ", ".join(["%s"] * len(keys))
                                inner_cur.executemany(
                                    f"INSERT INTO {table_name} VALUES ({values_stmt})",
                                    table.to_pydict().values(),
                                )
                            inner_conn.commit()
                case _:
                    raise Exception(f"Unsupported runtime {runtime}")

    def handle_layer(self, tempdir: str, layer: Descriptor):
        temp_path = Path(tempdir).resolve()
        blob_algo, blob_name = layer.digest.split(":")
        blob_path = self.working_dir / "blobs" / blob_algo / blob_name
        with open(blob_path, "rb") as f:
            bytes = f.read()
            file_hash = hashlib.sha256(bytes).hexdigest()
            if not file_hash == blob_name:
                raise Exception(f"Hash mismatch for {blob_name}")
        match layer.media_type:
            case MediaType.IMAGE_TAR_GZIP:
                try:
                    with tarfile.open(fileobj=io.BytesIO(bytes), mode="r:gz") as tar:
                        tar.extractall(path=temp_path)
                except tarfile.ReadError:
                    with tarfile.open(fileobj=io.BytesIO(bytes), mode="r") as tar:
                        tar.extractall(path=temp_path)
            case MediaType.IMAGE_TAR:
                try:
                    with tarfile.open(fileobj=io.BytesIO(bytes), mode="r:") as tar:
                        tar.extractall(path=temp_path)
                except tarfile.ReadError:
                    with tarfile.open(fileobj=io.BytesIO(bytes), mode="r") as tar:
                        tar.extractall(path=temp_path)
        return bytes
