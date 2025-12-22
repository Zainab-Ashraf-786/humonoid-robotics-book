---
title: Gazebo for Robot Simulation
sidebar_label: Gazebo Simulation
---

# Gazebo for Robot Simulation

Gazebo is a powerful, open-source robotics simulator that provides accurate physics simulation, realistic sensor models, and a rich environment for testing robot algorithms. It's one of the most widely-used simulators in robotics research and development, particularly for ROS/ROS 2 integration.

## Learning Objectives

After completing this section, you will:
- Understand Gazebo's architecture and core components
- Know how to create and configure Gazebo simulation environments
- Understand how to integrate robot models with Gazebo's physics engine
- Be able to simulate robot motion and sensor behavior in Gazebo
- Know how to connect Gazebo with ROS/ROS 2 for robot control

## Introduction to Gazebo

### What is Gazebo?
Gazebo is a 3D simulation environment for robotics that provides:
- Realistic physics simulation using ODE, Bullet, or DART physics engines
- High-fidelity rendering with OpenGL
- Accurate sensor simulation (cameras, LIDAR, IMUs, etc.)
- A wide library of robots, sensors, and environments
- Seamless integration with ROS/ROS 2

### Gazebo's Role in the Robotics Ecosystem
Gazebo serves as a bridge between abstract algorithm development and real-world robot deployment. It allows developers to:
- Test algorithms safely before physical deployment
- Simulate various environments and conditions
- Generate large amounts of synthetic data for AI training
- Validate sensor models and robot behaviors

## Installing and Setting Up Gazebo

### System Requirements
- **OS**: Ubuntu 20.04/22.04 LTS, Windows 10/11, or macOS 10.15+ 
- **CPU**: Multi-core processor
- **RAM**: 8GB minimum (16GB recommended)
- **GPU**: OpenGL 3.3+ compatible graphics card with dedicated GPU recommended
- **Storage**: 2GB available space

### Installation
For Ubuntu with ROS 2 Humble Hawksbill:
```bash
sudo apt update
sudo apt install gazebo libgazebo-dev
```

For direct installation:
```bash
sudo apt install gz-harmonic  # For newer Gazebo Garden/Harmonic
# OR
sudo apt install gazebo-classic  # For legacy Gazebo Classic
```

### Basic Launch
```bash
gz sim  # For Gazebo Garden/Harmonic
# OR
gazebo  # For Gazebo Classic
```

## Gazebo Architecture

### Core Components
1. **Physics Engine**: Simulates rigid body dynamics (ODE, Bullet, DART)
2. **Rendering Engine**: Handles visualization (OpenGL)
3. **Sensor System**: Simulates various sensor types
4. **GUI**: Graphical interface for interaction
5. **Transport System**: Inter-component messaging

### Worlds and Models
- **Worlds**: Define the environment, physics properties, and static objects
- **Models**: Represent robots, objects, and dynamic entities
- **Scenarios**: Combine worlds and models for specific simulations

## Defining Gazebo Worlds

### World File Structure
A Gazebo world file is an XML file that defines the simulation environment:

```xml
<?xml version="1.0"?>
<sdf version="1.6">
  <world name="my_world">
    <!-- Physics engine settings -->
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Lighting -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.4 0.2 -0.9</direction>
    </light>

    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
            <specular>0.2 0.2 0.2 1</specular>
          </material>
        </visual>
      </link>
    </model>

    <!-- Include custom models -->
    <!-- More content... -->
  </world>
</sdf>
```

### Physics Configuration
The physics engine settings control simulation accuracy and performance:
- **max_step_size**: Smaller steps increase accuracy but decrease performance
- **real_time_factor**: Target speed relative to real time (1.0 = real-time)
- **real_time_update_rate**: Updates per second

## Robot Model Integration in Gazebo

### SDF vs URDF
- **URDF**: Unified Robot Description Format, primarily used by ROS/ROS 2
- **SDF**: Simulation Description Format, used by Gazebo
- Gazebo can load both formats, but SDF offers more simulation-specific features

### Adding Gazebo-Specific Elements to URDF
To work with Gazebo, URDF models need additional Gazebo-specific elements:

```xml
<robot name="my_robot">
  <!-- Standard URDF content -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="1 1 0.2" />
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="1 1 0.2" />
      </geometry>
    </collision>
    <inertial>
      <mass value="10" />
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0" />
    </inertial>
  </link>

  <!-- Gazebo-specific elements -->
  <gazebo reference="base_link">
    <material>Gazebo/Green</material>
  </gazebo>

  <!-- Sensors -->
  <gazebo reference="imu_link">
    <sensor name="imu_sensor" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <imu>
        <angular_velocity>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </z>
        </angular_velocity>
        <linear_acceleration>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </z>
        </linear_acceleration>
      </imu>
    </sensor>
  </gazebo>
</robot>
```

### Joint Actuation in Gazebo
Controlling robot joints in Gazebo involves defining transmission elements:

```xml
<transmission name="wheel_trans_left">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="left_wheel_hinge">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
  </joint>
  <actuator name="left_wheel_motor">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

## Sensor Simulation in Gazebo

### Camera Sensors
```xml
<gazebo reference="camera_link">
  <sensor name="camera" type="camera">
    <update_rate>30</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>800</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="gz-sim-camera-plugin">
      <frame_name>camera_link_optical</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### LIDAR Sensors
```xml
<gazebo reference="lidar_link">
  <sensor name="lidar" type="gpu_lidar">
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-1.570796</min_angle>
          <max_angle>1.570796</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.10</min>
        <max>30.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="gpu_lidar_controller" filename="gz-sim-lidar-plugin">
      <frame_name>lidar_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### IMU Sensors
```xml
<gazebo reference="imu_link">
  <sensor name="imu" type="imu">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <plugin name="imu_plugin" filename="gz-sim-imu-sensor-system">
      <topic>imu/data</topic>
    </plugin>
  </sensor>
</gazebo>
```

## Gazebo Plugins

### Types of Plugins
Gazebo uses plugins to extend functionality:
- **Sensor Plugins**: Interface sensors with ROS/ROS 2
- **Model Plugins**: Add custom behavior to models
- **World Plugins**: Add custom world behavior
- **System Plugins**: Modify Gazebo's core functionality

### Example Model Plugin
```cpp
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>

namespace gazebo 
{
  class CustomController : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _model, sdf::ElementPtr _sdf)
    {
      this->model = _model;
      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&CustomController::OnUpdate, this));
    }

    public: void OnUpdate()
    {
      // Custom behavior goes here
      this->model->SetLinearVel(math::Vector3(0.5, 0, 0)); // Move forward
    }

    private: physics::ModelPtr model;
    private: event::ConnectionPtr updateConnection;
  };

  GZ_REGISTER_MODEL_PLUGIN(CustomController)
}
```

## ROS/ROS 2 Integration

### Gazebo Bridge
Gazebo integrates with ROS/ROS 2 through bridges that translate between Gazebo messages and ROS/ROS 2 messages:

```xml
<!-- In world file -->
<world>
  <!-- ... other content ... -->
  <gazebo>
    <plugin name="ros_gz_bridge" filename="gz-sim-ros-bridge-system">
      <ros>
        <namespace>/robot</namespace>
      </ros>
      <services>
        <service name="/spawn_entity" type="gazebo_msgs::SpawnEntity">
          <request>
            <entity_name>my_robot</entity_name>
            <robot_namespace>/robot</robot_namespace>
          </request>
        </service>
      </services>
    </plugin>
  </gazebo>
</world>
```

### Common ROS/ROS 2 Topics in Gazebo
- `/clock`: Simulation clock (when enabled)
- `/joint_states`: Joint positions, velocities, efforts
- `/tf` and `/tf_static`: Transform data
- `/gazebo/model_states`: Model poses and twists
- `/gazebo/link_states`: Link poses and twists
- Sensor data topics (e.g., `/camera/image_raw`, `/scan`)

### Controlling Robots in Gazebo with ROS/ROS 2

**Joint Control Example:**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

class GazeboController(Node):
    def __init__(self):
        super().__init__('gazebo_controller')
        
        # Publisher for joint commands
        self.joint_cmd_pub = self.create_publisher(Float64MultiArray, '/joint_commands', 10)
        
        # Subscriber for joint states
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10)
        
        # Timer for control loop
        self.control_timer = self.create_timer(0.02, self.control_loop)  # 50 Hz
        
        self.joint_positions = {}
        
    def joint_state_callback(self, msg):
        self.joint_positions = dict(zip(msg.name, msg.position))
        
    def control_loop(self):
        # Implement control logic
        cmd_msg = Float64MultiArray()
        cmd_msg.data = [0.5, 0.3, -0.2]  # Example joint commands
        self.joint_cmd_pub.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    controller = GazeboController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()
```

## Physics Configuration and Tuning

### Material Properties
Define realistic material interactions in Gazebo:

```xml
<gazebo reference="some_link">
  <collision>
    <surface>
      <friction>
        <ode>
          <mu>0.5</mu>
          <mu2>0.3</mu2>
        </ode>
      </friction>
    </surface>
  </collision>
</gazebo>
```

### Solver Parameters
Tune physics solvers for better stability:

```xml
<physics name="ode" type="ode">
  <solver>
    <type>quick</type>
    <iters>10</iters>
    <sor>1.3</sor>
  </solver>
  <constraints>
    <cfm>0</cfm>
    <erp>0.2</erp>
    <contact_max_correcting_vel>100</contact_max_correcting_vel>
    <contact_surface_layer>0.001</contact_surface_layer>
  </constraints>
</physics>
```

## Gazebo Best Practices for Humanoid Robots

### Kinematic Stability
Humanoid robots require careful attention to stability:

1. **Mass Distribution**: Ensure center of mass remains within the support polygon
2. **Joint Limits**: Set realistic limits for humanoid joints
3. **Friction Parameters**: Tune friction for feet to prevent slipping
4. **Actuator Models**: Use realistic actuator models with limits

### Simulation Fidelity Considerations
For humanoid robotics applications:
- Use high-resolution collision meshes for feet and hands
- Carefully tune COM and moment of inertia properties
- Validate that ZMP and CoM behaviors match expectations
- Implement whole-body controllers properly

### Performance Optimization
- Simulate only necessary parts of the robot when possible
- Use simplified collision geometries for non-critical parts
- Adjust physics update rates based on required accuracy
- Consider using GPU sensors for high-rate data simulation

## Debugging Gazebo Simulations

### Common Issues and Solutions

1. **Robot Falls Through Ground**:
   - Verify collision geometries are properly defined
   - Check that models have appropriate mass and inertial properties
   - Adjust ERP and CFM parameters if needed

2. **Jitters/Unstable Behavior**:
   - Reduce physics time step
   - Adjust solver parameters (iterations, sor, erp, cfm)
   - Check for very thin or malformed collision meshes
   - Verify mass properties are reasonable

3. **Actuators Don't Respond Properly**:
   - Verify transmission configuration matches joint names
   - Check that control interfaces match in URDF and controller
   - Validate control loop timing and message rates

### Debugging Tools
- Use Gazebo's model inspector to examine properties
- Enable contact visualization to see force interactions
- Monitor joint states and effort values in real-time
- Use `gazebo` with verbose flags for detailed logging

## Advanced Gazebo Features

### Multi-Robot Simulation
Gazebo can handle multiple robots in the same environment:
- Use unique namespaces for each robot
- Ensure TF frames don't conflict
- Configure separate controllers for each robot

### Dynamic Environments
Create programmatically changing environments:
- Spawn/remove models during simulation
- Modify properties of existing models
- Generate procedural terrain

### Recording and Playback
Record simulation data for later analysis:
- Use `gz log` to record simulation runs
- Export sensor data for offline processing
- Replay scenarios for consistent testing

## Troubleshooting Common Issues

### Installation and Setup
- **Missing Graphics Support**: Ensure OpenGL 3.3+ is available
- **Permission Issues**: Check user permissions for device access
- **Dependency Problems**: Verify all ROS/ROS 2 dependencies are installed

### Simulation Stability
- **Large Timesteps**: Reduce physics step size for better accuracy
- **High Gains**: Lower controller gains if experiencing oscillation
- **Under-Constrained Models**: Ensure all models are properly constrained

## Summary

Gazebo provides a powerful and flexible platform for robot simulation, particularly for robotics research and development. Its integration with ROS/ROS 2 makes it an ideal choice for testing and validating robotic algorithms on humanoid robots. The key to effective Gazebo usage lies in understanding:

1. The XML-based world and model definition formats
2. How to properly configure physics and sensor properties
3. How to integrate with ROS/ROS 2 for robot control
4. How to tune parameters for optimal performance and stability

## Next Steps

In the next section, we'll explore Unity, which provides high-fidelity rendering and human-robot interaction capabilities that complement Gazebo's physics-focused simulation. Together, these platforms offer comprehensive simulation capabilities for humanoid robotics applications.