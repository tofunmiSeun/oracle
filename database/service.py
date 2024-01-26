from typing import List
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from bson import ObjectId
from .models import Namespace, Datasource, DocumentEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGODB_URI')
# Todo: fix TLS certificate validation
mongo_client = MongoClient(uri, tlsAllowInvalidCertificates=True)
mongo_database = mongo_client.oracle

try:
    mongo_client.admin.command('ping')
except Exception as e:
    print(e)


def get_unique_document_id(website_url: str) -> str:
    return f'website_{website_url.strip().lower()}'


class DatabaseService:
    def __init__(self) -> None:
        database = mongo_database
        self.namespace_collection: Collection[Namespace] = database[
            'namespace']
        self.datasource_collection: Collection[Datasource] = database[
            'datasource']
        self.embeddings_collection: Collection[DocumentEmbeddings] = database[
            'document_embeddings']

    def create_namespace(self, title: str, description: str) -> str:
        namespace = Namespace(title=title, description=description)
        result = self.namespace_collection.insert_one(namespace)
        return str(result.inserted_id)

    def get_all_namespaces(self) -> List[Namespace]:
        result: List[Namespace] = []

        cursor = self.namespace_collection.find({})
        for item in cursor:
            result.append(item)

        return result

    def delete_namespace(self, id: str) -> bool:
        result = self.namespace_collection.delete_one({"_id": ObjectId(id)})
        deleted = result.deleted_count > 0
        print('Deleted: {}'.format(deleted))
        return deleted

    def create_datasource(self, namespace_id: str, website: str) -> str:
        doc_id = get_unique_document_id(website)
        datasource = Datasource(namespace_id=namespace_id, document_id=doc_id,
                                website=website,
                                data_analysed=False)
        result = self.datasource_collection.insert_one(datasource)
        return str(result.inserted_id)

    def get_datasource(self, id) -> Datasource:
        return self.datasource_collection.find_one({"_id": ObjectId(id)})

    def get_document_ids_for_namespace(self, namespace_id: str) -> List[str]:
        cursor = self.datasource_collection.find(
            {"namespace_id": namespace_id},
            {"document_id": 1})

        doc_ids: List[str] = []
        for item in cursor:
            doc_ids.append(item['document_id'])

        return doc_ids

    def insert_embeddings(self, document_id: str, content: str,
                          embeddings: List[float]) -> None:
        document_embeddings = DocumentEmbeddings(document_id=document_id,
                                                 content=content,
                                                 embeddings=embeddings)
        self.embeddings_collection.insert_one(document_embeddings)

    def search_embeddings(self, embeddings: List[float],
                          document_ids: List[str]) -> List[str]:

        cursor = self.embeddings_collection.aggregate([
            {
                "$vectorSearch": {
                    "queryVector": embeddings,
                    "path": "embeddings",
                    "numCandidates": 100,
                    "limit": 3,
                    "index": "embeddings_vector_idx",
                    "filter": {"document_id": {"$in": document_ids}}
                }
            },
            {
                "$project": {"_id": 0, "content": 1}
            }
        ])

        results: List[str] = []
        for item in cursor:
            results.append(item['content'])

        return results
