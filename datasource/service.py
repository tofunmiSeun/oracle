from pymongo.database import Database
from pymongo.collection import Collection
import asyncio
import curator
from .models import Datasource


loop = asyncio.get_event_loop()


class DatasourceService:
    def __init__(self, database: Database) -> None:
        self.collection: Collection[Datasource] = database.datasource

    def create_datasource(self, namespace_id: str, website: str) -> str:
        datasource = Datasource(namespace_id=namespace_id, website=website,
                                data_analysed=False)
        result = self.collection.insert_one(datasource)

        loop.create_task(curator.run(website=website))

        return str(result.inserted_id)
