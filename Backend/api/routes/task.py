# Endpoint for submitting tasks
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict

# Import wrapper functions instead of direct imports
from core.wrappers import process_task, orchestrate_task

router = APIRouter()

# Define a request model for task submission
class TaskRequest(BaseModel):
    task: str  # High-level task in natural language (e.g., "Order pizza via Zomato")
    user_id: Optional[str] = None  # Optional user ID for personalization metadata

# Define a response model
class TaskResponse(BaseModel):
    task_id: str  # Unique ID for the submitted task
    status: str  # Current status of the task
    details: Optional[Dict] = None  # Optional info about task processing steps or results

# In-memory task queue or database replacement for development
task_db = {}

@router.post("/", response_model=TaskResponse)
async def create_task(task_request: TaskRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to submit a high-level task.
    1. Translates the human-readable task into actionable subtasks using the task planner.
    2. Orchestrates steps, sends requests to APIs, and processes responses.
    """

    # Sample unique ID generation for task (you can replace this with UUIDs)
    task_id = f"task_{len(task_db) + 1}"

    # Add task to task_db with initial status
    task_db[task_id] = {
        "task": task_request.task,
        "status": "in_progress",
        "details": None
    }

    # Process task in the background to avoid blocking the API response
    def process_and_orchestrate():
        try:
            # Step 1: Break down the task using the task planner
            subtasks = process_task(task_request.task)

            # Step 2: Execute tasks dynamically using the orchestrator
            results = orchestrate_task(subtasks)

            # Update task status and details
            task_db[task_id]["status"] = "completed"
            task_db[task_id]["details"] = results

        except Exception as e:
            # Handle exceptions and mark the task as failed
            task_db[task_id]["status"] = "failed"
            task_db[task_id]["details"] = {"error": str(e)}

    # Assign the background processing task
    background_tasks.add_task(process_and_orchestrate)

    # Return the initial response to user
    return {
        "task_id": task_id,
        "status": "in_progress",
        "details": None
    }

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """
    Endpoint to check the status of a submitted task.
    Retrieves the current state of task execution and provides feedback.
    """
    task = task_db.get(task_id)

    if not task:
        # Return error if task is not found
        raise HTTPException(status_code=404, detail="Task not found")

    # Return the current task status
    return {
        "task_id": task_id,
        "status": task["status"],
        "details": task["details"]
    }