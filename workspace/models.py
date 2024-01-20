from typing import TypedDict, NotRequired
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
