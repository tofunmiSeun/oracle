from typing import TypedDict, NotRequired
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
import asyncio
import curator

loop = asyncio.get_event_loop()


class Datasource(TypedDict):
    _id: NotRequired[ObjectId]
    workspace_id: str
    website: str


class DatasourceService:
    def __init__(self, database: Database) -> None:
        self.collection: Collection[Datasource] = database.datasource

    def create_datasource(self, workspace_id: str, website: str) -> str:
        datasource = Datasource(workspace_id=workspace_id, website=website,
                                data_analysed=False)
        result = self.collection.insert_one(datasource)

        loop.create_task(curator.run(website=website))

        return str(result.inserted_id)
