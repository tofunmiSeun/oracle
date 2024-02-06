from typing import TypedDict, NotRequired, List, Literal
from bson import ObjectId


class Workspace(TypedDict):
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


class ChatMessage(TypedDict):
    _id: NotRequired[ObjectId]
    workspace_id: str
    created_at: float
    sender: Literal['human', 'AI']
    message: str
    thread_id: NotRequired[str]
