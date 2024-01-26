from pydantic import BaseModel


class CreateNamespaceRequest(BaseModel):
    title: str
    description: str


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
