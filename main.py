from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import api.models
from database import db_service
import threading
import datasource_processer
from embeddings import embed_query
from llm import ask_llm
import loaded_env_variables

app = FastAPI()

frontend_url = loaded_env_variables.FRONTEND_URL
if frontend_url is not None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[loaded_env_variables.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/workspace")
def create_workspace(body: api.models.CreateWorkspaceRequest) -> str:
    workspace_id = db_service.create_workspace(body.title, body.description)
    return workspace_id


@app.get("/workspace")
def get_all_workspaces() -> List[api.models.WorkspaceViewModel]:
    workspaces = db_service.get_all_workspaces()
    return [
        api.models.WorkspaceViewModel(
            id=str(item["_id"]), title=item["title"], description=item["description"]
        )
        for item in workspaces
    ]


@app.get("/workspace/{id}")
def get_workspace(id: str) -> api.models.WorkspaceViewModel:
    workspace = db_service.get_workspace(id)
    return api.models.WorkspaceViewModel(
        id=str(workspace["_id"]),
        title=workspace["title"],
        description=workspace["description"],
    )


@app.post("/workspace/{id}")
def update_workspace(id: str, body: api.models.UpdateWorkspaceRequest) -> None:
    db_service.update_workspace(id, body.title, body.description)


@app.delete("/workspace/{workspace_id}")
def delete_workspace(workspace_id: str) -> None:
    db_service.delete_workspace(id=workspace_id)


@app.post("/datasource")
def create_datasource(body: api.models.CreateDatasourceRequest) -> str:
    datasource_id = db_service.create_datasource(body.workspace_id, body.website)

    datasource = db_service.get_datasource(datasource_id)

    thread = threading.Thread(
        target=datasource_processer.process_website,
        args=(
            datasource["website"],
            datasource["document_id"],
        ),
    )
    thread.start()

    return datasource_id


@app.get("/datasource/{workspace_id}")
def get_datasources(workspace_id: str) -> List[api.models.DatasourceViewModel]:
    workspaces = db_service.get_datasources(workspace_id)
    return [
        api.models.DatasourceViewModel(
            id=str(item["_id"]),
            workspace_id=item["namespace_id"],
            website=item["website"],
        )
        for item in workspaces
    ]


@app.delete("/datasource/{datasource_id}")
def delete_datasource(datasource_id: str) -> None:
    db_service.delete_datasource(id=datasource_id)


@app.get("/ask/{workspace_id}")
def ask_question(workspace_id: str, query: str = "") -> str:
    doc_ids = db_service.get_document_ids_for_workspace(workspace_id)
    embeddings = embed_query(query)
    retrieved_documents = db_service.search_embeddings(embeddings, doc_ids)

    return ask_llm(query, retrieved_documents)
