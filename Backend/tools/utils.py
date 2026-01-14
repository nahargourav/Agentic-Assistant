import logging
from datetime import datetime, timezone, timedelta
import json
from typing import Any, Dict, Optional

# Configure logging for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("utils")

def get_current_utc_timestamp() -> str:
    """
    Returns the current UTC timestamp in ISO 8601 format.
    Returns:
        str: Current UTC timestamp.
    """
    current_time = datetime.now(timezone.utc).isoformat()
    logger.info(f"Current UTC timestamp: {current_time}")
    return current_time

def validate_json(data: str) -> Optional[Dict[str, Any]]:
    """
    Validates if a string is a valid JSON and parses it.
    Args:
        data (str): JSON string to validate.

    Returns:
        Optional[Dict[str, Any]]: Parsed JSON object if valid, None otherwise.
    """
    try:
        json_data = json.loads(data)
        logger.info("JSON string successfully validated and parsed.")
        return json_data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON string: {data}. Error: {str(e)}")
        return None

def format_response(status: str, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    """
    Formats a JSON response structure.
    Args:
        status (str): Status of the response (e.g., "success", "error").
        message (str): Message providing details about the response.
        data (Optional[Any]): Additional data to include in the response.

    Returns:
        Dict[str, Any]: Formatted response.
    """
    response = {
        "status": status,
        "message": message,
        "data": data or {}
    }
    logger.info(f"Formatted response: {response}")
    return response

def time_difference_in_seconds(start_time: str, end_time: str) -> int:
    """
    Calculates the time difference in seconds between two ISO 8601 timestamps.
    Args:
        start_time (str): The start timestamp in ISO 8601 format.
        end_time (str): The end timestamp in ISO 8601 format.

    Returns:
        int: Difference in seconds.
    """
    try:
        start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        difference = (end - start).total_seconds()
        logger.info(f"Time difference: {difference} seconds (from {start_time} to {end_time})")
        return int(difference)
    except Exception as e:
        logger.error(f"Error calculating time difference: {str(e)}")
        raise ValueError(f"Invalid timestamps: {start_time}, {end_time}. Error: {str(e)}")

def add_seconds_to_timestamp(timestamp: str, seconds: int) -> str:
    """
    Adds seconds to an ISO 8601 timestamp and returns the updated timestamp.
    Args:
        timestamp (str): The initial timestamp in ISO 8601 format.
        seconds (int): Number of seconds to add.

    Returns:
        str: Updated timestamp.
    """
    try:
        time_obj = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        updated_time = time_obj + timedelta(seconds=seconds)
        updated_time_str = updated_time.isoformat()
        logger.info(f"Timestamp {timestamp} updated by {seconds} seconds to {updated_time_str}")
        return updated_time_str
    except Exception as e:
        logger.error(f"Error adding seconds to timestamp: {timestamp}. Error: {str(e)}")
        raise ValueError(f"Invalid timestamp: {timestamp}. Error: {str(e)}")

def parse_tool_response(tool: str, action: str, response: Any) -> Dict[str, Any]:
    """
    Parses and formats responses from external tools/APIs.
    Args:
        tool (str): Name of the tool (e.g., "zomato", "uber_eats").
        action (str): Action performed (e.g., "search", "order").
        response (Any): Raw response from the tool.

    Returns:
        Dict[str, Any]: Formatted response with standardized structure.
    """
    try:
        formatted_response = {
            "tool": tool,
            "action": action,
            "status": "success",
            "data": response
        }
        logger.info(f"Tool response parsed successfully for {tool}/{action}")
        return formatted_response
    except Exception as e:
        logger.error(f"Error parsing tool response: {str(e)}")
        return {
            "tool": tool,
            "action": action,
            "status": "error",
            "error": str(e)
        }
