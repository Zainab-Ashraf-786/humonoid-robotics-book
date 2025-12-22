---
title: Sensor Simulation Across Platforms
sidebar_label: Sensor Simulation
---

# Sensor Simulation Across Platforms

Robotic perception relies heavily on sensor data to understand and interact with the environment. This section compares sensor simulation capabilities across Gazebo and Unity, covering LiDAR, depth cameras, IMUs, and other sensors. Understanding the strengths and weaknesses of each platform is crucial for selecting appropriate simulation tools for your robotics applications.

## Learning Objectives

After completing this section, you will:
- Understand how to simulate LiDAR in both Gazebo and Unity
- Know how to implement depth camera simulation approaches
- Be able to create IMU simulation models
- Compare sensor simulation approaches between Gazebo and Unity
- Understand the trade-offs between physics accuracy and visual fidelity in sensor simulation
- Select the appropriate platform for specific sensing tasks

## Overview of Sensor Simulation

### The Importance of Sensor Simulation
Accurate sensor simulation is crucial for robotics development because:
- It allows testing without expensive hardware
- It enables repeatable experimentation
- It can generate large training datasets for perception algorithms
- It provides a safety buffer before real-world deployment
- It allows testing in dangerous or inaccessible environments

### Sensor Simulation Challenges
Effective sensor simulation faces several challenges:
- **Noise Modeling**: Real sensors have inherent noise and inaccuracies
- **Environmental Effects**: Weather, lighting, and atmospheric conditions affect sensors
- **Computational Cost**: High-fidelity simulation can be computationally expensive
- **Calibration**: Simulated sensors must match real-world characteristics
- **Latency**: Simulated processing should match real-world delays

## LiDAR Simulation

### LiDAR in Gazebo

#### Implementation Approach
Gazebo uses raycasting for LiDAR simulation with high computational efficiency:

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

#### Gazebo LiDAR Characteristics
- **Raycasting**: Uses geometric ray-surface intersection
- **Performance**: Optimized for real-time physics simulation
- **Accuracy**: Good for geometric features, may miss thin objects
- **Noise**: Configurable Gaussian noise parameters
- **Range**: Limited by physics engine and update rates

#### Gazebo LiDAR Configuration
Key parameters for tuning LiDAR simulation in Gazebo:
- **Samples**: Number of beams (affects resolution and performance)
- **Resolution**: Angular resolution between samples
- **Range**: Min/max detectable distances
- **Update Rate**: Frequency of sensor readings
- **Noise**: Standard deviation and bias parameters

### LiDAR in Unity

#### Implementation Approach
Unity uses custom raycasting or specialized assets for LiDAR simulation:

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
                intensities[i] = CalculateIntensity(hit.point, hit.normal); // Placeholder
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
        scanMsg.time_increment = 0.0f; // Calculate based on performance
        scanMsg.scan_time = 0.1f; // Based on update rate
        
        scanMsg.range_min = 0.1f;
        scanMsg.range_max = maxDistance;
        
        // Convert Unity arrays to ROS message format
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
        // Calculate intensity based on material properties, angle of incidence, etc.
        return 100.0f; // Placeholder
    }
}
```

#### Unity LiDAR Characteristics
- **Visual Fidelity**: Can incorporate realistic material properties for intensity calculations
- **Integration**: Direct access to Unity's rendering and lighting systems
- **Flexibility**: Fully customizable scanning algorithms
- **Performance**: Can be computationally demanding depending on complexity
- **Realism**: Better for simulating real-world visual conditions

#### Unity LiDAR Configuration
Key parameters for Unity LiDAR:
- **Ray Count**: Number of rays cast determines resolution
- **Detection Layers**: Unity's layer system determines what's detected
- **Material Properties**: Affects intensity and reflection modeling
- **Update Rate**: Frame rate dependent, may need optimization
- **Physics vs Rendering**: Choose between physics system or rendering-based detection

### Comparing LiDAR Simulation Approaches

| Aspect | Gazebo | Unity |
|--------|--------|-------|
| **Performance** | Excellent for real-time physics | Good, but can be demanding |
| **Geometric Accuracy** | High precision ray-surface intersection | High, with more customization |
| **Visual Fidelity** | Low (simple geometric representation) | High (with material properties) |
| **Material Sensitivity** | Basic (distance-based) | Advanced (with realistic reflections) |
| **Integration with Physics** | Native (PhysX via ODE/Bullet) | Good (NVIDIA PhysX) |
| **Ease of Setup** | Straightforward with XML | Requires scripting |

## Depth Camera Simulation

### Depth Camera in Gazebo

#### Implementation
Gazebo's depth camera simulation uses the rendering engine to generate accurate depth maps:

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

#### Gazebo Depth Camera Features
- **GPU Acceleration**: Uses GPU for efficient depth calculations
- **Multiple Outputs**: RGB, depth, point clouds from single sensor
- **Camera Models**: Supports various projection models
- **Distortion**: Configurable intrinsic and extrinsic parameters
- **Performance**: Optimized for real-time applications

### Depth Camera in Unity

#### Implementation
Unity provides depth camera simulation through shader-based rendering:

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
        // Set up depth camera
        depthCam.aspect = (float)width / height;
        depthCam.orthographic = false;
        
        // Create render textures
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
        // Capture RGB image
        RenderTexture.active = depthCam.targetTexture;
        rgbTexture.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        rgbTexture.Apply();
        
        // Capture depth information
        RenderTexture.active = depthCam.targetTexture;
        depthTexture2D.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        depthTexture2D.Apply();
        
        // Convert to ROS message format
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
        imgMsg.step = (uint)(tex.width * 3); // 3 bytes per pixel for RGB
        
        // Convert texture to byte array
        byte[] imageData = tex.EncodeToPNG();
        imgMsg.data = System.Array.ConvertAll(imageData, b => (byte)b);
        
        return imgMsg;
    }
}
```

#### Unity Depth Camera Features
- **High Visual Fidelity**: Photorealistic rendering with advanced lighting
- **Shader-Based**: Can implement custom depth calculation shaders
- **Flexible Output**: Direct access to rendered data
- **Material Properties**: Realistic material interaction simulation
- **Post-Processing**: Can apply various visual effects to simulate real sensors

### Comparing Depth Camera Simulation

| Aspect | Gazebo | Unity |
|--------|--------|-------|
| **Visual Quality** | Good geometric accuracy | Excellent photorealistic quality |
| **Depth Accuracy** | High geometric precision | High with custom shaders |
| **Performance** | Optimized for real-time | Variable based on visual quality |
| **Realism** | Good for geometry | Superior for realistic perception |
| **Integration** | Direct to ROS | Requires custom networking |
| **Customization** | XML configuration | Complete script control |

## IMU Simulation

### IMU in Gazebo

#### Implementation
Gazebo's IMU simulation provides realistic acceleration and angular velocity data:

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

#### Gazebo IMU Features
- **Physics Integration**: Directly uses Gazebo's physics engine
- **Noise Models**: Sophisticated noise modeling with biases
- **Multiple Outputs**: Orientation, angular velocity, and linear acceleration
- **Calibration**: Simulates calibration errors and drift
- **Accuracy**: High accuracy for physics-based measurements

### IMU in Unity

#### Implementation
Unity simulates IMU data using the physics engine combined with noise models:

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
        
        // Get angular velocity from rigidbody
        Vector3 angularVel = rb.angularVelocity;
        imuMsg.angular_velocity.x = AddNoise(angularVel.x, noiseAngVelMean.x, noiseAngVelStdDev.x);
        imuMsg.angular_velocity.y = AddNoise(angularVel.y, noiseAngVelMean.y, noiseAngVelStdDev.y);
        imuMsg.angular_velocity.z = AddNoise(angularVel.z, noiseAngVelMean.z, noiseAngVelStdDev.z);
        
        // Create covariance matrices (simplified)
        for(int i = 0; i < 9; i++)
        {
            if(i % 4 == 0) // diagonal elements
                imuMsg.angular_velocity_covariance[i] = noiseAngVelStdDev.magnitude * noiseAngVelStdDev.magnitude;
            else
                imuMsg.angular_velocity_covariance[i] = 0.0;
        }
        
        // Get linear acceleration (remove gravity)
        Vector3 worldLinearAcceleration = (rb.velocity - rb.GetPointVelocity(transform.position)) / Time.fixedDeltaTime;
        Vector3 localLinearAcceleration = transform.InverseTransformDirection(worldLinearAcceleration);
        
        imuMsg.linear_acceleration.x = AddNoise(localLinearAcceleration.x, noiseLinearAccMean.x, noiseLinearAccStdDev.x);
        imuMsg.linear_acceleration.y = AddNoise(localLinearAcceleration.y, noiseLinearAccMean.y, noiseLinearAccStdDev.y);
        // Add gravity compensation - this is approximate
        imuMsg.linear_acceleration.z = AddNoise(localLinearAcceleration.z + 9.81f, noiseLinearAccMean.z, noiseLinearAccStdDev.z);
        
        for(int i = 0; i < 9; i++)
        {
            if(i % 4 == 0) // diagonal elements
                imuMsg.linear_acceleration_covariance[i] = noiseLinearAccStdDev.magnitude * noiseLinearAccStdDev.magnitude;
            else
                imuMsg.linear_acceleration_covariance[i] = 0.0;
        }
        
        // For simplicity, we won't calculate orientation from physics
        // In practice, you'd integrate angular velocity or use Unity's orientation
        imuMsg.orientation.w = transform.rotation.w;
        imuMsg.orientation.x = transform.rotation.x;
        imuMsg.orientation.y = transform.rotation.y;
        imuMsg.orientation.z = transform.rotation.z;
        
        for(int i = 0; i < 9; i++)
        {
            if(i % 4 == 0) // diagonal elements
                imuMsg.orientation_covariance[i] = 0.01;  // Placeholder
            else
                imuMsg.orientation_covariance[i] = 0.0;
        }
        
        ros.Send(topicName, imuMsg);
    }
    
    float AddNoise(float value, float mean, float stddev)
    {
        // Box-Muller transformation for Gaussian noise
        float u1 = Random.value;
        float u2 = Random.value;
        float normal = Mathf.Sqrt(-2.0f * Mathf.Log(u1)) * Mathf.Cos(2.0f * Mathf.PI * u2);
        return value + mean + normal * stddev;
    }
}
```

#### Unity IMU Features
- **Complete Control**: Full customization of noise and error models
- **Integration Flexibility**: Easy integration with other Unity systems
- **Visual Feedback**: Can visualize IMU data directly in 3D
- **Customization**: Tailor sensor characteristics to specific hardware
- **Performance**: Can be tuned based on required accuracy

### Comparing IMU Simulation

| Aspect | Gazebo | Unity |
|--------|--------|-------|
| **Physics Integration** | Native and accurate | Good with Rigidbody access |
| **Noise Modeling** | Sophisticated, with bias parameters | Customizable with full control |
| **Performance** | Optimized for simulation | Moderate, depends on complexity |
| **Ease of Configuration** | XML-based, straightforward | Script-based, requires coding |
| **Accuracy** | High for physics-based simulation | High, with proper implementation |
| **Flexibility** | Moderate (limited by XML) | Maximum (complete script control) |

## Other Important Sensors

### GPS Simulation

**Gazebo Implementation:**
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

**Unity Implementation:**
```csharp
// Unity GPS would require custom implementation that calculates GPS coordinates
// based on world position and adds appropriate noise models
```

### Force/Torque Sensors

**In Gazebo**, force/torque sensors are simulated as part of joint or contact sensors:
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

## Performance Considerations and Optimization

### Gazebo Optimizations
- **Update Rates**: Balance accuracy with performance using appropriate update rates
- **Ray Counts**: Reduce number of LiDAR rays if performance is critical
- **Simplification**: Use simplified models for sensors when possible
- **Threading**: Use Gazebo's multi-threaded capabilities

### Unity Optimizations
- **Render Quality**: Adjust quality settings based on sensor requirements
- **LODs**: Use Level of Detail for complex environments
- **Culling**: Implement occlusion culling for distant objects
- **Baking**: Pre-bake static lighting and environments

### Cross-Platform Considerations
- **Calibration**: Ensure sensor parameters match between platforms
- **Coordinate Systems**: Account for differences in frame conventions
- **Timing**: Simulate sensor processing delays appropriately
- **Data Formats**: Use consistent message formats for ROS integration

## Accuracy Validation and Calibration

### Simulation vs Real-World Validation
For effective sensor simulation, you should:
- Capture data from real sensors in controlled conditions
- Compare simulation outputs to real-world data
- Calibrate noise models to match real sensor characteristics
- Validate across different environmental conditions

### Synthetic Data Validation
When using simulation for training perception systems:
- Verify that synthetic data covers real-world distributions
- Test trained models on real data to assess domain gap
- Use domain randomization techniques to improve generalization
- Validate performance metrics in both simulated and real environments

## Selecting the Right Platform

### When to Use Gazebo
Choose Gazebo when:
- Physics accuracy is paramount
- Real-time performance is critical
- Integration with ROS navigation stack is required
- Sensor simulation needs to be close to real physics
- Working with wheeled or legged robots with complex dynamics

### When to Use Unity
Choose Unity when:
- High visual fidelity is required
- Human-robot interaction is important
- Photorealistic sensor simulation is needed
- VR/AR applications are planned
- Synthetic data generation for vision-based AI is the goal

### Hybrid Approaches
For complex humanoid robotics applications, consider:
- Using Gazebo for physics and basic sensor simulation
- Using Unity for high-fidelity vision and human interaction
- Connecting both platforms using ROS bridges
- Developing custom sensor fusion solutions

## Troubleshooting Sensor Simulation

### Common Issues and Solutions

1. **LiDAR Missing Objects**:
   - Gazebo: Check mesh resolution and use `<resolution>1</resolution>` to increase ray density
   - Unity: Verify layer masks and collision detection settings

2. **Depth Camera Artifacts**:
   - Gazebo: Adjust near/far clip planes and rendering settings
   - Unity: Fine-tune shader parameters and camera settings

3. **IMU Drift**:
   - Both platforms: Verify noise parameters match real sensors
   - Check gravity compensation in Unity implementations

4. **Performance Issues**:
   - Reduce sensor update rates where possible
   - Optimize mesh complexity for sensor raycasting
   - Use appropriate quality settings

### Debugging Techniques
- Visualize sensor FOV and detection ranges
- Log sensor data alongside ground truth for validation
- Use ROS tools like `rqt_plot` to analyze sensor streams
- Validate coordinate frame transforms

## Summary

Sensor simulation is a critical component of effective robotics development, allowing for safe, repeatable, and cost-effective testing of perception systems. Gazebo excels at physics-based sensor simulation with high computational efficiency, while Unity provides superior visual fidelity and customization options.

The choice between platforms (or using both) depends on your specific application requirements, including the importance of physics accuracy versus visual fidelity, performance requirements, and intended use cases.

Understanding the strengths and trade-offs of each platform enables better simulation design and ultimately more effective robotics development.

## Next Steps

In the next section, we'll summarize Module 2 and provide guidance for applying these simulation concepts to your humanoid robotics projects.