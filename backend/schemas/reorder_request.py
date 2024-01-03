from pydantic import BaseModel
from typing import List


class ReorderTask(BaseModel):
    id: int
    position: int


class ReorderRequest(BaseModel):
    tasks: List[ReorderTask]
