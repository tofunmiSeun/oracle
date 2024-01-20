from pydantic import BaseModel


class CreateWorkspaceRequest(BaseModel):
    title: str
    description: str


class CreateDatasourceRequest(BaseModel):
    workspace_id: str
    website: str
