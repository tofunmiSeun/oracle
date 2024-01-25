from fastapi import FastAPI
from typing import List
from database import mongo_database
from api.models import CreateNamespaceRequest, CreateDatasourceRequest
from namespace.models import NamespaceViewModel
from namespace.service import NamespaceService
from datasource.service import DatasourceService

app = FastAPI()
namespace_service = NamespaceService(database=mongo_database)
datasource_service = DatasourceService(database=mongo_database)


@app.post("/namespace")
def create_namespace(body: CreateNamespaceRequest) -> str:
    namespace_id = namespace_service.create_namespace(body.title,
                                                      body.description)
    return namespace_id


@app.get("/namespace")
def get_all_namespaces() -> List[NamespaceViewModel]:
    return namespace_service.get_all_namespaces()


@app.delete("/namespace/{namespace_id}")
def delete_namespace(namespace_id: str) -> None:
    namespace_service.delete_namespace(id=namespace_id)


@app.post("/datasource")
def create_datasource(body: CreateDatasourceRequest) -> str:
    datasource_id = datasource_service.create_datasource(body.namespace_id,
                                                         body.website)
    return datasource_id
