"""
Wrapper functions for task planning and orchestration.
These are convenience functions that wrap the class-based implementations.
"""
from typing import List, Dict, Any
import os
import logging

from core.task_planner import TaskPlanner
from core.orchestrator import Orchestrator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wrappers")

# Initialize with environment variable or demo mode
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "demo-key")

def process_task(task: str) -> List[Dict[str, Any]]:
    """
    Wrapper function to process a high-level task and break it into subtasks.
    
    Args:
        task (str): High-level task description in natural language.
    
    Returns:
        List[Dict[str, Any]]: List of subtasks with tool and action information.
    """
    try:
        logger.info(f"Processing task: {task}")
        
        # For demo purposes, return a simple task breakdown
        # In production, this would use TaskPlanner with actual API key
        if not OPENAI_API_KEY or OPENAI_API_KEY == "demo-key":
            logger.warning("Using demo mode - no actual API calls")
            # Return demo subtasks
            if "order" in task.lower() and "food" in task.lower():
                return [
                    {"tool": "zomato", "action": "search", "params": {"query": "pizza"}},
                    {"tool": "zomato", "action": "order", "params": {"restaurant_id": 123}}
                ]
            else:
                return [
                    {"tool": "generic", "action": "process", "params": {"task": task}}
                ]
        
        # Use actual TaskPlanner if API key is available
        planner = TaskPlanner(OPENAI_API_KEY)
        subtasks = planner.decompose_task(task)
        return subtasks
        
    except Exception as e:
        logger.error(f"Error processing task: {str(e)}")
        # Return a basic fallback
        return [{"tool": "generic", "action": "error", "params": {"error": str(e)}}]

def orchestrate_task(subtasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Wrapper function to orchestrate and execute a list of subtasks.
    
    Args:
        subtasks (List[Dict[str, Any]]): List of subtasks to execute.
    
    Returns:
        Dict[str, Any]: Combined results from all executed subtasks.
    """
    try:
        logger.info(f"Orchestrating {len(subtasks)} subtasks")
        
        orchestrator = Orchestrator()
        results = orchestrator.execute_subtasks(subtasks)
        
        return results
        
    except Exception as e:
        logger.error(f"Error orchestrating tasks: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "results": []
        }
