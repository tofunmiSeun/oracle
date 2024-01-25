
from typing import TypedDict, NotRequired, List
from bson import ObjectId
from pymongo.database import Database
from pymongo.collection import Collection


class DocumentEmbeddings(TypedDict):
    _id: NotRequired[ObjectId]
    document_id: str
    content: str
    embeddings: List[float]


class EmbeddingsService:
    def __init__(self, database: Database) -> None:
        self.collection: Collection[DocumentEmbeddings] = database[
            'document_embeddings']

    def insert_embedding(self, document_id: str, content: str,
                         embeddings: List[float]):
        document_embeddings = DocumentEmbeddings(document_id=document_id,
                                                 content=content,
                                                 embeddings=embeddings)
        self.collection.insert_one(document_embeddings)
