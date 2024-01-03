from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm.exc import StaleDataError
from models import Task, get_db
from schemas.reorder_request import ReorderRequest

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/reorder")
def reorder_tasks(request: ReorderRequest, db: Session = Depends(get_db)) -> dict:
    task_ids = [task.id for task in request.tasks]
    db_tasks = db.execute(select(Task).where(Task.id.in_(task_ids)).with_for_update()).scalars().all()
    if len(db_tasks) != len(task_ids):
        found_task_ids = {task.id for task in db_tasks}
        missing_task_ids = set(task_ids) - {int(task_id) for task_id in found_task_ids}
        raise HTTPException(status_code=400, detail=f"Some tasks not found: {missing_task_ids}")
    for task_data in request.tasks:
        db_task = next((task for task in db_tasks if task.id == task_data.id), None)
        if db_task:
            db_task.position = task_data.position
        else:
            raise HTTPException(status_code=404, detail=f"Task with id {task_data.id} not found")
    try:
        db.commit()
    except StaleDataError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Data conflict error: {str(e)}")

    return {"message": "Tasks reordered successfully"}
