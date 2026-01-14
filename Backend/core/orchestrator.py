# Logic for dynamic tool invocation and retries
# Handles API calls, connections to external services (e.g., Zomato).

import logging
from typing import List, Dict, Any

# Example: Assume we have these utility imports for external integration
from tools.zomato_wrapper import ZomatoAPI
from tools.utils import parse_tool_response

# Configure logging for production-grade troubleshooting and observability
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("orchestrator")

class Orchestrator:
    """
    Orchestrator is responsible for dynamically invoking external tools/APIs
    and orchestrating subtasks for task fulfillment.
    """

    def __init__(self):
        # Initialize external API integrations
        self.zomato_api = ZomatoAPI()

    def execute_subtasks(self, subtasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes subtasks by routing them dynamically to the appropriate tools.
        Args:
            subtasks (List[Dict[str, Any]]): List of subtasks with high-level metadata
                e.g., [{"tool": "zomato", "action": "search", "params": {...}}]

        Returns:
            Dict[str, Any]: Combined responses from all executed subtasks.
        """
        results = []

        for subtask in subtasks:
            tool = subtask.get("tool")
            action = subtask.get("action")
            params = subtask.get("params", {})

            try:
                if tool == "zomato":
                    result = self._execute_zomato_action(action, params)
                else:
                    # Add support for more tools here (e.g., Uber Eats, Swiggy, etc.)
                    raise ValueError(f"Unsupported tool: {tool}")

                # Parse, log, and append the result
                parsed_result = parse_tool_response(tool, action, result)
                results.append(parsed_result)

            except Exception as e:
                logger.error(f"Failed to execute subtask for tool '{tool}' with error: {str(e)}")
                results.append({"tool": tool, "action": action, "error": str(e)})

        return {"status": "completed", "results": results}

    def _execute_zomato_action(self, action: str, params: Dict[str, Any]) -> Any:
        """
        Routes actions for the Zomato tool to its API integration.
        Args:
            action (str): Zomato action type (e.g., "search", "order", etc.)
            params (Dict[str, Any]): Parameters for the Zomato API.

        Returns:
            Any: Response from Zomato API.
        """
        if action == "search":
            return self.zomato_api.search(params)
        elif action == "order":
            return self.zomato_api.create_order(params)
        else:
            raise ValueError(f"Unsupported action for Zomato: {action}")