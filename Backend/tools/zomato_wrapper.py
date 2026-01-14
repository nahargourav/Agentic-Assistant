import logging
import requests
from typing import Dict, Any

# Configure logging for monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("zomato_wrapper")

class ZomatoAPIError(Exception):
    """Custom exception class for Zomato API errors."""
    pass

class ZomatoAPI:
    """
    Wrapper for the Zomato API to facilitate restaurant search, details retrieval,
    and order placement.
    """

    BASE_URL = "https://developers.zomato.com/api/v2.1"  # Update to the correct API endpoint

    def __init__(self, api_key: str = None):
        """
        Initializes the ZomatoAPI wrapper with the API key.
        Args:
            api_key (str): Zomato API Key to authenticate requests.
        """
        self.api_key = api_key or "demo_api_key"  # Use demo key if not provided
        self.headers = {"user-key": self.api_key}

    def search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Searches for restaurants based on parameters.
        Args:
            params (Dict[str, Any]): Search parameters (query, location, etc.).

        Returns:
            Dict[str, Any]: Response data containing matched restaurants.
        """
        query = params.get("query", "")
        lat = params.get("lat", 0.0)
        lon = params.get("lon", 0.0)
        count = params.get("count", 10)
        
        return self.search_restaurants(query, lat, lon, count)

    def search_restaurants(self, query: str, lat: float, lon: float, count: int = 10) -> Dict[str, Any]:
        """
        Searches for restaurants based on a query string and location coordinates.
        Args:
            query (str): Search query (e.g., "pizza").
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.
            count (int): Number of results to return.

        Returns:
            Dict[str, Any]: Response data containing matched restaurants.

        Raises:
            ZomatoAPIError: If the API response indicates an error.
        """
        endpoint = f"{self.BASE_URL}/search"
        params = {
            "q": query,
            "lat": lat,
            "lon": lon,
            "count": count
        }
        try:
            logger.info(f"Searching for restaurants with query '{query}' at location ({lat}, {lon}).")
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info("Successfully fetched restaurant search results.")
            return response.json()
        except requests.RequestException as e:
            error_msg = f"Failed to fetch restaurants: {str(e)}"
            logger.error(error_msg)
            raise ZomatoAPIError(error_msg)

    def get_restaurant_details(self, restaurant_id: int) -> Dict[str, Any]:
        """
        Retrieves details for a specific restaurant.
        Args:
            restaurant_id (int): ID of the restaurant to retrieve details for.

        Returns:
            Dict[str, Any]: Response data containing restaurant details.

        Raises:
            ZomatoAPIError: If the API response indicates an error.
        """
        endpoint = f"{self.BASE_URL}/restaurant"
        params = {"res_id": restaurant_id}
        try:
            logger.info(f"Fetching restaurant details for ID: {restaurant_id}")
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info("Successfully fetched restaurant details.")
            return response.json()
        except requests.RequestException as e:
            error_msg = f"Failed to fetch restaurant details: {str(e)}"
            logger.error(error_msg)
            raise ZomatoAPIError(error_msg)

    def create_order(self, restaurant_id: int, items: Dict[str, int]) -> Dict[str, Any]:
        """
        Simulates creating an order with Zomato (this endpoint may not exist for all APIs).
        This is a custom implementation to integrate with backend logic.
        Args:
            restaurant_id (int): ID of the restaurant where the order is being placed.
            items (Dict[str, int]): A dictionary of item IDs and their quantities.

        Returns:
            Dict[str, Any]: Response data simulating order confirmation.

        Raises:
            ZomatoAPIError: If there is an issue in processing the order.
        """
        logger.info(f"Creating order for restaurant ID {restaurant_id} with items: {items}")

        # In real implementations, you would replace this with actual API integration.
        try:
            # Simulated response for demonstration purposes
            simulated_response = {
                "order_id": "order_12345",
                "restaurant_id": restaurant_id,
                "items": items,
                "status": "confirmed",
                "delivery_time": "30 minutes"
            }
            logger.info("Order created successfully.")
            return simulated_response
        except Exception as e:
            error_msg = f"Failed to simulate order creation: {str(e)}"
            logger.error(error_msg)
            raise ZomatoAPIError(error_msg)