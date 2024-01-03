from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Task, get_db
from schemas.task import TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[TaskResponse]:
    tasks = db.query(Task).order_by(Task.position).offset(skip).limit(limit).all()
    return [TaskResponse.from_orm(task) for task in tasks]
