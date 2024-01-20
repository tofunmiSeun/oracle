from fastapi import FastAPI
from typing import List
from mongoclient import database
from api.models import CreateWorkspaceRequest, CreateDatasourceRequest
from workspace.models import WorkspaceViewModel
from workspace.service import WorkspaceService
from datasource import DatasourceService

app = FastAPI()
workspace_service = WorkspaceService(database=database)
datasource_service = DatasourceService(database=database)


@app.post("/workspace")
def create_workspace(body: CreateWorkspaceRequest) -> str:
    workspace_id = workspace_service.create_workspace(body.title,
                                                      body.description)
    return workspace_id


@app.get("/workspace")
def get_all_workspaces() -> List[WorkspaceViewModel]:
    return workspace_service.get_all_workspaces()


@app.delete("/workspace/{workspace_id}")
def delete_workspace(workspace_id: str) -> None:
    workspace_service.delete_workspace(id=workspace_id)


@app.post("/datasource")
def create_datasource(body: CreateDatasourceRequest) -> str:
    datasource_id = datasource_service.create_datasource(body.workspace_id,
                                                         body.website)
    return datasource_id
