# Keeps track of session/task states
# Includes persistent storage and context management.
import threading
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import uuid

# Set up logging for debugging and audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("state_manager")

class StateManager:
    """
    A thread-safe manager for handling task and session states.
    In-memory storage is used by default, with an option to extend for database persistence.
    """

    def __init__(self, task_expiry_minutes: int = 60):
        """
        Initializes the StateManager.
        Args:
            task_expiry_minutes (int): Duration (in minutes) after which tasks will expire.
        """
        self._state_store: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self.task_expiry_minutes = task_expiry_minutes
        logger.info("StateManager initialized with task expiry of %d minutes.", task_expiry_minutes)

    def create_task(self, task_data: Dict[str, Any]) -> str:
        """
        Creates and stores the initial state for a new task.
        Args:
            task_data (Dict[str, Any]): Metadata for the task to store (e.g., description, user_id).
        Returns:
            str: Unique task ID for this task.
        """
        with self._lock:
            # Generate a unique task ID
            task_id = f"task_{uuid.uuid4().hex}"
            state_entry = {
                "task_id": task_id,
                "data": task_data,
                "status": "created",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            self._state_store[task_id] = state_entry
            logger.info("Task created: %s", task_id)
            return task_id

    def update_task_status(self, task_id: str, status: str, details: Optional[Dict[str, Any]] = None):
        """
        Updates the status of an existing task.
        Args:
            task_id (str): Unique ID of the task to update.
            status (str): New status of the task (e.g., "in_progress", "completed", "failed").
            details (Optional[Dict[str, Any]]): Additional metadata to store with the task.
        Raises:
            KeyError: If the task ID does not exist.
        """
        with self._lock:
            if task_id not in self._state_store:
                logger.error("Task ID not found: %s", task_id)
                raise KeyError(f"Task ID {task_id} not found.")

            # Update the task's status and details
            self._state_store[task_id]["status"] = status
            self._state_store[task_id]["details"] = details or {}
            self._state_store[task_id]["updated_at"] = datetime.utcnow()
            logger.info("Task %s updated to status '%s'.", task_id, status)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """
        Retrieves the state of a specific task.
        Args:
            task_id (str): Unique ID of the task to retrieve.
        Returns:
            Dict[str, Any]: The task's state.
        Raises:
            KeyError: If the task ID does not exist.
        """
        with self._lock:
            if task_id not in self._state_store:
                logger.error("Task ID not found: %s", task_id)
                raise KeyError(f"Task ID {task_id} not found.")
            return self._state_store[task_id]

    def clean_expired_tasks(self):
        """
        Removes tasks that have passed their expiration time.
        This feature is useful to prevent memory bloat in long-running applications.
        """
        with self._lock:
            now = datetime.utcnow()
            expired_tasks = [
                task_id for task_id, task_data in self._state_store.items()
                if now - task_data["created_at"] > timedelta(minutes=self.task_expiry_minutes)
            ]
            for task_id in expired_tasks:
                del self._state_store[task_id]
                logger.info("Expired task cleaned: %s", task_id)

    def list_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """
        Lists all tasks currently stored in the state manager.
        Returns:
            Dict[str, Dict[str, Any]]: All stored tasks with their details.
        """
        with self._lock:
            return self._state_store.copy()

    def delete_task(self, task_id: str):
        """
        Deletes a specific task from the state manager.
        Args:
            task_id (str): Unique ID of the task to delete.
        Raises:
            KeyError: If the task ID does not exist.
        """
        with self._lock:
            if task_id not in self._state_store:
                logger.error("Task ID not found: %s", task_id)
                raise KeyError(f"Task ID {task_id} not found.")
            del self._state_store[task_id]
            logger.info("Task deleted: %s", task_id)