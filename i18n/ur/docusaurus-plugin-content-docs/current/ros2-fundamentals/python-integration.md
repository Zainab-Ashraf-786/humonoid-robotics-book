---
title: rclpy کے ساتھ پائی تھن انٹیگریشن
sidebar_label: پائی تھن انٹیگریشن
---

# rclpy کے ساتھ پائی تھن انٹیگریشن

یہ سیکشن ROS 2 سسٹم کے ساتھ تعامل کے لیے `rclpy`، ROS 2 کے لیے پائی تھن کلائنٹ لائبریری کا استعمال کرتے ہوئے پائی تھن کو استعمال کرنے کا طریقہ احاطہ کرتا ہے۔ پائی تھن اکثر روبوٹکس ڈویلپمنٹ کے لیے انتخاب کی زبان ہے کیونکہ اس کی استعمال کی آسانی، وسیع لائبریریز، اور سائنسی کمپیوٹنگ کی مضبوط حمایت کی بدولت۔

## سیکھنے کے اہداف

اس سیکشن کو مکمل کرنے کے بعد، آپ کر سکیں گے:
- `rclpy` کی بنیادی باتوں کو سمجھنا اور ROS 2 نوڈس کو پائی تھن میں کیسے بنانا ہے
- ٹاپکس کو پبلش اور سبسکرائب کرنا پائی تھن کا استعمال کرتے ہوئے
- سروسز اور ایکشنز کو پائی تھن میں بنانا اور استعمال کرنا
- یہ سمجھنا کہ پائی تھن ایجنٹس ROS کنٹرولرز کے ساتھ کیسے تعامل کرتے ہیں
- ہیومنائڈ روبوٹکس ایپلی کیشنز میں پائی تھن-مبنی ROS 2 ڈویلپمنٹ کو لاگو کرنا

## rclpy کا تعارف

### rclpy کیا ہے؟
`rclpy` ROS 2 کے لیے پائی تھن کلائنٹ لائبریری ہے۔ یہ ROS 2 کلائنٹ لائبریری (rcl) کے لیے پائی تھن بائنڈنگ فراہم کرتا ہے اور پائی تھن ڈویلپرز کو ROS 2 نوڈس لکھنے، ٹاپکس کو پبلش/سبسکرائب کرنے، سروسز فراہم کرنے/استعمال کرنے، اور ایکشنز بھیجنے/انجام دینے کی اجازت دیتا ہے۔

### روبوٹکس کے لیے پائی تھن کیوں؟
- تیز پروٹو ٹائپنگ اور ڈویلپمنٹ
- وسیع سائنسی اور ریاضیاتی لائبریریز (NumPy، SciPy)
- مضبوط کمیونٹی حمایت
- مشین لرننگ فریم ورکس کے ساتھ آسان انٹیگریشن
- پڑھنے اور برقرار رکھنے میں آسان کوڈ

### انسٹالیشن
`rclpy` عام طور پر ROS 2 تقسیم کا حصہ کے طور پر انسٹال ہوتا ہے۔ آپ اسے براہ راست pip کا استعمال کرتے ہوئے انسٹال کر سکتے ہیں، لیکن اسے ROS 2 سیٹ اپ عمل کے ذریعے انسٹال کرنا تجویز کیا جاتا ہے۔

## پائی تھن میں ROS 2 نوڈ بنانا

### بنیادی نوڈ ساخت
پائی تھن میں ایک بنیادی ROS 2 نوڈ اس ساخت کو فالو کرتا ہے:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('node_name')
        # نوڈ کمپونینٹس یہاں شروع کریں

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

### نوڈ لائف سائیکل
1. **شروعات**: rclpy کو شروع کریں اور نوڈ بنائیں
2. **سیٹ اپ**: پبلشرز، سبسکرائبرز، سروسز، وغیرہ تشکیل دیں
3. **عمل**: نوڈ کو زندہ رکھنے کے لیے `rclpy.spin()` استعمال کریں
4. **کلین اپ**: نوڈ کو تباہ کریں اور rclpy کو بند کریں

## ٹاپکس کو پبلش اور سبسکرائب کرنا

### ایک پبلشر بنانا
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'topic_name', 10)
        timer_period = 0.5  # سیکنڈ
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

### ایک سبسکرائبر بنانا
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
        self.subscription  # غیر استعمال شدہ متغیر کی وارننگ کو روکیں

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    rclpy.spin(listener)
    listener.destroy_node()
    rclpy.shutdown()
```

## پائی تھن میں سروسز

### ایک سروس سرور بنانا
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

### ایک سروس کلائنٹ بنانا
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

## پائی تھن میں ایکشنز

### ایک ایکشن سرور بنانا
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

### ایک ایکشن کلائنٹ بنانا
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

## پائی تھن اور ہیومنائڈ روبوٹکس

### ہیومنائڈ کنٹرول نوڈس
ہیومنائڈ روبوٹکس کے لیے پائی تھن خاص طور پر مفید ہے کیونکہ اس کی پیچیدہ الگوری دم اور تیز پروٹو ٹائپنگ کی ضروریات کے ساتھ انضمام کی صلاحیت کی بدولت:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist

class HumanoidController(Node):
    def __init__(self):
        super().__init__('humanoid_controller')

        # جوڑ کی حالت کے لیے سبسکرائب کریں
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)

        # کمانڈ ویلوسیٹیز کے لیے پبلشر
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        # کنٹرول لوپ کے لیے ٹائمر
        self.control_timer = self.create_timer(0.05, self.control_loop)  # 20 Hz

    def joint_state_callback(self, msg):
        # جوڑ کی حالت کی معلومات کو پروسیس کریں
        self.joint_positions = dict(zip(msg.name, msg.position))

    def control_loop(self):
        # ہیومنائڈ کنٹرول لاگک یہاں نافذ کریں
        cmd_vel = Twist()
        # کنٹرول الگوری دم کے مطابق مناسب کمانڈ کا حساب لگائیں
        self.cmd_vel_pub.publish(cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    controller = HumanoidController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()
```

### مشین لرننگ کے ساتھ انٹیگریشن
ML میں پائی تھن کی طاقت اسے اے آئی ڈرائیون روبوٹکس ایپلی کیشنز کے لیے مثالی بنا دیتی ہے:

```python
import rclpy
from rclpy.node import Node
import tensorflow as tf  # مثال ML لائبریری
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class MLPerceptionNode(Node):
    def __init__(self):
        super().__init__('ml_perception_node')
        self.bridge = CvBridge()
        self.model = self.load_model()  # اپنا تربیت یافتہ ماڈل لوڈ کریں

        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)

    def load_model(self):
        # اپنا تربیت یافتہ ML ماڈل لوڈ کریں
        return tf.keras.models.load_model('path/to/model')

    def image_callback(self, msg):
        # ROS امیج کو OpenCV فارمیٹ میں تبدیل کریں
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # انفرینس چلائیں
        prediction = self.model.predict(cv_image[None, ...])

        # پریڈکشن کو پروسیس کریں اور ممکنہ طور پر نتائج کو شائع کریں
        # دیگر نوڈس کے استعمال کے لیے ٹاپکس پر
```

## ROS 2 میں پائی تھن کے لیے بہترین طریقے

### کارکردگی
- ریاضیاتی کمپیوٹیشنز کے لیے numpy استعمال کریں
- کارکردگی کے اہم اجزاء کے لیے Cython پر غور کریں
- پائی تھن کے گلوبل انٹرپریٹر لاک (GIL) محدودیات پر توجہ دیں
- ضرورت کے مطابق مناسب تھریڈنگ ماڈلز استعمال کریں

### خامی کا انتظام
- مناسب خامی کا انتظام نافذ کریں
- ڈیبگنگ کے لیے ROS 2 کے لاگنگ سسٹم کا استعمال کریں
- کنکشن ناکامیوں کو نرمی سے سنبھالیں
- سروس کالز اور ایکشنز کے لیے ٹائم آوٹس نافذ کریں

### کوڈ کی تنظیم
- کوڈ کی تنظیم کے لیے ROS 2 پیکجز استعمال کریں
- PEP 8 سٹائل ہدایات کو فالو کریں
- مناسب docstrings کے ساتھ کوڈ کو دستاویز کریں
- مناسب جگہوں پر ٹائپ ہنٹس استعمال کریں

## عام مسائل کا حل

### امپورٹ کے مسائل
- اس بات کو یقینی بنائیں کہ آپ کا پائی تھن ماحول مناسب طریقے سے تشکیل دیا گیا ہے
- چیک کریں کہ `rclpy` صحیح ماحول میں انسٹال ہے
- تصدیق کریں کہ آپ کا ROS 2 ماحول ذریعہ ہے

### نوڈ مواصلات کے مسائل
- `ros2 node list` استعمال کریں تاکہ تصدیق کریں کہ نوڈس چل رہے ہیں
- `ros2 topic list` استعمال کریں تاکہ تصدیق کریں کہ ٹاپکس دستیاب ہیں
- چیک کریں کہ ٹاپک نام پبلشرز اور سبسکرائبرز کے درمیان بالکل مماثل ہیں

### کارکردگی کے مسائل
- CPU اور میموری کے استعمال کو مانیٹر کریں
- ٹائمر فریکوئنسیز کو مناسب طریقے سے ایڈجسٹ کریں
- کثافت کے کاموں کے لیے غیر ہم وقت پروسیسنگ کا استعمال کرنا پر غور کریں

## خلاصہ

`rclpy` کے ساتھ پائی تھن ROS 2 ایپلی کیشنز تیار کرنے کا ایک طاقتور اور قابل رسائی طریقہ فراہم کرتا ہے۔ اس کی انضمام کی صلاحیتیں، استعمال کی آسانی، اور مضبوط ایکو سسٹم اسے روبوٹکس ڈویلپمنٹ کے لیے ایک عمدہ انتخاب بناتے ہیں، خاص طور پر ہیومنائڈ روبوٹکس میں جہاں تیز پروٹو ٹائپنگ اور مشین لرننگ انضمام اہم ہے۔

## اگلے اقدامات

اگلے سیکشن میں، ہم URDF (یونیفائیڈ روبوٹ ڈسکرپشن فارمیٹ) کو احاطہ کریں گے، جو ROS 2 میں روبوٹس کی وضاحت کے لیے ضروری ہے، خاص طور پر پیچیدہ کنیمیٹک سٹرکچر والے ہیومنائڈ روبوٹس کے لیے اہم ہے۔