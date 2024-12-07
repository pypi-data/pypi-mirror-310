import re
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

# class MediaType(str, Enum):
#     CONFIG_JSON = "application/vnd.oci.image.config.v1+json"
#     EMPTY_JSON = "application/vnd.oci.empty.v1+json"
#     IMAGE_MANIFEST = "application/vnd.oci.image.manifest.v1+json"
#     IMAGE_CONFIG = "application/vnd.oci.image.config.v1+json"
#     OPENAPI_SPEC = "application/vnd.oai.openapi+json;version=3.0"
#     UNKNOWN = "application/octet-stream"


class MediaTypeJSON(str, Enum):
    EMPTY_JSON = "application/vnd.oci.empty.v1+json"
    CONFIG_JSON = "application/vnd.oci.image.config.v1+json"
    MANIFEST_JSON = "application/vnd.oci.image.manifest.v1+json"
    INDEX_JSON = "application/vnd.oci.image.index.v1+json"


class MediaTypeTar(str, Enum):
    IMAGE_TAR = "application/vnd.oci.image.layer.v1.tar"
    IMAGE_TAR_GZIP = "application/vnd.oci.image.layer.v1.tar+gzip"
    IMAGE_TAR_ZSTD = "application/vnd.oci.image.layer.v1.tar+zstd"


class StepType(str, Enum):
    INGEST = "ingest"
    EXTEND = "extend"
    RUN    = "run"


class BaseStep(BaseModel):
    type: StepType


class StepWithSource(BaseStep):
    source: Path

class RunStep(BaseStep):
    type: StepType = StepType.RUN
    command: List[str]


class IngestStep(StepWithSource):
    type: StepType = StepType.INGEST
    destination: str
    source_extensions: list[str]


class BaseJSONSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
    )


class Annotation(str, Enum):
    IMAGE_VERSION = "org.opencontainers.image.version"
    CREATED = "org.opencontainers.image.created"


class MediaType(str, Enum):
    CONFIG_JSON = "application/vnd.oci.image.config.v1+json"
    EMPTY_JSON = "application/vnd.oci.empty.v1+json"
    IMAGE_MANIFEST = "application/vnd.oci.image.manifest.v1+json"
    IMAGE_CONFIG = "application/vnd.oci.image.config.v1+json"
    OPENAPI_SPEC = "application/vnd.oai.openapi+json;version=3.0"
    IMAGE_TAR = "application/vnd.oci.image.layer.v1.tar"
    IMAGE_TAR_GZIP = "application/vnd.oci.image.layer.v1.tar+gzip"
    IMAGE_TAR_ZSTD = "application/vnd.oci.image.layer.v1.tar+zstd"
    UNKNOWN = "application/octet-stream"


DIGEST_REGEX = r"(?P<algorithm>[a-z0-9]+)(?P<algorithm_components>([+._-][a-z0-9]+)*):(?P<encoded>[a-zA-Z0-9=_-]+)"


def validate_digest(digest: str) -> str:
    assert re.match(DIGEST_REGEX, digest), "invalid digest"
    return digest


Digest = Annotated[str, AfterValidator(validate_digest)]


class Descriptor(BaseJSONSchema):
    media_type: MediaType
    digest: Digest
    size: int
    urls: Optional[List[str]] = None
    annotations: Optional[Dict[str, str]] = None
    data: Optional[str] = None
    artifact_type: Optional[str] = None


class ImageManifest(BaseJSONSchema):
    schema_version: int = 2
    media_type: MediaType
    artifact_type: Optional[str] = None
    config: Descriptor
    layers: List[Descriptor] = []
    subject: Optional[Descriptor] = None
    annotations: Optional[Dict[str, str]] = None
    digest: Optional[Digest] = None


class OCILayout(BaseJSONSchema):
    image_layout_version: str = "1.0.0"


class IndexJSON(BaseJSONSchema):
    schema_version: int = 2
    media_type: MediaTypeJSON = MediaTypeJSON.INDEX_JSON
    manifests: List[Descriptor] = []
    annotations: Dict[str, str] = {}
