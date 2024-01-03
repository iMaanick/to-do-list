from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router as tasks_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)


@app.get("/")
def read_root() -> dict:
    return {
        "/tasks": "Retrieve all tasks",
        "/tasks/{id}": "Retrieve, update, or delete a specific task by ID",
        "/tasks/reorder": "Reorder tasks",
        "/tasks/{task_id}/title": "Update task title"
    }
