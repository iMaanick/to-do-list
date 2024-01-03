from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from models import Task, get_db
from schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> TaskResponse:
    db_task = Task(
        title=task.title,
        completed=task.completed,
        createdAt=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponse.from_orm(db_task)
