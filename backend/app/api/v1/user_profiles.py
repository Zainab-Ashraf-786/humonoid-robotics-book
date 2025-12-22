"""
User Profile API Endpoints for the Physical AI & Humanoid Robotics Platform
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any, Optional
import logging

from app.database import DatabaseManager, get_db
from app.services.user_profile_service import UserProfileService

from app.models.user_profile import UserProfile

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.get("/", response_model=Dict[str, Any])
async def get_profile(
    current_user: Optional[Dict] = None,
    db: DatabaseManager = Depends(get_db)
):
    """
    Get the current user's profile information
    """
    try:
        # If no user is authenticated, return an empty profile
        if not current_user or not current_user.get("id"):
            profile_data = {
                "user_id": "anonymous",
                "software_background": None,
                "hardware_background": None,
                "experience_level": "beginner",
                "programming_languages": "not specified",
                "learning_goals": "general learning",
                "created_at": None,
                "updated_at": None
            }
            return profile_data

        # Create profile service instance
        profile_service = UserProfileService(db)

        # Get user profile
        profile = await profile_service.get_user_profile(current_user["id"])

        if not profile:
            # Return empty profile if user doesn't have one yet
            profile_data = {
                "user_id": current_user["id"],
                "software_background": None,
                "hardware_background": None,
                "experience_level": "beginner",
                "programming_languages": "not specified",
                "learning_goals": "general learning",
                "created_at": None,
                "updated_at": None
            }
        else:
            profile_data = profile.to_dict()

        return profile_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting profile: {e}")

        # Raise a generic error to avoid exposing internal details
        raise HTTPException(status_code=500, detail="An error occurred while retrieving profile")


@router.put("/", response_model=Dict[str, Any])
async def update_profile(
    request: Request,
    software_background: Optional[str] = None,
    hardware_background: Optional[str] = None,
    experience_level: Optional[str] = None,
    programming_languages: Optional[str] = None,
    learning_goals: Optional[str] = None,
    current_user: Optional[Dict] = None,
    db: DatabaseManager = Depends(get_db)
):
    """
    Update the current user's profile information
    """
    try:
        # If no user is authenticated, return an error or handle as needed
        if not current_user or not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Authentication required to update profile")

        # Validate experience level if provided
        if experience_level and experience_level not in ["beginner", "intermediate", "advanced"]:
            raise HTTPException(status_code=400, detail="Experience level must be one of: beginner, intermediate, advanced")

        # Create profile service instance
        profile_service = UserProfileService(db)

        # Prepare updates
        updates = {}
        if software_background is not None:
            updates["software_background"] = software_background
        if hardware_background is not None:
            updates["hardware_background"] = hardware_background
        if experience_level is not None:
            updates["experience_level"] = experience_level
        if programming_languages is not None:
            updates["programming_languages"] = programming_languages
        if learning_goals is not None:
            updates["learning_goals"] = learning_goals

        # Update user profile
        success = await profile_service.update_user_profile(current_user["id"], **updates)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to update profile")

        # Return updated profile
        updated_profile = await profile_service.get_user_profile(current_user["id"])
        return updated_profile.to_dict()

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        logger = logging.getLogger(__name__)
        logger.error(f"Error updating profile: {e}")

        # Raise a generic error to avoid exposing internal details
        raise HTTPException(status_code=500, detail="An error occurred while updating profile")