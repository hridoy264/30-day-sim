# Day 20 — Sensors in Gazebo: LiDAR, Camera & IMU

## 🎯 Today's Goal
Give your mobile robot perception: add a **LiDAR**, a **camera**, and an **IMU**, then read their data on ROS 2 topics. These three sensors power most real-world robot navigation.

---

## Overview

Your robot can drive (Day 19) but it's blind. Today we add the perception trio that nearly every autonomous robot carries. In Gazebo, sensors are added as `<sensor>` tags on a link, activated by a system plugin, and their data is published to topics you bridge into ROS 2 — the same data a real robot's sensors would produce.

---

## The Pattern: Sensor Tag + Plugin + Bridge

Every Gazebo sensor follows three steps:

1. **Declare** a `<sensor>` on a robot link in SDF.
2. **Enable** the matching Gazebo **system plugin** in the world (e.g., the Sensors system).
3. **Bridge** its topic into ROS 2 so your code can read it.

---

## Sensor 1 — LiDAR (laser scanner)

LiDAR sweeps laser beams to measure distances all around — the backbone of obstacle avoidance and mapping. Add to your robot's base link:

```xml
<sensor name="lidar" type="gpu_lidar">
  <topic>scan</topic>
  <update_rate>10</update_rate>
  <lidar>
    <scan><horizontal>
      <samples>360</samples>          <!-- 360 beams = 1 per degree -->
      <min_angle>-3.14159</min_angle>
      <max_angle>3.14159</max_angle>
    </horizontal></scan>
    <range><min>0.1</min><max>10.0</max></range>
  </lidar>
</sensor>
```

This is exactly the Day-9 ray-fan idea, now as a proper sensor. It publishes a `LaserScan` message of 360 distances.

---

## Sensor 2 — Camera

A camera gives the robot vision — for detection, line following, or just monitoring:

```xml
<sensor name="camera" type="camera">
  <topic>camera</topic>
  <update_rate>30</update_rate>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>   <!-- ~60 degrees -->
    <image><width>640</width><height>480</height></image>
    <clip><near>0.1</near><far>100</far></clip>
  </camera>
</sensor>
```

It publishes `Image` messages — view them live in RViz tomorrow.

---

## Sensor 3 — IMU (inertial measurement unit)

An IMU reports orientation, angular velocity, and linear acceleration — how the robot is tilting and accelerating. Essential for balancing and for fusing with odometry:

```xml
<sensor name="imu" type="imu">
  <topic>imu</topic>
  <update_rate>100</update_rate>
</sensor>
```

It publishes `Imu` messages. This is the simulated version of the accelerometer/gyro from Day 14.

---

## Enabling the Sensors System

Sensors only produce data if the world loads the Sensors system plugin. Add to your world's `<world>`:

```xml
<plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
  <render_engine>ogre2</render_engine>
</plugin>
<plugin filename="gz-sim-imu-system" name="gz::sim::systems::Imu"/>
```

> ⚠️ **Common gotcha:** a sensor declared but producing no data usually means the **Sensors system plugin is missing** from the world. Always check this first.

---

## Bridging Sensor Data to ROS 2

Bridge each topic with its message type (Day 18 pattern):

```bash
ros2 run ros_gz_bridge parameter_bridge \
  /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan \
  /imu@sensor_msgs/msg/Imu@gz.msgs.IMU
```

Then verify:

```bash
ros2 topic echo /scan      # see 360 distance values
ros2 topic echo /imu       # see orientation & acceleration
```

When real sensor messages stream into ROS 2 from your simulated robot, you have a fully perceiving robot.

---

## 📝 Today's Task

1. Add a **LiDAR**, **camera**, and **IMU** to your Day-19 robot's SDF.
2. Add the **Sensors** and **IMU** system plugins to your world.
3. Bridge `/scan` and `/imu` into ROS 2.
4. `ros2 topic echo /scan` and drive the robot toward an obstacle — watch the front distances shrink.
5. `ros2 topic echo /imu` while turning — watch the angular velocity change.

---

## ✅ Key Takeaways

✓ Every Gazebo sensor = **`<sensor>` tag** + **system plugin** in the world + **bridge** to ROS 2.

✓ **LiDAR** publishes `LaserScan` (distances all around) — the basis of obstacle avoidance & mapping.

✓ **Camera** publishes `Image` (robot vision); **IMU** publishes orientation/acceleration.

✓ No sensor data? The **Sensors system plugin is probably missing** from the world.

✓ Bridged sensor topics give your sim robot the same perception streams as real hardware.

---

## 📚 References & Resources

- [Gazebo: Sensors tutorial](https://gazebosim.org/docs/harmonic/sensors/)
- [sensor_msgs/LaserScan](https://docs.ros.org/en/api/sensor_msgs/html/msg/LaserScan.html)
- [Gazebo sensors SDF reference](http://sdformat.org/spec?ver=1.9&elem=sensor)

---

## 🔭 What's Next?

**Day 21 — Teleop & Visualizing in RViz.** We'll drive the robot with your keyboard and use RViz, ROS 2's powerful visualization tool, to *see* the LiDAR scans and camera feed in real time.

---

*"A robot's intelligence is only as good as its senses. Now yours can see, scan, and feel."*
