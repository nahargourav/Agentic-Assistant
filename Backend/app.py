"""
Main entry point for the FastAPI Assistant Application.
Starts the backend server for the Assistant App.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# Import routers
from api.routes import task, status
from api.routes.auth import router as auth_router
from api.routes.assistant import router as assistant_router

# Lifespan handles startup and shutdown logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting up the Assistant API...")
    yield  # Serve the application
    # Shutdown logic
    print("Shutting down the Assistant API...")

# Create FastAPI instance with lifespan context
app = FastAPI(
    title="Assistant API",
    description="API backend for the AI-powered Assistant with authentication and voice/text commands.",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow client requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(assistant_router, prefix="/assistant", tags=["Assistant"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(status.router, prefix="/status", tags=["Status"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that provides a welcome message.
    """
    return {"message": "Welcome to the Assistant API. Ready to process your commands!"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
