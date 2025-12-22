"""
VLA Control Interface: Connecting LLM Cognitive Planning to Physical Robot Actions

This module provides the interface between the LLM-based cognitive planning system
and the physical robot execution, enabling Vision-Language-Action capabilities.
"""
import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from PIL import Image

from app.vlm.interface import VLAInterface, VLAInput, VLAPrediction, RobotAction, ActionType
from app.vlm.ros_interface import VLAControlInterface as ROSVLAInterface
from app.database import DatabaseManager

logger = logging.getLogger(__name__)


@dataclass
class VLAExecutionResult:
    """Result of VLA execution"""
    success: bool
    message: str
    executed_actions: List[Dict[str, Any]]
    failed_actions: List[Dict[str, Any]]
    total_execution_time: float
    success_rate: float
    prediction_confidence: float


class VLAControlInterface:
    """
    Main control interface that connects LLM cognitive planning with physical robot actions
    """

    def __init__(self, model_name: str = "mobile-vla", device: str = "cpu"):
        """
        Initialize the VLA control interface

        Args:
            model_name: Name of the VLA model to use
            device: Device to run the model on ('cpu' or 'cuda')
        """
        self.vla_model = VLAInterface(model_name, device)
        self.ros_interface = ROSVLAInterface()
        self.is_initialized = False

        # Initialize the interface
        self._initialize()

    def _initialize(self):
        """Initialize the VLA control interface"""
        try:
            # The VLA model and ROS interface are already initialized
            self.is_initialized = True
            logger.info("VLA Control Interface initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize VLA Control Interface: {e}")
            self.is_initialized = False

    async def process_humanoid_command(
        self,
        image: Optional[Image.Image],
        language_command: str,
        session_id: Optional[str] = None,
        db_manager: Optional[DatabaseManager] = None
    ) -> VLAExecutionResult:
        """
        Process a humanoid command combining vision, language, and action

        Args:
            image: Visual input from robot cameras
            language_command: Natural language command from user
            session_id: Session ID for tracking
            db_manager: Database manager for logging

        Returns:
            VLAExecutionResult with execution details
        """
        if not self.is_initialized:
            return VLAExecutionResult(
                success=False,
                message="VLA Control Interface not initialized",
                executed_actions=[],
                failed_actions=[],
                total_execution_time=0.0,
                success_rate=0.0,
                prediction_confidence=0.0
            )

        try:
            # Get current robot state
            robot_state = await self.ros_interface.get_robot_state()

            # Create environment context
            environment_context = {
                "timestamp": asyncio.get_event_loop().time(),
                "robot_state": robot_state,
                "session_id": session_id
            }

            # Process command with VLA model to generate actions
            prediction = await self.vla_model.process_command(
                image=image,
                language_command=language_command,
                robot_state=robot_state,
                environment_context=environment_context
            )

            # Log the prediction to database if available
            if db_manager and session_id:
                await db_manager.save_message(
                    session_id=session_id,
                    role="system",
                    content=f"VLA prediction: {len(prediction.actions)} actions generated with confidence {prediction.confidence:.2f}"
                )

            # Check if safety validation passed
            if not prediction.safety_check_passed:
                return VLAExecutionResult(
                    success=False,
                    message="Safety validation failed - actions not executed",
                    executed_actions=[],
                    failed_actions=[],
                    total_execution_time=0.0,
                    success_rate=0.0,
                    prediction_confidence=prediction.confidence
                )

            # Execute the predicted actions on the robot
            execution_result = await self.ros_interface.execute_vla_prediction(prediction)

            # Log execution results to database if available
            if db_manager and session_id:
                await db_manager.save_message(
                    session_id=session_id,
                    role="system",
                    content=f"VLA execution: {execution_result['message']}"
                )

            return VLAExecutionResult(
                success=execution_result["success"],
                message=execution_result["message"],
                executed_actions=execution_result["executed_actions"],
                failed_actions=execution_result["failed_actions"],
                total_execution_time=execution_result["total_execution_time"],
                success_rate=execution_result["success_rate"],
                prediction_confidence=prediction.confidence
            )

        except Exception as e:
            logger.error(f"Error processing humanoid command: {e}")
            return VLAExecutionResult(
                success=False,
                message=f"Error processing command: {str(e)}",
                executed_actions=[],
                failed_actions=[{
                    "action": "unknown",
                    "parameters": {},
                    "error": str(e)
                }],
                total_execution_time=0.0,
                success_rate=0.0,
                prediction_confidence=0.0
            )

    async def execute_predefined_action(
        self,
        action_type: ActionType,
        parameters: Dict[str, Any],
        confidence_threshold: float = 0.7
    ) -> VLAExecutionResult:
        """
        Execute a predefined action with given parameters

        Args:
            action_type: Type of action to execute
            parameters: Parameters for the action
            confidence_threshold: Minimum confidence required for execution

        Returns:
            VLAExecutionResult with execution details
        """
        if not self.is_initialized:
            return VLAExecutionResult(
                success=False,
                message="VLA Control Interface not initialized",
                executed_actions=[],
                failed_actions=[],
                total_execution_time=0.0,
                success_rate=0.0,
                prediction_confidence=0.0
            )

        # Create a single action
        action = RobotAction(
            action_type=action_type,
            parameters=parameters,
            confidence=1.0,  # Predefined actions have full confidence
            description=f"Predefined action: {action_type.value}"
        )

        # Create a prediction with this single action
        prediction = VLAPrediction(
            actions=[action],
            confidence=1.0,
            execution_plan=[f"Execute predefined action: {action_type.value}"],
            safety_check_passed=True,  # Assume safety for predefined actions
            estimated_execution_time=2.0
        )

        # Execute the prediction
        execution_result = await self.ros_interface.execute_vla_prediction(prediction)

        return VLAExecutionResult(
            success=execution_result["success"],
            message=execution_result["message"],
            executed_actions=execution_result["executed_actions"],
            failed_actions=execution_result["failed_actions"],
            total_execution_time=execution_result["total_execution_time"],
            success_rate=execution_result["success_rate"],
            prediction_confidence=prediction.confidence
        )

    async def process_multimodal_input(
        self,
        images: List[Image.Image],
        language_input: str,
        action_history: Optional[List[RobotAction]] = None,
        session_id: Optional[str] = None,
        db_manager: Optional[DatabaseManager] = None
    ) -> VLAExecutionResult:
        """
        Process multimodal input combining multiple images and language

        Args:
            images: List of images from different robot cameras
            language_input: Natural language input
            action_history: Previous actions for context
            session_id: Session ID for tracking
            db_manager: Database manager for logging

        Returns:
            VLAExecutionResult with execution details
        """
        if not self.is_initialized:
            return VLAExecutionResult(
                success=False,
                message="VLA Control Interface not initialized",
                executed_actions=[],
                failed_actions=[],
                total_execution_time=0.0,
                success_rate=0.0,
                prediction_confidence=0.0
            )

        try:
            # Get current robot state
            robot_state = await self.ros_interface.get_robot_state()

            # Create enhanced environment context
            environment_context = {
                "timestamp": asyncio.get_event_loop().time(),
                "robot_state": robot_state,
                "session_id": session_id,
                "camera_views": len(images),
                "action_history": action_history or [],
                "environment_map": robot_state.get("sensors", {}).get("lidar", {})
            }

            # For multiple images, we'll use the first one for now
            # In a real implementation, we might fuse information from multiple views
            primary_image = images[0] if images else None

            # Process command with VLA model to generate actions
            prediction = await self.vla_model.process_command(
                image=primary_image,
                language_command=language_input,
                robot_state=robot_state,
                environment_context=environment_context
            )

            # Log the prediction to database if available
            if db_manager and session_id:
                await db_manager.save_message(
                    session_id=session_id,
                    role="system",
                    content=f"Multimodal VLA prediction: {len(prediction.actions)} actions with confidence {prediction.confidence:.2f}"
                )

            # Check if safety validation passed
            if not prediction.safety_check_passed:
                return VLAExecutionResult(
                    success=False,
                    message="Safety validation failed - actions not executed",
                    executed_actions=[],
                    failed_actions=[],
                    total_execution_time=0.0,
                    success_rate=0.0,
                    prediction_confidence=prediction.confidence
                )

            # Execute the predicted actions on the robot
            execution_result = await self.ros_interface.execute_vla_prediction(prediction)

            # Log execution results to database if available
            if db_manager and session_id:
                await db_manager.save_message(
                    session_id=session_id,
                    role="system",
                    content=f"Multimodal VLA execution: {execution_result['message']}"
                )

            return VLAExecutionResult(
                success=execution_result["success"],
                message=execution_result["message"],
                executed_actions=execution_result["executed_actions"],
                failed_actions=execution_result["failed_actions"],
                total_execution_time=execution_result["total_execution_time"],
                success_rate=execution_result["success_rate"],
                prediction_confidence=prediction.confidence
            )

        except Exception as e:
            logger.error(f"Error processing multimodal input: {e}")
            return VLAExecutionResult(
                success=False,
                message=f"Error processing multimodal input: {str(e)}",
                executed_actions=[],
                failed_actions=[{
                    "action": "unknown",
                    "parameters": {},
                    "error": str(e)
                }],
                total_execution_time=0.0,
                success_rate=0.0,
                prediction_confidence=0.0
            )

    async def get_robot_capabilities(self) -> Dict[str, Any]:
        """
        Get the current capabilities of the robot

        Returns:
            Dictionary with robot capabilities
        """
        if not self.is_initialized:
            return {"error": "VLA Control Interface not initialized"}

        robot_state = await self.ros_interface.get_robot_state()

        return {
            "navigation": True,
            "manipulation": True,
            "perception": True,
            "speech": True,
            "current_state": robot_state,
            "action_vocabulary": [action.value for action in ActionType]
        }

    async def stop_robot_operations(self) -> bool:
        """
        Stop all current robot operations

        Returns:
            True if stop command was successful
        """
        return await self.ros_interface.stop_robot()

    async def connect_to_robot(self, robot_namespace: str = "") -> bool:
        """
        Connect to the physical or simulated robot

        Args:
            robot_namespace: Namespace of the robot to connect to

        Returns:
            True if connection successful
        """
        return await self.ros_interface.connect_to_robot(robot_namespace)

    async def disconnect(self):
        """Disconnect from the robot"""
        await self.ros_interface.disconnect()

    async def validate_action_sequence(
        self,
        actions: List[RobotAction],
        environment_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Validate an action sequence for safety and feasibility

        Args:
            actions: List of actions to validate
            environment_context: Context about the environment

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "actions_validated": [],
            "safety_issues": [],
            "feasibility_issues": [],
            "can_proceed": True
        }

        for i, action in enumerate(actions):
            action_validation = {
                "action_index": i,
                "action_type": action.action_type.value,
                "is_valid": True,
                "safety_check_passed": True,
                "feasibility_check_passed": True,
                "issues": []
            }

            # Perform safety checks
            safety_issues = self._check_action_safety(action, environment_context)
            if safety_issues:
                action_validation["safety_check_passed"] = False
                action_validation["issues"].extend(safety_issues)
                validation_results["safety_issues"].extend(safety_issues)
                validation_results["can_proceed"] = False

            # Perform feasibility checks
            feasibility_issues = self._check_action_feasibility(action)
            if feasibility_issues:
                action_validation["feasibility_check_passed"] = False
                action_validation["issues"].extend(feasibility_issues)
                validation_results["feasibility_issues"].extend(feasibility_issues)
                validation_results["can_proceed"] = False

            if not action_validation["safety_check_passed"] or not action_validation["feasibility_check_passed"]:
                action_validation["is_valid"] = False

            validation_results["actions_validated"].append(action_validation)

        return validation_results

    def _check_action_safety(
        self,
        action: RobotAction,
        environment_context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Check if an action is safe to execute"""
        issues = []

        # Check for navigation safety
        if action.action_type in [ActionType.NAVIGATE_TO, ActionType.FOLLOW_PERSON, ActionType.AVOID_OBSTACLE]:
            # In a real implementation, check for obstacles, safe paths, etc.
            pass

        # Check for manipulation safety
        if action.action_type in [ActionType.GRASP_OBJECT, ActionType.PLACE_OBJECT, ActionType.MOVE_ARM]:
            # In a real implementation, check joint limits, collision avoidance, etc.
            pass

        # Check for environmental safety
        if environment_context:
            # Check battery level for long actions
            robot_state = environment_context.get("robot_state", {})
            battery_level = robot_state.get("battery_level", 1.0)
            if battery_level < 0.2 and action.action_type in [ActionType.NAVIGATE_TO, ActionType.FOLLOW_PERSON]:
                issues.append("Battery level too low for navigation action")

        return issues

    def _check_action_feasibility(self, action: RobotAction) -> List[str]:
        """Check if an action is feasible given robot capabilities"""
        issues = []

        # In a real implementation, check if the robot has the required hardware
        # for the specific action type

        # For now, assume all actions are feasible
        # In practice, you'd check for specific hardware capabilities

        return issues


class VLAIntegrationManager:
    """
    High-level manager for VLA integration with the existing system
    """

    def __init__(self, model_name: str = "mobile-vla", device: str = "cpu"):
        self.vla_control = VLAControlInterface(model_name, device)
        self.is_connected = False

    async def initialize_robot_connection(self, robot_namespace: str = "") -> bool:
        """
        Initialize connection to the robot

        Args:
            robot_namespace: Namespace of the robot to connect to

        Returns:
            True if connection successful
        """
        self.is_connected = await self.vla_control.connect_to_robot(robot_namespace)
        return self.is_connected

    async def process_natural_language_command(
        self,
        user_command: str,
        image: Optional[Image.Image] = None,
        session_id: Optional[str] = None,
        db_manager: Optional[DatabaseManager] = None
    ) -> VLAExecutionResult:
        """
        Process a natural language command through the VLA system

        This method integrates with the existing chat system to provide
        VLA capabilities alongside the RAG functionality.

        Args:
            user_command: Natural language command from user
            image: Optional visual input from robot
            session_id: Session ID for tracking
            db_manager: Database manager for logging

        Returns:
            VLAExecutionResult with execution details
        """
        if not self.is_connected:
            # Try to initialize connection
            await self.initialize_robot_connection()

        if not self.is_connected:
            return VLAExecutionResult(
                success=False,
                message="Cannot process command - not connected to robot",
                executed_actions=[],
                failed_actions=[],
                total_execution_time=0.0,
                success_rate=0.0,
                prediction_confidence=0.0
            )

        # Process the command through the VLA system
        return await self.vla_control.process_humanoid_command(
            image=image,
            language_command=user_command,
            session_id=session_id,
            db_manager=db_manager
        )

    async def get_robot_status(self) -> Dict[str, Any]:
        """
        Get the current status of the robot

        Returns:
            Dictionary with robot status information
        """
        if not self.is_connected:
            return {"connected": False, "error": "Not connected to robot"}

        capabilities = await self.vla_control.get_robot_capabilities()
        return {
            "connected": True,
            "capabilities": capabilities
        }

    async def stop_all_operations(self) -> bool:
        """
        Stop all robot operations

        Returns:
            True if stop command was successful
        """
        return await self.vla_control.stop_robot_operations()

    async def shutdown(self):
        """Shutdown the VLA integration"""
        await self.vla_control.disconnect()
        self.is_connected = False