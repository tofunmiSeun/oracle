from typing import TypedDict, NotRequired, List
from bson import ObjectId


class Namespace(TypedDict):
    _id: NotRequired[ObjectId]
    title: str
    description: str


class Datasource(TypedDict):
    _id: NotRequired[ObjectId]
    namespace_id: str
    document_id: str
    website: str


class DocumentEmbeddings(TypedDict):
    _id: NotRequired[ObjectId]
    document_id: str
    content: str
    embeddings: List[float]
