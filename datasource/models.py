
from typing import TypedDict, NotRequired
from bson import ObjectId


class Datasource(TypedDict):
    _id: NotRequired[ObjectId]
    namespace_id: str
    website: str
