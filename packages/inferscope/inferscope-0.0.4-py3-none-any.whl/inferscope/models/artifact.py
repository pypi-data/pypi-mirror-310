from typing import Literal, List, Union

from pydantic import BaseModel, Field

from inferscope._utils import AutoStrEnum
from inferscope.models.data_description import DataDescription


class ArtifactType(AutoStrEnum):
    EXTERNAL_LINK = "external_link"


class BaseArtifact(BaseModel):
    path: str = Field(min_length=1, max_length=120)
    type: ArtifactType
    data_description: Union[DataDescription, None] = None


class ExternalLinkArtifact(BaseArtifact):
    type: Literal[ArtifactType.EXTERNAL_LINK] = ArtifactType.EXTERNAL_LINK
    uri: str


class ArtifactInstance(BaseModel):
    name: str
    version: Union[str, None] = None
    description: Union[str, None] = None


class ArtifactPack(BaseModel):
    artifacts: Union[List[ExternalLinkArtifact], None] = None
