from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from models import get_db, Task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskCreate(BaseModel):
    title: str
    completed: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    createdAt: datetime

    class Config:
        from_attributes = True


class TaskTitleUpdate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    completed: bool


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/tasks/", response_model=TaskResponse)
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


@app.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[TaskResponse]:
    tasks = db.query(Task).order_by(Task.position).offset(skip).limit(limit).all()
    return [TaskResponse.from_orm(task) for task in tasks]


@app.patch("/tasks/{task_id}/title", response_model=TaskResponse)
def update_task_title(task_id: int, task_update: TaskTitleUpdate, db: Session = Depends(get_db)) -> TaskResponse:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task_update.title
    db.commit()
    db.refresh(db_task)
    return TaskResponse.from_orm(db_task)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)) -> TaskResponse:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return TaskResponse.from_orm(db_task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)) -> dict:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    try:
        remaining_tasks = db.execute(select(Task).order_by(Task.position).with_for_update()).scalars().all()
        for index, task in enumerate(remaining_tasks):
            task.position = index
        db.commit()
    except StaleDataError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Data conflict error: {str(e)}")
    return {"ok": True}
