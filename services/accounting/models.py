from enum import Enum

from pydantic import BaseModel, EmailStr


class Status(str, Enum):
    in_progress = 'in_progress'
    ready = 'ready'


class Score(BaseModel):
    id: int
    user_id: int
    user_email: EmailStr


class Log(BaseModel):
    score: Score
    amount_diff: int
    task_description: str
