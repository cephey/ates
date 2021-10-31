from datetime import date

from pydantic import BaseModel


class Analytics(BaseModel):
    day: date
    max_task_amount: int
    sum_manager_count: int
    popug_count: int
