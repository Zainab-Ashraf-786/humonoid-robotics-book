---
title: اعلیٰ معیار کی رینڈرنگ کے لیے یونٹی
sidebar_label: یونٹی رینڈرنگ
---

# اعلیٰ معیار کی رینڈرنگ کے لیے یونٹی

یونٹی ایک طاقتور گیم انجن ہے جو روبوٹکس سمیولیشن میں بڑھتی ہوئی اہمیت اختیار کر چکا ہے، خاص طور پر اعلیٰ معیار کی رینڈرنگ، انسان-روبوٹ انٹرایکشن، اور ورچوئل ریلٹی ایپلی کیشنز کے لیے۔ جبکہ گزیبو فزکس سمیولیشن میں مہارت رکھتا ہے، یونٹی امیر دیکھنے کی معیار اور انسانی انٹرایکشن کی صلاحیتیں فراہم کرتا ہے۔

## سیکھنے کے اہداف

اس سیکشن کو مکمل کرنے کے بعد، آپ کر سکیں گے:
- یونٹی کی آرکیٹیکچر اور اس کا روبوٹکس سمیولیشن میں اطلاق کو سمجھنا
- یونٹی روبوٹکس پیکج کے ساتھ روبوٹکس ایپلی کیشنز کے لیے یونٹی کو سیٹ اپ کرنا
- روبوٹکس ویژولائزیشن کے لیے یونٹی کی رینڈرنگ کی صلاحیتیں سمجھنا
- یونٹی میں انسان-روبوٹ انٹرایکشن انٹرفیسز سے واقف ہونا
- ROS/ROS 2 کے ساتھ یونٹی کو روبوٹ کنٹرول کے لیے منسلک کرنا

## روبوٹکس میں یونٹی کا تعارف

### یونٹی کیا ہے؟
یونٹی ایک کراس پلیٹ فارم گیم انجن ہے جو 3D ماحول کو اعلیٰ بصری معیار کے ساتھ رینڈر کرتا ہے۔ جبکہ روایتی طور پر گیمنگ کے لیے استعمال ہوتا ہے، یونٹی کو مندرجہ ذیل میں اہم اطلاقات مل گئے ہیں:
- روبوٹکس کے لیے اعلیٰ معیار کی سمیولیشن
- ورچوئل اور ایوگمنٹڈ ریلٹی ایپلی کیشنز
- انسان-روبوٹ انٹرایکشن انٹرفیس ڈیزائن
- ادراک سسٹم کی ترقی
- مصنوعی ڈیٹا کے ساتھ AI کی تربیت

### روبوٹکس کے لیے یونٹی بمقابلہ گزیبو
جبکہ دونوں پلیٹ فارم روبوٹس کو سمولیٹ کر سکتے ہیں، وہ مختلف مقاصد کے لیے کام آتے ہیں:
- **گزیبو**: فزکس پر مرکوز، روبوٹ ڈائنامکس اور سینسر ماڈلز کی درست سمیولیشن
- **یونٹی**: بصری پر مرکوز، اعلیٰ معیار کی رینڈرنگ اور انسانی انٹرایکشن

یونٹی وہاں جیت جاتا ہے جہاں بصری حقیقت پسندانہ اہم ہو، جیسے:
- فوٹو ریلٹسٹک رینڈرنگ کے ساتھ کمپیوٹر وژن کی تربیت
- انسان-روبوٹ انٹرایکشن ڈیزائن
- VR/AR ایپلی کیشنز
- عوامی مظاہرے جہاں بصری معیار اہم ہو

### یونٹی روبوٹکس پیکج
یونٹی روبوٹکس پیکج روبوٹکس ایپلی کیشنز کے لیے ضروری ٹولز فراہم کرتا ہے:
- ROS/ROS 2 رابطہ برج
- روبوٹ کنٹرول انٹرفیسز
- مصنوعی ڈیٹا جنریشن کے لیے ادراک ٹولز
- سمیولیشن تیزی کی خصوصیات

## روبوٹکس کے لیے یونٹی کو انسٹال کرنا اور سیٹ اپ کرنا

### سسٹم کی ضروریات
- **Windows**: Windows 10/11 64-bit، .NET فریم ورک 4.7.2+
- **macOS**: macOS 10.14+، میٹل-قابل GPU
- **Linux**: Ubuntu 18.04/20.04، OpenGL 3.3+ (پیش نظارہ سپورٹ)
- **GPU**: DirectX 10/OpenGL 3.3+/Metal-قابل GPU
- **RAM**: 8GB کم از کم (16GB تجویز کردہ)
- **اسٹوریج**: 10GB+ یونٹی کے لیے، پروجیکٹ کی جگہ کے علاوہ

### انسٹالیشن عمل
1. یونٹی کی ویب سائٹ سے یونٹی ہب ڈاؤن لوڈ کریں
2. یونٹی ہب انسٹال کریں اور اکاؤنٹ بنائیں
3. یونٹی ہب کا استعمال کر کے یونٹی ورژن 2021.3 LTS یا بعد کا ورژن انسٹال کریں
4. یونٹی روبوٹکس پیکج انسٹال کریں
5. مضبوطی کی تربیت کے لیے یونٹی ML-ایجنٹس ٹول کٹ انسٹال کریں

### ضروری پیکجز
- **یونٹی روبوٹکس پیکج**: ROS/ROS 2 انضمام کے لیے ضروری
- **یونٹی ML-ایجنٹس**: مضبوطی کی تربیت کے ایپلی کیشنز کے لیے
- **XR پیکجز**: VR/AR ایپلی کیشنز ترقی دینے کے لیے
- **یونیورسل رینڈر پائپ لائن (URP)** یا **ہائی ڈیفینیشن رینڈر پائپ لائن (HDRP)**: اعلیٰ درجے کی رینڈرنگ کے لیے

### روبوٹکس کے لیے ابتدائی سیٹ اپ
یونٹی اور ضروری پیکجز انسٹال کرنے کے بعد، ایک نیا 3D پروجیکٹ بنائیں:
1. یونٹی ہب کھولیں
2. "نیا پروجیکٹ" پر کلک کریں
3. روبوٹکس ایپلی کیشنز کے لیے "3D (Built-in Render Pipeline)" یا "3D (URP)" منتخب کریں
4. پروجیکٹ کو "RoboticsSimulation" جیسے وضاحتی نام دیں
5. "پروجیکٹ بنائیں" پر کلک کریں

## روبوٹکس کے لیے یونٹی آرکیٹیکچر

### بنیادی اجزاء
1. **منظر**: تمام اشیاء پر مشتمل 3D جگہ
2. **GameObject**: منظر میں ہر چیز (روبوٹس، سینسرز، ماحول)
3. **کمپونینٹس**: منسلک رویے (MeshRenderer، Rigidbody، اسکرپٹس)
4. **اثاثے**: دوبارہ استعمال کے قابل وسائل (ماڈلز، مواد، اسکرپٹس)
5. **اسکرپٹس**: C# کوڈ جو رویہ کنٹرول کرتا ہے

### روبوٹکس-مخصوص اجزاء
یونٹی روبوٹکس پیکج روبوٹکس-مخصوص اجزاء شامل کرتا ہے:
- **RosConnector**: ROS/ROS 2 رابطہ کو ہینڈل کرتا ہے
- **UnityROSTcpConnector**: TCP-مبنی ROS کنکشن
- **RobotControl**: روبوٹ کمانڈز کے لیے انٹرفیس
- **سینسر کمپونینٹس**: مختلف سینسر نفاذ

## یونٹی میں روبوٹ ماڈلز کو سیٹ کرنا

### 3D ماڈلز درآمد کرنا
یونٹی متعدد 3D ماڈل فارمیٹس کی حمایت کرتا ہے:
- **FBX**: سب سے عام، اینیمیشنز اور مواد کی حمایت کرتا ہے
- **OBJ**: سادہ جیومیٹری، وسیع حمایت یافتہ
- **GLTF/GLB**: جدید فارمیٹ جس کے ساتھ یونٹی کی اچھی حمایت ہے
- **DAE**: کولیڈا فارمیٹ

### URDF کو یونٹی میں تبدیل کرنا
موجود URDF ماڈلز والے روبوٹس کے لیے:
1. URDF کو COLLADA (.dae) فارمیٹ میں ایکسپورٹ کریں
2. COLLADA فائل کو یونٹی میں درآمد کریں
3. جوڑ کے تعلقات کو دستی طور پر دوبارہ تعمیر کریں
4. یونٹی-مخصوص کمپونینٹس شامل کریں

متبادل طور پر، **بلینڈر** جیسے سافٹ ویئر کا استعمال کر کے تبدیل کریں:
```bash
# URDF کو COLLADA میں کنورٹر ٹول کے ذریعے ایکسپورٹ کریں
# پھر COLLADA کو یونٹی میں درآمد کریں
```

### روبوٹ ہائیرارکیز کو سیٹ کرنا
یونٹی روبوٹکس کی articulation کو ظاہر کرنے کے لیے ٹرانسفارم ہائیرارکی استعمال کرتا ہے:
```
Robot_Base
├── Torso
│   ├── Left_Shoulder
│   │   ├── Left_Elbow
│   │   └── Left_Wrist
│   └── Right_Shoulder
│       ├── Right_Elbow
│       └── Right_Wrist
└── Left_Hip
    ├── Left_Knee
    └── Left_Ankle
```

### جوڑ کمپونینٹس
گزیبو کے SDF/URDF کے برعکس، یونٹی کو جوڑ کے رویے کے لیے حسب ضرورت اسکرپٹس کی ضرورت ہوتی ہے:

```csharp
using UnityEngine;

public class UnityJoint : MonoBehaviour
{
    public float minAngle = -90f;
    public float maxAngle = 90f;
    public float speed = 100f;

    private float currentAngle = 0f;

    void Update()
    {
        // ان پٹ یا کمانڈز کی بنیاد پر جوڑ حرکت کریں
        float targetAngle = GetTargetAngle(); // ROS یا مقامی کنٹرول سے
        currentAngle = Mathf.Clamp(targetAngle, minAngle, maxAngle);

        // گھمائیں لاگو کریں
        transform.localRotation = Quaternion.Euler(0, currentAngle, 0); // مثال: Y-محور گھمائیں
    }

    float GetTargetAngle()
    {
        // ROS پیغامات یا مقامی منطق سے آ سکتا ہے
        return currentAngle; // جگہ کا نام
    }
}
```

## یونٹی میں فزکس سمیولیشن

### بلٹ ان فزکس انجن
یونٹی ڈیفالٹ طور پر NVIDIA PhysX استعمال کرتا ہے:
- **Rigidbody**: GameObjects میں فزکس خصوصیات شامل کرتا ہے
- **Colliders**: کولیژن شکلیں بیان کرتا ہے
- **Joints**: Rigidbody کمپونینٹس کو قیود کے ساتھ جوڑتا ہے

### روبوٹکس کے لیے فزکس کو تشکیل دینا
روبوٹکس ایپلی کیشنز کے لیے، ان فزکس ترتیبات کو ایڈجسٹ کریں:
```
ترمیم > پروجیکٹ ترتیبات > فزکس
```

اہم ترتیبات:
- **Solver Iteration Count**: مستحکم جوڑ قیود کے لیے زیادہ (تجویز کردہ: 10-15)
- **Auto Simulation**: خودکار فزکس اپ ڈیٹس کے لیے فعال
- **Default Material**: روبوٹ-دنیا کے تعاملات کے لیے فریکشن اور باؤنس تشکیل دیں

### روبوٹ فزکس سیٹ اپ
```csharp
using UnityEngine;

public class RobotPhysics : MonoBehaviour
{
    public Rigidbody[] linkRigidbodies;
    public ConfigurableJoint[] joints;

    void Start()
    {
        // ہر لنک کی فزکس خصوصیات تشکیل دیں
        foreach(Rigidbody rb in linkRigidbodies)
        {
            rb.useGravity = true;
            rb.drag = 0.1f;
            rb.angularDrag = 0.1f;
        }

        // ہر جوڑ کی قیود تشکیل دیں
        foreach(ConfigurableJoint joint in joints)
        {
            ConfigureJoint(joint);
        }
    }

    void ConfigureJoint(ConfigurableJoint joint)
    {
        // جوڑ حدیں، سپرنگ، ڈیمپر، وغیرہ سیٹ کریں
        SoftJointLimit limit = new SoftJointLimit();
        limit.limit = 45f; // زیادہ سے زیادہ زاویہ
        joint.linearLimit = limit; // لکیری جوڑ کے لیے

        // گھومتے جوڑ کے لیے، زاویہ حدیں تشکیل دیں
        joint.highAngularXLimit = new SoftJointLimit() { limit = 45f };
        joint.lowAngularXLimit = new SoftJointLimit() { limit = -45f };
    }
}
```

## یونٹی میں سینسر سمیولیشن

### کیمرہ سینسرز
یونٹی انتہائی حقیقی کیمرہ سینسرز فراہم کرتا ہے:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using Unity.Robotics.Core;

public class CameraSensor : MonoBehaviour
{
    public Camera cam;
    public string topicName = "/camera/rgb/image_raw";
    public int updateFrequency = 30; // Hz

    private ROSConnection ros;
    private RenderTexture renderTexture;
    private Texture2D textureCopy;
    private int updateInterval;
    private int frameCount;

    void Start()
    {
        ros = ROSConnection.instance;
        updateInterval = Mathf.RoundToInt(60f / updateFrequency); // 60 FPS کا فرض کر کے
        frameCount = 0;

        // رینڈر ٹیکسچر سیٹ کریں
        renderTexture = new RenderTexture(cam.pixelWidth, cam.pixelHeight, 24);
        cam.targetTexture = renderTexture;
        textureCopy = new Texture2D(cam.pixelWidth, cam.pixelHeight, TextureFormat.RGB24, false);
    }

    void Update()
    {
        if (++frameCount >= updateInterval)
        {
            frameCount = 0;
            PublishCameraImage();
        }
    }

    void PublishCameraImage()
    {
        // رینڈر ٹیکسچر کو عام ٹیکسچر میں کاپی کریں
        RenderTexture.active = renderTexture;
        textureCopy.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
        textureCopy.Apply();

        // ROS پیغام فارمیٹ میں تبدیل کریں (سادہ)
        // عمل میں، sensor_msgs/Image کے بطور انکوڈ کریں گے
        // ros.Send(topicName, imageMessage);
    }
}
```

### LIDAR سمیولیشن
LIDAR سمیولیشن کے لیے، یونٹی رے کاسٹنگ استعمال کر سکتا ہے:

```csharp
using System.Collections.Generic;
using UnityEngine;

public class LidarSimulation : MonoBehaviour
{
    public int numberOfBeams = 720;
    public float angleMin = -Mathf.PI / 2;
    public float angleMax = Mathf.PI / 2;
    public float rangeMax = 10.0f;
    public LayerMask detectionLayers = -1;

    [System.Serializable]
    public struct RangeReading
    {
        public float angle;
        public float distance;
    }

    public List<RangeReading> lastScan = new List<RangeReading>();

    void Update()
    {
        lastScan.Clear();

        for(int i = 0; i < numberOfBeams; i++)
        {
            float angle = Mathf.Lerp(angleMin, angleMax, (float)i / (numberOfBeams - 1));
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));
            direction = transform.TransformDirection(direction);

            RaycastHit hit;
            float distance = rangeMax;

            if(Physics.Raycast(transform.position, direction, out hit, rangeMax, detectionLayers))
            {
                distance = hit.distance;
            }

            RangeReading reading = new RangeReading()
            {
                angle = angle,
                distance = distance
            };

            lastScan.Add(reading);
        }

        // اسکین ڈیٹا کو پروسیس یا شائع کریں
        PublishLidarData();
    }

    void PublishLidarData()
    {
        // sensor_msgs/LaserScan فارمیٹ میں ROS میں ڈیٹا بھیجیں
    }
}
```

### IMU سمیولیشن
IMU ڈیٹا یونٹی کی فزکس کا استعمال کرتے ہوئے تقریباً کیا جا سکتا ہے:

```csharp
using UnityEngine;
using RosMessageTypes.Sensor;

public class IMUSimulation : MonoBehaviour
{
    private Rigidbody rb;
    public string topicName = "/imu/data";

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {
        var imuMsg = new ImuMsg();

        // زاویہ کی رفتار (تقریب)
        imuMsg.angular_velocity.x = rb.angularVelocity.x;
        imuMsg.angular_velocity.y = rb.angularVelocity.y;
        imuMsg.angular_velocity.z = rb.angularVelocity.z;

        // لکیری تیزی (گریویٹی کمپنیشن چیلنج شامل کرتا ہے)
        imuMsg.linear_acceleration.x = rb.velocity.x; // سادہ
        imuMsg.linear_acceleration.y = rb.velocity.y;
        imuMsg.linear_acceleration.z = rb.velocity.z + Physics.gravity.z; // تقریبی گریویٹی


        // جہت کو زاویہ کی رفتار کو ضم کرنے کی ضرورت ہوگی

        // پیغام شائع کریں
        // ros.Send(topicName, imuMsg);
    }
}
```

## ROS/ROS 2 انضمام

### یونٹی ROS برج
یونٹی روبوٹکس پیکج TCP-مبنی رابطہ ROS/ROS 2 کے ساتھ فراہم کرتا ہے:

#### انسٹالیشن
1. یونٹی میں، ونڈو > پیکج مینیجر پر جائیں
2. + بٹن پر کلک کریں > گٹ URL سے پیکج شامل کریں
3. درج کریں: `com.unity.robotics.ros-tcp-connector`
4. پیکج انسٹال کریں

#### بنیادی کنکشن سیٹ اپ
```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

public class UnityROSConnection : MonoBehaviour
{
    ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Connect("127.0.0.1", 10000); // ڈیفالٹ پورٹ
    }

    public void SendStringMessage(string topic, string message)
    {
        ros.Send(topic, new StringMsg(message));
    }
}
```

### شائع کرنا اور سبسکرائب کرنا

#### شائع کنندہ کی مثال
```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class JointStatePublisher : MonoBehaviour
{
    public string topicName = "/joint_states";
    private ROSConnection ros;

    // جوڑ حوالہ جات
    public Transform[] jointTransforms;
    public string[] jointNames;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
    }

    void FixedUpdate()
    {
        PublishJointStates();
    }

    void PublishJointStates()
    {
        var msg = new JointStateMsg();
        msg.name = new string[jointNames.Length];
        msg.position = new double[jointNames.Length];
        msg.velocity = new double[jointNames.Length];
        msg.effort = new double[jointNames.Length];

        for(int i = 0; i < jointNames.Length; i++)
        {
            msg.name[i] = jointNames[i];
            msg.position[i] = GetJointPosition(i); // نفاذ پر منحصر
            msg.velocity[i] = GetJointVelocity(i);
            msg.effort[i] = GetJointEffort(i);
        }

        msg.header.stamp = new TimeStamp(Time.time);
        msg.header.frame_id = "base_link";

        ros.Send(topicName, msg);
    }

    double GetJointPosition(int index)
    {
        // زاویہ میں جوڑ کی پوزیشن لوٹائیں
        return 0.0f; // جگہ کا نام
    }

    double GetJointVelocity(int index)
    {
        // rad/s میں جوڑ کی رفتار لوٹائیں
        return 0.0f; // جگہ کا نام
    }

    double GetJointEffort(int index)
    {
        // N*m میں جوڑ کی کوشش لوٹائیں
        return 0.0f; // جگہ کا نام
    }
}
```

#### سبسکرائبر کی مثال
```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;
using UnityEngine;

public class JointCommandSubscriber : MonoBehaviour
{
    public string topicName = "/joint_commands";

    void Start()
    {
        ROSConnection.GetOrCreateInstance().Subscribe<Float32MultiArrayMsg>(
            topicName, JointCommandCallback);
    }

    void JointCommandCallback(Float32MultiArrayMsg msg)
    {
        // جوڑ کمانڈز کو پروسیس کریں
        for(int i = 0; i < msg.data.Count; i++)
        {
            if(i < jointControllers.Length)
            {
                jointControllers[i].SetTargetPosition(msg.data[i]);
            }
        }
    }

    public UnityJoint[] jointControllers;
}
```

## اعلیٰ معیار کی رینڈرنگ کی صلاحیتیں

### رینڈر پائپ لائنز
یونٹی متعدد رینڈرنگ حل فراہم کرتا ہے:

#### یونیورسل رینڈر پائپ لائن (URP)
- ہلکا اور کارآمد
- حقیقی وقت کی روبوٹکس ایپلی کیشنز کے لیے اچھا
- زیادہ تر عام رینڈرنگ خصوصیات کی حمایت کرتا ہے
- کم طاقت والے ہارڈ ویئر پر بہتر کارکردگی

#### ہائی ڈیفینیشن رینڈر پائپ لائن (HDRP)
- انتہائی حقیقی رینڈرنگ
- اعلیٰ درجے کی لائٹنگ اور شیڈنگ
- اعلیٰ معیار کی ویژولائزیشن کے لیے بہتر
- زیادہ طاقت والے ہارڈ ویئر کی ضرورت

### لائٹنگ اور شیڈنگ
یونٹی کا لائٹنگ سسٹم حقیقی روبوٹکس سمیولیشن کے لیے اہم ہے:

**ڈائریکشنل لائٹس**: سورج/ماحول کی لائٹنگ کی شبیہہ دہراتی ہے
```csharp
// یونٹی میں: ایک ڈائریکشنل لائٹ کمپونینٹ شامل کریں
// حقیقی روبوٹ کے سائے کے لیے سایہ ترتیبات تشکیل دیں
```

**حقیقی مواد**: فزیکلی-مبنی شیڈرز استعمال کریں
```csharp
// حقیقی metallic/smoothness قدریں والے مواد بنائیں
// مختلف روبوٹ اجزاء کے لیے مرآت، پلاسٹک، دھات کی خصوصیات
```

### پوسٹ-پروسیسنگ
پوسٹ-پروسیسنگ اثرات کے ساتھ بصری حقیقت پسندی بڑھائیں:
- **ایمبیئنٹ اوکلیوشن**: حقیقی سایہ داری شامل کرتا ہے
- **بلوم**: روشنی کے پھیلنے کے اثرات پیدا کرتا ہے
- **کلر گریڈنگ**: حقیقی دنیا کے کیمرہ خصوصیات سے مماثل کرتا ہے
- **لینس ڈسٹورشن**: کیمرہ لینس اثرات کی شبیہہ دہراتا ہے

## یونٹی میں انسان-روبوٹ انٹرایکشن

### انٹرفیس ڈیزائن
یونٹی جاذب انٹرفیسز بنانے میں مہارت رکھتا ہے:

#### 3D صارف انٹرفیسز
- 3D جگہ میں تعامل کے روبوٹ کنٹرولز
- اشارہ-مبنی انٹرایکشن
- غوطہ خور کنٹرول کے لیے VR/AR انٹرفیسز

#### ڈیش بورڈ تخلیق
```csharp
using UnityEngine;
using UnityEngine.UI; // UI عناصر کے لیے

public class RobotDashboard : MonoBehaviour
{
    public Text statusText;
    public Text batteryText;
    public Slider speedSlider;
    public Button emergencyStopButton;

    void Update()
    {
        UpdateRobotStatus();
    }

    void UpdateRobotStatus()
    {
        // ROS کی روبوٹ کی حالت کے مطابق UI اپ ڈیٹ کریں
        // statusText.text = robotStatus; // ROS ٹاپک سے لیا گیا
    }

    public void OnEmergencyStop()
    {
        // روبوٹ کو ہنگامی سٹاپ کمانڈ بھیجیں
        // ros.Send("/emergency_stop", new EmptyMsg());
    }
}
```

### VR/AR انضمام
یونٹی کی XR صلاحیتیں غوطہ خور HRI کو فعال کرتی ہیں:
- **ورچوئل ریلٹی**: صارف 3D میں چل سکتے ہیں اور روبوٹس کے ساتھ تعامل کر سکتے ہیں
- **ایوگمنٹڈ ریلٹی**: حقیقی دنیا کے مناظر پر روبوٹ کی معلومات اوور لے کر سکتے ہیں
- **مکسڈ ریلٹی**: ورچوئل روبوٹس کو جسمانی ماحول کے ساتھ ملا سکتے ہیں

## ادراک کی تربیت کے لیے یونٹی

### مصنوعی ڈیٹا جنریشن
یونٹی لیبل والے تربیتی ڈیٹا جنریٹ کرنے میں مہارت رکھتا ہے:

#### انسٹینس سیگمینٹیشن
یونٹی سیمنٹک سیگمینٹیشن ماسکس رینڈر کر سکتا ہے:
```csharp
// ہر اشیاء کی کلاس کے لیے منفرد رنگوں والے مختلف مواد استعمال کریں
// سیگمینٹیشن کے لیے علیحدہ RT میں رینڈر کریں
```

#### ڈیپتھ میپس
ہر پکسل کے لیے ڈیپتھ معلومات تک رسائی:
```csharp
// حسب ضرورت شیڈر یا اسکرپٹ میں
// کیمرہ سے ہر پکسل تک ڈیپتھ کا حساب لگائیں
```

#### زمینی حقیقت لیبلز
یونٹی کے لیے مکمل زمینی حقیقت فراہم کرتا ہے:
- اشیاء کی پوزیشنز اور جہتیں
- ڈیپتھ معلومات
- لائٹنگ کی شرائط
- مادہ کی خصوصیات

### ڈیٹا سیٹ جنریشن پائپ لائن
```csharp
using UnityEngine;
using System.IO;
using Unity.Robotics.ROSTCPConnector;

public class DatasetGenerator : MonoBehaviour
{
    public Camera sensorCamera;
    public int datasetSize = 1000;
    public string outputFolder = "TrainingData";

    private int currentSample = 0;

    void Update()
    {
        if(Input.GetKeyDown(KeyCode.Space))
        {
            CaptureDatasetSample();
        }
    }

    void CaptureDatasetSample()
    {
        // روبوٹ/اشیاء کو بے ترتیب کنفیگریشن میں لائیں
        RandomizeScene();

        // RGB تصویر کیپچر کریں
        Texture2D rgbImage = CaptureRGBImage();

        // ڈیپتھ ڈیٹا کیپچر کریں
        Texture2D depthImage = CaptureDepthImage();

        // تشریحات کے ساتھ محفوظ کریں
        SaveSample(rgbImage, depthImage, currentSample++);
    }

    Texture2D CaptureRGBImage()
    {
        // کیمرہ تصویر کیپچر کرنے کا نفاذ
        return null; // جگہ کا نام
    }

    Texture2D CaptureDepthImage()
    {
        // ڈیپتھ کیپچر کرنے کا نفاذ
        return null; // جگہ کا نام
    }

    void SaveSample(Texture2D rgb, Texture2D depth, int sampleIndex)
    {
        byte[] rgbBytes = rgb.EncodeToPNG();
        File.WriteAllBytes($"{outputFolder}/rgb_{sampleIndex:D6}.png", rgbBytes);

        byte[] depthBytes = depth.EncodeToPNG();
        File.WriteAllBytes($"{outputFolder}/depth_{sampleIndex:D6}.png", depthBytes);
    }

    void RandomizeScene()
    {
        // روبوٹ کی پوزیشن، اشیاء کی پوزیشنز، لائٹنگ، وغیرہ بے ترتیب کریں
    }
}
```

## روبوٹکس کے لیے کارکردگی کی بہتری

### رینڈرنگ کی بہتری
- **LOD سسٹم**: دور کے روبوٹس کے لیے تفصیل کم کریں
- **اوکلیوژن کلینگ**: چھپی ہوئی اشیاء رینڈر نہ کریں
- **شیڈر کی بہتری**: جہاں ممکن ہو سادہ شیڈرز استعمال کریں
- **ڈائنامک بیچنگ**: مشابہ اشیاء کو جوڑیں

### فزکس کی بہتری
- **لیئر-مبنی فزکس**: کولیژن میٹرکس کو بہتر بنائیں
- **سو جانے کی حدیں**: سٹیٹک اشیاء کو سو جانے دیں
- **سادہ کولیڈرز**: فزکس کے لیے بنیادی کولیڈرز استعمال کریں

### نیٹ ورک کی بہتری
- **پیغام کی فریکوئنسی**: ضرورت سے زیادہ شائع نہ کریں
- **ڈیٹا کمپریشن**: بڑے پیغامات کو کمپریس کریں
- **کارآمد سیریلائزیشن**: پیغام فارمیٹس کو بہتر بنائیں

## یونٹی روبوٹکس ایپلی کیشنز کا ڈیبگ کرنا

### عام مسائل اور حل

1. **کارکردگی کے مسائل**:
   - فریم ریٹ چیک کریں: ونڈو > تجزیہ > پروفائلر
   - رینڈرنگ/فزکس/اسکرپٹس میں بٹنیکس کی شناخت کریں
   - پیچیدہ شیڈرز یا زیادہ پولی ماڈلز کو بہتر بنائیں
   - غیر ضروری ڈیٹا کی اپ ڈیٹ فریکوئنسی کم کریں

2. **ROS کنکشن کے مسائل**:
   - یقین کریں کہ ROS ماسٹر چل رہا ہے
   - یونٹی میں IP ایڈریسز اور پورٹس چیک کریں
   - یقین کریں کہ ROS پیغام کی اقسام درست طریقے سے وضع کردہ ہیں
   - پیغام کے بہاؤ کی تصدیق کے لیے rostopic echo استعمال کریں

3. **فزکس عدم استحکام**:
   - فزکس ترتیبات میں حل کنندہ دہرائیاں بڑھائیں
   - جوڑ کی حدیں اور قیود ایڈجسٹ کریں
   - ماس اور انیشیا کی خصوصیات کی تصدیق کریں
   - متداخل اشیاء چیک کریں

4. **سینسر کی درستگی**:
   - حقیقی ہم مند مقابلہ میں مصنوعی سینسرز کیلیبریٹ کریں
   - حقیقی سینسرز سے مماثل نوائز پیرامیٹر ایڈجسٹ کریں
   - کوآرڈینیٹ فریم کنونشنز کی تصدیق کریں
   - کنٹرول والے ماحول میں جانچ کریں

### ڈیبگنگ ٹولز
- **یونٹی پروفائلر**: کارکردگی کے بٹنیکس کو مانیٹر کریں
- **منظر ویو**: ٹرانسفارم، کولیڈرز، اور جوڑ کی تفتیش کریں
- **کنسول**: خامی کے پیغامات چیک کریں
- **فزکس ڈیبگر**: کولیژن شکلیں اور قیود دیکھیں
- **ROS ٹولز**: rostopic، rqt، rviz پیغام ڈیبگنگ کے لیے

## روبوٹکس میں یونٹی کے لیے بہترین طریقے

### پروجیکٹ کی تنظیم
- یونٹی کی فولڈر سٹرکچر کو منطقی طریقے سے استعمال کریں
- روبوٹ ماڈلز، ماحول، اور اسکرپٹس کو الگ کریں
- اثاثوں کو مناسب طریقے سے ورژن کنٹرول کریں
- منظر کے سیٹ اپس اور کنفیگریشنز کو دستاویز کریں

### کمپونینٹ ڈیزائن
- اسکرپٹس کو مرکز اور ماڈیولر رکھیں
- مشترکہ کنفیگریشن کے لیے ScriptableObject استعمال کریں
- مختلف روبوٹس کے مابین دوبارہ استعمال کے لیے ڈیزائن کریں
- یونٹی کے کمپونینٹ-مبنی آرکیٹیکچر کو فالو کریں

### کارکردگی کے مسائل
- ہدف والے ہارڈ ویئر کی خصوصیات کے لیے بہتر بنائیں
- بصری معیار اور کارکردگی کے درمیان توازن قائم کریں
- حقیقی وقت کی قیود کے لیے منصوبہ بندی کریں
- ہدف والے ڈپلائمنٹ ہارڈ ویئر پر جانچ کریں

## عام مسائل کا حل

### انسٹالیشن کے مسائل
- **پیکج انسٹالیشن**: یقین کریں کہ یونٹی پیکج مینیجر مناسب طریقے سے کام کرتا ہے
- **لائسنسنگ**: یقین کریں کہ یونٹی لائسنس فعال ہے
- **وابستگیاں**: .NET فریم ورک اور دیگر ضروریات چیک کریں

### انضمام کے مسائل
- **ROS رابطہ**: نیٹ ورک کنفیگریشنز کی تصدیق کریں
- **پیغام کی اقسام**: یونٹی اور ROS کے درمیان مطابقت کی تصدیق کریں
- **کوآرڈینیٹ فریم**: یونٹی (بائیں-ہاتھ والا) کو ROS (دائیں-ہاتھ والا) سے مماثل کریں

### رینڈرنگ کے مسائل
- **گمشدہ ٹیکسچرز**: مواد کی تفویض چیک کریں
- **لائٹنگ کے مسائل**: لائٹنگ سیٹ اپ کی تصدیق کریں
- **کارکردگی**: فریم ریٹ کو مانیٹر کریں اور مناسب طریقے سے بہتر بنائیں

## خلاصہ

یونٹی اعلیٰ معیار کی رینڈرنگ کی صلاحیتیں فراہم کرتا ہے جو فزکس-مرکز سمیولیٹر جیسے گزیبو کو مکمل کرتی ہے۔ اس کی مضبوطیاں ہیں:
- فوٹو ریلٹسٹک بصری رینڈرنگ
- اعلیٰ درجے کی انسان-روبوٹ انٹرایکشن انٹرفیسز
- مصنوعی ڈیٹا سیٹ جنریشن
- VR/AR انضمام کی صلاحیتیں
- لچکدار اور حسب ضرورت ماحول

یونٹی روبوٹکس پیکج اور مناسب ROS انضمام کے ساتھ جمع کر کے، یونٹی روبوٹکس سمیولیشن پائپ لائن میں ایک قیمتی ٹول بن جاتا ہے، خاص طور پر ان ایپلی کیشنز کے لیے جن میں اعلیٰ بصری معیار یا پیچیدہ انسانی انٹرایکشن کی ضرورت ہو۔

## اگلے اقدامات

اگلے سیکشن میں، ہم گزیبو اور یونٹی دونوں پلیٹ فارم پر سینسرز کی سمیولیشن کا جائزہ لیں گے، ان کی مضبوطیوں کا موازنہ کریں گے اور ہر ایک کے لیے مناسب استعمال کے کیسز پر بات چیت کریں گے۔