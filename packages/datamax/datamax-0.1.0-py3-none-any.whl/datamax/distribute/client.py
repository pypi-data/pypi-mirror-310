from abc import abstractmethod
import os
from pathlib import Path
from typing import Optional, Any
import requests
from google import auth
from google.auth.transport import requests as grequests
from google.cloud import storage
from pydantic import BaseModel
from pydantic_core import Url
from datamax.console import console
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from urllib.parse import quote_plus
import tarfile
import shutil
import io
from requests_toolbelt import MultipartEncoder
import json
from abc import ABC

from datamax.types import MediaType


class GCPConfig(BaseModel):
    project: str
    location: str
    repository: str

    @classmethod
    def from_env(cls):
        return cls(
            project=os.environ["GCP_PROJECT"],
            location=os.environ["GCP_LOCATION"],
            repository=os.environ["GCP_REPOSITORY"],
        )

class GCPClient(ABC):
    def __init__(self, config: GCPConfig):
        self.config = config
        self.creds, self.project = auth.default()
        auth_request = grequests.Request()
        self.creds.refresh(auth_request)

    @abstractmethod
    def upload_file(self, file_path: Path, image_ref: str, version: str) -> Any:
        return NotImplemented

    @abstractmethod
    def download_file(self, file_path: Path, image_ref: str, version: str, artifact_id: str, media_type: Optional[MediaType] = None) -> Any:
        return NotImplemented

class ArtifactRegistryClient(GCPClient):
    # def upload_file(self, file_path: Path, image_ref: str, version: str):
    #     version = version if version != "latest" else "unknown"
    #     upload_url = Url(
    #         f"https://artifactregistry.googleapis.com/upload/v1/projects/{self.config.project}/locations/{self.config.location}/repositories/{self.config.repository}/genericArtifacts:create?alt=json&uploadType=multipart"
    #     )
    #     console.log(f"Uploading file {file_path} to {upload_url.unicode_string()}")
    #     absolute_path = Path(file_path).resolve()
    #     related = MIMEMultipart("related")
    #     with open(absolute_path, "rb") as f:
    #         bytes = f.read()
    #         file = MIMEApplication(bytes, "octet-stream", lambda x: x)
    #     relative_path = os.path.join(*absolute_path.parts[absolute_path.parts.index(image_ref)+1:])
    #     body = MIMEApplication(json.dumps({"packageId": image_ref, "filename": relative_path, "versionId": version}), "json", lambda x: x)
    #     related.attach(body)
    #     related.attach(file)
    #     response = requests.post(
    #         upload_url.unicode_string(),
    #         data=related.as_bytes(),
    #         headers={"Authorization": f"Bearer {self.creds.token}", **dict(related.items())},
    #     )
    #     return response
    def upload_file(self, file_path: Path, image_ref: str, version: str):
        version = version if version != "latest" else "unknown"
        upload_url = Url(
            f"https://artifactregistry.googleapis.com/upload/v1/projects/{self.config.project}/locations/{self.config.location}/repositories/{self.config.repository}/genericArtifacts:create?alt=json&uploadType=multipart"
        )
        console.log(f"Uploading file {file_path} to {upload_url.unicode_string()}")

        # Prepare file and metadata
        absolute_path = Path(file_path).resolve()
        relative_path = os.path.join(*absolute_path.parts[absolute_path.parts.index(image_ref) + 1:])
        metadata = {
            "packageId": image_ref,
            "filename": relative_path,
            "versionId": version,
        }

        # Construct the multipart payload
        multipart_data = MultipartEncoder(
            fields={
                "metadata": ("metadata.json", json.dumps(metadata), "application/json"),
                "file": (absolute_path.name, open(absolute_path, "rb"), "application/octet-stream"),
            }
        )

        # Send the request
        response = requests.post(
            upload_url.unicode_string(),
            data=multipart_data,
            headers={
                "Authorization": f"Bearer {self.creds.token}",
                "Content-Type": multipart_data.content_type,
            },
        )

        # Return the response for debugging
        if not response.ok:
            raise ValueError(f"Failed to upload image: {response.text}")
        return response

    def download_file(self, file_path: Path, image_ref: str, version: str, artifact_id: str, media_type: Optional[MediaType] = None):
        download_url = Url(
            f"https://artifactregistry.googleapis.com/v1/projects/{self.config.project}/locations/{self.config.location}/repositories/{self.config.repository}/files/{image_ref}:{version}:{artifact_id}:download?alt=media"
        )
        absolute_path = Path(file_path).resolve()
        absolute_path.parent.mkdir(parents=True, exist_ok=True)
        console.log(f"Downloading file {artifact_id} to {absolute_path}")
        response = requests.get(
            download_url.unicode_string(),
            headers={"Authorization": f"Bearer {self.creds.token}"},
            stream=True,
        )
        # match media_type:
            # case MediaType.IMAGE_TAR_GZIP:
            #     breakpoint()
            #     with tarfile.open(absolute_path, "w:gz") as tar:
            #         tar_info = tarfile.TarInfo(absolute_path.stem)
            #         tar_info.size = len(response.content)
            #         tar.addfile(tar_info, io.BytesIO(response.content))
            # case _:
        with open(absolute_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=None):
                f.write(chunk)
        return response

class CloudStorageClient(GCPClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage_client = storage.Client(project=self.config.project, credentials=self.creds)
        self.bucket = self.storage_client.get_bucket(self.config.repository)

    def upload_file(self, file_path: Path, image_ref: str, version: str):
        absolute_path = Path(file_path).resolve()
        image_name, image_tag = image_ref.split(":")
        version = version if not image_tag else image_tag
        relative_path = os.path.join(image_name, version, *absolute_path.parts[absolute_path.parts.index(version) + 1:])
        blob = self.bucket.blob(relative_path)
        console.log(f"Uploading file {file_path} to {relative_path}")
        blob.upload_from_filename(absolute_path)
        response = requests.Response()
        response.status_code = 200
        return response

    def download_file(self, file_path: Path, image_ref: str, version: str, artifact_id: str, media_type: Optional[MediaType] = None):
        absolute_path = Path(file_path).resolve()
        absolute_path.parent.mkdir(parents=True, exist_ok=True)
        image_name, image_tag = image_ref.split(":")
        version = version if not image_tag else image_tag
        relative_path = os.path.join(image_name, version, *absolute_path.parts[absolute_path.parts.index(version) + 1:])
        console.log(f"Downloading file {artifact_id} to {absolute_path}")
        blob = self.bucket.blob(relative_path)
        blob.download_to_filename(absolute_path)
        response = requests.Response()
        response.status_code = 200
        return response
