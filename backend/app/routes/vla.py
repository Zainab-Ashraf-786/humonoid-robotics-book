"""
VLA (Vision-Language-Action) API Routes

This module provides API endpoints for VLA functionality,
connecting the web interface with the VLA pipeline and ROS 2 systems.
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import uuid
from datetime import datetime

from PIL import Image
import io

from app.database import DatabaseManager, get_db
from app.services.user_profile_service import UserProfileService
from app.vlm.pipeline import VLAPipelineManager, VLAPipelineInput, VLAPipelineOutput
from app.vlm.interface import ActionType

logger = logging.getLogger(__name__)
router = APIRouter()

# Global VLA pipeline manager instance
vla_manager = VLAPipelineManager()


class VLARequest(BaseModel):
    """Request model for VLA commands"""
    image: Optional[str] = None  # Base64 encoded image or URL
    language_command: str
    session_id: Optional[str] = None
    robot_namespace: Optional[str] = ""


class VLACommandSequenceRequest(BaseModel):
    """Request model for VLA command sequences"""
    commands: List[str]
    session_id: Optional[str] = None
    robot_namespace: Optional[str] = ""


class VLAResponse(BaseModel):
    """Response model for VLA operations"""
    success: bool
    message: str
    session_id: str
    actions_executed: List[Dict[str, Any]]
    execution_time: float
    confidence: float


class VLAStatusResponse(BaseModel):
    """Response model for VLA status"""
    connected: bool
    robot_status: Dict[str, Any]
    pipeline_status: str
    active_sessions: int


@router.post("/vla/command", response_model=VLAResponse)
async def vla_command(
    request: VLARequest,
    current_user: Optional[dict] = None,
    db: DatabaseManager = Depends(get_db)
):
    """
    Process a Vision-Language-Action command
    """
    try:
        # Determine user ID - use authenticated user ID if available, otherwise anonymous
        user_id = "anonymous"
        if current_user and current_user.get("id"):
            user_id = current_user["id"]

        # Get user profile for personalization if user is authenticated
        user_profile_context = {}
        if user_id != "anonymous" and db is not None:
            try:
                profile_service = UserProfileService(db)
                user_profile_context = await profile_service.get_personalization_context(user_id)
            except Exception as e:
                logger.warning(f"Could not retrieve user profile for personalization: {e}")
                # Use default context for anonymous users
                user_profile_context = {
                    "experience_level": "beginner",
                    "software_background": "general",
                    "hardware_background": "general",
                    "programming_languages": "not specified",
                    "learning_goals": "general learning"
                }
        else:
            # Default context for anonymous users
            user_profile_context = {
                "experience_level": "beginner",
                "software_background": "general",
                "hardware_background": "general",
                "programming_languages": "not specified",
                "learning_goals": "general learning"
            }

        # Generate session ID if not provided
        session_id = request.session_id or f"vla_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"

        # Log the command to database with user context
        if db:
            await db.save_message(
                session_id=session_id,
                role="user",
                content=f"VLA command: {request.language_command}",
                user_id=user_id
            )

        # Process the command through the VLA pipeline
        result = await vla_manager.run_single_command(
            language_command=request.language_command,
            image=None,  # For now, no image processing through this endpoint
            session_id=session_id,
            db_manager=db
        )

        # Log the response to database
        if db:
            await db.save_message(
                session_id=session_id,
                role="assistant",
                content=f"VLA response: {result.message}",
                user_id=user_id
            )

        # Extract confidence from the first action if available
        confidence = 0.0
        if result.execution_result:
            confidence = result.execution_result.prediction_confidence

        return VLAResponse(
            success=result.success,
            message=result.message,
            session_id=session_id,
            actions_executed=result.actions_executed,
            execution_time=result.execution_time,
            confidence=confidence
        )

    except Exception as e:
        logger.error(f"Error in VLA command endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing VLA command: {str(e)}")


@router.post("/vla/command-with-image", response_model=VLAResponse)
async def vla_command_with_image(
    language_command: str,
    image: UploadFile = File(...),
    session_id: Optional[str] = None,
    robot_namespace: Optional[str] = "",
    current_user: Optional[dict] = None,
    db: DatabaseManager = Depends(get_db)
):
    """
    Process a Vision-Language-Action command with image input
    """
    try:
        # Determine user ID - use authenticated user ID if available, otherwise anonymous
        user_id = "anonymous"
        if current_user and current_user.get("id"):
            user_id = current_user["id"]

        # Get user profile for personalization if user is authenticated
        user_profile_context = {}
        if user_id != "anonymous" and db is not None:
            try:
                profile_service = UserProfileService(db)
                user_profile_context = await profile_service.get_personalization_context(user_id)
            except Exception as e:
                logger.warning(f"Could not retrieve user profile for personalization: {e}")
                # Use default context for anonymous users
                user_profile_context = {
                    "experience_level": "beginner",
                    "software_background": "general",
                    "hardware_background": "general",
                    "programming_languages": "not specified",
                    "learning_goals": "general learning"
                }
        else:
            # Default context for anonymous users
            user_profile_context = {
                "experience_level": "beginner",
                "software_background": "general",
                "hardware_background": "general",
                "programming_languages": "not specified",
                "learning_goals": "general learning"
            }

        # Generate session ID if not provided
        session_id = session_id or f"vla_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"

        # Read and process the uploaded image
        image_content = await image.read()
        pil_image = Image.open(io.BytesIO(image_content))

        # Log the command to database
        if db:
            await db.save_message(
                session_id=session_id,
                role="user",
                content=f"VLA command with image: {language_command}",
                user_id=user_id
            )

        # Process the command through the VLA pipeline
        result = await vla_manager.run_single_command(
            language_command=language_command,
            image=pil_image,
            session_id=session_id,
            db_manager=db
        )

        # Log the response to database
        if db:
            await db.save_message(
                session_id=session_id,
                role="assistant",
                content=f"VLA response: {result.message}",
                user_id=user_id
            )

        # Extract confidence from the first action if available
        confidence = 0.0
        if result.execution_result:
            confidence = result.execution_result.prediction_confidence

        return VLAResponse(
            success=result.success,
            message=result.message,
            session_id=session_id,
            actions_executed=result.actions_executed,
            execution_time=result.execution_time,
            confidence=confidence
        )

    except Exception as e:
        logger.error(f"Error in VLA command with image endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing VLA command with image: {str(e)}")


@router.post("/vla/command-sequence", response_model=VLAResponse)
async def vla_command_sequence(
    request: VLACommandSequenceRequest,
    current_user: Optional[dict] = None,
    db: DatabaseManager = Depends(get_db)
):
    """
    Process a sequence of Vision-Language-Action commands
    """
    try:
        # Determine user ID - use authenticated user ID if available, otherwise anonymous
        user_id = "anonymous"
        if current_user and current_user.get("id"):
            user_id = current_user["id"]

        # Get user profile for personalization if user is authenticated
        user_profile_context = {}
        if user_id != "anonymous" and db is not None:
            try:
                profile_service = UserProfileService(db)
                user_profile_context = await profile_service.get_personalization_context(user_id)
            except Exception as e:
                logger.warning(f"Could not retrieve user profile for personalization: {e}")
                # Use default context for anonymous users
                user_profile_context = {
                    "experience_level": "beginner",
                    "software_background": "general",
                    "hardware_background": "general",
                    "programming_languages": "not specified",
                    "learning_goals": "general learning"
                }
        else:
            # Default context for anonymous users
            user_profile_context = {
                "experience_level": "beginner",
                "software_background": "general",
                "hardware_background": "general",
                "programming_languages": "not specified",
                "learning_goals": "general learning"
            }

        # Generate session ID if not provided
        session_id = request.session_id or f"vla_seq_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"

        # Log the command sequence to database
        if db:
            await db.save_message(
                session_id=session_id,
                role="user",
                content=f"VLA command sequence: {len(request.commands)} commands",
                user_id=user_id
            )

        # Process the command sequence
        results = await vla_manager.run_task_sequence(
            commands=request.commands,
            session_id=session_id,
            db_manager=db
        )

        # Aggregate results
        success = all(result.success for result in results)
        total_execution_time = sum(result.execution_time for result in results)
        total_actions = sum(len(result.actions_executed) for result in results)

        message = f"Executed {len(results)} commands, {total_actions} total actions"
        if not success:
            message += " (some commands failed)"

        # Calculate average confidence
        valid_confidences = [
            result.execution_result.prediction_confidence
            for result in results
            if result.execution_result
        ]
        avg_confidence = sum(valid_confidences) / len(valid_confidences) if valid_confidences else 0.0

        # Log the response to database
        if db:
            await db.save_message(
                session_id=session_id,
                role="assistant",
                content=f"VLA sequence response: {message}",
                user_id=user_id
            )

        return VLAResponse(
            success=success,
            message=message,
            session_id=session_id,
            actions_executed=[],  # Actions are aggregated differently for sequences
            execution_time=total_execution_time,
            confidence=avg_confidence
        )

    except Exception as e:
        logger.error(f"Error in VLA command sequence endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing VLA command sequence: {str(e)}")


@router.get("/vla/status", response_model=VLAStatusResponse)
async def vla_status():
    """
    Get the status of the VLA system
    """
    try:
        # Get robot status
        robot_status = await vla_manager.pipeline.vla_control.get_robot_status()

        return VLAStatusResponse(
            connected=robot_status.get("connected", False),
            robot_status=robot_status,
            pipeline_status="initialized" if vla_manager.pipeline.is_initialized else "not_initialized",
            active_sessions=len(vla_manager.active_sessions)
        )

    except Exception as e:
        logger.error(f"Error in VLA status endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting VLA status: {str(e)}")


@router.post("/vla/stop-session")
async def stop_vla_session(
    session_id: str
):
    """
    Stop a VLA session
    """
    try:
        success = await vla_manager.stop_session(session_id)
        return {"success": success, "session_id": session_id}
    except Exception as e:
        logger.error(f"Error stopping VLA session: {e}")
        raise HTTPException(status_code=500, detail=f"Error stopping VLA session: {str(e)}")


@router.get("/vla/session/{session_id}")
async def get_vla_session_status(
    session_id: str
):
    """
    Get the status of a specific VLA session
    """
    try:
        status = vla_manager.get_session_status(session_id)
        if status is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting VLA session status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting VLA session status: {str(e)}")


# Enhanced endpoint that connects with the existing chat system
@router.post("/vla/chat-integration")
async def vla_chat_integration(
    request: VLARequest,
    current_user: Optional[dict] = None,
    db: DatabaseManager = Depends(get_db)
):
    """
    VLA integration with the existing chat system
    This endpoint can be called when the chat system determines that a command
    requires physical robot action rather than just informational response.
    """
    try:
        # Determine user ID - use authenticated user ID if available, otherwise anonymous
        user_id = "anonymous"
        if current_user and current_user.get("id"):
            user_id = current_user["id"]

        # Get user profile for personalization if user is authenticated
        user_profile_context = {}
        if user_id != "anonymous" and db is not None:
            try:
                profile_service = UserProfileService(db)
                user_profile_context = await profile_service.get_personalization_context(user_id)
            except Exception as e:
                logger.warning(f"Could not retrieve user profile for personalization: {e}")
                # Use default context for anonymous users
                user_profile_context = {
                    "experience_level": "beginner",
                    "software_background": "general",
                    "hardware_background": "general",
                    "programming_languages": "not specified",
                    "learning_goals": "general learning"
                }
        else:
            # Default context for anonymous users
            user_profile_context = {
                "experience_level": "beginner",
                "software_background": "general",
                "hardware_background": "general",
                "programming_languages": "not specified",
                "learning_goals": "general learning"
            }

        # Generate session ID if not provided
        session_id = request.session_id or f"vla_chat_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"

        # Log the integration request to database
        if db:
            await db.save_message(
                session_id=session_id,
                role="system",
                content=f"VLA chat integration: {request.language_command}",
                user_id=user_id
            )

        # Process the command through the VLA pipeline
        result = await vla_manager.run_single_command(
            language_command=request.language_command,
            image=None,
            session_id=session_id,
            db_manager=db
        )

        # Prepare response in format compatible with chat system
        response_data = {
            "vla_success": result.success,
            "message": result.message,
            "session_id": session_id,
            "actions_executed": result.actions_executed,
            "execution_time": result.execution_time,
            "requires_physical_action": True,  # Indicate this was a physical action
            "chat_fallback": False,  # Indicate this was handled by VLA
            "user_profile_context": user_profile_context  # Include user profile context for potential use
        }

        # Log the response to database
        if db:
            await db.save_message(
                session_id=session_id,
                role="system",
                content=f"VLA chat integration response: {result.message}",
                user_id=user_id
            )

        return response_data

    except Exception as e:
        logger.error(f"Error in VLA chat integration endpoint: {e}")

        # Return fallback response that can be handled by chat system
        return {
            "vla_success": False,
            "message": f"VLA system unavailable: {str(e)}",
            "session_id": request.session_id,
            "actions_executed": [],
            "execution_time": 0.0,
            "requires_physical_action": True,
            "chat_fallback": True,  # Indicate that chat system should handle this
            "fallback_message": f"Physical action requested but VLA system unavailable: {request.language_command}",
            "user_profile_context": user_profile_context  # Include user profile context for potential use
        }


# Initialize robot connection when the service starts
async def initialize_vla_system(robot_namespace: str = ""):
    """
    Initialize the VLA system and connect to robot
    This function can be called at application startup
    """
    try:
        success = await vla_manager.pipeline.vla_control.initialize_robot_connection(robot_namespace)
        if success:
            logger.info("VLA system initialized and connected to robot")
        else:
            logger.warning("VLA system initialized but could not connect to robot")
        return success
    except Exception as e:
        logger.error(f"Error initializing VLA system: {e}")
        return False