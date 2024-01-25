from pymongo.database import Database
from pymongo.collection import Collection
import asyncio
import curator
from .models import Datasource


loop = asyncio.get_event_loop()


def get_unique_document_id(website_url: str) -> str:
    return f'website_{website_url.strip().lower()}'


class DatasourceService:
    def __init__(self, database: Database) -> None:
        self.collection: Collection[Datasource] = database.datasource

    def create_datasource(self, namespace_id: str, website: str) -> str:
        doc_id = get_unique_document_id(website)
        datasource = Datasource(namespace_id=namespace_id, document_id=doc_id,
                                website=website,
                                data_analysed=False)
        result = self.collection.insert_one(datasource)

        loop.create_task(curator.run(website, doc_id))

        return str(result.inserted_id)
