from typing import TypedDict, NotRequired
from pymongo.database import Database
from bson import ObjectId


class Datasource(TypedDict):
    _id: NotRequired[ObjectId]
    workspace_id: str
    website: str


class DatasourceService:
    def __init__(self, database: Database) -> None:
        self.collection = database.datasource

    def create_datasource(self, workspace_id: str, website: str) -> str:
        datasource = Datasource(workspace_id=workspace_id, website=website)
        result = self.collection.insert_one(datasource)
        return str(result.inserted_id)
