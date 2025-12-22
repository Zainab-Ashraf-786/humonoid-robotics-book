---
title: ادراک اور نیویگیشن کے لیے Isaac ROS
sidebar_label: Isaac ROS
---

# ادراک اور نیویگیشن کے لیے Isaac ROS

Isaac ROS NVIDIA کے ہارڈ ویئر-تیز کردہ ادراک اور نیویگیشن پیکجز کی نمائندگی کرتا ہے جو ROS/ROS 2 ایکو سسٹم کے ساتھ بے دریغ انضمام فراہم کرتا ہے۔ یہ پیکجز کمپیوٹ-تیز روبوٹکس الگوری دم کے لیے GPU تیزی فراہم کرتا ہے، خاص طور پر ہیومنائڈ روبوٹکس ایپلی کیشنز میں ادراک اور نیویگیشن کے کاموں کے لیے فائدہ مند ہے۔

## سیکھنے کے اہداف

اس سیکشن کو مکمل کرنے کے بعد، آپ کر سکیں گے:
- Isaac ROS پیکجز کی آرکیٹیکچر اور مقصد کو سمجھنا
- Isaac ROS ادراک پیکجز کو تشکیل دینا اور استعمال کرنا
- GPU-تیز کردہ نیویگیشن سٹیکس نافذ کرنا
- یہ سمجھنا کہ Isaac ROS Isaac Sim اور حقیقی ہارڈ ویئر سے کیسے منسلک ہوتا ہے
- ہیومنائڈ روبوٹکس میں Isaac ROS کے عملی اطلاق کے ساتھ واقف ہونا

## Isaac ROS کا تعارف

### Isaac ROS کیا ہے؟

Isaac ROS ہارڈ ویئر-تیز کردہ پیکجز کا مجموعہ ہے جو NVIDIA کی GPU کمپیوٹنگ صلاحیتوں اور ROS/ROS 2 روبوٹکس فریم ورک کے درمیان خلا کو پر کرتا ہے۔ یہ عام روبوٹکس الگوری دم کے بہتر نفاذ فراہم کرتا ہے جو NVIDIA کی GPU آرکیٹیکچر کا فائدہ اٹھاتا ہے بہتر کارکردگی کے لیے۔

Isaac ROS پیکجز میں شامل ہیں:
- **ادراک سٹیک**: تیز کمپیوٹر وژن، سینسر پروسیسنگ، اور فیچر ایکسٹریکشن
- **نیویگیشن سٹیک**: GPU-تیز راستہ منصوبہ بندی اور رکاوٹ سے بچاؤ
- **سینسر پروسیسنگ**: بہترین سینسر ڈیٹا پروسیسنگ اور فیوژن
- **گہری سیکھنے کا انضمام**: روبوٹکس کاموں کے لیے تیز نیورل نیٹ ورک انفرینس

### معیاری ROS پیکجز سے کلیدی فرق

| پہلو | معیاری ROS پیکجز | Isaac ROS پیکجز |
|--------|----------------------|--------------------|
| پروسیسنگ یونٹ | CPU | GPU (CPU فال بیک کے ساتھ) |
| کارکردگی | معیاری CPU کارکردگی | GPU-تیز (اکثر 5-50x تیز) |
| ہارڈ ویئر کی ضروریات | کوئی مطابقت رکھنے والا CPU | CUDA کی حمایت کے ساتھ NVIDIA GPU |
| میموری مینجمنٹ | صرف CPU RAM | GPU VRAM + CUDA میموری مینجمنٹ |
| الگوری دم نفاذ | جنرل-پرپز | GPU-بہتر الگوری دم |
| انضمام | معیاری ROS انٹرفیسز | GPU تیزی کے ساتھ ROS انٹرفیسز |

### ہیومنائڈ روبوٹکس کے لیے فوائد

Isaac ROS ہیومنائڈ روبوٹکس کے لیے مخصوص فوائد فراہم کرتا ہے:
- **حقیقی وقت کا ادراک**: ماحول پر تیز ردعمل کے لیے تیز پروسیسنگ
- **کارآمد SLAM**: نیویگیشن کے لیے تیز میپنگ اور لوکلائزیشن
- **اعلیٰ درجے کی کمپیوٹر وژن**: حقیقی وقت میں آبجیکٹ ڈیٹیکشن اور ریکوگنیشن
- **سینسر فیوژن**: متعدد سینسر سٹریمز کا کارآمد انضمام
- **پاور کارآمدی**: بہتر پاور مینجمنٹ کے لیے بہترین الگوری دم

## Isaac ROS پیکج آرکیٹیکچر

### بنیادی اجزاء

Isaac ROS کئی کلیدی اجزاء پر مشتمل ہے جو ایک ساتھ کام کرتے ہیں:

1. **Isaac ROS Common**: Isaac ROS پیکجز کے لیے بیس یوٹیلیٹیز
2. **Isaac ROS Messages**: GPU-تیز کردہ کاموں کے لیے حسب ضرورت پیغام کی اقسام
3. **Isaac ROS Extensions**: عام روبوٹکس کاموں کے لیے ہارڈ ویئر-تیز کردہ پیکجز
4. **Isaac ROS Tools**: Isaac ROS سسٹم کی نگرانی اور پروفائلنگ کے لیے یوٹیلیٹیز

### ہارڈ ویئر تیزی کا ڈھانچہ

Isaac ROS پیکجز متعدد NVIDIA ٹیکنالوجیز کا فائدہ اٹھاتے ہیں:
- **CUDA**: متوازی کمپیوٹیشن کے لیے
- **TensorRT**: بہترین نیورل نیٹ ورک انفرینس کے لیے
- **OptiX**: تیز رے ٹریسنگ کے لیے (LiDAR سمیولیشن)
- **RTX پلیٹ فارم**: جدید رینڈرنگ اور ادراک کے لیے

### انسٹالیشن اور سیٹ اپ

#### شرائط لازمہ
- NVIDIA GPU (RTX سیریز ترجیحی، کم از کم 4GB VRAM)
- CUDA-مطابقت رکھنے والا ڈرائیور (470+)
- ROS/ROS 2 انسٹالیشن (Humble Hawksbill تجویز کردہ)
- Isaac Sim (سمیولیشن انضمام کے لیے)

#### انسٹالیشن عمل

```bash
# NVIDIA پیکج ذخیرہ شامل کریں
wget https://developer.download.nvidia.com/devzone/devcenter/software/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update

# Isaac ROS پیکجز انسٹال کریں
sudo apt install nvidia-isaac-ros-common
sudo apt install nvidia-isaac-ros-navigation
sudo apt install nvidia-isaac-ros-perception
sudo apt install nvidia-isaac-ros-gpu-voxel-map
```

#### توثیق
```bash
# Isaac ROS انسٹالیشن چیک کریں
dpkg -l | grep nvidia-isaac-ros

# GPU رسائی کی تصدیق کریں
nvidia-smi

# بنیادی Isaac ROS فعل کی جانچ کریں
ros2 run isaac_ros_test test_compatibility
```

## Isaac ROS ادراک سٹیک

### GPU-تیز کردہ کمپیوٹر وژن

Isaac ROS عام کمپیوٹر وژن کاموں کے لیے GPU-تیز نفاذ فراہم کرتا ہے:

#### AprilTag ڈیٹیکشن

AprilTag ڈیٹیکشن Isaac ROS کے ساتھ تیز کردہ ہے فیڈوکل-مبنی محل وقوع کے لیے درست:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from isaac_ros_apriltag_interfaces.msg import AprilTagDetectionArray

class AprilTagProcessor(Node):
    def __init__(self):
        super().__init__('apriltag_processor')

        # کیمرہ امیج کو سبسکرائب کریں
        self.image_sub = self.create_subscription(
            Image,
            '/camera/rgb/image_rect_color',
            self.image_callback,
            10)

        # AprilTag ڈیٹیکشنز کو سبسکرائب کریں
        self.tag_sub = self.create_subscription(
            AprilTagDetectionArray,
            '/tag_detections',
            self.tag_callback,
            10)

        # پروسیس کردہ نتائج کا شائع کنندہ
        self.pose_pub = self.create_publisher(
            PoseStamped,
            '/camera/apriltag_pose',
            10)

    def tag_callback(self, msg):
        if len(msg.detections) > 0:
            detection = msg.detections[0]  # پہلا ڈیٹیکشن پروسیس کریں

            # ٹیگ ڈیٹیکشن سے پوز تخلیق کریں
            pose_msg = PoseStamped()
            pose_msg.header = detection.pose.header
            pose_msg.pose = detection.pose.pose.pose

            self.pose_pub.publish(pose_msg)
            self.get_logger().info(f'ٹیگ ڈیٹیکٹڈ: {detection.id}, پوزیشن: ({detection.pose.pose.pose.position.x:.2f}, {detection.pose.pose.pose.position.y:.2f})')

def main(args=None):
    rclpy.init(args=args)
    processor = AprilTagProcessor()
    rclpy.spin(processor)
    processor.destroy_node()
    rclpy.shutdown()
```

#### اسٹیریو ڈینس ریکن سٹرکشن

ماحول کی 3D سمجھ کے لیے:

```yaml
# لانچ فائل: stereo_dense_reconstruction.launch.py
from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    container = ComposableNodeContainer(
        name='stereo_reconstruction_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[
            ComposableNode(
                package='isaac_ros_stereo_image_proc',
                plugin='isaac_ros::stereo_image_proc::DisparityNode',
                name='disparity_node',
                parameters=[{
                    'disp_num_disparities': 64,
                    'disp_min_disparity': -1,
                    'disp_uniqueness_ratio': 15,
                    'disp_texture_threshold': 10,
                    'disp_speckle_size': 100,
                    'disp_speckle_range': 4
                }],
                remappings=[
                    ('left/image_rect', '/camera/left/image_rect'),
                    ('right/image_rect', '/camera/right/image_rect'),
                    ('left/camera_info', '/camera/left/camera_info'),
                    ('right/camera_info', '/camera/right/camera_info'),
                    ('disparity', '/disparity')]
            ),

            ComposableNode(
                package='isaac_ros_pointcloud_utils',
                plugin='isaac_ros::pointcloud_utils::PointCloud2BuilderNode',
                name='pointcloud2_builder_node',
                remappings=[('image', '/camera/left/image_rect'),
                            ('camera_info', '/camera/left/camera_info'),
                            ('disparity', '/disparity'),
                            ('pointcloud', '/pointcloud')]
            )
        ]
    )

    return LaunchDescription([container])
```

### GPU-وکسل میپنگ

Isaac ROS GPU-وکسل میپنگ کے ساتھ تیز 3D میپنگ فراہم کرتا ہے:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
import numpy as np

class GpuVoxelMapper(Node):
    def __init__(self):
        super().__init__('gpu_voxel_mapper')

        # Isaac ROS سے پروسیس کردہ پوائنٹ کلاؤڈ کو سبسکرائب کریں
        self.pc_sub = self.create_subscription(
            PointCloud2,
            '/pointcloud_fused',
            self.pointcloud_callback,
            10)

        # وکسل میپ کا شائع کنندہ
        self.voxel_pub = self.create_publisher(
            PointCloud2,
            '/voxel_map',
            10)

        # کنفیگریشن پیرامیٹر
        self.resolution = 0.05  # 5cm ریزولوشن
        self.max_range = 10.0   # 10m زیادہ سے زیادہ فاصلہ

    def pointcloud_callback(self, msg):
        # Isaac ROS GPU-وکسل میپنگ ان پٹ کو پروسیس کرتا ہے
        # یہ ایک تصوراتی مثال ہے - حقیقی نفاذ Isaac ROS نوڈس کا استعمال کرے گا
        points = point_cloud2.read_points(msg, field_names=["x", "y", "z"], skip_nans=True)

        # GPU-تیز کردہ وکسلائزیشن کا استعمال کرتے ہوئے پوائنٹس پروسیس کریں
        points_list = []
        for point in points:
            if all(np.isfinite(coord) for coord in point[:3]):  # درست کوآرڈینیٹس کی چیک کریں
                points_list.append(point[:3])  # صرف x، y، z

        # عمل میں، یہ Isaac ROS GPU-وکسل میپنگ کے ساتھ انٹرفیس کرے گا
        # جو GPU پر اصل وکسلائزیشن انجام دیتا ہے
        self.process_gpu_voxel_map(points_list)

def main(args=None):
    rclpy.init(args=args)
    mapper = GpuVoxelMapper()
    rclpy.spin(mapper)
    mapper.destroy_node()
    rclpy.shutdown()
```

## Isaac ROS نیویگیشن سٹیک

### GPU-تیز کردہ راستہ منصوبہ بندی

Isaac ROS Nav2 کے ساتھ انضمام کرتا ہے GPU-تیز نیویگیشن کی صلاحیتیں فراہم کرنے کے لیے:

#### GPU-تیز کردہ کوسٹ میپ

```yaml
# costmap_config.yaml
local_costmap:
  global_frame: odom
  robot_base_frame: base_link
  update_frequency: 10.0
  publish_frequency: 10.0
  resolution: 0.05  # میٹر فی پکسل
  inflation_radius: 0.55
  plugins:
    - {name: static_layer, type: "nav2_costmap_2d::StaticLayer"}
    - {name: obstacle_layer, type: "nav2_costmap_2d::ObstacleLayer"}
    - {name: inflation_layer, type: "nav2_costmap_2d::IsaacInflationLayer"}  # Isaac GPU-بہتر انفلیشن
  obstacle_layer:
    enabled: true
    observation_sources: scan
    scan:
      topic: /scan
      max_obstacle_height: 2.0
      clearing: true
      marking: true
      data_type: LaserScan
      raytrace_max_range: 10.0
      raytrace_min_range: 0.0
      obstacle_max_range: 8.0
      obstacle_min_range: 0.0

global_costmap:
  global_frame: map
  robot_base_frame: base_link
  update_frequency: 1.0
  publish_frequency: 0.0
  resolution: 0.05
  plugins:
    - {name: static_layer, type: "nav2_costmap_2d::StaticLayer"}
    - {name: obstacle_layer, type: "nav2_costmap_2d::ObstacleLayer"}
    - {name: inflation_layer, type: "nav2_costmap_2d::IsaacInflationLayer"}  # Isaac GPU-بہتر انفلیشن
```

#### Isaac-تیز کردہ گلوبل پلینر

Isaac ROS گلوبل پلینر GPU تیزی کا استعمال کرتا ہے راستہ کی بہتری کے لیے:

```python
# Isaac-تیز کردہ پلینرز کی مثال
import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid, Path
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import ComputePathToPose

class IsaacPathPlanner(Node):
    def __init__(self):
        super().__init__('isaac_path_planner')

        # Isaac ROS GPU-تیز کردہ راستہ کمپیوٹیشن فراہم کرتا ہے
        self.path_publisher = self.create_publisher(Path, 'global_plan', 10)

        # راستہ کمپیوٹیشن کے لیے ایکشن کلائنٹ
        self.path_client = ActionClient(self, ComputePathToPose, 'compute_path_to_pose')

        # کوسٹ میپ کو سبسکرائب کریں تاکہ راستہ کی قابلیت کی تصدیق کی جا سکے
        self.costmap_sub = self.create_subscription(
            OccupancyGrid,
            'global_costmap/costmap',
            self.costmap_callback,
            10)

        self.get_logger().info('Isaac راستہ پلینر شروع کیا گیا')

    def compute_path(self, start_pose, goal_pose):
        """Isaac-تیز کردہ GPU منصوبہ بندی کا استعمال کرتے ہوئے راستہ کمپیوٹ کریں"""
        goal = ComputePathToPose.Goal()
        goal.start = start_pose
        goal.goal = goal_pose
        goal.planner_id = "IsaacAStar"  # Isaac کا GPU-تیز کردہ A* پلینر استعمال کریں

        future = self.path_client.send_goal_async(goal)
        return future

def main(args=None):
    rclpy.init(args=args)
    planner = IsaacPathPlanner()

    # مثال: موجودہ پوز سے ایک ہدف تک راستہ کمپیوٹ کریں
    # یہ عام طور پر نیویگیشن کی درخواست سے محرک کیا جائے گا
    rclpy.spin(planner)

    planner.destroy_node()
    rclpy.shutdown()
```

### Isaac for Humanoid Locomotion

خصوصاً ہیومنائڈ روبوٹس کے لیے، Isaac ROS مخصوص صلاحیتیں فراہم کرتا ہے:

#### وہول-بائڈی ٹریجیکٹری پلاننگ

Isaac ROS ہیومنائڈ لوموشن کے لیے پیچیدہ صلاحیتیں کا انضمام کرتا ہے:

```yaml
# controller_manager_config.yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    # ہیومنائڈ لوموشن کے لیے Isaac-تیز کردہ کنٹرولرز
    IsaacWholeBodyController:
      type: isaac_ros_controllers/IsaacWholeBodyController
    IsaacBalanceController:
      type: isaac_ros_controllers/IsaacBalanceController
    IsaacGaitPatternGenerator:
      type: isaac_ros_controllers/IsaacGaitPatternGenerator

IsaacWholeBodyController:
  ros__parameters:
    # GPU-تیز کردہ انورس کنیمیٹکس
    ik_solver_type: "IsaacGPU_IK"
    update_rate: 100
    chain_root: "base_link"
    chain_tip: "right_foot"
    max_iterations: 100
    tolerance: 0.001

IsaacBalanceController:
  ros__parameters:
    # GPU-تیز کردہ توازن کنٹرول
    balance_method: "IsaacGPUBalance"
    update_rate: 200  # ڈائنامک توازن کے لیے زیادہ شرح
    zmp_reference_source: "isaac_zmp_generator"
    com_tracking_enabled: true
    pelvis_orientation_control_enabled: true

IsaacGaitPatternGenerator:
  ros__parameters:
    # GPU-تیز کردہ گیٹ پیٹرن جنریشن
    gait_type: "dynamic_walk"
    update_rate: 50
    step_height: 0.1
    step_duration: 0.8
    support_margin: 0.02
```

#### ہیومنائڈ-مخصوص نیویگیشن

ہیومنائڈ نیویگیشن چکر والے روبوٹس سے کئی کلیدی طریقوں میں مختلف ہوتا ہے جن کا Isaac ROS کو سامنا ہے:

```python
# ہیومنائڈ-مخصوص نیویگیشن کنفیگریشن
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateWithRecovery
from geometry_msgs.msg import PoseWithCovarianceStamped
from visualization_msgs.msg import MarkerArray

class HumanoidNavigator(Node):
    def __init__(self):
        super().__init__('humanoid_navigator')

        # ہیومنائڈ-مخصوص نیویگیشن پیرامیٹر
        self.declare_parameters(
            namespace='',
            parameters=[
                ('step_size', 0.3),  # ہیومنائڈ قدم کا سائز
                ('step_height', 0.1),  # چھوٹی رکاوٹوں پر قدم
                ('turn_speed_limit', 0.5),  # توازن کے لیے کنٹرولڈ ٹرننگ
                ('balance_margin', 0.15),  # توازن کے لیے تحفظی حد
            ])

        # Isaac ROS ہیومنائڈ-آگاہ نیویگیشن فراہم کرتا ہے
        self.nav_client = ActionClient(self, NavigateWithRecovery, 'navigate_with_recovery')
        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            'initialpose',
            self.initial_pose_callback,
            10)

        # ہیومنائڈ-مخصوص ویژولائزیشن کے لیے شائع کنندہ
        self.footstep_pub = self.create_publisher(MarkerArray, 'footsteps', 10)
        self.center_of_mass_pub = self.create_publisher(MarkerArray, 'center_of_mass', 10)

    def plan_humanoid_path(self, goal_pose):
        """ہیومنائڈ-مخصوص قیود کو مدنظر رکھتے ہوئے راستہ منصوبہ بندی کریں"""
        # Isaac GPU تیزی ہیومنائڈ کنیمیٹکس کو ہینڈل کرتا ہے
        # توازن، قدم کی قیود، اور رکاوٹ کلیئرنس کو مدنظر رکھتے ہوئے

        # ہیومنائڈ-مخصوص قیود کے ساتھ نیویگیشن ہدف تخلیق کریں
        goal = NavigateWithRecovery.Goal()
        goal.pose = goal_pose

        # Isaac ROS ہیومنائڈ-مخصوص نیویگیشن کی ضروریات کو ہینڈل کرتا ہے
        # جیسے سپورٹ پولی گان کے اندر مرکز کو مدنظر رکھنا
        return self.nav_client.send_goal_async(goal)

def main(args=None):
    rclpy.init(args=args)
    navigator = HumanoidNavigator()
    rclpy.spin(navigator)
    navigator.destroy_node()
    rclpy.shutdown()
```

## Isaac Sim کے ساتھ انضمام

### سمیولیشن-سے-حقیقت منتقلی

Isaac ROS کی کلیدی طاقت میں سے ایک Isaac Sim کے ساتھ اس کا بے دریغ انضمام ہے سمیولیشن-سے-حقیقت منتقلی کے لیے:

```yaml
# Isaac Sim انضمام کنفیگریشن
isaac_ros_common:
  ros_bridge_node:
    ros__parameters:
      # Isaac Sim سے Isaac ROS تک ہم وقت سازی
      sync_mode: "time_based"  # سمیولیشن اور حقیقی وقت کو ہم وقت کریں
      publish_tf_frequency: 100
      clock_publish_frequency: 100

      # Isaac Sim سینسر ڈیٹا کو Isaac ROS میں راؤٹ کرنا
      topic_mappings: [
        # Isaac Sim سے Isaac ROS ادراک تک کیمرہ سینسر ڈیٹا
        {topic_from: "/isaac_sim/camera/rgb/image", topic_to: "/camera/color/image_raw", qos: 10},
        {topic_from: "/isaac_sim/camera/depth/image", topic_to: "/camera/depth/image_rect_raw", qos: 10},
        {topic_from: "/isaac_sim/camera/camera_info", topic_to: "/camera/color/camera_info", qos: 10},

        # Isaac Sim سے Isaac ROS تک LiDAR ڈیٹا
        {topic_from: "/isaac_sim/lidar/scan", topic_to: "/scan", qos: 10},

        # IMU اور دیگر سینسر ڈیٹا
        {topic_from: "/isaac_sim/imu/data", topic_to: "/imu/data", qos: 10},
        {topic_from: "/isaac_sim/odom", topic_to: "/odom", qos: 10},
      ]

isaac_perception_pipeline:
  ros__parameters:
    # Isaac ROS ادراک پائپ لائن سمیولیشن ڈیٹا کے لیے
    processing_mode: "simulation_optimized"  # Isaac Sim ڈیٹا کے لیے خصوصی موڈ
    gpu_id: 0
    optimization_level: "performance"  # Isaac Sim کے بہتر ڈیٹا کا فائدہ اٹھائیں

    # سمیولیشن-مخصوص بہتریاں
    synthetic_noise_models: {
      camera: "isaac_photorealistic",  # Isaac Sim کے حقیقی نويز ماڈلز استعمال کریں
      lidar: "isaac_ray_traced",       # Isaac Sim کے رے ٹریسنگ کا LiDAR کے لیے استعمال کریں
      imu: "isaac_physics_based"       # Isaac Sim کی فزکس کو IMU کے لیے استعمال کریں
    }
```

### AI تربیت کے لیے ڈومین رینڈمائزیشن

Isaac ROS Isaac Sim کے ڈومین رینڈمائزیشن کی صلاحیتوں کا فائدہ اٹھاتا ہے:

```python
# AI تربیت کے لیے ڈومین رینڈمائزیشن کی مثال
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.synthetic_utils import SyntheticDataHelper
import random

class DomainRandomizer:
    def __init__(self):
        self.synthetic_helper = SyntheticDataHelper()

    def randomize_material_properties(self):
        """سینٹھیٹک ڈیٹا جنریشن کے لیے مادہ کی خصوصیات کو رینڈمائز کریں"""
        # حقیقی سینسر سمیولیشن کے لیے سطح کی خصوصیات کو رینڈمائز کریں
        materials = [
            "floor_concrete", "floor_tile", "grass",
            "wood_floor", "carpet", "metal_grate"
        ]

        selected_material = random.choice(materials)
        self.apply_randomized_material(selected_material)

    def randomize_lighting_conditions(self):
        """متغیر بصری حالات کے لیے لائٹنگ کو رینڈمائز کریں"""
        # Isaac Sim حقیقی لائٹنگ کی تبدیلیوں کی اجازت دیتا ہے
        light = get_prim_at_path("/World/Light")

        # شدت اور رنگ کے درجہ حرارت کو رینڈمائز کریں
        intensity = random.uniform(500, 3000)
        color_temp = random.uniform(4000, 8000)

        light.GetAttribute("inputs:intensity").Set(intensity)
        light.GetAttribute("inputs:colorTemperature").Set(color_temp)

    def randomize_weather_conditions(self):
        """ outdoor مناظر کے لیے موسم کی حالتیں رینڈمائز کریں"""
        # Isaac Sim فضا کے اثرات کی حمایت کرتا ہے
        conditions = ["sunny", "overcast", "rain_light", "fog_light"]
        selected_condition = random.choice(conditions)

        # حالت-مخصوص ترتیبات لاگو کریں
        self.apply_atmospheric_effects(selected_condition)
```

## کارکردگی کے مسائل

### GPU وسائل کا نظم

Isaac ROS پیکجز GPU وسائل کے نظم کے لیے بہتر بنائے گئے ہیں:

```python
# GPU میموری اور کارکردگی کی بہتری کی مثال
import pycuda.driver as cuda
import tensorrt as trt

class IsaacGPUOptimizer:
    def __init__(self):
        # CUDA کنٹیکس شروع کریں
        cuda.init()
        self.device = cuda.Device(0)  # پہلے GPU کا استعمال کریں
        self.context = self.device.make_context()

        # Isaac ROS GPU میموری کے استعمال کو بہتر بناتا ہے
        self.max_memory_usage = 0.8  # GPU میموری کا 80% تک استعمال کریں
        self.stream = cuda.Stream()

    def optimize_tensorrt_engine(self, engine_path):
        """Isaac ROS استعمال کے لیے TensorRT انجن کو بہتر بنائیں"""
        # Isaac ROS انفرینس تیزی کے لیے TensorRT استعمال کرتا ہے
        with open(engine_path, 'rb') as f:
            engine_data = f.read()

        runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
        engine = runtime.deserialize_cuda_engine(engine_data)

        # بہتری بفرس تفویض کریں
        context = engine.create_execution_context()
        return context

    def cleanup(self):
        """GPU وسائل کو مناسب طریقے سے صاف کریں"""
        self.context.pop()  # CUDA کنٹیکس کو نکالیں
        del self.stream
```

### حقیقی وقت کی کارکردگی کی ضروریات

Isaac ROS حقیقی وقت کے روبوٹکس ایپلی کیشنز کے لیے ڈیزائن کیا گیا ہے:

```yaml
# کارکردگی کی بہتری کنفیگریشن
isaac_performance_config:
  ros__parameters:
    # Isaac ROS کارکردگی پیرامیٹر
    scheduling_policy: "SCHED_FIFO"  # حقیقی وقت کی شیڈولنگ
    cpu_affinity_mask: "0xF0"  # مخصوص CPU کورز سے منسلک کریں
    gpu_compute_mode: "exclusive_process"  # مخصوص GPU رسائی

    # Isaac-مخصوص کارکردگی کی بہتریاں
    pipeline_depth: 3  # مستحکم پروسیسنگ کے لیے متعدد فریم بفر کریں
    async_processing_enabled: true  # اسینکرون پروسیسنگ فعال کریں
    memory_pool_size_mb: 1024  # پروسیسنگ کے لیے GPU میموری پول

    # Isaac Sim ہم وقت سازی
    max_sim_time_drift: 0.01  # سمیولیشن ٹائم کو ہم وقت رکھیں
    render_skip_threshold: 5  # پیچھے ہونے پر رینڈرنگ چھوڑیں تاکہ پروسیسنگ کی رفتار برقرار رہے
```

## Isaac ROS کا ڈیبگ کرنا

### عام مسائل اور حل

#### GPU میموری کے مسائل
```bash
# GPU میموری استعمال چیک کریں
nvidia-smi

# Isaac ROS پائپ لائن گہرائی کم کریں
# میموری کی ضروریات کم کرنے کے لیے کنفیگریشن میں تبدیلی کریں
pipeline_depth: 2  # 3 سے کم کریں

# جہاں ممکن ہو چھوٹے ان پٹ سائز استعمال کریں
# مثال کے طور پر، سمیولیشن میں کیمرہ ریزولوشن کم کریں
```

#### CUDA مطابقت کے مسائل
```bash
# CUDA انسٹالیشن کی تصدیق کریں
nvcc --version

# Isaac ROS CUDA مطابقت کی چیک کریں
# NVIDIA کے مطابقت میٹرکس کو دیکھیں
# یقین کریں کہ Isaac ROS ورژن CUDA ورژن سے مماثل ہے
```

#### Isaac Sim کنکشن کے مسائل
```bash
# Isaac Sim چل رہا ہے کی تصدیق کریں
ros2 node list | grep isaac

# ٹاپک کنکشنز چیک کریں
ros2 topic list | grep -E "(isaac_sim|isaac_ros)"

# Isaac ROS برج فعال ہے کی تصدیق کریں
ros2 run isaac_ros_test test_connection
```

### Isaac ROS سسٹم کی ڈیبگنگ

#### Isaac ROS کارکردگی کی نگرانی
```bash
# Isaac ROS نوڈس کی نگرانی کریں
ros2 run isaac_ros_common isaac_monitor

# GPU استعمال کی نگرانی کریں
nvidia-smi dmon -s u -d 1

# میموری استعمال کی نگرانی کریں
ros2 run isaac_ros_common gpu_memory_profiler
```

#### لاگنگ اور ڈائیگنوسٹکس
```python
# Isaac ROS ڈیبگنگ فعال کریں
import rclpy
from rclpy.logging import LoggingSeverity

def setup_logging():
    logger = rclpy.logging.get_logger('isaac_ros_application')
    logger.set_level(LoggingSeverity.DEBUG)

    # Isaac ROS تفصیلی ڈائیگنوسٹک معلومات فراہم کرتا ہے
    logger.info('Isaac ROS ایپلی کیشن ڈیبگنگ فعال کے ساتھ شروع ہوا')
```

## بہترین طریقے

### Isaac ROS کے لیے ڈیزائن پیٹرنز

1. **کمپونینٹ آرکیٹیکچر**: GPU وسائل کے اشتراک کو بہتر بنانے کے لیے کمپوزیبل نوڈس استعمال کریں
2. **پائپ لائن ڈیزائن**: Isaac ROS نوڈس کو موثر طریقے سے جوڑیں GPU استعمال کو زیادہ سے زیادہ کرنے کے لیے
3. **وسیلہ کا نظم**: GPU میموری اور کمپیوٹ وسائل کا مناسب طریقے سے نظم کریں
4. **خرابی کا سامنا**: GPU کاموں کے لیے مضبوط خرابی کا سامنا نافذ کریں

### Isaac ROS برائے پیداواری سسٹم

```python
# پیداوار کے لیے تیار Isaac ROS ایپلی کیشن ٹیمپلیٹ
import rclpy
from rclpy.lifecycle import LifecycleNode, TransitionCallbackReturn
from isaac_ros.common import IsaacROSBaseNode

class ProductionIsaacROSApp(IsaacROSBaseNode):
    def __init__(self):
        super().__init__('production_isaac_app')

        # Isaac ROS پیداوار کے بہترین طریقے
        self.declare_parameters(
            namespace='',
            parameters=[
                ('safe_mode', True),  # پیداوار کے لیے محفوظ موڈ فعال کریں
                ('health_check_interval', 5.0),  # صحت کی چیک کی مدت
                ('fallback_behavior', 'stop'),  # خرابی پر واپسی کا طرز
                ('gpu_health_monitoring', True),  # GPU صحت کی نگرانی
            ])

    def on_configure(self, state):
        # Isaac ROS اجزاء کو محفوظ طریقے سے شروع کریں
        try:
            # GPU وسائل شروع کریں
            self.initialize_gpu_resources()

            # Isaac ROS ادراک پائپ لائن کو تشکیل دیں
            self.setup_perception_pipeline()

            # اگر مناسب ہو تو Isaac Sim کنکشن کی تصدیق کریں
            self.validate_simulation_connection()

        except Exception as e:
            self.get_logger().error(f'کنفیگریشن ناکام ہو گئی: {e}')
            return TransitionCallbackReturn.FAILURE

        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state):
        # Isaac ROS وسائل کو مناسب طریقے سے صاف کریں
        self.cleanup_gpu_resources()
        self.shutdown_perception_pipeline()

        return TransitionCallbackReturn.SUCCESS
```

## پچھلے ماڈیولز سے ربط

Isaac ROS پچھلے ماڈیولز کے تصورات پر تعمیر کرتا ہے:
- **ماڈیول 1 (ROS 2)**: تمام Isaac ROS نوڈس ROS 2 رابطہ کے نمونوں کو فالو کرتے ہیں
- **ماڈیول 2 (سمیولیشن)**: Isaac ROS Isaac Sim کے ساتھ بے دریغ انضمام فراہم کرتا ہے حقیقی سینسر سمیولیشن کے لیے

## اگلے اقدامات

ادراک اور نیویگیشن کے لیے Isaac ROS کو سمجھنے کے بعد، اگلا سیکشن [VSLAM اور ادراک ورک لوڈز](./perception) پر ہے، جہاں آپ VSLAM کے لیے مخصوص GPU-تیز الگوری دم کے بارے میں سیکھیں گے جو Isaac ROS کی صلاحیتوں کا فائدہ اٹھاتے ہیں۔

## خلاصہ

Isaac ROS روبوٹکس سافٹ ویئر میں ایک اہم ترقی کی نمائندگی کرتا ہے، GPU-تیز نفاذ فراہم کرتا ہے عام الگوری دم کے جو کمپیوٹ-تیز کاموں کے لیے کارکردگی کو نمایاں طور پر بہتر بناتا ہے۔ یہ پلیٹ فارم خاص طور پر ہیومنائڈ روبوٹکس ایپلی کیشنز کے لیے قیمتی ہے جہاں حقیقی وقت کا ادراک اور نیویگیشن کی صلاحیتیں ضروری ہیں۔ Isaac ROS کو مناسب طریقے سے نافذ کر کے، ڈیولپرز کارکردگی میں نمایاں بہتری حاصل کر سکتے ہیں جبکہ ROS/ROS 2 ایکو سسٹم کے ساتھ مطابقت برقرار رکھ سکتے ہیں۔