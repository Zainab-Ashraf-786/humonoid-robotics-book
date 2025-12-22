---
title: Navigation and Path Planning with Nav2
sidebar_label: Navigation & Path Planning
---

# Navigation and Path Planning with Nav2

Navigation and path planning are critical capabilities for humanoid robots, enabling them to move intelligently through complex environments. This section covers how NVIDIA Isaac accelerates navigation workloads using GPU acceleration with the Navigation2 (Nav2) framework.

## Learning Objectives

After completing this section, you will:
- Understand the Nav2 architecture and its components
- Know how Isaac ROS accelerates navigation workloads with GPU acceleration
- Be able to configure Nav2 for humanoid robotics applications
- Understand the integration between Isaac Sim and Nav2 for testing
- Be familiar with human-aware navigation and social robotics considerations
- Know how to validate navigation performance in Isaac environments

## Introduction to Navigation2 (Nav2)

### Nav2 vs Legacy Navigation Stack

Navigation2 (Nav2) represents a complete rewrite of the ROS navigation stack with several key improvements:

1. **Modern Architecture**: Component-based design with lifecycle management
2. **Improved Performance**: Better computational efficiency and real-time performance
3. **Better Recovery Behaviors**: Robust recovery mechanisms for navigation failures
4. **Advanced Planning**: State-of-the-art global and local planners
5. **Plugin Architecture**: Extensible design for custom navigation solutions

### Nav2 Architecture Components

Nav2 consists of several key components that work together:
- **Planners Server**: Global and local path planning
- **Controller Server**: Trajectory control and execution
- **Recovery Server**: Recovery behavior management
- **BT Navigator**: Behavior tree-based navigation execution
- **Lifecycle Manager**: Component lifecycle management

## Isaac ROS Navigation Acceleration

### GPU-Accelerated Navigation Components

Isaac ROS provides GPU acceleration for computationally intensive navigation tasks:

#### GPU-Accelerated Costmaps

Traditional costmap operations are computationally intensive, especially for large maps or high-resolution grids. Isaac ROS provides GPU-accelerated costmap processing:

```yaml
# isaac_gpu_costmap_params.yaml
local_costmap:
  ros__parameters:
    # Isaac GPU-accelerated local costmap
    update_frequency: 10.0
    publish_frequency: 10.0
    global_frame: odom
    robot_base_frame: base_link
    transform_tolerance: 0.5
    resolution: 0.05  # 5cm resolution
    
    # Isaac GPU acceleration parameters
    enable_isaac_gpu_costmap: true
    enable_isaac_gpu_inflation: true
    enable_isaac_gpu_obstacles: true
    
    # GPU memory management
    gpu_memory_budget_mb: 512
    gpu_compute_shares: 80  # Percentage of GPU compute to allocate
    
    # Costmap plugins with Isaac GPU acceleration
    plugins: [
      "static_layer",
      "obstacle_layer", 
      "inflation_layer"
    ]
    
    static_layer:
      plugin: "nav2_costmap_2d::StaticLayer"
    
    obstacle_layer:
      plugin: "nav2_costmap_2d::ObstacleLayer"
      enabled: True
      observation_sources: scan
      scan:
        topic: /scan
        max_obstacle_height: 2.0
        clearing: True
        marking: True
        data_type: "LaserScan"
        raytrace_max_range: 10.0
        raytrace_min_range: 0.0
        obstacle_max_range: 8.0
        obstacle_min_range: 0.0
        
        # Isaac-specific GPU-accelerated parameters
        enable_isaac_gpu_raytracing: true
        enable_isaac_gpu_scan_processing: true
    
    inflation_layer:
      plugin: "nav2_costmap_2d::IsaacInflationLayer"  # Isaac GPU-enhanced inflation
      enabled: True
      cost_scaling_factor: 10.0
      inflation_radius: 0.55
      inflate_unknown: False
      inflate_around_unknown: True
      
      # Isaac GPU acceleration for inflation
      enable_isaac_gpu_inflation_algorithm: true
      inflation_thread_count: 8  # GPU threads for parallel inflation

global_costmap:
  ros__parameters:
    # Isaac GPU-accelerated global costmap
    update_frequency: 1.0
    publish_frequency: 0.0
    global_frame: map
    robot_base_frame: base_link
    rolling_window: false
    resolution: 0.05  # 5cm resolution
    
    # Isaac GPU acceleration parameters
    enable_isaac_gpu_costmap: true
    enable_isaac_gpu_inflation: true
    
    plugins: [
      "static_layer",
      "obstacle_layer",
      "inflation_layer"
    ]
    
    static_layer:
      plugin: "nav2_costmap_2d::StaticLayer"
    
    obstacle_layer:
      plugin: "nav2_costmap_2d::VoxelLayer"  # For 3D obstacle representation
      enabled: True
      observation_sources: pointcloud
      pointcloud:
        topic: /pointcloud
        max_obstacle_height: 2.0
        min_obstacle_height: 0.0
        obstacle_range: 8.0
        raytrace_range: 10.0
        voxel_size: 0.05
        max_obstacle_height: 2.0
        
        # Isaac GPU acceleration for pointcloud processing
        enable_isaac_gpu_pointcloud_processing: true
        enable_isaac_gpu_voxel_operations: true
    
    inflation_layer:
      plugin: "nav2_costmap_2d::IsaacInflationLayer"
      enabled: True
      cost_scaling_factor: 5.0
      inflation_radius: 1.0
      inflate_unknown: False
      inflate_around_unknown: False
      
      # Isaac GPU acceleration
      enable_isaac_gpu_inflation_algorithm: true
```

### Isaac-Accelerated Global Planners

Isaac provides GPU-accelerated global planners for faster path computation:

```yaml
# isaac_gpu_global_planner.yaml
bt_navigator:
  ros__parameters:
    # Behavior tree configuration
    plugin_lib_names: [
      "bt_navigator/NavigateToPose",
      "bt_navigator/Wait",
      "bt_navigator/BackUp",
      "bt_navigator/Spin",
      "bt_navigator/ThroughPortals"
    ]

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    # Isaac GPU-accelerated planners
    planner_plugins: ["GridBased"]
    GridBased:
      # Isaac A* planner with GPU acceleration
      plugin: "nav2_navfn_planner/IsaacAStarPlanner"  # Isaac GPU-enhanced A*
      
      # Isaac-specific GPU acceleration parameters
      enable_isaac_gpu_pathfinding: true
      enable_isaac_gpu_heuristic_calculation: true
      enable_isaac_gpu_path_optimization: true
      
      # GPU memory and thread configuration
      gpu_memory_pool_size: 1024  # MB
      gpu_thread_block_size: 32   # CUDA thread block size
      gpu_grid_partition_size: 1024  # Grid partitions for parallel processing
      
      # Path planning parameters
      use_astar: true
      allow_unknown: true
      tolerance: 0.5
      smooth_path: true

controller_server:
  ros__parameters:
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    
    # Isaac GPU-accelerated controller
    controller_plugins: ["FollowPath"]
    
    FollowPath:
      plugin: "nav2_mppi_controller/IsaacMppiController"  # Isaac GPU-enhanced MPPI
      
      # Isaac GPU acceleration
      enable_isaac_gpu_prediction: true
      enable_isaac_gpu_optimization: true
      enable_isaac_gpu_feedback_linearization: true
      
      # GPU configuration
      gpu_prediction_horizon_samples: 2048
      gpu_optimization_threads: 512
      
      # Controller parameters
      time_steps: 20
      control_freq: 10
      feedback_control: true
      Kp_rho: 2.5
      Kp_alpha: 2.0
      Kp_beta: 0.7
      delta: 0.1
      rho_tolerance: 0.1
      alpha_tolerance: 0.2
      beta_tolerance: 0.2
      transform_tolerance: 0.1
      xy_goal_tolerance: 0.25
      trans_stopped_velocity: 0.01
      theta_stopped_velocity: 0.01
      max_linear_speed: 0.5
      min_linear_speed: 0.0
      max_angular_speed: 1.0
      min_angular_speed: 0.0
```

## Isaac Sim Navigation Integration

### Simulated Navigation Testing

Isaac Sim provides realistic environments for navigation testing:

```python
# Isaac Sim navigation test environment
import omni
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.prims import RigidPrim, XFormPrim
from omni.isaac.core.utils.prims import get_prim_at_path
import numpy as np

class IsaacNavigationTestEnvironment:
    def __init__(self):
        self.world = World(stage_units_in_meters=1.0)
        self.navigation_goals = []
        self.obstacles = []
        
    def setup_navigation_world(self):
        """Set up a navigation testing environment in Isaac Sim"""
        
        # Add the humanoid robot
        robot_asset_path = "path/to/humanoid/robot.usd"
        add_reference_to_stage(usd_path=robot_asset_path, prim_path="/World/HumanoidRobot")
        
        # Create a complex environment with obstacles
        self.create_indoor_environment()
        self.add_dynamic_obstacles()
        self.set_navigation_goals()
        
        # Integrate with Isaac ROS navigation
        self.setup_ros_bridge()
    
    def create_indoor_environment(self):
        """Create a complex indoor environment for navigation testing"""
        # Add walls and structures
        wall_paths = [
            "/World/Wall_1", "/World/Wall_2", "/World/Wall_3", 
            "/World/Wall_4", "/World/Doorway", "/World/Hallway"
        ]
        
        for i, wall_path in enumerate(wall_paths):
            # Add wall geometry with collision
            wall_xform = XFormPrim(prim_path=wall_path, name=f"wall_{i}")
            
            # Configure physics properties
            # ... implementation details ...
    
    def add_dynamic_obstacles(self):
        """Add moving obstacles to test dynamic navigation"""
        # Add humans and moving obstacles to test navigation robustness
        for i in range(5):
            human_path = f"/World/DynamicObstacle_{i}"
            human_xform = XFormPrim(prim_path=human_path, name=f"dynamic_obs_{i}")
            
            # Configure as dynamic object with collision properties
            self.obstacles.append(human_xform)
    
    def set_navigation_goals(self):
        """Define navigation goals for testing"""
        goal_positions = [
            [3.0, 2.0, 0.0],   # Room 1
            [-2.0, 4.0, 0.0],  # Room 2
            [1.0, -3.0, 0.0],  # Corridor
            [-4.0, -1.0, 0.0]  # Room 3
        ]
        
        for i, pos in enumerate(goal_positions):
            goal_path = f"/World/Goal_{i}"
            xform = XFormPrim(prim_path=goal_path, name=f"goal_{i}", 
                             position=np.array(pos))
            self.navigation_goals.append(xform)
    
    def setup_ros_bridge(self):
        """Set up ROS bridge for navigation communication"""
        # Configure Isaac Sim to publish navigation-relevant data to ROS topics
        from omni.isaac.ros_bridge import ROSBridge
        
        # Connect Isaac Sim sensors to ROS topics for navigation
        # ... implementation details ...
    
    def run_navigation_test(self):
        """Run navigation tests in Isaac Sim"""
        for goal_idx, goal in enumerate(self.navigation_goals):
            print(f"Running navigation test to goal {goal_idx}")
            
            # Use Isaac ROS navigation stack to navigate to goal
            # ... implementation details ...
            
            # Track navigation metrics
            success, time_taken, path_length = self.evaluate_navigation()
            
            print(f"Navigation test {goal_idx}: Success={success}, "
                  f"Time={time_taken:.2f}s, Path={path_length:.2f}m")
    
    def evaluate_navigation(self):
        """Evaluate navigation performance"""
        # Metrics: success rate, time taken, path efficiency, safety
        success = True  # Determined by reaching goal within tolerance
        time_taken = 15.5  # Example time
        path_length = 8.7  # Example path length
        return success, time_taken, path_length

def main():
    env = IsaacNavigationTestEnvironment()
    env.setup_navigation_world()
    
    # Run comprehensive navigation tests
    env.run_navigation_test()

if __name__ == "__main__":
    main()
```

### Isaac Sim Navigation Scenarios

Isaac Sim can create various navigation scenarios for testing:

```yaml
# navigation_scenarios.yaml - Isaac Sim navigation testing scenarios
navigation_scenarios:
  # Scenario 1: Indoor Navigation with Static Obstacles
  indoor_static:
    environment: "office_building"
    obstacles: "static"
    robot_start: [0.0, 0.0, 0.0]  # x, y, theta
    goals: [[5.0, 3.0, 0.0], [2.0, -4.0, 1.57]]
    metrics: ["success_rate", "time_to_goal", "path_efficiency"]
  
  # Scenario 2: Dynamic Obstacle Navigation
  indoor_dynamic:
    environment: "cluttered_office"
    obstacles: "dynamic_pedestrians"
    robot_start: [0.0, 0.0, 0.0]
    goals: [[8.0, 2.0, 0.0]]
    metrics: ["success_rate", "collision_avoidance", "social_compliance"]
    
  # Scenario 3: Multi-floor Navigation
  multi_floor:
    environment: "multi_story_building"
    obstacles: "mixed"
    robot_start: [1.0, 1.0, 0.0]
    goals: [[15.0, -10.0, 0.0]]  # Navigate to different floor
    metrics: ["floor_transition_success", "elevator_awareness", "long_term_navigability"]
  
  # Scenario 4: Human-aware Navigation
  human_aware:
    environment: "crowded_corridor"
    obstacles: "moving_humans"
    robot_start: [0.0, 0.0, 0.0]
    goals: [[10.0, 0.0, 0.0]]
    metrics: ["social_norm_compliance", "personal_space_respect", "navigation_efficiency"]

isaac_sim_integration:
  ros__parameters:
    # Configuration for Isaac Sim integration with Nav2
    sim_to_nav_mapping:
      # Map Isaac Sim coordinate frame to navigation frame
      sim_frame: "world"
      nav_frame: "map"
      sim_robot_name: "HumanoidRobot"
      nav_robot_frame: "base_link"
    
    # Isaac Sim sensor simulation for navigation
    simulated_sensors:
      - type: "lidar"
        topic: "/scan"
        frame: "lidar_link"
        update_rate: 10.0
        parameters:
          range: 10.0
          resolution: 0.5
          gpu_accelerated: true
          
      - type: "camera"
        topic: "/camera/depth/image_rect"
        frame: "camera_depth_optical_frame"
        update_rate: 30.0
        parameters:
          width: 640
          height: 480
          fov: 1.047  # 60 degrees
          gpu_accelerated: true
          
      - type: "imu"
        topic: "/imu/data"
        frame: "imu_link"
        update_rate: 100.0
        parameters:
          noise_density: 0.0002
          random_walk: 0.00002
          gpu_accelerated: false  # IMU not GPU accelerated