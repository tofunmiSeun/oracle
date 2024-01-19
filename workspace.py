
from typing import TypedDict, List, NotRequired
from pymongo.database import Database
from bson import ObjectId


class Workspace(TypedDict):
    _id: NotRequired[ObjectId]
    title: str
    description: str


class WorkspaceService:
    def __init__(self, database: Database) -> None:
        self.data: List[Workspace] = []
        self.collection = database.workspace

    def new_workspace(self, title: str, description: str) -> str:
        workspace = Workspace(title=title, description=description)
        result = self.collection.insert_one(workspace)
        return str(result.inserted_id)

    def delete_workspace(self, id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(id)})
        deleted = result.deleted_count > 0
        print('Deleted: {}'.format(deleted))
        return deleted
