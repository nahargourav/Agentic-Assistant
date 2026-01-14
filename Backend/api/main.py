# Entry point for REST APIs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.routes import task, status

# Lifespan handles startup and shutdown logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting up the Agentic Assistant API...")
    # Add database connection initialization or model loading here
    yield  # Serve the application
    # Shutdown logic
    print("Shutting down the Agentic Assistant API...")
    # Add resource cleanup logic here

# Create FastAPI instance with lifespan context
app = FastAPI(
    title="Agentic Assistant API",
    description="API backend for the FAANG-level Agentic Assistant built with Model-Context-Protocol (MCP).",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow client requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(status.router, prefix="/status", tags=["Status"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that provides a welcome message.
    """
    return {"message": "Welcome to the Agentic Assistant API. Ready to process tasks!"}