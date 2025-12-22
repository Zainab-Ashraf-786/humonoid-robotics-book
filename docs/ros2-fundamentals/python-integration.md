---
title: Python Integration with rclpy
sidebar_label: Python Integration
---

# Python Integration with rclpy

This section covers how to use Python to interact with ROS 2 systems using `rclpy`, the Python client library for ROS 2. Python is often the language of choice for robotics development due to its ease of use, extensive libraries, and strong support for scientific computing.

## Learning Objectives

After completing this section, you will:
- Understand the basics of `rclpy` and how to create ROS 2 nodes in Python
- Be able to publish and subscribe to topics using Python
- Create and use services and actions in Python
- Understand how Python agents interact with ROS controllers
- Apply Python-based ROS 2 development to humanoid robotics applications

## Introduction to rclpy

### What is rclpy?
`rclpy` is the Python client library for ROS 2. It provides Python bindings for the ROS 2 client library (rcl) and enables Python developers to write ROS 2 nodes, publish/subscribe to topics, provide/use services, and send/execute actions.

### Why Python for Robotics?
- Rapid prototyping and development
- Extensive scientific and mathematical libraries (NumPy, SciPy)
- Strong community support
- Easy integration with machine learning frameworks
- Readable and maintainable code

### Installation
`rclpy` is typically installed as part of a ROS 2 distribution. You can install it directly using pip, but it's recommended to install it through the ROS 2 setup process.

## Creating a ROS 2 Node in Python

### Basic Node Structure
A basic ROS 2 node in Python follows this structure:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('node_name')
        # Initialize node components here
        
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Node Lifecycle
1. **Initialization**: Initialize rclpy and create the node
2. **Setup**: Configure publishers, subscribers, services, etc.
3. **Execution**: Use `rclpy.spin()` to keep the node alive
4. **Cleanup**: Destroy the node and shut down rclpy

## Publishing and Subscribing to Topics

### Creating a Publisher
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'topic_name', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    talker = Talker()
    rclpy.spin(talker)
    talker.destroy_node()
    rclpy.shutdown()
```

### Creating a Subscriber
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String,
            'topic_name',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    rclpy.spin(listener)
    listener.destroy_node()
    rclpy.shutdown()
```

## Services in Python

### Creating a Service Server
```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Returning: {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
```

### Creating a Service Client
```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalClient(Node):
    def __init__(self):
        super().__init__('minimal_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClient()
    response = minimal_client.send_request(1, 2)
    minimal_client.get_logger().info(f'Result of add_two_ints: {response.sum}')
    minimal_client.destroy_node()
    rclpy.shutdown()
```

## Actions in Python

### Creating an Action Server
```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]
        
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()
                
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)
        
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
    fibonacci_action_server.destroy_node()
    rclpy.shutdown()
```

### Creating an Action Client
```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

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
        self.get_logger().info(f'Received feedback: {feedback.sequence}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    action_client.send_goal(10)
    rclpy.spin(action_client)
```

## Python and Humanoid Robotics

### Humanoid Control Nodes
Python is particularly useful for humanoid robotics due to its ability to integrate with complex algorithms and rapid prototyping needs:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist

class HumanoidController(Node):
    def __init__(self):
        super().__init__('humanoid_controller')
        
        # Subscribe to joint states
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)
        
        # Publisher for command velocities
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)
        
        # Timer for control loop
        self.control_timer = self.create_timer(0.05, self.control_loop)  # 20 Hz
        
    def joint_state_callback(self, msg):
        # Process joint state information
        self.joint_positions = dict(zip(msg.name, msg.position))
        
    def control_loop(self):
        # Implement humanoid control logic here
        cmd_vel = Twist()
        # Calculate appropriate command based on control algorithm
        self.cmd_vel_pub.publish(cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    controller = HumanoidController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()
```

### Integration with Machine Learning
Python's strength in ML makes it ideal for AI-driven robotics applications:

```python
import rclpy
from rclpy.node import Node
import tensorflow as tf  # Example ML library
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class MLPerceptionNode(Node):
    def __init__(self):
        super().__init__('ml_perception_node')
        self.bridge = CvBridge()
        self.model = self.load_model()  # Load your trained model
        
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
    
    def load_model(self):
        # Load your trained ML model
        return tf.keras.models.load_model('path/to/model')
    
    def image_callback(self, msg):
        # Convert ROS image to OpenCV format
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Run inference
        prediction = self.model.predict(cv_image[None, ...])
        
        # Process prediction and potentially publish results
        # to topics for other nodes to use
```

## Best Practices for Python in ROS 2

### Performance
- Use numpy for mathematical computations
- Consider Cython for performance-critical components
- Be mindful of Python's Global Interpreter Lock (GIL) limitations
- Use appropriate threading models where needed

### Error Handling
- Implement proper exception handling
- Use ROS 2's logging system for debugging
- Handle connection failures gracefully
- Implement timeouts for service calls and actions

### Code Organization
- Use ROS 2 packages for code organization
- Follow PEP 8 style guidelines
- Document code with appropriate docstrings
- Use type hints where appropriate

## Troubleshooting Common Issues

### Import Issues
- Ensure your Python environment is properly configured
- Check that `rclpy` is installed in the correct environment
- Verify that your ROS 2 environment is sourced

### Node Communication Issues
- Use `ros2 node list` to verify nodes are running
- Use `ros2 topic list` to verify topics are available
- Check that topic names match exactly between publishers and subscribers

### Performance Issues
- Monitor CPU and memory usage
- Adjust timer frequencies appropriately
- Consider using asynchronous processing for intensive operations

## Summary

Python with `rclpy` provides a powerful and accessible way to develop ROS 2 applications. Its integration capabilities, ease of use, and strong ecosystem make it an excellent choice for robotics development, particularly in humanoid robotics where rapid prototyping and machine learning integration are important.

## Next Steps

In the next section, we'll cover URDF (Unified Robot Description Format), which is essential for describing robots in ROS 2, particularly important for humanoid robots with complex kinematic structures.