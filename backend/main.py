from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

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
