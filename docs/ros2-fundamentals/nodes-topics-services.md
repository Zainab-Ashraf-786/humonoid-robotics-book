---
title: ROS 2 Nodes, Topics, Services and Actions
sidebar_label: Nodes, Topics, Services, Actions
---

# ROS 2 Nodes, Topics, Services and Actions

This section covers the fundamental communication patterns in ROS 2 that form the "nervous system" of robotic applications. Understanding these concepts is crucial for working with any modern robotics platform.

## Learning Objectives

After completing this section, you will:
- Understand the basic architecture of ROS 2
- Differentiate between nodes, topics, services, and actions
- Know when to use each communication pattern
- Be able to identify these patterns in humanoid robotics applications

## Overview of ROS 2 Architecture

ROS 2 implements a distributed system architecture where computation is spread across multiple processes (potentially on multiple machines) that work together as a single robotic system. The fundamental building blocks of this architecture are:

- **Nodes**: The basic computational unit that performs specific tasks
- **Topics**: Asynchronous, many-to-many communication channels
- **Services**: Synchronous, request-response communication patterns
- **Actions**: Goal-oriented communication for long-running tasks

## Nodes: The Basic Computational Units

### Definition
A node is an executable that uses ROS 2 client library to communicate with other nodes. Nodes are processes that perform computation and can publish or subscribe to messages from topics, provide or use services, and send or execute actions.

### Key Characteristics
- Nodes are organized into packages for distribution
- Each node should have a single responsibility (Unix philosophy)
- Nodes communicate with each other through topics, services, and actions
- Nodes can be written in different languages (C++, Python, etc.)

### Node Naming
- Each node must have a unique name within a ROS 2 domain
- Names should be descriptive of the node's function
- Use lower-case letters and hyphens (e.g., "joint_state_publisher")

### Example Use Cases in Robotics
- Hardware interface nodes: Interface with physical sensors and actuators
- Perception nodes: Process sensor data (computer vision, LIDAR processing)
- Control nodes: Implement control algorithms for robot movement
- Planning nodes: Compute paths and trajectories
- Visualization nodes: Display robot state in GUI applications

## Topics: Asynchronous, Many-to-Many Communication

### Definition
Topics provide a one-way communication channel where one or more publishers send messages to one or more subscribers. This pattern is asynchronous and follows the publish-subscribe model.

### Key Characteristics
- Unidirectional data flow from publishers to subscribers
- Asynchronous communication (no direct coordination needed)
- Many-to-many: multiple publishers can publish to a topic, multiple subscribers can subscribe
- Message-based: data is sent as structured messages
- No delivery guarantees (messages may be lost)
- Rate-based: often used for streaming data at regular intervals

### Quality of Service (QoS)
ROS 2 topics support Quality of Service settings that allow fine-tuning of reliability, durability, and other communication parameters:
- **Reliability**: Reliable vs. Best-effort delivery
- **Durability**: Volatile vs. Transient-local (transient stores messages for late joiners)
- **History**: Keep-all vs. Keep-last (how many messages to store in the queue)

### Example Use Cases in Robotics
- Sensor data streams (LIDAR scans, camera images, IMU readings)
- Robot state information (joint positions, velocities)
- Navigation goals and feedback
- Sensor fusion results

## Services: Synchronous Request-Response Communication

### Definition
Services enable synchronous, two-way communication where a client sends a request and waits for a response from a server. This pattern follows the traditional client-server model.

### Key Characteristics
- Synchronous communication (client waits for response)
- One-to-one: one server serves one request at a time
- Request-response pattern with guaranteed delivery
- Request and response have structured message types
- Not suitable for streaming data

### Example Use Cases in Robotics
- Parameter configuration (setting robot parameters)
- Coordinate transformation lookups
- Map loading and saving
- Robot calibration
- Service-based planning (compute a path once)

## Actions: Goal-Oriented Communication for Long-Running Tasks

### Definition
Actions are a communication pattern for long-running tasks that require goal setting, feedback during execution, and result reporting. They are ideal for tasks that take significant time to complete.

### Key Characteristics
- Asynchronous communication with feedback
- Supports goals, feedback, and results
- Can be preempted to cancel ongoing tasks
- Includes status tracking for long-running operations
- Goal-oriented: designed for tasks with specific objectives

### Three-Part Communication
Actions involve three types of messages:
- **Goal**: Specifies the action request
- **Feedback**: Provides updates during execution
- **Result**: Contains the final outcome

### Example Use Cases in Robotics
- Navigation: Move robot to a specific location with progress updates
- Manipulation: Perform complex arm movements with status updates
- Camera control: Pan, tilt, zoom with feedback on position
- Perception tasks: Long-running object detection with progress updates

## Comparison of Communication Patterns

| Pattern | Synchronicity | Direction | Use Case |
|---------|---------------|-----------|----------|
| Topics | Asynchronous | Unidirectional | Streaming data, state broadcasting |
| Services | Synchronous | Bidirectional | One-off computations, queries |
| Actions | Asynchronous | Bidirectional | Long-running tasks with feedback |

## Humanoid Robotics Specific Considerations

In humanoid robotics applications, these communication patterns are used in specific ways:

### Nodes in Humanoid Systems
- Joint controllers: individual nodes for each joint or group of joints
- Balance controllers: nodes for maintaining stability
- Gait generators: nodes for creating walking patterns
- Vision processing: face detection, object recognition, etc.
- State machines: coordination of complex behaviors

### Topics in Humanoid Systems

**Joint State Broadcasting**
```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class HumanoidJointStatePublisher(Node):
    def __init__(self):
        super().__init__('humanoid_joint_state_publisher')
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.05, self.publish_joint_states)  # 20 Hz

        # Simulated joint positions (in a real robot, these would come from encoders)
        self.joint_positions = {
            'left_hip_yaw': 0.0,
            'left_hip_roll': 0.0,
            'left_hip_pitch': 0.0,
            'left_knee': 0.0,
            'left_ankle_pitch': 0.0,
            'left_ankle_roll': 0.0,
            'right_hip_yaw': 0.0,
            'right_hip_roll': 0.0,
            'right_hip_pitch': 0.0,
            'right_knee': 0.0,
            'right_ankle_pitch': 0.0,
            'right_ankle_roll': 0.0,
            'torso_yaw': 0.0,
            'left_shoulder_pitch': 0.0,
            'left_shoulder_roll': 0.0,
            'left_elbow': 0.0,
            'right_shoulder_pitch': 0.0,
            'right_shoulder_roll': 0.0,
            'right_elbow': 0.0,
            'neck_yaw': 0.0,
            'neck_pitch': 0.0
        }

    def publish_joint_states(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"

        # Get joint names and positions
        msg.name = list(self.joint_positions.keys())
        msg.position = [self.joint_positions[joint] for joint in msg.name]

        # Simulate some periodic movement for demonstration
        t = self.get_clock().now().nanoseconds / 1e9  # time in seconds
        self.joint_positions['left_elbow'] = 0.5 * math.sin(t)
        self.joint_positions['right_shoulder_pitch'] = 0.2 * math.cos(t * 0.7)

        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    publisher = HumanoidJointStatePublisher()
    rclpy.spin(publisher)
    publisher.destroy_node()
    rclpy.shutdown()
```

**Sensor Data Streams**
- IMU: Broadcasting orientation, angular velocity, and linear acceleration data
- Force/Torque Sensors: Publishing ground contact forces, joint torques
- Cameras: Streaming RGB, depth, and thermal images
- LIDAR: Providing environmental distance measurements

### Services in Humanoid Systems
- Emergency stop: quickly stop all robot motion
- Calibration: calibrate sensors or joint offsets
- Map management: load, save, or clear maps
- Parameter updates: modify controller parameters during run-time

**Example Service Call for Calibration**
```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import time

class CalibrationManager(Node):
    def __init__(self):
        super().__init__('calibration_manager')
        self.cli = self.create_client(Trigger, '/calibrate_joints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Calibration service not available, waiting...')

    def calibrate_robot(self):
        req = Trigger.Request()
        future = self.cli.call_async(req)

        # Wait for the result
        rclpy.spin_until_future_complete(self, future)

        result = future.result()
        if result.success:
            self.get_logger().info('Robot calibration completed successfully')
        else:
            self.get_logger().error(f'Calibration failed: {result.message}')

def main(args=None):
    rclpy.init(args=args)
    calibrator = CalibrationManager()

    # Start calibration process
    calibrator.calibrate_robot()

    calibrator.destroy_node()
    rclpy.shutdown()
```

### Actions in Humanoid Systems
- Walking: move to a specific location with step-by-step feedback
- Reaching: move arm to grasp an object with path updates
- Audio playback: play speech with start/progress/end tracking
- Complex behaviors: dance routines, exercise sequences

**Example Action for Walking Navigation**
```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import time

class HumanoidWalker(Node):
    def __init__(self):
        super().__init__('humanoid_walker')
        self._action_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose')

    def send_goal(self, x, y, theta):
        goal_msg = NavigateToPose.Goal()

        # Create pose
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0

        # Convert angle to quaternion
        from math import sin, cos
        qw = cos(theta / 2)
        qz = sin(theta / 2)
        goal_msg.pose.pose.orientation.w = qw
        goal_msg.pose.pose.orientation.z = qz

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: Current pose = {feedback.current_pose.pose.position.x:.2f}, {feedback.current_pose.pose.position.y:.2f}')

    def get_result_callback(self, future):
        result = future.result().result
        if result.result.status == result.result.SUCCEEDED:
            self.get_logger().info('Navigation goal reached!')
        else:
            self.get_logger().info('Navigation failed!')


def main(args=None):
    rclpy.init(args=args)
    walker = HumanoidWalker()

    # Send a walking goal (move to coordinates 1.0, 1.0 with rotation)
    walker.send_goal(1.0, 1.0, 0.0)

    rclpy.spin(walker)
    walker.destroy_node()
    rclpy.shutdown()
```

## Best Practices

### Design Principles
- Keep nodes focused: each node should have a single, well-defined responsibility
- Use appropriate communication patterns: don't use services for streaming data
- Design message types carefully: keep them efficient and well-structured
- Consider QoS settings: choose appropriate reliability and durability settings

### Performance Considerations
- Limit message frequency on topics to avoid network congestion
- Use appropriate message sizes: avoid very large messages on high-frequency topics
- Consider data compression for large sensor streams
- Use latching for static data that late-joining nodes need

### Debugging and Monitoring
- Use `ros2 topic echo` to monitor topic data
- Use `ros2 service call` to test services
- Use `ros2 action send_goal` to test actions
- Use `rqt_graph` to visualize the node graph

## Summary

ROS 2's communication patterns (nodes, topics, services, and actions) form the backbone of robotic software architecture. Understanding when and how to use each pattern is crucial for building robust, maintainable robotic systems. These concepts will be used extensively throughout the course as we build increasingly complex robotic applications, particularly in humanoid robotics where coordination of many subsystems is essential.

## Next Steps

In the next section, we'll explore how to work with these concepts using Python and the `rclpy` client library, which is the primary interface for Python-based ROS 2 nodes.