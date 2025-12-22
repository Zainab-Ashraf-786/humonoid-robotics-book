---
title: روبوٹ سمیولیشن کے لیے گزیبو
sidebar_label: گزیبو سمیولیشن
---

# روبوٹ سمیولیشن کے لیے گزیبو

گزیبو ایک طاقتور، اوپن سورس روبوٹکس سمولیٹر ہے جو درست فزکس سمیولیشن، حقیقی سینسر ماڈلز، اور روبوٹ الگوری دم کی جانچ کے لیے امیر ماحول فراہم کرتا ہے۔ یہ روبوٹکس تحقیق اور ترقی میں سب سے زیادہ استعمال ہونے والا سمولیٹر ہے، خاص طور پر ROS/ROS 2 انضمام کے لیے۔

## سیکھنے کے اہداف

اس سیکشن کو مکمل کرنے کے بعد، آپ کر سکیں گے:
- گزیبو کی آرکیٹیکچر اور بنیادی اجزاء کو سمجھنا
- گزیبو سمیولیشن ماحول کو بنانا اور تشکیل دینا
- گزیبو کے فزکس انجن کے ساتھ روبوٹ ماڈلز کو انضمام کرنا
- گزیبو میں روبوٹ موشن اور سینسر رویہ کو سمولیٹ کرنا
- ROS/ROS 2 کے ساتھ گزیبو کو روبوٹ کنٹرول کے لیے منسلک کرنا

## گزیبو کا تعارف

### گزیبو کیا ہے؟
گزیبو روبوٹکس کے لیے ایک 3D سمیولیشن ماحول ہے جو فراہم کرتا ہے:
- ODE، بُلیٹ، یا DART فزکس انجن کا استعمال کرتے ہوئے حقیقی فزکس سمیولیشن
- OpenGL کے ساتھ اعلیٰ معیار کی رینڈرنگ
- درست سینسر سمیولیشن (کیمرہ، LIDAR، IMUs، وغیرہ)
- روبوٹس، سینسرز، اور ماحول کی وسیع لائبریری
- ROS/ROS 2 کے ساتھ بے دریغ انضمام

### روبوٹکس ایکو سسٹم میں گزیبو کا کردار
گزیبو ام abstract الگوری دم کی ترقی اور حقیقی دنیا کے روبوٹ ڈپلائمنٹ کے درمیان پل کا کام کرتا ہے۔ یہ ڈویلپرز کو اجازت دیتا ہے:
- فزیکل ڈپلائمنٹ سے پہلے محفوظ طریقے سے الگوری دم کی جانچ
- مختلف ماحول اور حالات کو سمولیٹ کرنا
- AI تربیت کے لیے بڑی مقدار میں مصنوعی ڈیٹا تیار کرنا
- سینسر ماڈلز اور روبوٹ رویوں کی توثیق کرنا

## گزیبو کو انسٹال کرنا اور سیٹ اپ کرنا

### سسٹم کی ضروریات
- **OS**: Ubuntu 20.04/22.04 LTS، Windows 10/11، یا macOS 10.15+
- **CPU**: ملٹی-کور پروسیسر
- **RAM**: 8GB کم از کم (16GB تجویز کردہ)
- **GPU**: OpenGL 3.3+ مطابق گرافکس کارڈ کے ساتھ ڈیڈیکٹیڈ GPU تجویز کردہ
- **اسٹوریج**: 2GB دستیاب جگہ

### انسٹالیشن
Ubuntu کے لیے ROS 2 Humble Hawksbill کے ساتھ:
```bash
sudo apt update
sudo apt install gazebo libgazebo-dev
```

براہ راست انسٹالیشن کے لیے:
```bash
sudo apt install gz-harmonic  # Gazebo Garden/Harmonic کے لیے
# یا
sudo apt install gazebo-classic  # legacy Gazebo Classic کے لیے
```

### بنیادی لانچ
```bash
gz sim  # Gazebo Garden/Harmonic کے لیے
# یا
gazebo  # Gazebo Classic کے لیے
```

## گزیبو آرکیٹیکچر

### بنیادی اجزاء
1. **فزکس انجن**: جامد جسم کے ڈائنامکس کو سمولیٹ کرتا ہے (ODE، بُلیٹ، DART)
2. **رینڈرنگ انجن**: ویژولائزیشن کو ہینڈل کرتا ہے (OpenGL)
3. **سینسر سسٹم**: مختلف سینسر کی اقسام کو سمولیٹ کرتا ہے
4. **GUI**: تعامل کے لیے گریفیکل انٹرفیس
5. **ٹرانسپورٹ سسٹم**: انٹر-کمپوننٹ میسجینگ

### دنیا اور ماڈلز
- **دنیا**: ماحول، فزکس خصوصیات، اور سٹیٹک اشیاء کی وضاحت کرتا ہے
- **ماڈلز**: روبوٹس، اشیاء، اور ڈائنامک اداروں کی نمائندگی کرتا ہے
- ** scenari**: خاص سمیولیشنز کے لیے دنیا اور ماڈلز کو جوڑتا ہے

## گزیبو دنیا کی وضاحت

### دنیا کی فائل کی ساخت
گزیبو دنیا کی فائل ایک XML فائل ہے جو سمیولیشن ماحول کی وضاحت کرتی ہے:

```xml
<?xml version="1.0"?>
<sdf version="1.6">
  <world name="my_world">
    <!-- فزکس انجن کی ترتیبات -->
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- لائٹنگ -->
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

    <!-- زمینی سطح -->
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

    <!-- حسب ضرورت ماڈلز شامل کریں -->
    <!-- مزید مواد... -->
  </world>
</sdf>
```

### فزکس کنفیگریشن
فزکس انجن کی ترتیبات سمیولیشن کی درستگی اور کارکردگی کو کنٹرول کرتی ہیں:
- **max_step_size**: چھوٹے قدم درستگی بڑھاتے ہیں لیکن کارکردگی کم کرتے ہیں
- **real_time_factor**: حقیقی وقت کے مقابلے میں ہدف کی رفتار (1.0 = حقیقی وقت)
- **real_time_update_rate**: فی سیکنڈ اپ ڈیٹس

## گزیبو میں روبوٹ ماڈل انضمام

### SDF بمقابلہ URDF
- **URDF**: یونیفائیڈ روبوٹ ڈسکرپشن فارمیٹ، ROS/ROS 2 کے ذریعے استعمال کیا جاتا ہے
- **SDF**: سمیولیشن ڈسکرپشن فارمیٹ، گزیبو کے ذریعے استعمال کیا جاتا ہے
- گزیبو دونوں فارمیٹس لوڈ کر سکتا ہے، لیکن SDF زیادہ سمیولیشن-مخصوص خصوصیات فراہم کرتا ہے

### URDF میں گزیبو-مخصوص عناصر شامل کرنا
گزیبو کے ساتھ کام کرنے کے لیے، URDF ماڈلز کو اضافی گزیبو-مخصوص عناصر کی ضرورت ہوتی ہے:

```xml
<robot name="my_robot">
  <!-- معیاری URDF مواد -->
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

  <!-- گزیبو-مخصوص عناصر -->
  <gazebo reference="base_link">
    <material>Gazebo/Green</material>
  </gazebo>

  <!-- سینسرز -->
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

### گزیبو میں جوڑ کنٹرول
گزیبو میں روبوٹ جوڑوں کو کنٹرول کرنے میں ٹرانسمیشن عناصر کی وضاحت شامل ہے:

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

## گزیبو میں سینسر سمیولیشن

### کیمرہ سینسرز
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

### LIDAR سینسرز
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

### IMU سینسرز
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

## گزیبو پلگ انز

### پلگ ان کی اقسام
گزیبو اضافی فعالیت کو بڑھانے کے لیے پلگ انز استعمال کرتا ہے:
- **سینسر پلگ انز**: سینسرز کو ROS/ROS 2 کے ساتھ انٹرفیس کرتا ہے
- **ماڈل پلگ انز**: ماڈلز میں حسب ضرورت رویہ شامل کرتا ہے
- **دنیا پلگ انز**: حسب ضرورت دنیا کا رویہ شامل کرتا ہے
- **سسٹم پلگ انز**: گزیبو کی بنیادی فعالیت کو تبدیل کرتا ہے

### مثال ماڈل پلگ ان
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
      // حسب ضرورت رویہ یہاں جاتا ہے
      this->model->SetLinearVel(math::Vector3(0.5, 0, 0)); // آگے بڑھیں
    }

    private: physics::ModelPtr model;
    private: event::ConnectionPtr updateConnection;
  };

  GZ_REGISTER_MODEL_PLUGIN(CustomController)
}
```

## ROS/ROS 2 انضمام

### گزیبو برج
گزیبو گزیبو پیغامات اور ROS/ROS 2 پیغامات کے درمیان ترجمہ کے ذریعے ROS/ROS 2 کے ساتھ انضمام کرتا ہے:

```xml
<!-- دنیا کی فائل میں -->
<world>
  <!-- ... دیگر مواد ... -->
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

### گزیبو میں عام ROS/ROS 2 ٹاپکس
- `/clock`: سمیولیشن کلاک (جب فعال ہو)
- `/joint_states`: جوڑ کی پوزیشنز، رفتاریں، کوششیں
- `/tf` اور `/tf_static`: ٹرانسفارم ڈیٹا
- `/gazebo/model_states`: ماڈل کی پوزیشنز اور ٹویسٹ
- `/gazebo/link_states`: لنک کی پوزیشنز اور ٹویسٹ
- سینسر ڈیٹا ٹاپکس (مثلاً `/camera/image_raw`, `/scan`)

### ROS/ROS 2 کے ساتھ گزیبو میں روبوٹس کو کنٹرول کرنا

**جوڑ کنٹرول کی مثال:**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

class GazeboController(Node):
    def __init__(self):
        super().__init__('gazebo_controller')

        # جوڑ کمانڈز کے لیے پبلشر
        self.joint_cmd_pub = self.create_publisher(Float64MultiArray, '/joint_commands', 10)

        # جوڑ کی حالت کے لیے سبسکرائبر
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10)

        # کنٹرول لوپ کے لیے ٹائمر
        self.control_timer = self.create_timer(0.02, self.control_loop)  # 50 Hz

        self.joint_positions = {}

    def joint_state_callback(self, msg):
        self.joint_positions = dict(zip(msg.name, msg.position))

    def control_loop(self):
        # کنٹرول لاگک نافذ کریں
        cmd_msg = Float64MultiArray()
        cmd_msg.data = [0.5, 0.3, -0.2]  # مثال جوڑ کمانڈز
        self.joint_cmd_pub.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    controller = GazeboController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()
```

## فزکس کنفیگریشن اور ٹیوننگ

### میٹریل کی خصوصیات
گزیبو میں حقیقی میٹریل انٹرایکشنز کی وضاحت کریں:

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

### حل کنندہ پیرامیٹر
بہتر استحکام کے لیے فزکس حل کنندہ ٹیون کریں:

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

## ہیومنائڈ روبوٹس کے لیے گزیبو کی بہترین طریقے

### کنیمیٹک استحکام
ہیومنائڈ روبوٹس کو استحکام کے لیے احتیاط کی ضرورت ہوتی ہے:

1. **ماس تقسیم**: یقین کریں کہ مرکز کا ماس سپورٹ پولی گان کے اندر رہتا ہے
2. **جوڑ کی حدیں**: ہیومنائڈ جوڑوں کے لیے حقیقی حدیں سیٹ کریں
3. **فریکشن پیرامیٹر**: پاؤں کے لیے پھسلن کو روکنے کے لیے فریکشن ٹیون کریں
4. **ایکچو ایٹر ماڈلز**: حدود کے ساتھ حقیقی ایکچو ایٹر ماڈلز استعمال کریں

### سمیولیشن فیڈیلٹی کے مسائل
ہیومنائڈ روبوٹکس ایپلی کیشنز کے لیے:
- پاؤں اور ہاتھوں کے لیے ہائی ریزولوشن کولیژن مشس استعمال کریں
- COM اور لمحہ کی انیشیا کی خصوصیات کو احتیاط سے ٹیون کریں
- یقین کریں کہ ZMP اور CoM کا رویہ امکانات سے مماثل ہے
- وہول-بائڈی کنٹرولرز مناسب طریقے سے نافذ کریں

### کارکردگی کی بہتری
- جہاں ممکن ہو روبوٹ کے صرف ضروری حصے سمولیٹ کریں
- غیر اہم حصوں کے لیے سادہ کولیژن جیومیٹریز استعمال کریں
- درکار درستگی کے مطابق فزکس اپ ڈیٹ کی شرح ایڈجسٹ کریں
- ہائی ریٹ ڈیٹا سمیولیشن کے لیے GPU سینسرز پر غور کریں

## گزیبو سمیولیشنز کا ڈیبگ کرنا

### عام مسائل اور حل

1. **روبوٹ زمین کے ذریعے گر جاتا ہے**:
   - یقین کریں کہ کولیژن جیومیٹریز مناسب طریقے سے وضاحت شدہ ہیں
   - چیک کریں کہ ماڈلز کے پاس مناسب ماس اور انیشیل خصوصیات ہیں
   - ضرورت پڑنے پر ERP اور CFM پیرامیٹر ایڈجسٹ کریں

2. **جِٹر/بے استحکم رویہ**:
   - فزکس ٹائم سٹیپ کم کریں
   - حل کنندہ پیرامیٹر ایڈجسٹ کریں (دہرائیاں، sor، erp، cfm)
   - بہت پتلی یا غلط کولیژن مشس چیک کریں
   - یقین کریں کہ ماس کی خصوصیات مناسب ہیں

3. **ایکچو ایٹر مناسب طریقے سے جواب نہیں دیتے**:
   - یقین کریں کہ ٹرانسمیشن کنفیگریشن جوڑ کے ناموں سے مماثل ہے
   - چیک کریں کہ URDF اور کنٹرولر میں کنٹرول انٹرفیسز مماثل ہیں
   - کنٹرول لوپ ٹائمنگ اور میسج کی شرح کی توثیق کریں

### ڈیبگنگ ٹولز
- خصوصیات کی تفتیش کے لیے گزیبو کا ماڈل انسپیکٹر استعمال کریں
- قوت کے تعاملات دیکھنے کے لیے کولیژن ویژولائزیشن فعال کریں
- جوڑ کی حالت اور کوشش کی قدریں حقیقی وقت میں مانیٹر کریں
- تفصیلی لاگنگ کے لیے ڈیبگ فلیگز کے ساتھ `gazebo` استعمال کریں

## اعلیٰ درجے کی گزیبو خصوصیات

### متعدد روبوٹ سمیولیشن
گزیبو ایک ہی ماحول میں متعدد روبوٹس کو ہینڈل کر سکتا ہے:
- ہر روبوٹ کے لیے منفرد نیمسپیسز استعمال کریں
- TF فریم کانفک نہ ہونے کو یقینی بنائیں
- ہر روبوٹ کے لیے علیحدہ کنٹرولرز تشکیل دیں

### ڈائنامک ماحول
پروگرامی طور پر تبدیل ہونے والا ماحول تخلیق کریں:
- سمیولیشن کے دوران ماڈلز اسپون/ہٹا دیں
- موجودہ ماڈلز کی خصوصیات کو تبدیل کریں
- طریق کار کے ذریعے زمین تیار کریں

### ریکارڈنگ اور پلے بیک
بعد کے تجزیات کے لیے سمیولیشن ڈیٹا ریکارڈ کریں:
- `gz log` استعمال کر کے سمیولیشن رنز ریکارڈ کریں
- آف لائن پروسیسنگ کے لیے سینسر ڈیٹا ایکسپورٹ کریں
- مسلسل جانچ کے لیے سیناریو دوبارہ چلائیں

## عام مسائل کا حل

### انسٹالیشن اور سیٹ اپ
- **گرافکس سپورٹ کی کمی**: یقین کریں کہ OpenGL 3.3+ دستیاب ہے
- **اجازت کے مسائل**: ڈیوائس تک رسائی کے لیے صارف کی اجازت چیک کریں
- **وابستگی کے مسائل**: یقین کریں کہ تمام ROS/ROS 2 وابستگیاں انسٹال ہیں

### سمیولیشن استحکام
- **بڑے ٹائم سٹیپس**: بہتر درستگی کے لیے فزکس اسٹیپ سائز کم کریں
- **ہائی گینز**: آسیلیشن کا تجربہ کر رہے ہوں تو کنٹرولر گینز کم کریں
- **ناکافی قیود والے ماڈلز**: یقین کریں کہ تمام ماڈلز مناسب طریقے سے قید ہیں

## خلاصہ

گزیبو روبوٹ سمیولیشن کے لیے ایک طاقتور اور لچکدار پلیٹ فارم فراہم کرتا ہے، خاص طور پر روبوٹکس تحقیق اور ترقی کے لیے۔ ROS/ROS 2 کے ساتھ اس کا انضمام ہیومنائڈ روبوٹس پر روبوٹک الگوری دم کی جانچ اور توثیق کے لیے ایک مناسب انتخاب بناتا ہے۔ مؤثر گزیبو استعمال کی کلید ہے:

1. XML-مبنی دنیا اور ماڈل کی وضاحت کے فارمیٹس کو سمجھنا
2. فزکس اور سینسر کی خصوصیات کو مناسب طریقے سے کنفیگر کرنا
3. روبوٹ کنٹرول کے لیے ROS/ROS 2 کے ساتھ انضمام کرنا
4. بہترین کارکردگی اور استحکام کے لیے پیرامیٹر ٹیون کرنا

## اگلے اقدامات

اگلے سیکشن میں، ہم یونٹی کو تلاش کریں گے، جو گزیبو کی فزکس-مرکز سمیولیشن کے ساتھ مکمل کرنے والی اعلیٰ معیار کی رینڈرنگ اور انسان-روبوٹ انٹرایکشن کی صلاحیتیں فراہم کرتا ہے۔ ایک ساتھ، یہ پلیٹ فارم ہیومنائڈ روبوٹکس ایپلی کیشنز کے لیے جامع سمیولیشن کی صلاحیتیں فراہم کرتے ہیں۔