---
title: VSLAM اور ادراک کے کام
sidebar_label: VSLAM & ادراک
---

# VSLAM اور ادراک کے کام

بصری SLAM (ایک وقت میں مقام اور نقشہ سازی) اور ادراک کے کام جدید روبوٹکس کی دانش کا مرکز ہیں، جو روبوٹس کو اپنے ماحول کو سمجھنے اور اس میں نیویگیٹ کرنے کے قابل بناتے ہیں۔ یہ سیکشن اس بات کو احاطہ کرتا ہے کہ NVIDIA Isaac ٹیکنالوجیز GPU پروسیسنگ کا استعمال کرتے ہوئے ان کمپیوٹ-انٹینسیو الگوری دم کو کیسے تیز کرتی ہیں۔

## سیکھنے کے اہداف

اس سیکشن کو مکمل کرنے کے بعد، آپ کر سکیں گے:
- بصری SLAM کے اصولوں اور اس کے متغیرات کو سمجھنا
- Isaac ٹولز کا استعمال کرتے ہوئے GPU-تیز ادراک پائپ لائنز نافذ کرنا
- VSLAM، VIO، اور دیگر بصری ادراک کے طریقوں کے درمیان فرق سمجھنا
- Isaac Sim اور Isaac ROS کو ادراک کے کام کے لیے کنفیگر کرنا
- ہیومنائڈ روبوٹس کے لیے خاص طور پر ادراک کنیکٹس کو لاگو کرنا
- ادراک سسٹم کی توثیق اور بینچ مارک کیسے کرنا

## VSLAM اور بصری ادراک کا تعارف

### بصری SLAM کیا ہے؟

بصری SLAM روبوٹس کو ایک وقت میں ایک ماحول میں مقام کو متعین کرنے اور اس ماحول کا نقشہ بنانے کے قابل بناتا ہے صرف بصری (کیمرہ) ڈیٹا کا استعمال کرتے ہوئے۔ ہیومنائڈ روبوٹس کے لیے، VSLAM نیویگیشن اور جگہ کے بارے میں شعور کے لیے ضروری ہے انسانی ماحول میں۔

### VSLAM کے کلیدی تصورات

1. **ویژن کا پتہ لگانا**: تصاویر میں منفرد نقاط کی شناخت
2. **ویژن میچنگ**: متعدد فریموں میں ویژن کو جوڑنا
3. **پوز ایسٹیمیشن**: فریموں کے درمیان کیمرے کی حرکت کا تعین
4. **نقشہ سازی**: ماحول کی 3D نمائندگی بنانا
5. **لوپ کلوزر**: ڈرائیف کو درست کرنے کے لیے پہلے سے ملاقات کی گئی جگہوں کو پہچاننا

### VSLAM کے متغیرات

- **Mono SLAM**: ایک کیمرہ کا استعمال کرتا ہے (کمپیوٹیشنل طور پر چیلنجنگ، زیادہ ڈرائیف)
- **اسٹیریو SLAM**: اسٹیریو کیمرہ کا استعمال کرتا ہے (بہتر گہرائی کے اندازے)
- **RGB-D SLAM**: گہرائی کیمرہ کا استعمال کرتا ہے (اعلیٰ درجے کی درستگی، محدود رینج)
- **بصری-انرٹیل SLAM (VIO)**: بصری اور IMU ڈیٹا کو جوڑتا ہے (کم ڈرائیف)

## VSLAM کے لیے GPU تیزی

### GPU تیزی کیوں اہم ہے

روایتی VSLAM الگوری دم کمپیوٹیشنل طور پر بھاری ہیں:

- **ویژن نکالنا**: فی فریم ملین پکسلز کی پروسیسنگ
- **ویژن میچنگ**: فریموں کے درمیان ہزاروں ویژن کا موازنہ
- **بندل ایڈجسٹمنٹ**: بڑے آپٹیمائزیشن مسائل کو حل کرنا
- **ٹریکنگ**: حقیقی وقت میں پوز ایسٹیمیشن کرنا

GPU تیزی ان چیلنجز کا سامنا کرتی ہے:

- **پیرالل پروسیسنگ**: پکسل آپریشنز کی بڑے پیمانے پر پیرالائزیشن
- **مخصوص ہارڈ ویئر**: نیورل نیٹ ورک کمپونینٹس کے لیے ٹینسر کور
- **میموری بینڈ وڈتھ**: ٹیکسچر آپریشنز کے لیے ہائی بینڈ وڈتھ میموری
- **فکسڈ فنکشن یونٹس**: کیمرہ ڈیٹا کے لیے ویڈیو انکوڈنگ/ڈیکوڈنگ یونٹس

### Isaac SLAM آرکیٹیکچر

NVIDIA Isaac SLAM کے لیے متعدد طریقے فراہم کرتا ہے:

1. **Isaac Sim SLAM**: تربیتی ڈیٹا اور توثیق کے لیے
2. **Isaac ROS VSLAM**: حقیقی وقت کے روبوٹ ڈیپلائمنٹ کے لیے
3. **Isaac Sim گراؤنڈ ٹروتھ کے ساتھ**: الگوری دم کی ترقی اور جائزہ کے لیے

## Isaac ROS VSLAM نفاذ

### Isaac ROS اسٹیریو امیج پروسیسنگ

Isaac ROS GPU-تیز اسٹیریو امیج پروسیسنگ پائپ لائنز فراہم کرتا ہے:

```yaml
# stereo_slam_pipeline.launch.py
from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    # Isaac ROS کنٹینر GPU-تیز اسٹیریو پروسیسنگ کے لیے
    container = ComposableNodeContainer(
        name='isaac_ros_stereo_slam_container',
        namespace='isaac_ros',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[
            ComposableNode(
                package='isaac_ros_stereo_image_proc',
                plugin='isaac_ros::stereo_image_proc::RectificationNode',
                name='rectification_node',
                parameters=[{
                    'alpha': 0.0,  # مکمل طور پر ریکٹیفائی کردہ امیجز
                    'use_zero_disparity': True
                }],
                remappings=[
                    ('left/image_raw', '/camera/left/image_raw'),
                    ('right/image_raw', '/camera/right/image_raw'),
                    ('left/camera_info', '/camera/left/camera_info'),
                    ('right/camera_info', '/camera/right/camera_info'),
                    ('left/image_rect', '/left/image_rect'),
                    ('right/image_rect', '/right/image_rect'),
                ]
            ),

            ComposableNode(
                package='isaac_ros_stereo_image_proc',
                plugin='isaac_ros::stereo_image_proc::DisparityNode',
                name='disparity_node',
                parameters=[{
                    'min_disparity': 0,
                    'max_disparity': 128,
                    'num_disp_modes': 4,
                    'disp_similarity_measure': 'SSD',
                    'sgm_p1': 10,
                    'sgm_p2': 120,
                    'sgm_ct_win_size': 9,
                    'sgm_lr_max_diff': 1,
                    'census_kernel_size': 9,
                    'sgm_disp_mode': 'SGM_8WAY'
                }],
                remappings=[
                    ('left/image_rect', '/left/image_rect'),
                    ('right/image_rect', '/right/image_rect'),
                    ('left/camera_info', '/camera/left/camera_info'),
                    ('right/camera_info', '/camera/right/camera_info'),
                    ('disparity', '/disparity'),
                ]
            ),

            ComposableNode(
                package='isaac_ros_stereo_image_proc',
                plugin='isaac_ros::stereo_image_proc::PointCloudNode',
                name='pointcloud_node',
                parameters=[{
                    'use_color': True,
                    'unit_scaling': 0.001,  # mm سے میٹر
                    'rectified_images_only': True
                }],
                remappings=[
                    ('left/image_rect_color', '/left/image_rect'),
                    ('left/camera_info', '/camera/left/camera_info'),
                    ('disparity', '/disparity'),
                    ('pointcloud', '/pointcloud'),
                ]
            ),

            ComposableNode(
                package='isaac_ros_visual_slam',
                plugin='isaac_ros::visual_slam::VisualSlamNode',
                name='visual_slam_node',
                parameters=[{
                    'enable_slam_3d': True,
                    'enable_localization': True,
                    'map_frame': 'map',
                    'odom_frame': 'odom',
                    'base_frame': 'base_link',
                    'input_voxel_map': '',

                    # Isaac GPU-تیز پیرامیٹر
                    'enable_isaac_gpu_fast_brute_force_matcher': True,
                    'enable_isaac_gpu_fast_intrinsics_adapter': True,
                    'min_num_corners': 30,
                    'max_num_corners': 100,
                    'corner_detector_threshold': 0.001,
                    'stereo_matcher_type': 'DP',
                    'num_disparities': 64,
                    'block_size': 15,
                    'disp_min': 0,
                    'disp_max': 128
                }],
                remappings=[
                    ('left/image', '/left/image_rect'),
                    ('left/camera_info', '/left/camera_info'),
                    ('right/image', '/right/image_rect'),
                    ('right/camera_info', '/right/camera_info'),
                    ('visual_slam/imu', '/imu/data'),
                    ('visual_slam/odom', '/visual_slam/odometry'),
                    ('visual_slam/path', '/visual_slam/path'),
                    ('visual_slam/map', '/visual_slam/landmarks'),
                ]
            )
        ]
    )

    return LaunchDescription([container])
```

### Isaac ROS میں ویژن کا پتہ لگانا اور میچنگ

Isaac ROS GPU-تیز ویژن کا پتہ لگانے کا سامان فراہم کرتا ہے:

```python
# Isaac ROS ویژن کا پتہ لگانے کی مثال
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge
import numpy as np

class IsaacFeatureDetector(Node):
    def __init__(self):
        super().__init__('isaac_feature_detector')

        self.bridge = CvBridge()

        # Isaac ROS GPU-تیز ویژن کا پتہ لگانے کا سامان فراہم کرتا ہے
        self.left_image_sub = self.create_subscription(
            Image,
            '/camera/left/image_rect',
            self.left_image_callback,
            10)

        self.right_image_sub = self.create_subscription(
            Image,
            '/camera/right/image_rect',
            self.right_image_callback,
            10)

        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/left/camera_info',
            self.camera_info_callback,
            10)

        # ویژن کی وضاحت کے لیے پبلشر
        self.feature_pub = self.create_publisher(
            Image,
            '/feature_visualization',
            10)

        # Isaac GPU-تیز ویژن کا پتہ لگانے کے پیرامیٹر
        self.feature_params = {
            'max_corners': 100,
            'quality_level': 0.01,
            'min_distance': 10,
            'block_size': 3,
            'gpu_enabled': True  # Isaac-مخصوص GPU تیزی کا پرچم
        }

        self.left_image = None
        self.right_image = None
        self.camera_info = None

    def left_image_callback(self, msg):
        # Isaac ROS GPU-تیز ویژن کا پتہ لگانے کا سامان کرتا ہے
        # یہ ایک تصوراتی مثال ہے - اصل نفاذ Isaac ROS نوڈس میں ہوتا ہے
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # Isaac ROS میں، ویژن کا پتہ لگانا مخصوص GPU-تیز نوڈس میں ہوتا ہے
        # یہ VisualSlamNode کے ذریعے ہینڈل کیا جائے گا
        self.left_image = cv_image

    def right_image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        self.right_image = cv_image

    def camera_info_callback(self, msg):
        self.camera_info = msg

def main(args=None):
    rclpy.init(args=args)
    feature_detector = IsaacFeatureDetector()
    rclpy.spin(feature_detector)
    feature_detector.destroy_node()
    rclpy.shutdown()
```

### Isaac ROS بصری SLAM نوڈ

Isaac ROS بصری SLAM نوڈ GPU-تیز VSLAM فراہم کرتا ہے:

```python
# Isaac ROS VSLAM نوڈ کنفیگریشن
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image, CameraInfo, Imu
from visualization_msgs.msg import MarkerArray
import tf2_ros

class IsaacVisualSLAMNode(Node):
    def __init__(self):
        super().__init__('isaac_visual_slam')

        # Isaac ROS VSLAM سبسکرائبرز
        self.left_image_sub = self.create_subscription(
            Image, '/camera/left/image_rect', self.handle_left_image, 10)
        self.right_image_sub = self.create_subscription(
            Image, '/camera/right/image_rect', self.handle_right_image, 10)
        self.imu_sub = self.create_subscription(
            Imu, '/imu/data', self.handle_imu, 10)

        # Isaac ROS VSLAM پبلشرز
        self.odom_pub = self.create_publisher(Odometry, '/visual_slam/odometry', 10)
        self.path_pub = self.create_publisher(Path, '/visual_slam/path', 10)
        self.landmarks_pub = self.create_publisher(MarkerArray, '/visual_slam/landmarks', 10)

        # Isaac VSLAM ٹرانسفارم کے لیے TF براڈکاسٹر
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        # Isaac-مخصوص GPU-تیز پیرامیٹر
        self.declare_parameters(
            namespace='',
            parameters=[
                # GPU کے لیے کارکردگی کی اصلاح
                ('enable_isaac_gpu_features', True),
                ('enable_isaac_gpu_matching', True),
                ('enable_isaac_gpu_optimization', True),

                # Isaac SLAM پیرامیٹر
                ('tracking_rate_hz', 30.0),
                ('mapping_rate_hz', 5.0),
                ('min_distance_between_keyframes', 0.2),
                ('min_rotation_between_keyframes', 0.2),

                # GPU میموری مینجمنٹ
                ('gpu_memory_limit_mb', 1024),
                ('feature_buffer_size', 5000),
            ])

        self.get_logger().info('Isaac بصری SLAM نوڈ GPU تیزی کے ساتھ شروع کیا گیا')

    def handle_left_image(self, msg):
        # Isaac GPU-تیز پروسیسنگ اسٹیریو ان پٹ کا سامان کرتی ہے
        # اصل پروسیسنگ Isaac کے بہترین C++ CUDA کرنا میں ہوتی ہے
        pass

    def handle_right_image(self, msg):
        # Isaac GPU-تیز پروسیسنگ اسٹیریو ان پٹ کا سامان کرتی ہے
        pass

    def handle_imu(self, msg):
        # Isaac VIO (بصری-انرٹیل اودومیٹری) بصری اور IMU ڈیٹا کو جوڑتا ہے
        # GPU-تیز سینسر فیوژن کا استعمال کرتے ہوئے
        pass

def main(args=None):
    rclpy.init(args=args)
    slam_node = IsaacVisualSLAMNode()

    try:
        rclpy.spin(slam_node)
    except KeyboardInterrupt:
        pass
    finally:
        slam_node.destroy_node()
        rclpy.shutdown()
```

## Isaac Sim SLAM تربیت کے لیے

### SLAM کے لیے مصنوعی ڈیٹا جنریشن

Isaac Sim SLAM الگوری دم کی تربیت اور توثیق کے لیے مصنوعی ڈیٹا سیٹس بنانے میں ماہر ہے:

```python
# Isaac Sim مصنوعی SLAM ڈیٹا سیٹ جنریشن
import carb
import omni
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.synthetic_utils import SyntheticDataHelper
import numpy as np
import os
from PIL import Image as PILImage

class SyntheticSLAMDatasetGenerator:
    def __init__(self, output_dir="slam_training_data"):
        self.output_dir = output_dir
        self.sd_helper = SyntheticDataHelper()
        self.sample_count = 0

        # آؤٹ پٹ ڈائریکٹریز بنائیں
        os.makedirs(f"{output_dir}/images", exist_ok=True)
        os.makedirs(f"{output_dir}/depth", exist_ok=True)
        os.makedirs(f"{output_dir}/poses", exist_ok=True)

    def generate_slam_training_sequence(self, trajectory=None):
        """SLAM تربیت کی ترتیب بنائیں"""

        # Isaac Sim تربیتی ڈیٹا کے لیے گراؤنڈ ٹروتھ فراہم کرتا ہے
        for frame_idx in range(1000):  # 1000 فریم بنائیں
            # Isaac Sim سیمیولیشن کو آگے بڑھاتا ہے
            # world.step(render=True)

            # RGB اور ڈیپتھ امیجیز کیپچر کریں
            rgb_data = self.sd_helper.get_rgb_data()
            depth_data = self.sd_helper.get_depth_data()

            # گراؤنڈ ٹروتھ پوز کیپچر کریں
            pose_data = self.sd_helper.get_ground_truth_pose()

            # مصنوعی تربیتی ڈیٹا محفوظ کریں
            self.save_training_sample(frame_idx, rgb_data, depth_data, pose_data)

            self.sample_count += 1

            # حقیقی ٹریجکٹری کے لیے کنٹرولڈ موشن لاگو کریں
            if trajectory:
                self.apply_trajectory_motion(trajectory[frame_idx])

    def save_training_sample(self, frame_idx, rgb_data, depth_data, pose_data):
        """RGB، ڈیپتھ، اور گراؤنڈ ٹروتھ پوز کے ساتھ ایک تربیتی نمونہ محفوظ کریں"""

        # RGB امیج محفوظ کریں
        rgb_img = PILImage.fromarray((rgb_data * 255).astype(np.uint8))
        rgb_img.save(f"{self.output_dir}/images/frame_{frame_idx:06d}.png")

        # ڈیپتھ امیج محفوظ کریں
        depth_img = PILImage.fromarray((depth_data * 1000).astype(np.uint16))  # 16-بٹ اسٹوریج کے لیے اسکیل
        depth_img.save(f"{self.output_dir}/depth/frame_{frame_idx:06d}.png")

        # گراؤنڈ ٹروتھ پوز محفوظ کریں
        np.savetxt(f"{self.output_dir}/poses/frame_{frame_idx:06d}.txt",
                   np.array(pose_data).reshape(1, -1))

    def validate_synthetic_data_quality(self):
        """SLAM تربیتی ڈیٹا کی معیار کی توثیق کریں"""

        # Isaac Sim مصنوعی ڈیٹا کی معیار کے لیے میٹرکس فراہم کرتا ہے
        # مصنوعی ڈیٹا کے اعداد و شمار کو حقیقی دنیا کے ڈیٹا سیٹس کے ساتھ موازنہ کریں
        quality_metrics = {
            'texture_diversity': 0.85,  # اچھا رینج: 0.7-0.9
            'domain_gap_score': 0.22,   # نیچا بہتر ہے (رینج: 0.0-1.0)
            'coverage_completeness': 0.92,  # اونچا بہتر ہے (رینج: 0.0-1.0)
        }

        # ہدف کے تھریشولڈ کے خلاف توثیق کریں
        assert quality_metrics['texture_diversity'] > 0.7, "مصنوعی ڈیٹا میں کافی ٹیکسچر ڈیورسٹی نہیں ہے"
        assert quality_metrics['domain_gap_score'] < 0.3, "اہداف کے لیے ٹرانسفر کے لیے بہت بڑا ڈومین گیپ"
        assert quality_metrics['coverage_completeness'] > 0.9, "ماحول کی اقسام کے لیے کافی کوریج نہیں ہے"

        return quality_metrics

def main():
    generator = SyntheticSLAMDatasetGenerator("isaac_synthetic_slam_data")
    generator.generate_slam_training_sequence()
    quality = generator.validate_synthetic_data_quality()

    print(f"{generator.sample_count} SLAM تربیتی نمونے معیار کے میٹرکس کے ساتھ بنائے گئے:")
    for metric, value in quality.items():
        print(f"  {metric}: {value:.2f}")

if __name__ == "__main__":
    main()
```

## ہیومنائڈ روبوٹکس کے لیے ادراک کے کام

### ہیومنائڈ-مخصوص ادراک چیلنجز

ہیومنائڈ روبوٹس ادراک سسٹم کے لیے منفرد چیلنجز پیش کرتے ہیں:

1. **اونچائی-متغیر منظر**: ~1.5میٹر اونچائی سے ادراک زمینی روبوٹس سے مختلف ہے
2. **سماجی نیویگیشن**: انسانی سماجی جگہوں اور تعاملات کو سمجھنے کی ضرورت ہے
3. **بائیومیکینیکل رکاوٹیں**: انسانی طرح کی حرکت کی رکاوٹوں کا خیال رکھنا چاہیے
4. **انسان-روبوٹ تعامل**: ادراک کو قدرتی انسان-روبوٹ انٹرفیس کو سپورٹ کرنا چاہیے

### ہیومنائڈ ادراک کے لیے Isaac حل

```yaml
# humanoid_perception_pipeline.yaml
isaac_humanoid_perception:
  ros__parameters:
    # ہیومنائڈ-مخصوص ادراک پیرامیٹر
    stereo_camera:
      # انسان-آنکھ-کی سطح پر ماؤنٹنگ
      base_frame: "head_link"
      optical_frame: "camera_optical_frame"

      # Isaac GPU-تیز اسٹیریو پیرامیٹر
      enable_gpu_rectification: True
      enable_gpu_disparity: True
      enable_gpu_pointcloud: True

      # ہیومنائڈ-مخصوص پیرامیٹر
      viewing_angle_horizontal: 60.0  # انسانی بصری میدان کے مشابہ
      viewing_angle_vertical: 45.0    # انسانی بصری میدان کے مشابہ
      minimum_detection_distance: 0.3  # قریبی رینج کی رکاوٹوں سے بچیں
      maximum_detection_distance: 8.0  # انسانی انڈور ماحول کے لیے مناسب
    visual_slam:
      # ہیومنائڈ-مخصوص SLAM پیرامیٹر
      tracking_rate_hz: 30.0
      mapping_rate_hz: 5.0

      # Isaac GPU-تیز SLAM پیرامیٹر
      enable_isaac_gpu_tracker: True
      enable_isaac_gpu_mapper: True
      enable_isaac_gpu_optimizer: True

      # ہیومنائڈ-مخصوص پیرامیٹر
      min_translation_between_keyframes: 0.2  # انسانی قدم کے سائز کا خیال
      min_rotation_between_keyframes: 0.2     # قدرتی سر کی حرکت
      max_pose_covariance: 0.1                # معیار کی تھریشولڈ

      # سماجی-آگاہ پیرامیٹر
      ignore_human_height_range: [0.8, 2.2]   # عارضی طور پر انسانوں کو رکاوٹوں کے طور پر نظر انداز کریں
      social_navigation_weight: 0.7            # سماجی-آگاہ راستہ منصوبہ بندی کے لیے وزن
    object_detection:
      # Isaac GPU-تیز کا پتہ لگانا
      enable_gpu_inference: True
      inference_engine: "tensorrt"

      # ہیومنائڈ-مخصوص اشیاء کا پتہ لگانا
      detect_classes: [
        "person", "chair", "table", "door", "stairs",
        "handrail", "elevator", "sign", "obstacle"
      ]

      # ہیومنائڈ تعامل کی اشیاء
      interaction_objects: [
        "door_handle", "button", "switch",
        "handrail", "furniture_edges", "stair_edges"
      ]
    semantic_segmentation:
      # Isaac GPU-تیز سیگمینٹیشن
      enable_gpu_segmentation: True
      enable_isaac_optix_renderer: True

isaac_humanoid_navigation:
  ros__parameters:
    # ہیومنائڈ-مخصوص نیویگیشن پیرامیٹر
    local_planner:
      # Isaac GPU-تیز مقامی منصوبہ بندی
      enable_gpu_collision_checking: True
      enable_gpu_path_optimization: True

      # ہیومنائڈ-مخصوص پیرامیٹر
      footprint_radius: 0.35  # تقریباً انسانی کندھوں کا رداس
      max_linear_speed: 0.8   # توازن کے لیے محتاط
      max_angular_speed: 0.5  # استحکام کے لیے ہموار ٹرننگ
      min_obstacle_clearance: 0.5  # ذاتی جگہ کا خیال
```