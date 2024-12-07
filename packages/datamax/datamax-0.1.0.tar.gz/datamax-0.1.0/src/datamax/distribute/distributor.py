import re
from urllib.parse import quote_plus

from datamax.config import CONFIG
from datamax.distribute.client import ArtifactRegistryClient, GCPConfig, CloudStorageClient
from datamax.console import console
from datamax.types import Annotation, ImageManifest, IndexJSON
import os

GCP_URL_RE = r"gcr.io/projects/([^/]+)/locations/([^/]+)/repositories/([^/]+)"


class Distributor:
    def __init__(self, image_ref: str, repo_url: str):
        self.config = CONFIG
        self.image_ref: str = image_ref
        if not repo_url:
            config = GCPConfig.from_env()
        else:
            re_match = re.match(GCP_URL_RE, repo_url)
            if not re_match:
                raise ValueError(f"Invalid repo URL: {repo_url}")
            project = re_match.group(1)
            location = re_match.group(2)
            repository = re_match.group(3)
            config = GCPConfig(
                project=project, location=location, repository=repository
            )
        self.client = CloudStorageClient(config)

    def push(self):
        image_name, image_tag = self.image_ref.split(":")
        image_home = self.config.datamax_home / "images" / self.image_ref if not image_tag else self.config.datamax_home / "images" / image_name / image_tag
        index_json_path = image_home / "index.json"
        with open(index_json_path, "r") as f:
            index_json = IndexJSON.model_validate_json(f.read())
        version = image_tag
        response = self.client.upload_file(image_home / "oci-layout", self.image_ref, version)
        if not response.ok:
            raise ValueError(f"Failed to upload image: {response.text}")
        for algo in (image_home / "blobs").iterdir():
            for blob in algo.iterdir():
                console.log(f"Uploading layer: {algo.stem}:{blob.stem}")
                response = self.client.upload_file(blob, self.image_ref, version)
                if not response.ok:
                    raise ValueError(f"Failed to upload image: {response.text}")
        response = self.client.upload_file(index_json_path, self.image_ref, version)
        if not response.ok:
            raise ValueError(f"Failed to upload image: {response.text}")
        console.log("Image uploaded successfully")

    def pull(self, version: str = "unknown"):
        image_name, image_tag = self.image_ref.split(":")
        image_home = self.config.datamax_home / "images" / self.image_ref if not image_tag else self.config.datamax_home / "images" / image_name / image_tag
        index_json_path = image_home / "index.json"
        oci_layout_path = image_home / "oci-layout"
        response = self.client.download_file(index_json_path, self.image_ref, version, "index.json")
        response = self.client.download_file(oci_layout_path, self.image_ref, version, "oci-layout")
        if not response.ok:
            raise ValueError(f"Failed to download image: {response.text}")
        with open(index_json_path, "r") as f:
            index_json = IndexJSON.model_validate_json(f.read())
        for manifest in index_json.manifests:
            manifest_algo, manifest_hash = manifest.digest.split(":")
            (image_home / "blobs" / manifest_algo).mkdir(parents=True, exist_ok=True)
            destination_path = image_home / "blobs" / manifest_algo / manifest_hash
            response = self.client.download_file(destination_path, self.image_ref, version, quote_plus(os.path.join("blobs", manifest_algo, manifest_hash)))
            if not response.ok:
                raise ValueError(f"Failed to download image: {response.text}")
            with open(destination_path, "r") as f2:
                manifest = ImageManifest.model_validate_json(f2.read())
            for layer in manifest.layers:
                layer_algo, layer_hash = layer.digest.split(":")
                (image_home / "blobs" / layer_algo).mkdir(parents=True, exist_ok=True)
                destination_path = image_home / "blobs" / layer_algo / layer_hash
                response = self.client.download_file(destination_path, self.image_ref, version, quote_plus(os.path.join("blobs", layer_algo, layer_hash)), layer.media_type)
