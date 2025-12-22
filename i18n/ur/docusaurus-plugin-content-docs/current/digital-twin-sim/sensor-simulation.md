---
title: پلیٹ فارم کے درمیان سینسر سمیولیشن
sidebar_label: سینسر سمیولیشن
---

# پلیٹ فارم کے درمیان سینسر سمیولیشن

روبوٹک ادراک ماحول کو سمجھنے اور اس کے ساتھ تعامل کے لیے سینسر ڈیٹا پر زیادہ تر انحصار کرتا ہے۔ یہ سیکشن گزیبو اور یونٹی کے درمیان سینسر سمیولیشن کی صلاحیتوں کا موازنہ کرتا ہے، جس میں LiDAR، ڈیپتھ کیمرہ، IMUs، اور دیگر سینسرز شامل ہیں۔ ہر پلیٹ فارم کی مضبوطیوں اور کمزوریوں کو سمجھنا آپ کی روبوٹکس ایپلی کیشنز کے لیے مناسب سمیولیشن ٹولز کا انتخاب کرنے کے لیے اہم ہے۔

## سیکھنے کے اہداف

اس سیکشن کو مکمل کرنے کے بعد، آپ کر سکیں گے:
- گزیبو اور یونٹی دونوں میں LiDAR کو سمولیٹ کرنا
- ڈیپتھ کیمرہ سمیولیشن کے طریقے نافذ کرنا
- IMU سمیولیشن ماڈلز تخلیق کرنا
- گزیبو اور یونٹی کے درمیان سینسر سمیولیشن کے طریقے موازنہ کرنا
- فزکس کی درستگی اور سینسر سمیولیشن میں بصری معیار کے درمیان تنازعات کو سمجھنا
- مخصوص احساس کے کاموں کے لیے مناسب پلیٹ فارم منتخب کرنا

## سینسر سمیولیشن کا جائزہ

### سینسر سمیولیشن کی اہمیت
سینسر سمیولیشن روبوٹکس ترقی کے لیے اہم ہے کیونکہ:
- یہ مہنگے ہارڈ ویئر کے بغیر جانچ کی اجازت دیتا ہے
- یہ دہرانے والے تجربات کو فعال کرتا ہے
- یہ ادراک الگوری دم کے لیے بڑے تربیتی ڈیٹا سیٹ تیار کر سکتا ہے
- یہ حقیقی دنیا کے ڈپلائمنٹ سے پہلے ایک محفوظ بفر فراہم کرتا ہے
- یہ خطرناک یا غیر قابل رسائی ماحول میں جانچ کی اجازت دیتا ہے

### سینسر سمیولیشن کے چیلنجز
موثر سینسر سمیولیشن کو کئی چیلنجوں کا سامنا ہوتا ہے:
- **نويز ماڈلنگ**: حقیقی سینسرز میں ذاتی نويز اور غلطیاں ہوتی ہیں
- **ماحولیاتی اثرات**: موسم، لائٹنگ، اور فضائی حالات سینسرز کو متاثر کرتے ہیں
- **کمپیوٹیشنل خرچ**: اعلیٰ معیار کی سمیولیشن کمپیوٹیشنل طور پر مہنگی ہو سکتی ہے
- **کیلیبریشن**: سمولیٹڈ سینسرز کو حقیقی دنیا کی خصوصیات سے مماثل ہونا چاہیے
- **لیسی**: سمولیٹڈ پروسیسنگ کو حقیقی دنیا کے تاخیر سے مماثل ہونا چاہیے

## LiDAR سمیولیشن

### گزیبو میں LiDAR

#### نفاذ کا طریقہ
گزیبو LiDAR سمیولیشن کے لیے رے کاسٹنگ استعمال کرتا ہے جس میں زبردست کمپیوٹیشنل کارکردگی ہوتی ہے:

```xml
<gazebo reference="lidar_link">
  <sensor name="lidar" type="ray">  <!-- OR "gpu_lidar" for GPU acceleration -->
    <always_on>true</always_on>
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-1.570796</min_angle>  <!-- -π/2 -->
          <max_angle>1.570796</max_angle>   <!-- π/2 -->
        </horizontal>
      </scan>
      <range>
        <min>0.10</min>
        <max>30.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <remapping>~/out:=scan</remapping>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
    </plugin>
  </sensor>
</gazebo>
```

#### گزیبو LiDAR کی خصوصیات
- **رے کاسٹنگ**: جیومیٹرک رے-سطح کا تنازع استعمال کرتا ہے
- **کارکردگی**: حقیقی وقت کی فزکس سمیولیشن کے لیے بہتر بنایا گیا
- **درستگی**: جیومیٹرک خصوصیات کے لیے اچھا، پتلی اشیاء چھوڑ سکتا ہے
- **نويز**: کنفیگریبل گاؤسین نويز پیرامیٹر
- **رینج**: فزکس انجن اور اپ ڈیٹ ریٹس کے مطابق محدود

#### گزیبو LiDAR کنفیگریشن
گزیبو میں LiDAR سمیولیشن کو ٹیون کرنے کے لیے کلیدی پیرامیٹر:
- **نمونے**: بیم کی تعداد (ریزولوشن اور کارکردگی کو متاثر کرتا ہے)
- **ریزولوشن**: نمونوں کے درمیان زاویہ کا ریزولوشن
- **رینج**: کم از کم/زیادہ سے زیادہ قابل شناخت فاصلے
- **اپ ڈیٹ ریٹ**: سینسر کے پڑھنے کی فریکوئنسی
- **نويز**: معیاری انحراف اور بائیس پیرامیٹر

### یونٹی میں LiDAR

#### نفاذ کا طریقہ
یونٹی LiDAR سمیولیشن کے لیے حسب ضرورت رے کاسٹنگ یا مخصوص اثاثے استعمال کرتا ہے:

```csharp
using UnityEngine;
using System.Collections.Generic;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class UnityLidar : MonoBehaviour
{
    public int numRays = 720;
    public float minAngle = -Mathf.PI / 2;
    public float maxAngle = Mathf.PI / 2;
    public float maxDistance = 30.0f;
    public string scanTopic = "/scan";
    public LayerMask detectionLayers = -1;

    private ROSConnection ros;
    private float[] ranges;
    private float[] intensities;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ranges = new float[numRays];
        intensities = new float[numRays];
    }

    void Update()
    {
        PerformLidarScan();
    }

    void PerformLidarScan()
    {
        float angleStep = (maxAngle - minAngle) / (numRays - 1);

        for(int i = 0; i < numRays; i++)
        {
            float angle = minAngle + i * angleStep;
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));
            direction = transform.TransformDirection(direction);

            RaycastHit hit;
            ranges[i] = maxDistance;

            if(Physics.Raycast(transform.position, direction, out hit, maxDistance, detectionLayers))
            {
                ranges[i] = hit.distance;
                intensities[i] = CalculateIntensity(hit.point, hit.normal); // جگہ کا نام
            }
        }

        PublishLidarScan();
    }

    void PublishLidarScan()
    {
        var scanMsg = new LaserScanMsg();
        scanMsg.header.stamp = new TimeStamp(Time.time);
        scanMsg.header.frame_id = "lidar_link";

        scanMsg.angle_min = minAngle;
        scanMsg.angle_max = maxAngle;
        scanMsg.angle_increment = (maxAngle - minAngle) / (numRays - 1);
        scanMsg.time_increment = 0.0f; // کارکردگی کی بنیاد پر حساب لگائیں
        scanMsg.scan_time = 0.1f; // اپ ڈیٹ ریٹ کی بنیاد پر

        scanMsg.range_min = 0.1f;
        scanMsg.range_max = maxDistance;

        // یونٹی ارایز کو ROS پیغام فارمیٹ میں تبدیل کریں
        scanMsg.ranges = new double[ranges.Length];
        for(int i = 0; i < ranges.Length; i++)
        {
            scanMsg.ranges[i] = ranges[i];
        }

        scanMsg.intensities = new double[intensities.Length];
        for(int i = 0; i < intensities.Length; i++)
        {
            scanMsg.intensities[i] = intensities[i];
        }

        ros.Send(scanTopic, scanMsg);
    }

    float CalculateIntensity(Vector3 point, Vector3 normal)
    {
        // مادہ کی خصوصیات، ڈالنے کے زاویہ، وغیرہ کی بنیاد پر شدت کا حساب لگائیں
        return 100.0f; // جگہ کا نام
    }
}
```

#### یونٹی LiDAR کی خصوصیات
- **بصری معیار**: شدت کے حسابات کے لیے حقیقی مادہ کی خصوصیات کو شامل کر سکتا ہے
- **انضمام**: یونٹی کے رینڈرنگ اور لائٹنگ سسٹم تک براہ راست رسائی
- **لچک**: مکمل طور پر حسب ضرورت اسکیننگ الگوری دم
- **کارکردگی**: پیچیدگی کے مطابق کمپیوٹیشنل طور پر چیلنج کر سکتا ہے
- **حقیقت پسندی**: حقیقی دنیا کی بصری شرائط کی شبیہہ دہرانے کے لیے بہتر

#### یونٹی LiDAR کنفیگریشن
یونٹی LiDAR کے لیے کلیدی پیرامیٹر:
- **رے کاؤنٹ**: رے کی تعداد ریزولوشن کا تعین کرتی ہے
- **ڈیٹیکشن لیئرز**: یونٹی کا لیئر سسٹم یہ تعین کرتا ہے کہ کیا شناخت کیا جاتا ہے
- **مادہ کی خصوصیات**: شدت اور عکاسی ماڈلنگ کو متاثر کرتا ہے
- **اپ ڈیٹ ریٹ**: فریم ریٹ پر منحصر، بہتری کی ضرورت ہو سکتی ہے
- **فزکس بمقابلہ رینڈرنگ**: فزکس سسٹم یا رینڈرنگ-مبنی ڈیٹیکشن کے درمیان انتخاب کریں

### LiDAR سمیولیشن کے طریقے موازنہ

| پہلو | گزیبو | یونٹی |
|--------|--------|-------|
| **کارکردگی** | حقیقی وقت کی فزکس کے لیے بہترین | اچھی، لیکن چیلنج کر سکتی ہے |
| **جیومیٹرک درستگی** | زیادہ درست رے-سطح کا تنازع | زیادہ، مزید حسب ضرورت کے ساتھ |
| **بصری معیار** | کم (سادہ جیومیٹرک نمائندگی) | زیادہ (مادہ کی خصوصیات کے ساتھ) |
| **مادہ کی حساسیت** | بنیادی (فاصلہ-مبنی) | اعلیٰ (حقیقی عکاسی کے ساتھ) |
| **فزکس کے ساتھ انضمام** | قدرتی (ODE/Bullet کے ذریعے PhysX) | اچھا (NVIDIA PhysX) |
| **سیٹ اپ کی آسانی** | XML کے ساتھ آسان | اسکرپٹنگ کی ضرورت |

## ڈیپتھ کیمرہ سمیولیشن

### گزیبو میں ڈیپتھ کیمرہ

#### نفاذ
گزیبو کا ڈیپتھ کیمرہ سمیولیشن زیادہ درست ڈیپتھ میپس تیار کرنے کے لیے رینڈرنگ انجن استعمال کرتا ہے:

```xml
<gazebo reference="camera_link">
  <sensor name="depth_camera" type="depth">
    <always_on>true</always_on>
    <update_rate>30</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov> <!-- 60 degrees -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>10.0</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
      <alwaysOn>true</alwaysOn>
      <updateRate>30.0</updateRate>
      <cameraName>camera</cameraName>
      <imageTopicName>rgb/image_raw</imageTopicName>
      <depthImageTopicName>depth/image_raw</depthImageTopicName>
      <pointCloudTopicName>depth/points</pointCloudTopicName>
      <cameraInfoTopicName>rgb/camera_info</cameraInfoTopicName>
      <depthImageCameraInfoTopicName>depth/camera_info</depthImageCameraInfoTopicName>
      <frameName>camera_depth_optical_frame</frameName>
      <baseline>0.1</baseline>
      <distortion_k1>0.0</distortion_k1>
      <distortion_k2>0.0</distortion_k2>
      <distortion_k3>0.0</distortion_k3>
      <distortion_t1>0.0</distortion_t1>
      <distortion_t2>0.0</distortion_t2>
      <pointCloudCutoff>0.5</pointCloudCutoff>
      <pointCloudCutoffMax>3.0</pointCloudCutoffMax>
      <CxPrime>0.0</CxPrime>
      <Cx>320.0</Cx>
      <Cy>240.0</Cy>
      <focalLength>320.0</focalLength>
      <hackBaseline>0.07</hackBaseline>
    </plugin>
  </sensor>
</gazebo>
```

#### گزیبو ڈیپتھ کیمرہ کی خصوصیات
- **GPU تیزی**: موثر ڈیپتھ حسابات کے لیے GPU استعمال کرتا ہے
- **متعدد آؤٹ پٹ**: RGB، ڈیپتھ، پوائنٹ کلاؤڈز ایک ہی سینسر سے
- **کیمرہ ماڈلز**: مختلف پروجیکشن ماڈلز کی حمایت کرتا ہے
- **ڈسٹورشن**: کنفیگریبل انٹرنسک اور ایکسٹرنسک پیرامیٹر
- **کارکردگی**: حقیقی وقت کی ایپلی کیشنز کے لیے بہتر بنایا گیا

### یونٹی میں ڈیپتھ کیمرہ

#### نفاذ
یونٹی شیڈر-مبنی رینڈرنگ کے ذریعے ڈیپتھ کیمرہ سمیولیشن فراہم کرتا ہے:

```csharp
using UnityEngine;
using System.Collections;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class UnityDepthCamera : MonoBehaviour
{
    public Camera depthCam;
    public int width = 640;
    public int height = 480;
    public string rgbTopic = "/camera/rgb/image_raw";
    public string depthTopic = "/camera/depth/image_raw";
    public string infoTopic = "/camera/rgb/camera_info";

    private RenderTexture depthTexture;
    private Texture2D rgbTexture;
    private Texture2D depthTexture2D;
    private ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        InitializeCameras();
    }

    void InitializeCameras()
    {
        // ڈیپتھ کیمرہ سیٹ کریں
        depthCam.aspect = (float)width / height;
        depthCam.orthographic = false;

        // رینڈر ٹیکسچر تخلیق کریں
        depthTexture = new RenderTexture(width, height, 24, RenderTextureFormat.Depth);
        depthCam.targetTexture = depthTexture;

        rgbTexture = new Texture2D(width, height, TextureFormat.RGB24, false);
        depthTexture2D = new Texture2D(width, height, TextureFormat.RFloat, false);
    }

    void Update()
    {
        CaptureAndPublishImages();
    }

    void CaptureAndPublishImages()
    {
        // RGB تصویر کیپچر کریں
        RenderTexture.active = depthCam.targetTexture;
        rgbTexture.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        rgbTexture.Apply();

        // ڈیپتھ معلومات کیپچر کریں
        RenderTexture.active = depthCam.targetTexture;
        depthTexture2D.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        depthTexture2D.Apply();

        // ROS پیغام فارمیٹ میں تبدیل کریں
        var rgbMsg = CreateImageMessage(rgbTexture, rgbTopic);
        var depthMsg = CreateImageMessage(depthTexture2D, depthTopic, "32FC1");

        ros.Send(rgbTopic, rgbMsg);
        ros.Send(depthTopic, depthMsg);
    }

    ImageMsg CreateImageMessage(Texture2D tex, string topic, string encoding = "rgb8")
    {
        var imgMsg = new ImageMsg();
        imgMsg.header.stamp = new TimeStamp(Time.time);
        imgMsg.header.frame_id = transform.name;

        imgMsg.height = (uint)tex.height;
        imgMsg.width = (uint)tex.width;
        imgMsg.encoding = encoding;
        imgMsg.is_bigendian = 0;
        imgMsg.step = (uint)(tex.width * 3); // RGB کے لیے 3 بائٹس فی پکسل

        // ٹیکسچر کو بائٹ ارے میں تبدیل کریں
        byte[] imageData = tex.EncodeToPNG();
        imgMsg.data = System.Array.ConvertAll(imageData, b => (byte)b);

        return imgMsg;
    }
}
```

#### یونٹی ڈیپتھ کیمرہ کی خصوصیات
- **اعلیٰ بصری معیار**: اعلیٰ درجے کی لائٹنگ کے ساتھ فوٹو ریلٹسٹک رینڈرنگ
- **شیڈر-مبنی**: حسب ضرورت ڈیپتھ حساب شیڈر نافذ کر سکتے ہیں
- **لچک آؤٹ پٹ**: رینڈر کردہ ڈیٹا تک براہ راست رسائی
- **مادہ کی خصوصیات**: حقیقی مادہ کے تعامل کی شبیہہ دہرانے کی صلاحیت
- **پوسٹ-پروسیسنگ**: حقیقی سینسرز کی شبیہہ دہرانے کے لیے مختلف بصری اثرات لاگو کر سکتے ہیں

### ڈیپتھ کیمرہ سمیولیشن کا موازنہ

| پہلو | گزیبو | یونٹی |
|--------|--------|-------|
| **بصری معیار** | جیومیٹرک درستگی کے لیے اچھا | زبردست فوٹو ریلٹسٹک معیار |
| **ڈیپتھ درستگی** | زیادہ جیومیٹرک درستگی | زیادہ حسب ضرورت شیڈر کے ساتھ |
| **کارکردگی** | حقیقی وقت کے لیے بہتر بنایا گیا | بصری معیار کی بنیاد پر متغیر |
| **حقیقت پسندی** | جیومیٹری کے لیے اچھا | ادراک کے لیے زیادہ اعلیٰ |
| **انضمام** | براہ راست ROS کے لیے | حسب ضرورت نیٹ ورکنگ کی ضرورت |
| **اوصاف کاری** | XML کنفیگریشن | مکمل اسکرپٹ کنٹرول |

## IMU سمیولیشن

### گزیبو میں IMU

#### نفاذ
گزیبو کا IMU سمیولیشن حقیقی تیزی اور زاویہ کی رفتار کا ڈیٹا فراہم کرتا ہے:

```xml
<gazebo reference="imu_link">
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <topic>imu/data</topic>
    <visualize>true</visualize>
    <imu>
      <angular_velocity>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
            <bias_mean>0.0000075</bias_mean>
            <bias_stddev>0.0000008</bias_stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
            <bias_mean>0.0000075</bias_mean>
            <bias_stddev>0.0000008</bias_stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
            <bias_mean>0.0000075</bias_mean>
            <bias_stddev>0.0000008</bias_stddev>
          </noise>
        </z>
      </angular_velocity>
      <linear_acceleration>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
            <bias_mean>0.0</bias_mean>
            <bias_stddev>0.0</bias_stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
            <bias_mean>0.0</bias_mean>
            <bias_stddev>0.0</bias_stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
            <bias_mean>0.0</bias_mean>
            <bias_stddev>0.0</bias_stddev>
          </noise>
        </z>
      </linear_acceleration>
    </imu>
    <plugin name="imu_plugin" filename="libgazebo_ros_imu_sensor.so">
      <ros>
        <remapping>~/out:=imu/data</remapping>
      </ros>
      <update_rate>100</update_rate>
      <topic_name>imu/data</topic_name>
      <body_name>imu_link</body_name>
      <acceleration_scale>1</acceleration_scale>
      <orientation_scale>1</orientation_scale>
      <velocity_scale>1</velocity_scale>
    </plugin>
  </sensor>
</gazebo>
```

#### گزیبو IMU کی خصوصیات
- **فزکس انضمام**: گزیبو کے فزکس انجن کا براہ راست استعمال
- **نويز ماڈلز**: بائیسز کے ساتھ پیچیدہ نويز ماڈلنگ
- **متعدد آؤٹ پٹ**: جہت، زاویہ کی رفتار، اور لکیری تیزی
- **کیلیبریشن**: کیلیبریشن کی غلطیوں اور ڈرائیف کی شبیہہ دہراتا ہے
- **درستگی**: فزکس-مبنی پیمائش کے لیے زیادہ درستگی

### یونٹی میں IMU

#### نفاذ
یونٹی فزکس انجن کو نويز ماڈلز کے ساتھ جوڑ کر IMU ڈیٹا کی شبیہہ دہراتا ہے:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class UnityIMU : MonoBehaviour
{
    public string topicName = "/imu/data";
    public Vector3 noiseLinearAccMean = new Vector3(0.01f, 0.01f, 0.01f);
    public Vector3 noiseLinearAccStdDev = new Vector3(0.02f, 0.02f, 0.02f);
    public Vector3 noiseAngVelMean = new Vector3(0.001f, 0.001f, 0.001f);
    public Vector3 noiseAngVelStdDev = new Vector3(0.001f, 0.001f, 0.001f);

    private ROSConnection ros;
    private Rigidbody rb;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {
        PublishIMUData();
    }

    void PublishIMUData()
    {
        var imuMsg = new ImuMsg();
        imuMsg.header.stamp = new TimeStamp(Time.time);
        imuMsg.header.frame_id = transform.name;

        // رگیڈ بائڈی سے زاویہ کی رفتار حاصل کریں
        Vector3 angularVel = rb.angularVelocity;
        imuMsg.angular_velocity.x = AddNoise(angularVel.x, noiseAngVelMean.x, noiseAngVelStdDev.x);
        imuMsg.angular_velocity.y = AddNoise(angularVel.y, noiseAngVelMean.y, noiseAngVelStdDev.y);
        imuMsg.angular_velocity.z = AddNoise(angularVel.z, noiseAngVelMean.z, noiseAngVelStdDev.z);

        // کوویریئنس میٹرکس تخلیق کریں (سادہ)
        for(int i = 0; i < 9; i++)
        {
            if(i % 4 == 0) // قطری عناصر
                imuMsg.angular_velocity_covariance[i] = noiseAngVelStdDev.magnitude * noiseAngVelStdDev.magnitude;
            else
                imuMsg.angular_velocity_covariance[i] = 0.0;
        }

        // لکیری تیزی حاصل کریں (گریویٹی ہٹائیں)
        Vector3 worldLinearAcceleration = (rb.velocity - rb.GetPointVelocity(transform.position)) / Time.fixedDeltaTime;
        Vector3 localLinearAcceleration = transform.InverseTransformDirection(worldLinearAcceleration);

        imuMsg.linear_acceleration.x = AddNoise(localLinearAcceleration.x, noiseLinearAccMean.x, noiseLinearAccStdDev.x);
        imuMsg.linear_acceleration.y = AddNoise(localLinearAcceleration.y, noiseLinearAccMean.y, noiseLinearAccStdDev.y);
        // گریویٹی کمپنیشن شامل کریں - یہ تقریبی ہے
        imuMsg.linear_acceleration.z = AddNoise(localLinearAcceleration.z + 9.81f, noiseLinearAccMean.z, noiseLinearAccStdDev.z);

        for(int i = 0; i < 9; i++)
        {
            if(i % 4 == 0) // قطری عناصر
                imuMsg.linear_acceleration_covariance[i] = noiseLinearAccStdDev.magnitude * noiseLinearAccStdDev.magnitude;
            else
                imuMsg.linear_acceleration_covariance[i] = 0.0;
        }

        // سادگی کے لیے، ہم فزکس سے جہت کا حساب نہیں لگائیں گے
        // عمل میں، آپ زاویہ کی رفتار کو ضم کریں گے یا یونٹی کی جہت استعمال کریں گے
        imuMsg.orientation.w = transform.rotation.w;
        imuMsg.orientation.x = transform.rotation.x;
        imuMsg.orientation.y = transform.rotation.y;
        imuMsg.orientation.z = transform.rotation.z;

        for(int i = 0; i < 9; i++)
        {
            if(i % 4 == 0) // قطری عناصر
                imuMsg.orientation_covariance[i] = 0.01;  // جگہ کا نام
            else
                imuMsg.orientation_covariance[i] = 0.0;
        }

        ros.Send(topicName, imuMsg);
    }

    float AddNoise(float value, float mean, float stddev)
    {
        // گاؤسین نويز کے لیے باکس-میلر ٹرانسفارمیشن
        float u1 = Random.value;
        float u2 = Random.value;
        float normal = Mathf.Sqrt(-2.0f * Mathf.Log(u1)) * Mathf.Cos(2.0f * Mathf.PI * u2);
        return value + mean + normal * stddev;
    }
}
```

#### یونٹی IMU کی خصوصیات
- **مکمل کنٹرول**: نويز اور غلطی کے ماڈلز کی مکمل اوصاف کاری
- **انضمام کی لچک**: دیگر یونٹی سسٹم کے ساتھ آسان انضمام
- **بصری فیڈ بیک**: 3D میں براہ راست IMU ڈیٹا کی ویژولائز کر سکتے ہیں
- **اوصاف کاری**: مخصوص ہارڈ ویئر کے لیے سینسر کی خصوصیات کو ٹیلر کریں
- **کارکردگی**: درکار درستگی کی بنیاد پر ٹیون کی جا سکتی ہے

### IMU سمیولیشن کا موازنہ

| پہلو | گزیبو | یونٹی |
|--------|--------|-------|
| **فزکس انضمام** | قدرتی اور درست | اچھا رگیڈ بائڈی رسائی کے ساتھ |
| **نويز ماڈلنگ** | پیچیدہ، بائیس پیرامیٹر کے ساتھ | مکمل کنٹرول کے ساتھ قابل اوصاف کاری |
| **کارکردگی** | سمیولیشن کے لیے بہتر بنایا گیا | معتدل، پیچیدگی پر منحصر ہے |
| **کنفیگریشن کی آسانی** | XML-مبنی، آسان | اسکرپٹ-مبنی، کوڈنگ کی ضرورت |
| **درستگی** | فزکس-مبنی سمیولیشن کے لیے زیادہ | زیادہ، مناسب نفاذ کے ساتھ |
| **لچک** | معتدل (XML سے محدود) | زیادہ سے زیادہ (مکمل اسکرپٹ کنٹرول) |

## دیگر اہم سینسرز

### GPS سمیولیشن

**گزیبو نفاذ:**
```xml
<gazebo reference="gps_link">
  <sensor name="navsat" type="gps">
    <always_on>true</always_on>
    <update_rate>1</update_rate>
    <topic>gps/fix</topic>
    <gps>
      <position_sensing>
        <horizontal>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.5</stddev>
          </noise>
        </horizontal>
        <vertical>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2.5</stddev>
          </noise>
        </vertical>
      </position_sensing>
    </gps>
  </sensor>
</gazebo>
```

**یونٹی نفاذ:**
```csharp
// یونٹی GPS کو حسب ضرورت نفاذ کی ضرورت ہوگی جو GPS کوآرڈینیٹس کا حساب لگائے گا
// دنیا کی پوزیشن کی بنیاد پر اور مناسب نويز ماڈلز شامل کرے گا
```

### فورس/ٹورک سینسرز

**گزیبو میں**، فورس/ٹورک سینسرز جوڑ یا کولیژن سینسرز کے حصے کے طور پر سمولیٹ کیے جاتے ہیں:
```xml
<gazebo reference="wrist_ft_sensor">
  <sensor name="wrist_force_torque" type="force_torque">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <force_torque>
      <frame>sensor</frame>
      <measure_direction>child_to_parent</measure_direction>
    </force_torque>
  </sensor>
</gazebo>
```

## کارکردگی کے مسائل اور بہتری

### گزیبو کی بہتری
- **اپ ڈیٹ ریٹس**: مناسب اپ ڈیٹ ریٹس کا استعمال کر کے کارکردگی کے ساتھ درستگی کا توازن قائم کریں
- **رے کاؤنٹس**: اگر کارکردگی اہم ہو تو LiDAR ریز کی تعداد کم کریں
- **سادگی**: ممکن ہو تو سینسرز کے لیے سادہ ماڈلز استعمال کریں
- **تھریڈنگ**: گزیبو کی ملٹی-تھریڈ کی صلاحیتوں کا استعمال کریں

### یونٹی کی بہتری
- **رینڈر کی معیار**: سینسر کی ضروریات کی بنیاد پر معیار کی ترتیبات ایڈجسٹ کریں
- **LODs**: پیچیدہ ماحول کے لیے لیول آف ڈیٹیل استعمال کریں
- **کلینگ**: دور کی اشیاء کے لیے اوکلیوژن کلینگ نافذ کریں
- **بیکنگ**: سٹیٹک لائٹنگ اور ماحول کو پہلے سے بیک کریں

### کراس-پلیٹ فارم کے مسائل
- **کیلیبریشن**: یقین کریں کہ سینسر پیرامیٹر پلیٹ فارم کے درمیان مماثل ہیں
- **کوآرڈینیٹ سسٹم**: فریم کنونشنز کے فرق کو مدنظر رکھیں
- **ٹائمنگ**: سینسر پروسیسنگ کے تاخیر کو مناسب طریقے سے سمولیٹ کریں
- **ڈیٹا فارمیٹس**: ROS انضمام کے لیے مسلسل پیغام فارمیٹس استعمال کریں

## درستگی کی توثیق اور کیلیبریشن

### سمیولیشن بمقابلہ حقیقی دنیا کی توثیق
موثر سینسر سمیولیشن کے لیے، آپ کو چاہیے:
- کنٹرول شدہ حالات میں حقیقی سینسرز سے ڈیٹا کیپچر کریں
- سمیولیشن آؤٹ پٹ کو حقیقی دنیا کے ڈیٹا کے ساتھ موازنہ کریں
- حقیقی سینسر کی خصوصیات سے مماثل نويز ماڈلز کیلیبریٹ کریں
- مختلف ماحولیاتی حالات میں توثیق کریں

### مصنوعی ڈیٹا کی توثیق
ادراک سسٹم کی تربیت کے لیے سمیولیشن استعمال کرتے وقت:
- یقین کریں کہ مصنوعی ڈیٹا حقیقی دنیا کے تقسیم کو کور کرتا ہے
- تربیت یافتہ ماڈلز کو حقیقی ڈیٹا پر ٹیسٹ کر کے ڈومین گیپ کا جائزہ لیں
- جنرلائزیشن کو بہتر بنانے کے لیے ڈومین رینڈمائزیشن کی تکنیکوں کا استعمال کریں
- دونوں سمولیٹڈ اور حقیقی ماحول میں کارکردگی کے میٹرکس کی توثیق کریں

## صحیح پلیٹ فارم کا انتخاب

### گزیبو کب استعمال کریں
گزیبو کا انتخاب کریں جب:
- فزکس کی درستگی اہم ہو
- حقیقی وقت کی کارکردگی اہم ہو
- ROS نیویگیشن اسٹیک کے ساتھ انضمام کی ضرورت ہو
- سینسر سمیولیشن کو حقیقی فزکس کے قریب ہونا چاہیے
- پیچیدہ ڈائنامکس والے چکر والے یا پاؤں والے روبوٹس کے ساتھ کام کر رہے ہوں

### یونٹی کب استعمال کریں
یونٹی کا انتخاب کریں جب:
- اعلیٰ بصری معیار کی ضرورت ہو
- انسان-روبوٹ انٹرایکشن اہم ہو
- فوٹو ریلٹسٹک سینسر سمیولیشن کی ضرورت ہو
- VR/AR ایپلی کیشنز منصوبہ بند کی گئی ہوں
- وژن-مبنی AI کے لیے مصنوعی ڈیٹا جنریشن ہدف ہو

### ہائبرڈ طریقے
پیچیدہ ہیومنائڈ روبوٹکس ایپلی کیشنز کے لیے، غور کریں:
- فزکس اور بنیادی سینسر سمیولیشن کے لیے گزیبو استعمال کرنا
- اعلیٰ معیار کی وژن اور انسانی انٹرایکشن کے لیے یونٹی استعمال کرنا
- ROS برجز کا استعمال کر کے دونوں پلیٹ فارم جوڑنا
- حسب ضرورت سینسر فیوژن حل تیار کرنا

## سینسر سمیولیشن کا ڈیبگ کرنا

### عام مسائل اور حل

1. **LiDAR اشیاء چھوڑ رہا ہے**:
   - گزیبو: میش ریزولوشن چیک کریں اور `<resolution>1</resolution>` استعمال کر کے رے کثافت بڑھائیں
   - یونٹی: لیئر ماسکس اور کولیژن ڈیٹیکشن ترتیبات کی تصدیق کریں

2. **ڈیپتھ کیمرہ آرٹیفیکٹس**:
   - گزیبو: قریب/دور کلپ پلینز اور رینڈرنگ کی ترتیبات ایڈجسٹ کریں
   - یونٹی: شیڈر پیرامیٹر اور کیمرہ کی ترتیبات کو فائن ٹیون کریں

3. **IMU ڈرائیف**:
   - دونوں پلیٹ فارم: یقین کریں کہ نويز پیرامیٹر حقیقی سینسرز سے مماثل ہیں
   - یونٹی نفاذ میں گریویٹی کمپنیشن چیک کریں

4. **کارکردگی کے مسائل**:
   - جہاں ممکن ہو سینسر اپ ڈیٹ ریٹس کم کریں
   - سینسر رے کاسٹنگ کے لیے میش پیچیدگی کو بہتر بنائیں
   - مناسب معیار کی ترتیبات استعمال کریں

### ڈیبگنگ کی تکنیکیں
- سینسر FOV اور ڈیٹیکشن رینج کو ویژولائز کریں
- توثیق کے لیے زمینی حقیقت کے ساتھ سینسر ڈیٹا لاگ کریں
- سینسر سٹریمز کا تجزیہ کرنے کے لیے ROS ٹولز جیسے `rqt_plot` استعمال کریں
- کوآرڈینیٹ فریم ٹرانسفارم کی توثیق کریں

## خلاصہ

سینسر سمیولیشن مؤثر روبوٹکس ترقی کا ایک اہم جزو ہے، جو ادراک سسٹم کی محفوظ، دہرانے والی، اور قیمت مؤثر جانچ کی اجازت دیتا ہے۔ گزیبو کمپیوٹیشنل کارکردگی کے ساتھ فزکس-مبنی سینسر سمیولیشن میں مہارت رکھتا ہے، جبکہ یونٹی زبردست بصری معیار اور اوصاف کاری کے اختیارات فراہم کرتا ہے۔

پلیٹ فارم کے درمیان (یا دونوں استعمال کرنے) کا انتخاب آپ کی مخصوص ایپلی کیشن کی ضروریات پر منحصر ہے، بشمول فزکس کی درستگی کے مقابلے میں بصری معیار کی اہمیت، کارکردگی کی ضروریات، اور منصوبہ بند استعمال کے کیسز۔

ہر پلیٹ فارم کی مضبوطیوں اور تنازعات کو سمجھنا بہتر سمیولیشن ڈیزائن کو فعال کرتا ہے اور بالآخر زیادہ مؤثر روبوٹکس ترقی کرتا ہے۔

## اگلے اقدامات

اگلے سیکشن میں، ہم ماڈیول 2 کا خلاصہ پیش کریں گے اور اپنے ہیومنائڈ روبوٹکس پروجیکٹس میں یہ سمیولیشن تصورات لاگو کرنے کے لیے ہدایت فراہم کریں گے۔