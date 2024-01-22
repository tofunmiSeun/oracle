from pydantic import BaseModel


class CreateNamespaceRequest(BaseModel):
    title: str
    description: str


class CreateDatasourceRequest(BaseModel):
    namespace_id: str
    website: str
