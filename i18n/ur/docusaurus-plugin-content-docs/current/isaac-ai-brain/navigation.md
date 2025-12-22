---
title: Nav2 کے ساتھ نیویگیشن اور راستہ منصوبہ بندی
sidebar_label: نیویگیشن اور راستہ منصوبہ بندی
---

# Nav2 کے ساتھ نیویگیشن اور راستہ منصوبہ بندی

نیویگیشن اور راستہ منصوبہ بندی ہیومنائڈ روبوٹس کے لیے اہم صلاحیتیں ہیں، جو انہیں پیچیدہ ماحول میں ذہین طریقے سے حرکت کرنے کے قابل بناتی ہیں۔ یہ سیکشن اس بات کو احاطہ کرتا ہے کہ NVIDIA Isaac GPU تیزی کے ساتھ نیویگیشن2 (Nav2) فریم ورک کا استعمال کرتے ہوئے نیویگیشن کے کاموں کو کیسے تیز کرتا ہے۔

## سیکھنے کے اہداف

اس سیکشن کو مکمل کرنے کے بعد، آپ کر سکیں گے:
- Nav2 آرکیٹیکچر اور اس کے اجزاء کو سمجھنا
- جاننا کہ Isaac ROS GPU تیزی کے ساتھ نیویگیشن کے کاموں کو کیسے تیز کرتا ہے
- Nav2 کو ہیومنائڈ روبوٹکس ایپلی کیشنز کے لیے کنفیگر کرنا
- Isaac Sim اور Nav2 کے مابین انضمام کو سمجھنا ٹیسٹنگ کے لیے
- انسان-آگاہ نیویگیشن اور سوشل روبوٹکس کے خیالات سے واقف ہونا
- Isaac ماحول میں نیویگیشن کارکردگی کی توثیق کیسے کرنا

## نیویگیشن2 (Nav2) کا تعارف

### Nav2 بمقابلہ لیجسی نیویگیشن اسٹیک

نیویگیشن2 (Nav2) ROS نیویگیشن اسٹیک کا مکمل دوبارہ لکھنا ہے کئی کلیدی بہتریوں کے ساتھ:

1. **جدید آرکیٹیکچر**: لائف سائیکل مینجمنٹ کے ساتھ کمپونینٹ-مبنی ڈیزائن
2. **بہتر کارکردگی**: بہتر کمپیوٹیشنل کارکردگی اور حقیقی وقت کی کارکردگی
3. **بہتر ریکوری برتاؤ**: نیویگیشن کی ناکامیوں کے لیے مضبوط ریکوری میکنزم
4. **اعلیٰ درجے کی منصوبہ بندی**: جدید عہد کے عالمی اور مقامی منصوبہ ساز
5. **پلگ ان آرکیٹیکچر**: حسب ضرورت نیویگیشن حل کے لیے توسیع پذیر ڈیزائن

### Nav2 آرکیٹیکچر کے اجزاء

Nav2 کئی کلیدی اجزاء پر مشتمل ہے جو ایک ساتھ کام کرتے ہیں:
- **Planners Server**: عالمی اور مقامی راستہ منصوبہ بندی
- **Controller Server**: ٹریجکٹری کنٹرول اور انجام
- **Recovery Server**: ریکوری برتاؤ کا مینجمنٹ
- **BT Navigator**: برتاؤ ٹری-مبنی نیویگیشن انجام
- **Lifecycle Manager**: کمپونینٹ لائف سائیکل مینجمنٹ

## Isaac ROS نیویگیشن تیزی

### GPU-تیز نیویگیشن کمپونینٹس

Isaac ROS GPU تیزی فراہم کرتا ہے کمپیوٹیشنل طور پر بھاری نیویگیشن کاموں کے لیے:

#### GPU-تیز کوسٹ میپس

روایتی کوسٹ میپ آپریشنز کمپیوٹیشنل طور پر بھاری ہیں، خاص طور پر بڑے نقشہ جات یا زیادہ ریزولیوشن گرڈز کے لیے۔ Isaac ROS GPU-تیز کوسٹ میپ پروسیسنگ فراہم کرتا ہے:

```yaml
# isaac_gpu_costmap_params.yaml
local_costmap:
  ros__parameters:
    # Isaac GPU-تیز مقامی کوسٹ میپ
    update_frequency: 10.0
    publish_frequency: 10.0
    global_frame: odom
    robot_base_frame: base_link
    transform_tolerance: 0.5
    resolution: 0.05  # 5cm ریزولیوشن
    # Isaac GPU تیزی پیرامیٹر
    enable_isaac_gpu_costmap: true
    enable_isaac_gpu_inflation: true
    enable_isaac_gpu_obstacles: true
    # GPU میموری مینجمنٹ
    gpu_memory_budget_mb: 512
    gpu_compute_shares: 80  # GPU کمپیوٹ کا فیصد مختص
    # کوسٹ میپ پلگ ان Isaac GPU تیزی کے ساتھ
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
        # Isaac-مخصوص GPU-تیز پیرامیٹر
        enable_isaac_gpu_raytracing: true
        enable_isaac_gpu_scan_processing: true
    inflation_layer:
      plugin: "nav2_costmap_2d::IsaacInflationLayer"  # Isaac GPU-بہتر انفیلشن
      enabled: True
      cost_scaling_factor: 10.0
      inflation_radius: 0.55
      inflate_unknown: False
      inflate_around_unknown: True
      # Isaac GPU تیزی انفیلشن کے لیے
      enable_isaac_gpu_inflation_algorithm: true
      inflation_thread_count: 8  # GPU تھریڈس موازی انفیلشن کے لیے
global_costmap:
  ros__parameters:
    # Isaac GPU-تیز عالمی کوسٹ میپ
    update_frequency: 1.0
    publish_frequency: 0.0
    global_frame: map
    robot_base_frame: base_link
    rolling_window: false
    resolution: 0.05  # 5cm ریزولیوشن
    # Isaac GPU تیزی پیرامیٹر
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
      plugin: "nav2_costmap_2d::VoxelLayer"  # 3D رکاوٹ کی نمائندگی کے لیے
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
        # Isaac GPU تیز پوائنٹ کلاؤڈ پروسیسنگ کے لیے
        enable_isaac_gpu_pointcloud_processing: true
        enable_isaac_gpu_voxel_operations: true
    inflation_layer:
      plugin: "nav2_costmap_2d::IsaacInflationLayer"
      enabled: True
      cost_scaling_factor: 5.0
      inflation_radius: 1.0
      inflate_unknown: False
      inflate_around_unknown: False
      # Isaac GPU تیزی
      enable_isaac_gpu_inflation_algorithm: true
```

### Isaac-تیز عالمی منصوبہ ساز

Isaac GPU-تیز عالمی منصوبہ ساز فراہم کرتا ہے تیز راستہ کمپیوٹیشن کے لیے:

```yaml
# isaac_gpu_global_planner.yaml
bt_navigator:
  ros__parameters:
    # برتاؤ ٹری کنفیگریشن
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
    # Isaac GPU-تیز منصوبہ ساز
    planner_plugins: ["GridBased"]
    GridBased:
      # Isaac A* منصوبہ ساز GPU تیزی کے ساتھ
      plugin: "nav2_navfn_planner/IsaacAStarPlanner"  # Isaac GPU-بہتر A*
      # Isaac-مخصوص GPU تیزی پیرامیٹر
      enable_isaac_gpu_pathfinding: true
      enable_isaac_gpu_heuristic_calculation: true
      enable_isaac_gpu_path_optimization: true
      # GPU میموری اور تھریڈ کنفیگریشن
      gpu_memory_pool_size: 1024  # MB
      gpu_thread_block_size: 32   # CUDA تھریڈ بلاک سائز
      gpu_grid_partition_size: 1024  # موازی پروسیسنگ کے لیے گرڈ پارٹیشنز
      # راستہ منصوبہ بندی پیرامیٹر
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
    # Isaac GPU-تیز کنٹرولر
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "nav2_mppi_controller/IsaacMppiController"  # Isaac GPU-بہتر MPPI
      # Isaac GPU تیزی
      enable_isaac_gpu_prediction: true
      enable_isaac_gpu_optimization: true
      enable_isaac_gpu_feedback_linearization: true
      # GPU کنفیگریشن
      gpu_prediction_horizon_samples: 2048
      gpu_optimization_threads: 512
      # کنٹرولر پیرامیٹر
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

## Isaac Sim نیویگیشن انضمام

### مصنوعی نیویگیشن ٹیسٹنگ

Isaac Sim نیویگیشن ٹیسٹنگ کے لیے حقیقت نما ماحول فراہم کرتا ہے:

```python
# Isaac Sim نیویگیشن ٹیسٹ ماحول
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
        """Isaac Sim میں نیویگیشن ٹیسٹنگ ماحول کو سیٹ اپ کریں"""

        # ہیومنائڈ روبوٹ شامل کریں
        robot_asset_path = "path/to/humanoid/robot.usd"
        add_reference_to_stage(usd_path=robot_asset_path, prim_path="/World/HumanoidRobot")

        # رکاوٹوں کے ساتھ ایک پیچیدہ ماحول بنائیں
        self.create_indoor_environment()
        self.add_dynamic_obstacles()
        self.set_navigation_goals()

        # Isaac ROS نیویگیشن کے ساتھ انضمام
        self.setup_ros_bridge()

    def create_indoor_environment(self):
        """نیویگیشن ٹیسٹنگ کے لیے ایک پیچیدہ انڈور ماحول بنائیں"""
        # دیواریں اور ساختیں شامل کریں
        wall_paths = [
            "/World/Wall_1", "/World/Wall_2", "/World/Wall_3",
            "/World/Wall_4", "/World/Doorway", "/World/Hallway"
        ]

        for i, wall_path in enumerate(wall_paths):
            # دیوار جیومیٹری کالیژن کے ساتھ شامل کریں
            wall_xform = XFormPrim(prim_path=wall_path, name=f"wall_{i}")

            # فزکس خصوصیات کنفیگر کریں
            # ... نفاذ تفصیلات ...

    def add_dynamic_obstacles(self):
        """متحرک رکاوٹیں شامل کریں متحرک نیویگیشن کو ٹیسٹ کرنے کے لیے"""
        # ہیومنز اور متحرک رکاوٹیں شامل کریں نیویگیشن کی مضبوطی کو ٹیسٹ کرنے کے لیے
        for i in range(5):
            human_path = f"/World/DynamicObstacle_{i}"
            human_xform = XFormPrim(prim_path=human_path, name=f"dynamic_obs_{i}")

            # متحرک آبجیکٹ کے طور پر کنفیگر کریں کالیژن خصوصیات کے ساتھ
            self.obstacles.append(human_xform)

    def set_navigation_goals(self):
        """ٹیسٹنگ کے لیے نیویگیشن اہداف کی وضاحت کریں"""
        goal_positions = [
            [3.0, 2.0, 0.0],   # کمرہ 1
            [-2.0, 4.0, 0.0],  # کمرہ 2
            [1.0, -3.0, 0.0],  # گلیارہ
            [-4.0, -1.0, 0.0]  # کمرہ 3
        ]

        for i, pos in enumerate(goal_positions):
            goal_path = f"/World/Goal_{i}"
            xform = XFormPrim(prim_path=goal_path, name=f"goal_{i}",
                             position=np.array(pos))
            self.navigation_goals.append(xform)

    def setup_ros_bridge(self):
        """نیویگیشن کمیونیکیشن کے لیے ROS برج کو سیٹ اپ کریں"""
        # Isaac Sim کو ROS ٹاپکس میں نیویگیشن-متعلقہ ڈیٹا شائع کرنے کے لیے کنفیگر کریں
        from omni.isaac.ros_bridge import ROSBridge

        # Isaac Sim سینسرز کو نیویگیشن کے لیے ROS ٹاپکس سے جوڑیں
        # ... نفاذ تفصیلات ...

    def run_navigation_test(self):
        """Isaac Sim میں نیویگیشن ٹیسٹس چلائیں"""
        for goal_idx, goal in enumerate(self.navigation_goals):
            print(f"هدف {goal_idx} کی طرف نیویگیشن ٹیسٹ چلا رہا ہے")

            # Isaac ROS نیویگیشن اسٹیک کا استعمال کریں ہدف تک نیویگیٹ کرنے کے لیے
            # ... نفاذ تفصیلات ...

            # نیویگیشن میٹرکس ٹریک کریں
            success, time_taken, path_length = self.evaluate_navigation()

            print(f"نیویگیشن ٹیسٹ {goal_idx}: کامیابی={success}, "
                  f"وقت={time_taken:.2f}س، راستہ={path_length:.2f}م")

    def evaluate_navigation(self):
        """نیویگیشن کارکردگی کا جائزہ لیں"""
        # میٹرکس: کامیابی کی شرح، لگنے والا وقت، راستہ کی کارکردگی، حفاظت
        success = True  # ٹولرینس کے اندر ہدف تک پہنچنے سے تعین کیا گیا
        time_taken = 15.5  # مثال وقت
        path_length = 8.7  # مثال راستہ کی لمبائی
        return success, time_taken, path_length

def main():
    env = IsaacNavigationTestEnvironment()
    env.setup_navigation_world()

    # جامع نیویگیشن ٹیسٹس چلائیں
    env.run_navigation_test()

if __name__ == "__main__":
    main()
```

### Isaac Sim نیویگیشن منظر نامے

Isaac Sim ٹیسٹنگ کے لیے مختلف نیویگیشن منظر نامے بنا سکتا ہے:

```yaml
# navigation_scenarios.yaml - Isaac Sim نیویگیشن ٹیسٹنگ منظر نامے
navigation_scenarios:
  # منظر نامہ 1: سٹیٹک رکاوٹوں کے ساتھ انڈور نیویگیشن
  indoor_static:
    environment: "office_building"
    obstacles: "static"
    robot_start: [0.0, 0.0, 0.0]  # x, y, theta
    goals: [[5.0, 3.0, 0.0], [2.0, -4.0, 1.57]]
    metrics: ["success_rate", "time_to_goal", "path_efficiency"]

  # منظر نامہ 2: متحرک رکاوٹ نیویگیشن
  indoor_dynamic:
    environment: "cluttered_office"
    obstacles: "dynamic_pedestrians"
    robot_start: [0.0, 0.0, 0.0]
    goals: [[8.0, 2.0, 0.0]]
    metrics: ["success_rate", "collision_avoidance", "social_compliance"]

  # منظر نامہ 3: ملٹی- منزل نیویگیشن
  multi_floor:
    environment: "multi_story_building"
    obstacles: "mixed"
    robot_start: [1.0, 1.0, 0.0]
    goals: [[15.0, -10.0, 0.0]]  # مختلف منزل کی طرف نیویگیٹ کریں
    metrics: ["floor_transition_success", "elevator_awareness", "long_term_navigability"]

  # منظر نامہ 4: انسان-آگاہ نیویگیشن
  human_aware:
    environment: "crowded_corridor"
    obstacles: "moving_humans"
    robot_start: [0.0, 0.0, 0.0]
    goals: [[10.0, 0.0, 0.0]]
    metrics: ["social_norm_compliance", "personal_space_respect", "navigation_efficiency"]

isaac_sim_integration:
  ros__parameters:
    # Nav2 کے ساتھ Isaac Sim انضمام کے لیے کنفیگریشن
    sim_to_nav_mapping:
      # Isaac Sim کوآرڈینیٹ فریم کو نیویگیشن فریم پر میپ کریں
      sim_frame: "world"
      nav_frame: "map"
      sim_robot_name: "HumanoidRobot"
      nav_robot_frame: "base_link"

    # نیویگیشن کے لیے Isaac Sim سینسر سیمیولیشن
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
          fov: 1.047  # 60 ڈگری
          gpu_accelerated: true

      - type: "imu"
        topic: "/imu/data"
        frame: "imu_link"
        update_rate: 100.0
        parameters:
          noise_density: 0.0002
          random_walk: 0.00002
          gpu_accelerated: false  # IMU GPU تیز نہیں ہے
```