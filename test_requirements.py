#!/usr/bin/env python3
"""
Test script to verify that all required dependencies can be imported successfully.
This script tests the most critical imports for the Physical AI & Humanoid Robotics backend.
"""

def test_imports():
    """Test that all critical dependencies can be imported."""
    print("Testing imports...")

    # Core FastAPI and web framework
    try:
        import fastapi
        import uvicorn
        print("[✓] FastAPI and Uvicorn imports successful")
    except ImportError as e:
        print(f"✗ Failed to import FastAPI/Uvicorn: {e}")
        return False

    # Database dependencies
    try:
        import asyncpg
        import aiosqlite
        import sqlalchemy
        print("[✓] Database imports successful")
    except ImportError as e:
        print(f"✗ Failed to import database modules: {e}")
        return False

    # AI/ML dependencies
    try:
        import torch
        import numpy
        import cohere
        import sentence_transformers
        print("[✓] AI/ML imports successful")
    except ImportError as e:
        print(f"✗ Failed to import AI/ML modules: {e}")
        return False

    # Vector database
    try:
        from qdrant_client import QdrantClient
        print("[✓] Qdrant imports successful")
    except ImportError as e:
        print(f"✗ Failed to import Qdrant modules: {e}")
        return False

    # Image processing
    try:
        from PIL import Image
        print("[✓] PIL/Pillow imports successful")
    except ImportError as e:
        print(f"✗ Failed to import PIL/Pillow: {e}")
        return False

    # Utilities
    try:
        import httpx
        import dotenv
        import pydantic
        import tqdm
        import PyPDF2
        print("[✓] Utility imports successful")
    except ImportError as e:
        print(f"✗ Failed to import utility modules: {e}")
        return False

    # Security
    try:
        import bcrypt
        import cryptography
        import jwt
        print("[✓] Security imports successful")
    except ImportError as e:
        print(f"✗ Failed to import security modules: {e}")
        return False

    print("\n[✓] All critical imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🎉 Requirements installation test PASSED!")
    else:
        print("\n❌ Requirements installation test FAILED!")
        exit(1)