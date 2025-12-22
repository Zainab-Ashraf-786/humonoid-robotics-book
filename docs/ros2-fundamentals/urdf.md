---
title: URDF for Robot Description
sidebar_label: URDF
---

# URDF for Robot Description

This section covers URDF (Unified Robot Description Format), the standard XML format used in ROS for describing robot models. URDF is crucial for humanoid robotics as it defines the kinematic and dynamic properties of robots, enabling simulation, visualization, and control.

## Learning Objectives

After completing this section, you will:
- Understand the structure and components of URDF files
- Know how to create and modify robot descriptions using URDF
- Be familiar with common URDF elements and their properties
- Understand how URDF is used in simulation and visualization
- Apply URDF concepts to humanoid robot modeling

## Introduction to URDF

### What is URDF?
URDF (Unified Robot Description Format) is an XML format used to describe robot models in ROS. It specifies the physical properties of a robot including:
- Kinematic structure (joints and links)
- Visual and collision properties
- Inertial properties
- Sensor locations and properties

### Why URDF is Important
- **Simulation**: Allows robots to be accurately simulated in environments like Gazebo
- **Visualization**: Enables proper display of robots in tools like RViz
- **Control**: Provides kinematic information needed for motion planning and control
- **Standardization**: Offers a common format for robot description across the ROS ecosystem

## URDF Structure

### Basic Structure
A URDF file has a basic structure with a robot element as the root:

```xml
<?xml version="1.0" ?>
<robot name="robot_name" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Links define rigid bodies -->
  <link name="link_name">
    <!-- Visual properties -->
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <box size="1 1 1" />
      </geometry>
      <material name="color">
        <color rgba="0.8 0.2 0.2 1.0" />
      </material>
    </visual>
    
    <!-- Collision properties -->
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <box size="1 1 1" />
      </geometry>
    </collision>
    
    <!-- Inertial properties -->
    <inertial>
      <mass value="1.0" />
      <origin xyz="0 0 0" rpy="0 0 0" />
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0" />
    </inertial>
  </link>
  
  <!-- Joints connect links -->
  <joint name="joint_name" type="revolute">
    <parent link="parent_link" />
    <child link="child_link" />
    <origin xyz="0 0 1" rpy="0 0 0" />
    <axis xyz="0 0 1" />
    <limit lower="-3.14159" upper="3.14159" effort="100" velocity="1" />
  </joint>
</robot>
```

### Key Concepts
- **Links**: Rigid bodies that make up the robot structure
- **Joints**: Connections between links with specific degrees of freedom
- **Materials**: Visual properties like color and texture
- **Transmissions**: How joints connect to actuators (for control)

## Links: The Building Blocks

### Link Properties
Each link in a URDF represents a rigid body with three main components:

1. **Visual**: How the link appears in visualization
   - Geometry: Shape (box, cylinder, sphere, mesh)
   - Origin: Position and orientation relative to the link frame
   - Material: Color and appearance properties

2. **Collision**: How the link interacts in physics simulation
   - Usually simpler geometry than visual for performance
   - Defines collision boundaries

3. **Inertial**: Physical properties for dynamics simulation
   - Mass: The mass of the link
   - Origin: Center of mass location
   - Inertia: Moments and products of inertia

### Example Link Definition
```xml
<link name="base_link">
  <visual>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <geometry>
      <cylinder length="0.2" radius="0.1"/>
    </geometry>
    <material name="blue">
      <color rgba="0 0 0.8 1"/>
    </material>
  </visual>
  <collision>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <geometry>
      <cylinder length="0.2" radius="0.1"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="1.0"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.05"/>
  </inertial>
</link>
```

## Joints: Connecting the Robot

### Joint Types
URDF supports several joint types:

1. **Revolute**: Rotational joint with limited range
   ```xml
   <joint name="joint_name" type="revolute">
     <parent link="parent_link"/>
     <child link="child_link"/>
     <axis xyz="0 0 1"/>
     <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
   </joint>
   ```

2. **Continuous**: Rotational joint without limits
   ```xml
   <joint name="joint_name" type="continuous">
     <parent link="parent_link"/>
     <child link="child_link"/>
     <axis xyz="0 0 1"/>
   </joint>
   ```

3. **Prismatic**: Linear sliding joint with limits
   ```xml
   <joint name="joint_name" type="prismatic">
     <parent link="parent_link"/>
     <child link="child_link"/>
     <axis xyz="0 0 1"/>
     <limit lower="0" upper="0.1" effort="10" velocity="1"/>
   </joint>
   ```

4. **Fixed**: No movement between links
   ```xml
   <joint name="joint_name" type="fixed">
     <parent link="parent_link"/>
     <child link="child_link"/>
   </joint>
   ```

5. **Floating**: 6 degrees of freedom (rarely used)
6. **Planar**: Motion on a plane (rarely used)

### Joint Properties
- **Origin**: Position and orientation of the joint relative to the parent link
- **Axis**: Direction of motion for the joint
- **Limits**: For revolute and prismatic joints, the range of motion and physical limits
- **Safety Controller**: Optional safety limits

## URDF for Humanoid Robotics

### Humanoid Robot Structure
Humanoid robots have a specific structure that affects their URDF:
- **Torso**: Central body with sensors and processing units
- **Head**: With cameras, microphones, and displays
- **Arms**: With multiple joints for manipulation
- **Legs**: With joints for walking and balance
- **End effectors**: Hands and feet

### Kinematic Chains
Humanoid robots typically have multiple kinematic chains:
- Left arm: From torso to left hand
- Right arm: From torso to right hand
- Left leg: From torso to left foot
- Right leg: From torso to right foot
- Head: From torso to head

### Example Humanoid Joint Structure
```xml
<!-- Head joints -->
<joint name="neck_joint" type="revolute">
  <parent link="torso"/>
  <child link="head"/>
  <origin xyz="0 0 0.8" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-0.5" upper="0.5" effort="10" velocity="1"/>
</joint>

<!-- Simple arm structure -->
<joint name="shoulder_joint" type="revolute">
  <parent link="torso"/>
  <child link="upper_arm"/>
  <origin xyz="0.2 0 0.7" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
</joint>
```

## Working with Meshes in URDF

### Using 3D Models
For realistic visualization, URDF can reference 3D mesh files:

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <mesh filename="package://robot_description/meshes/part.stl" scale="1 1 1"/>
  </geometry>
  <material name="gray">
    <color rgba="0.5 0.5 0.5 1.0"/>
  </material>
</visual>
```

### Mesh Formats
- **STL**: Simple, widely supported
- **DAE**: Collada format with textures
- **OBJ**: Wavefront format
- **PLY**: Polygon file format

## URDF Tools and Validation

### xacro: URDF Macros
Xacro allows you to create reusable, parameterized URDF components:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="robot">

  <xacro:macro name="simple_link" params="name xyz:='0 0 0' rpy:='0 0 0'">
    <link name="${name}">
      <visual>
        <origin xyz="${xyz}" rpy="${rpy}"/>
        <geometry>
          <box size="0.1 0.1 0.1"/>
        </geometry>
        <material name="red">
          <color rgba="0.8 0.2 0.2 1.0"/>
        </material>
      </visual>
      <collision>
        <origin xyz="${xyz}" rpy="${rpy}"/>
        <geometry>
          <box size="0.1 0.1 0.1"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="0.1"/>
        <origin xyz="${xyz}" rpy="${rpy}"/>
        <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
      </inertial>
    </link>
  </xacro:macro>

  <xacro:simple_link name="base" xyz="0 0 0.05"/>
</robot>
```

### Validation Tools
- **check_urdf**: Command-line tool to validate URDF syntax
  ```bash
  check_urdf /path/to/robot.urdf
  ```

- **urdf_to_graphiz**: Visualize the kinematic tree
  ```bash
  urdf_to_graphiz robot.urdf
  ```

- **RViz**: Real-time visualization and debugging

## Transmissions: Connecting to Hardware

### Transmission Elements
Transmissions define how joints connect to actuators:

```xml
<transmission name="joint1_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="joint1">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
  </joint>
  <actuator name="joint1_motor">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Hardware Interfaces
- **PositionJointInterface**: Control joint position
- **VelocityJointInterface**: Control joint velocity
- **EffortJointInterface**: Control joint torque/force

## Gazebo-Specific Extensions

### Adding Gazebo Elements
URDF can include Gazebo-specific extensions:

```xml
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
</gazebo>
```

### Sensors in URDF
Gazebo sensors can be defined within the URDF:

```xml
<gazebo reference="camera_link">
  <sensor name="camera1" type="camera">
    <update_rate>30.0</update_rate>
    <camera name="head_camera">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>800</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_optical_frame</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## Best Practices

### Organization
- Use packages for URDF resources
- Separate visual and collision geometries when appropriate
- Use consistent naming conventions
- Group related parts in separate xacro files

### Performance
- Use simple collision geometries when possible
- Keep URDF files well-structured and readable
- Use appropriate mesh resolution for visualization vs. collision

### Accuracy
- Ensure inertial parameters are realistic
- Verify that kinematic structure is correct
- Test URDF in simulation before physical implementation

## Common Issues and Troubleshooting

### Kinematic Loops
Avoid creating closed loops in the kinematic structure unless explicitly modeling closed chains.

### Invalid Mass Properties
- All links should have mass and inertia defined
- Ensure inertia values are positive and physically meaningful

### Joint Limits
- Set appropriate joint limits based on physical constraints
- Consider safety margins in limit setting

### Coordinate Frames
- Use consistent coordinate frame conventions (typically x-forward, y-left, z-up)
- Verify that origin definitions are correct

## Summary

URDF is fundamental to representing robots in ROS, especially critical for humanoid robotics where complex kinematic structures are common. Understanding URDF allows you to:
- Accurately model your robot for simulation
- Enable proper visualization in tools like RViz
- Provide necessary kinematic information for planning and control algorithms
- Standardize robot descriptions across the ROS ecosystem

## Next Steps

In the next section, we'll create a module summary and outline next steps for students to apply what they've learned about ROS 2 fundamentals.