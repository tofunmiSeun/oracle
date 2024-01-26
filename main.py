from fastapi import FastAPI
from typing import List
import api.models
from database.service import DatabaseService
import asyncio
import datasource_processer
from embeddings import embed_query

app = FastAPI()
db_service = DatabaseService()
loop = asyncio.get_event_loop()


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


@app.delete("/namespace/{namespace_id}")
def delete_namespace(namespace_id: str) -> None:
    db_service.delete_namespace(id=namespace_id)


@app.post("/datasource")
def create_datasource(body: api.models.CreateDatasourceRequest) -> str:
    datasource_id = db_service.create_datasource(body.namespace_id,
                                                 body.website)

    datasource = db_service.get_datasource(datasource_id)
    loop.create_task(datasource_processer.process_website(
        datasource['website'], datasource['document_id']))

    return datasource_id


@app.get("/query/{namespace_id}")
def query_data(namespace_id: str, query: str = '') -> List[str]:
    doc_ids = db_service.get_document_ids_for_namespace(namespace_id)
    embeddings = embed_query(query)
    return db_service.search_embeddings(embeddings, doc_ids)
