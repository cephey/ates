from pydantic import BaseModel, EmailStr


class Role(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    email: EmailStr
    role: Role
    auth_token: str
