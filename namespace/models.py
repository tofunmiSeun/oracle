from typing import TypedDict, NotRequired
from pydantic import BaseModel
from bson import ObjectId


class Namespace(TypedDict):
    _id: NotRequired[ObjectId]
    title: str
    description: str


class NamespaceViewModel(BaseModel):
    id: str
    title: str
    description: str
