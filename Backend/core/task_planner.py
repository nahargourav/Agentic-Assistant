# GPT-4 task planner logic
# Placeholder for decomposing tasks into subtasks using GPT-based NLP models like OpenAI.
import logging
from typing import Dict, List
import openai

# Set up logging for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("task_planner")

class TaskPlannerError(Exception):
    """Custom exception for task planning errors."""
    pass

class TaskPlanner:
    """
    Task planner to break down high-level tasks into smaller subtasks using OpenAI GPT.
    """

    def __init__(self, api_key: str):
        """
        Initializes the Task Planner with the OpenAI API key.
        Args:
            api_key (str): API key for OpenAI GPT or similar services.
        """
        self.api_key = api_key
        openai.api_key = self.api_key

    def decompose_task(self, high_level_task: str) -> List[Dict[str, str]]:
        """
        Decomposes a high-level task into smaller, actionable subtasks.
        Args:
            high_level_task (str): The task in human-readable natural language.

        Returns:
            List[Dict[str, str]]: A list of subtasks with metadata.
        """
        try:
            logger.info(f"Decomposing task: {high_level_task}")

            # Prompt for GPT to generate subtasks
            prompt = self._generate_task_prompt(high_level_task)

            # Call OpenAI GPT API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an expert task planner."},
                          {"role": "user", "content": prompt}],
                temperature=0.7
            )

            # Extract subtasks from the GPT response
            task_plan = response["choices"][0]["message"]["content"]
            subtasks = self._parse_subtasks(task_plan)

            logger.info(f"Successfully decomposed task into {len(subtasks)} subtasks")
            return subtasks

        except Exception as e:
            logger.error(f"Error during task decomposition: {str(e)}")
            raise TaskPlannerError(f"Failed to decompose task: {str(e)}")

    def _generate_task_prompt(self, high_level_task: str) -> str:
        """
        Generates a prompt to feed into the GPT API for task decomposition.
        Args:
            high_level_task (str): The high-level task input.

        Returns:
            str: The prompt for GPT.
        """
        return (
            f"The user has provided the following high-level task:\n"
            f"'{high_level_task}'.\n\n"
            f"Please break this task down into smaller, actionable subtasks. "
            f"The response should be a JSON list where each subtask includes the following fields:\n"
            f"- 'step': Description of the subtask.\n"
            f"- 'tool': Recommended tool or API to execute the subtask (if applicable).\n\n"
            f"For example:\n"
            f"[{{'step': 'Find restaurants offering pizza', 'tool': 'zomato'}}, "
            f"{{'step': 'Place order on Zomato', 'tool': 'zomato'}}]"
        )

    def _parse_subtasks(self, task_plan: str) -> List[Dict[str, str]]:
        """
        Parses a GPT-generated task plan into a structured list of subtasks.
        Args:
            task_plan (str): Raw JSON-like string from GPT.

        Returns:
            List[Dict[str, str]]: Parsed list of subtasks.
        """
        try:
            import json
            # Parse the GPT response into a JSON object
            subtasks = json.loads(task_plan)

            # Validate subtasks and ensure each subtask contains the required fields
            for subtask in subtasks:
                if not all(key in subtask for key in ["step", "tool"]):
                    raise ValueError(f"Invalid subtask structure: {subtask}")

            return subtasks

        except Exception as e:
            logger.error(f"Error parsing subtasks: {str(e)}")
            raise TaskPlannerError(f"Failed to parse subtasks: {str(e)}")