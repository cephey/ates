from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    public_id: str


class UserInDB(User):
    hashed_password: str
    access_token: str


class Task(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: str
    public_id: str


class TaskInDB(Task):
    pass
