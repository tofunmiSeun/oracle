from fastapi import FastAPI
from pydantic import BaseModel
from workspace import WorkspaceService
from mongoclient import database

app = FastAPI()
workspace_service = WorkspaceService(database=database)


class CreateWorkspaceRequest(BaseModel):
    title: str
    description: str


@app.post("/workspace")
def create_workspace(body: CreateWorkspaceRequest) -> str:
    workspace_id = workspace_service.new_workspace(body.title,
                                                   body.description)
    return workspace_id


@app.delete("/workspace/{workspace_id}")
def delete_workspace(workspace_id: str) -> None:
    workspace_service.delete_workspace(id=workspace_id)
