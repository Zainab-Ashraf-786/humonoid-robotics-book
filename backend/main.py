import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import asyncpg
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize global components
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing application...")

    # Initialize database (will skip if DISABLE_DATABASE is True)
    from app.database import init_database
    await init_database()

    # Initialize VLA system
    logger.info("Initializing VLA (Vision-Language-Action) system...")
    vla_init_success = await initialize_vla_system()
    if vla_init_success:
        logger.info("VLA system initialized successfully")
    else:
        logger.warning("VLA system initialization failed - will operate in simulation mode")

    yield

    # Shutdown
    logger.info("Application shutdown complete")


# Create the FastAPI application
app = FastAPI(
    title="Physical AI & Humanoid Robotics Chat API",
    description="API for the Physical AI & Humanoid Robotics course chatbot with RAG capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow requests from the Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat router
from app.routes.chat import router as chat_router
app.include_router(chat_router)

# Include the VLA (Vision-Language-Action) router
from app.routes.vla import router as vla_router
from app.routes.vla import initialize_vla_system
app.include_router(vla_router)


# Include the user profile router
from app.api.v1.user_profiles import router as user_profiles_router
app.include_router(user_profiles_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "physical-ai-chat-api"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Physical AI & Humanoid Robotics Chat API", "version": "1.0.0"}