
from typing import TypedDict, NotRequired, List
from pymongo.database import Database
from pymongo.collection import Collection
from pydantic import BaseModel
from bson import ObjectId


class Workspace(TypedDict):
    _id: NotRequired[ObjectId]
    title: str
    description: str


class WorkspaceViewModel(BaseModel):
    id: str
    title: str
    description: str


class WorkspaceService:
    def __init__(self, database: Database) -> None:
        self.collection: Collection[Workspace] = database.workspace

    def create_workspace(self, title: str, description: str) -> str:
        workspace = Workspace(title=title, description=description)
        result = self.collection.insert_one(workspace)
        return str(result.inserted_id)

    def get_all_workspaces(self) -> List[Workspace]:
        result: List[Workspace] = []

        cursor = self.collection.find({})
        for item in cursor:
            result.append(WorkspaceViewModel(
                id=str(item['_id']),
                title=item['title'],
                description=item['description']))

        return result

    def delete_workspace(self, id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(id)})
        deleted = result.deleted_count > 0
        print('Deleted: {}'.format(deleted))
        return deleted
