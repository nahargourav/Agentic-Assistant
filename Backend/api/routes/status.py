# Endpoint for querying task states
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

# Assuming the same task_db from task.py
from api.routes.task import task_db

router = APIRouter()

# Define response models
class AllTasksResponse(BaseModel):
    task_id: str  # Unique ID for the task
    status: str  # Current status of the task
    details: Optional[Dict] = None  # Optional additional details

class HealthStatusResponse(BaseModel):
    service: str  # Name of the service
    status: str  # Overall status (e.g., "healthy", "degraded", "down")
    version: str  # API version
    tasks_in_progress: int  # Number of in-progress tasks

@router.get("/tasks", response_model=List[AllTasksResponse])
async def list_all_tasks():
    """
    Endpoint to list all submitted tasks and their statuses.
    Returns an array of task information for monitoring.
    """
    task_list = [
        {
            "task_id": task_id,
            "status": task_data["status"],
            "details": task_data["details"]
        }
        for task_id, task_data in task_db.items()
    ]

    return task_list

@router.get("/health", response_model=HealthStatusResponse)
async def health_check():
    """
    Endpoint to check the health of the system.
    Useful for monitoring and ensuring the service is operational.
    """
    tasks_in_progress = sum(1 for task in task_db.values() if task["status"] == "in_progress")

    return {
        "service": "Agentic Assistant API",
        "status": "healthy",
        "version": "1.0.0",
        "tasks_in_progress": tasks_in_progress
    }

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """
    Endpoint to delete a task from the system.
    In production, this might soft-delete or archive the task.
    """
    if task_id in task_db:
        del task_db[task_id]
        return  # HTTP 204 No Content
    else:
        raise HTTPException(status_code=404, detail="Task not found")