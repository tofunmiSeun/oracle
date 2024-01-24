
from typing import List
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
from .models import Namespace, NamespaceViewModel


class NamespaceService:
    def __init__(self, database: Database) -> None:
        self.collection: Collection[Namespace] = database.namespace

    def create_namespace(self, title: str, description: str) -> str:
        namespace = Namespace(title=title, description=description)
        result = self.collection.insert_one(namespace)
        return str(result.inserted_id)

    def get_all_namespaces(self) -> List[Namespace]:
        result: List[Namespace] = []

        cursor = self.collection.find({})
        for item in cursor:
            result.append(NamespaceViewModel(
                id=str(item['_id']),
                title=item['title'],
                description=item['description']))

        return result

    def delete_namespace(self, id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(id)})
        deleted = result.deleted_count > 0
        print('Deleted: {}'.format(deleted))
        return deleted
