import logging
from typing import Dict, List, Optional
import openai

# Set up logging for monitoring and debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("gpt4_planner")

class GPT4PlannerError(Exception):
    """Custom exception for GPT-4 planning errors."""
    pass

class GPT4Planner:
    """
    A class to interact with GPT-4 for high-level task decomposition.
    """

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initializes the GPT-4 planner with API key and model.
        Args:
            api_key (str): OpenAI API key.
            model (str): GPT model to use. Default is "gpt-4".
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
        logger.info(f"GPT-4 Planner initialized with model: {self.model}")

    def plan_task(self, high_level_task: str) -> List[Dict[str, str]]:
        """
        Breaks down a high-level task into smaller subtasks.
        Args:
            high_level_task (str): The task description in natural language.

        Returns:
            List[Dict[str, str]]: A list of subtasks with metadata.
        """
        try:
            logger.info(f"Planning task using GPT-4: {high_level_task}")

            # Generate the prompt
            prompt = self._generate_task_prompt(high_level_task)

            # Call the GPT-4 API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a highly skilled task planner."},
                          {"role": "user", "content": prompt}],
                temperature=0.7
            )

            # Extract the response content
            task_plan = response["choices"][0]["message"]["content"]

            # Parse the task plan
            subtasks = self._parse_subtasks(task_plan)
            logger.info(f"Successfully planned task with {len(subtasks)} subtasks.")
            return subtasks

        except Exception as e:
            logger.error(f"Error during task planning: {str(e)}")
            raise GPT4PlannerError(f"Failed to plan task: {str(e)}")

    def _generate_task_prompt(self, high_level_task: str) -> str:
        """
        Creates a structured prompt for the GPT-4 model for task planning.
        Args:
            high_level_task (str): High-level task description.

        Returns:
            str: A structured prompt for the GPT-4 model.
        """
        return (
            f"The user has described a high-level task:\n"
            f"'{high_level_task}'.\n\n"
            f"As a task planner, decompose this into a JSON array of subtasks. "
            f"Each subtask should be an object with:\n"
            f"1. 'step': The description of the subtask.\n"
            f"2. 'tool': The name of the recommended tool or API for execution (if applicable).\n\n"
            f"For example: "
            f"[{{'step': 'Search for pizza restaurants on Zomato', 'tool': 'zomato'}}, "
            f"{{'step': 'Place an order for a Margherita pizza', 'tool': 'zomato'}}]."
        )

    def _parse_subtasks(self, task_plan: str) -> List[Dict[str, str]]:
        """
        Extracts structured subtasks from GPT-4's raw response.
        Args:
            task_plan (str): Raw JSON-like response from GPT.

        Returns:
            List[Dict[str, str]]: Parsed list of subtasks.
        """
        try:
            import json
            # Parse task plan as JSON
            subtasks = json.loads(task_plan)

            # Validate subtasks
            for subtask in subtasks:
                if not all(key in subtask for key in ["step", "tool"]):
                    raise ValueError(f"Invalid subtask format: {subtask}")

            return subtasks

        except Exception as e:
            logger.error(f"Error parsing subtasks: {str(e)}")
            raise GPT4PlannerError(f"Failed to parse subtasks: {str(e)}")