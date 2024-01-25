
from typing import TypedDict, NotRequired, List
from bson import ObjectId


class DocumentEmbeddings(TypedDict):
    _id: NotRequired[ObjectId]
    document_id: str
    content: str
    embeddings: List[float]
