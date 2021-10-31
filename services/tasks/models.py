from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    in_progress = 'in_progress'
    ready = 'ready'


class User(BaseModel):
    id: int
    role: str


class Task(BaseModel):
    id: int
    user: User
    description: str
    status: Status
