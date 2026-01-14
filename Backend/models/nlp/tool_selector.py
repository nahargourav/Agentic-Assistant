import logging
from typing import Dict, Optional, Any

# Set up logging for troubleshooting and observability
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("tool_selector")

class ToolSelectorError(Exception):
    """Custom exception raised when tool selection fails."""
    pass

class ToolSelector:
    """
    ToolSelector dynamically selects the appropriate tool for a given task.
    """

    def __init__(self):
        """
        Initializes the ToolSelector with a predefined set of supported tools.
        """
        # Default registry of tools and their compatibility with specific actions
        self.tool_registry = {
            "zomato": ["order_food", "search_restaurants"],
            "uber_eats": ["order_food", "search_restaurants"],
            "google_maps": ["get_directions", "find_location"],
            "openai": ["text_summarization", "text_generation"],
            "custom_tool": ["analyze_data", "custom_action"]
        }
        logger.info("ToolSelector initialized with default tool registry.")

    def select_tool(self, action: str) -> Optional[str]:
        """
        Selects the most suitable tool for a given action.
        Args:
            action (str): The action for which a tool is required (e.g., 'order_food').
        
        Returns:
            str: The name of the tool best suited for the action.
        
        Raises:
            ToolSelectorError: If no suitable tool is found.
        """
        logger.info(f"Selecting tool for action: {action}")

        try:
            # Iterate through the registry and find a compatible tool
            for tool, supported_actions in self.tool_registry.items():
                if action in supported_actions:
                    logger.info(f"Selected tool '{tool}' for action '{action}'.")
                    return tool

            # If no tool matches the action, raise an error
            raise ToolSelectorError(f"No tool found to handle action: {action}")

        except Exception as e:
            logger.error(f"Error during tool selection: {str(e)}")
            raise ToolSelectorError(str(e))

    def add_tool(self, tool_name: str, supported_actions: Optional[Any] = None):
        """
        Adds a new tool to the registry.
        Args:
            tool_name (str): Name of the tool to add.
            supported_actions (Optional[Any]): List of supported actions for the tool. Defaults to empty list.
        """
        if supported_actions is None:
            supported_actions = []

        if tool_name in self.tool_registry:
            logger.warning(f"Tool '{tool_name}' already exists in the registry. Updating supported actions.")

        # Add or update the tool in the registry
        self.tool_registry[tool_name] = supported_actions
        logger.info(f"Tool '{tool_name}' added/updated in the registry with actions: {supported_actions}")

    def remove_tool(self, tool_name: str):
        """
        Removes a tool from the registry.
        Args:
            tool_name (str): Name of the tool to remove.

        Raises:
            ToolSelectorError: If the tool is not found.
        """
        if tool_name not in self.tool_registry:
            logger.error(f"Tool '{tool_name}' not found in the registry.")
            raise ToolSelectorError(f"Tool '{tool_name}' not found in the registry.")

        # Remove the tool
        del self.tool_registry[tool_name]
        logger.info(f"Tool '{tool_name}' removed from the registry.")

    def list_tools(self) -> Dict[str, Any]:
        """
        Lists all available tools and their supported actions.
        Returns:
            Dict[str, Any]: A dictionary containing all tools and their actions.
        """
        logger.info(f"Listing all tools in the registry: {self.tool_registry}")
        return self.tool_registry.copy()