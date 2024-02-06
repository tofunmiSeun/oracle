from typing import List, Optional, Literal
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
from .models import Workspace, Datasource, DocumentEmbeddings, ChatMessage
import time


def get_unique_document_id(website_url: str) -> str:
    return f"website_{website_url.strip().lower()}"


class DatabaseService:
    def __init__(self, database: Database) -> None:
        self.workspace_collection: Collection[Workspace] = database["namespace"]
        self.datasource_collection: Collection[Datasource] = database["datasource"]
        self.embeddings_collection: Collection[DocumentEmbeddings] = database[
            "document_embeddings"
        ]
        self.chat_messages_collection: Collection[ChatMessage] = database[
            "chat_messages"
        ]

    def create_workspace(self, title: str, description: str) -> str:
        workspace = Workspace(title=title, description=description)
        result = self.workspace_collection.insert_one(workspace)
        return str(result.inserted_id)

    def get_all_workspaces(self) -> List[Workspace]:
        result: List[Workspace] = []

        cursor = self.workspace_collection.find({})
        for item in cursor:
            result.append(item)

        return result

    def get_workspace(self, id: str) -> Workspace:
        workspace = self.workspace_collection.find_one({"_id": ObjectId(id)})

        if workspace is None:
            raise RuntimeError("Could not find workspace for given id")

        return workspace

    def update_workspace(
        self, id: str, title: Optional[str] = None, description: Optional[str] = None
    ) -> None:
        if title is None and description is None:
            return

        workspace = self.workspace_collection.find_one({"_id": ObjectId(id)})
        if workspace is None:
            return

        update_params: dict[str, str] = {}
        if title is not None:
            update_params["title"] = title
        if description is not None:
            update_params["description"] = description

        self.workspace_collection.update_one(
            {"_id": workspace["_id"]}, {"$set": update_params}
        )

    def delete_workspace(self, id: str) -> bool:
        result = self.workspace_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    def create_datasource(self, workspace_id: str, website: str) -> str:
        doc_id = get_unique_document_id(website)
        datasource = Datasource(
            namespace_id=workspace_id,
            document_id=doc_id,
            website=website,
            data_analysed=False,
        )
        result = self.datasource_collection.insert_one(datasource)
        return str(result.inserted_id)

    def get_datasources(self, workspace_id: str) -> List[Datasource]:
        result: List[Datasource] = []

        cursor = self.datasource_collection.find({"namespace_id": workspace_id})
        for item in cursor:
            result.append(item)

        return result

    def delete_datasource(self, id: str) -> bool:
        result = self.datasource_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    def get_datasource(self, id) -> Datasource:
        return self.datasource_collection.find_one({"_id": ObjectId(id)})

    def save_chat_message(
        self, workspace_id: str, sender: Literal["human", "AI"],
        message: str,
        thread_id: str = None
    ) -> str:
        chat_message = ChatMessage(
            workspace_id=workspace_id,
            created_at=time.time(),
            sender=sender,
            message=message,
            thread_id=thread_id
        )
        result = self.chat_messages_collection.insert_one(chat_message)
        return str(result.inserted_id)

    def get_chat_messages(self, workspace_id: str) -> List[ChatMessage]:
        result: List[ChatMessage] = []

        cursor = self.chat_messages_collection.find(
            {"workspace_id": workspace_id}).sort("created_at", -1)

        for item in cursor:
            result.append(item)

        return result

    def get_document_ids_for_workspace(self, workspace_id: str) -> List[str]:
        cursor = self.datasource_collection.find(
            {"namespace_id": workspace_id}, {"document_id": 1}
        )

        doc_ids: List[str] = []
        for item in cursor:
            doc_ids.append(item["document_id"])

        return doc_ids

    def insert_embeddings(
        self, document_id: str, content: str, embeddings: List[float]
    ) -> None:
        document_embeddings = DocumentEmbeddings(
            document_id=document_id, content=content, embeddings=embeddings
        )
        self.embeddings_collection.insert_one(document_embeddings)

    def search_embeddings(
        self, embeddings: List[float], document_ids: List[str]
    ) -> List[str]:

        cursor = self.embeddings_collection.aggregate(
            [
                {
                    "$vectorSearch": {
                        "queryVector": embeddings,
                        "path": "embeddings",
                        "numCandidates": 100,
                        "limit": 3,
                        "index": "embeddings_vector_idx",
                        "filter": {"document_id": {"$in": document_ids}},
                    }
                },
                {"$project": {"_id": 0, "content": 1}},
            ]
        )

        results: List[str] = []
        for item in cursor:
            results.append(item["content"])

        return results
