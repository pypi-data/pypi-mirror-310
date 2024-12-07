import hashlib
import json

from datamax.build.builder import Builder
from datamax.config import CONFIG
from datamax.types import IndexJSON


class TestRuntime:
    def test_build_runtime_init(self, basic_filepath, cleanup):
        builder = Builder.from_file(basic_filepath, "foo")
        cleanup.append(CONFIG.datamax_home / "images" / builder.name)
        print("foo")

    def test_build_runtime_run_program(self, basic_filepath, cleanup):
        builder = Builder.from_file(basic_filepath, "foo")
        build_dir = CONFIG.datamax_home / "images" / builder.name
        cleanup.append(build_dir)
        builder.run_program()
        for base_files in {"oci-layout", "index.json", "blobs"}:
            assert (build_dir / base_files).exists()
        with open(build_dir / "oci-layout", "r") as f:
            oci_layout = json.loads(f.read())
            assert oci_layout == {"imageLayoutVersion": "1.0.0"}
        with open(build_dir / "index.json", "r") as f:
            index_json = IndexJSON.model_validate_json(f.read())
        manifests = index_json.manifests
        for basic_manifest in manifests:
            manifest_digest = basic_manifest.digest
            manifest_digest_algo, manifest_digest_hash = manifest_digest.split(":")
            blob_path = (
                build_dir / "blobs" / manifest_digest_algo / manifest_digest_hash
            )
            with open(blob_path, "rb") as f:
                bytes = f.read()
                hash = hashlib.sha256(bytes).hexdigest()
            assert hash == manifest_digest_hash
