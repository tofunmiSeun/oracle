from typing import Optional
from pydantic import BaseModel, Field


class CreateNamespaceRequest(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str]


class CreateDatasourceRequest(BaseModel):
    namespace_id: str
    website: str


class NamespaceViewModel(BaseModel):
    id: str
    title: str
    description: str


class DatasourceViewModel(BaseModel):
    id: str
    namespace_id: str
    website: str


class UpdateNamespaceRequest(BaseModel):
    title: Optional[str]
    description: Optional[str]
