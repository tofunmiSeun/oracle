from typing import Optional
from pydantic import BaseModel, Field


class CreateWorkspaceRequest(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str]


class CreateDatasourceRequest(BaseModel):
    workspace_id: str
    website: str


class WorkspaceViewModel(BaseModel):
    id: str
    title: str
    description: str


class DatasourceViewModel(BaseModel):
    id: str
    workspace_id: str
    website: str


class UpdateWorkspaceRequest(BaseModel):
    title: Optional[str]
    description: Optional[str]
