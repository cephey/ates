from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None


class UserInDB(User):
    hashed_password: str
    access_token: str
