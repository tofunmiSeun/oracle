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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[loaded_env_variables.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/namespace")
def create_namespace(body: api.models.CreateNamespaceRequest) -> str:
    namespace_id = db_service.create_namespace(body.title, body.description)
    return namespace_id


@app.get("/namespace")
def get_all_namespaces() -> List[api.models.NamespaceViewModel]:
    namespaces = db_service.get_all_namespaces()
    return [api.models.NamespaceViewModel(id=str(item['_id']),
                                          title=item['title'],
                                          description=item['description'])
            for item in namespaces]


@app.post("/namespace/{id}")
def update_namespace(id: str, body: api.models.UpdateNamespaceRequest) -> None:
    db_service.update_namespace(id, body.title, body.description)


@app.delete("/namespace/{namespace_id}")
def delete_namespace(namespace_id: str) -> None:
    db_service.delete_namespace(id=namespace_id)


@app.post("/datasource")
def create_datasource(body: api.models.CreateDatasourceRequest) -> str:
    datasource_id = db_service.create_datasource(body.namespace_id,
                                                 body.website)

    datasource = db_service.get_datasource(datasource_id)

    thread = threading.Thread(target=datasource_processer.process_website,
                              args=(datasource['website'],
                                    datasource['document_id'],))
    thread.start()

    return datasource_id


@app.get("/datasource/{namespace_id}")
def get_datasources(namespace_id: str) -> List[api.models.DatasourceViewModel]:
    namespaces = db_service.get_datasources(namespace_id)
    return [api.models.DatasourceViewModel(id=str(item['_id']),
                                           namespace_id=item['namespace_id'],
                                           website=item['website'])
            for item in namespaces]


@app.delete("/datasource/{datasource_id}")
def delete_datasource(datasource_id: str) -> None:
    db_service.delete_datasource(id=datasource_id)


@app.get("/ask/{namespace_id}")
def ask_question(namespace_id: str, query: str = '') -> str:
    doc_ids = db_service.get_document_ids_for_namespace(namespace_id)
    embeddings = embed_query(query)
    retrieved_documents = db_service.search_embeddings(embeddings, doc_ids)

    return ask_llm(query, retrieved_documents)
