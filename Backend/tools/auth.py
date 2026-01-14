import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# Set up logging for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("auth")

# OAuth2 scheme to handle token extraction from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Default secret key and algorithm
SECRET_KEY = os.getenv("SECRET_KEY", "your-production-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expiry in minutes

class AuthError(Exception):
    """Custom exception class for authentication-related errors."""
    pass

class Auth:
    """
    A class to handle user authentication, including token generation and verification.
    """

    @staticmethod
    def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates a new JWT access token.
        Args:
            data (Dict[str, str]): The payload to encode into the token (e.g., user_id, email).
            expires_delta (Optional[timedelta]): Token expiration time.

        Returns:
            str: A signed JWT access token.
        """
        logger.info(f"Creating access token for payload: {data}")
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        try:
            token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            logger.info("Access token successfully created.")
            return token
        except Exception as e:
            logger.error(f"Error creating access token: {e}")
            raise AuthError(f"Failed to create access token: {e}")

    @staticmethod
    def verify_access_token(token: str) -> Dict[str, str]:
        """
        Verifies and decodes a JWT access token.
        Args:
            token (str): The JWT access token to verify.

        Returns:
            Dict[str, str]: The decoded payload from the token.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        logger.info("Verifying access token.")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            logger.info("Access token successfully verified.")
            return payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired.")
            raise HTTPException(status_code=401, detail="Token has expired.")
        except jwt.InvalidTokenError:
            logger.error("Invalid token.")
            raise HTTPException(status_code=401, detail="Invalid token.")

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
        """
        Retrieves the current authenticated user from the token.
        Args:
            token (str): The JWT access token from the request headers.

        Returns:
            Dict[str, str]: User information extracted from the token.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        logger.info("Getting current user from access token.")
        try:
            return Auth.verify_access_token(token)
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise HTTPException(status_code=401, detail=str(e))