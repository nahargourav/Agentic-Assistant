"""
Authentication routes for user login, registration, and token validation.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta
import logging

from tools.auth import Auth

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("auth_routes")

router = APIRouter()

# In-memory user storage (replace with database in production)
users_db = {}

# Request/Response Models
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    user: dict

class ValidationResponse(BaseModel):
    valid: bool
    user: Optional[dict] = None

# Password hashing utility
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register", status_code=201)
async def register_user(user_data: UserRegister):
    """
    Register a new user with name, email, and password.
    """
    logger.info(f"Registration attempt for email: {user_data.email}")
    
    # Check if user already exists
    if user_data.email in users_db:
        logger.warning(f"Registration failed: Email {user_data.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password and store user
    hashed_password = hash_password(user_data.password)
    users_db[user_data.email] = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password
    }
    
    logger.info(f"User registered successfully: {user_data.email}")
    return {
        "message": "User registered successfully",
        "user": {
            "name": user_data.name,
            "email": user_data.email
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: UserLogin):
    """
    Authenticate user and return JWT token.
    """
    logger.info(f"Login attempt for email: {credentials.email}")
    
    # Check if user exists
    user = users_db.get(credentials.email)
    if not user:
        logger.warning(f"Login failed: User {credentials.email} not found")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(credentials.password, user["password"]):
        logger.warning(f"Login failed: Invalid password for {credentials.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    token_data = {"email": user["email"], "name": user["name"]}
    access_token = Auth.create_access_token(
        data=token_data,
        expires_delta=timedelta(hours=24)
    )
    
    logger.info(f"User logged in successfully: {credentials.email}")
    return {
        "token": access_token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }

@router.get("/validate", response_model=ValidationResponse)
async def validate_token(current_user: dict = Depends(Auth.get_current_user)):
    """
    Validate JWT token and return user information.
    """
    logger.info(f"Token validation for user: {current_user.get('email')}")
    
    # Check if user still exists
    email = current_user.get("email")
    if email not in users_db:
        logger.warning(f"Token validation failed: User {email} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    return {
        "valid": True,
        "user": {
            "name": current_user.get("name"),
            "email": current_user.get("email")
        }
    }
