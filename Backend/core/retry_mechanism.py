# Error recovery and automatic retry logic
# Handles logic for failed tasks and timed retries.
import time
import logging
from typing import Callable, Any, Optional
from functools import wraps

# Set up logging for monitoring and debugging retries
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("retry_mechanism")

class RetryConfig:
    """
    Configuration for retry mechanism, including strategy, limits, and delay intervals.
    """
    def __init__(self, retries: int = 3, delay: int = 2, backoff: float = 1.5, jitter: Optional[int] = None):
        """
        Args:
            retries (int): Total number of retry attempts (default: 3).
            delay (int): Initial delay in seconds between retries (default: 2).
            backoff (float): Factor to increase delay after each retry (default: 1.5).
            jitter (Optional[int]): Random jitter (in seconds) to add to the delay (default: None).
        """
        self.retries = retries
        self.delay = delay
        self.backoff = backoff
        self.jitter = jitter

class RetryException(Exception):
    """Custom exception to signal max retry failure."""
    pass

def retry(config: RetryConfig):
    """
    Decorator to retry a function based on the provided configuration.
    Args:
        config (RetryConfig): Retry configuration defining the retry strategy.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = config.delay

            while attempts < config.retries:
                try:
                    # Attempt to execute the function
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(f"Attempt {attempts}/{config.retries} failed for {func.__name__}: {str(e)}")

                    if attempts == config.retries:
                        logger.error(f"All {config.retries} attempts failed for {func.__name__}. Raising RetryException.")
                        raise RetryException(f"Function {func.__name__} failed after {config.retries} retries.") from e

                    # Calculate next delay with jitter (if provided) and sleep
                    if config.jitter:
                        jitter = time.uniform(0, config.jitter)
                    else:
                        jitter = 0
                    time.sleep(current_delay + jitter)

                    # Update delay for next retry with exponential backoff
                    current_delay *= config.backoff

        return wrapper
    return decorator

class RetryManager:
    """
    Centralized retry manager to execute retryable tasks for fault-tolerant systems.
    """

    def __init__(self, retry_config: RetryConfig):
        self.retry_config = retry_config

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Executes a function with retries using the configured retry mechanism.
        Args:
            func (Callable): The function to execute with retries.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        Returns:
            Any: The result of the function if successful.
        Raises:
            RetryException: If all retry attempts fail.
        """
        @retry(self.retry_config)
        def wrapped_function():
            return func(*args, **kwargs)

        return wrapped_function()

# Demonstration function to simulate transient failures
def transient_task_simulation(succeed_after: int):
    """
    Simulates a task that fails transiently before succeeding after a fixed number of attempts.
    Args:
        succeed_after (int): Number of failed attempts before the task succeeds.
    """
    transient_task_simulation.attempts += 1
    if transient_task_simulation.attempts <= succeed_after:
        raise ValueError("Simulated transient failure.")
    return "Task succeeded!"

# Initialize counter for the simulation function
transient_task_simulation.attempts = 0