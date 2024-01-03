from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Task, get_db
from schemas.task import TaskTitleUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.patch("/{task_id}/title", response_model=TaskResponse)
def update_task_title(task_id: int, task_update: TaskTitleUpdate, db: Session = Depends(get_db)) -> TaskResponse:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = task_update.title
    db.commit()
    db.refresh(db_task)

    return TaskResponse.from_orm(db_task)
