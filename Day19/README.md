# Day 19 — A Differential-Drive Mobile Robot

## 🎯 Today's Goal
Build a two-wheeled (differential-drive) robot in SDF, add the drive plugin, and make it roll around your world using `/cmd_vel` commands from ROS 2.

---

## Overview

Time to build a robot that *moves*. A **differential-drive** robot — two independently driven wheels plus a balancing caster — is the most common mobile robot design (think Roomba). Today you assemble one in SDF, attach Gazebo's diff-drive plugin, and drive it with velocity commands. This is the classic "my first mobile robot" project, and it pulls together Days 16–18.

---

## How Differential Drive Works

Two wheels, each with its own motor:

- **Both wheels same speed forward** → robot drives straight.
- **Right wheel faster than left** → robot curves left.
- **Wheels opposite directions** → robot spins in place.

You don't compute wheel speeds by hand — you send a **`Twist`** message (forward speed + turn rate) on `/cmd_vel`, and the **diff-drive plugin** converts it into the right wheel velocities. This is the same `/cmd_vel` interface real robots use.

---

## Building the Robot in SDF

A diff-drive robot needs: a chassis (`base`), two wheels (continuous joints), and a caster. The structure (full file: `diff_drive.sdf`):

```xml
<model name="diff_bot">
  <pose>0 0 0.1 0 0 0</pose>

  <!-- chassis -->
  <link name="base_link">
    <inertial><mass>5</mass> ... </inertial>
    <visual name="v"><geometry><box><size>0.4 0.3 0.1</size></box></geometry></visual>
    <collision name="c"><geometry><box><size>0.4 0.3 0.1</size></box></geometry></collision>
  </link>

  <!-- left & right wheels (cylinders on continuous joints) -->
  <link name="left_wheel"> ... </link>
  <joint name="left_wheel_joint" type="revolute">
    <parent>base_link</parent><child>left_wheel</child>
    <axis><xyz>0 1 0</xyz></axis>
  </joint>
  <!-- right wheel similar -->

  <!-- the magic: diff-drive plugin -->
  <plugin filename="gz-sim-diff-drive-system"
          name="gz::sim::systems::DiffDrive">
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.3</wheel_separation>
    <wheel_radius>0.1</wheel_radius>
    <topic>cmd_vel</topic>
  </plugin>
</model>
```

The `<plugin>` block is what makes it drivable: it listens on `cmd_vel` and spins the named wheel joints accordingly. `wheel_separation` and `wheel_radius` must match your geometry or the motion will be wrong.

---

## Driving It

1. Launch the world with the robot, and start the bridge for `/cmd_vel` (Day 18).
2. Drive it forward:
   ```bash
   ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}}"
   ```
3. Make it turn:
   ```bash
   ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
     "{linear: {x: 0.3}, angular: {z: 0.5}}"
   ```

The robot rolls and curves around your Day-17 obstacles. You're driving a simulated robot with the exact interface used on real hardware.

---

## Reading Odometry

The diff-drive plugin also *publishes* where the robot thinks it is (odometry):

```bash
ros2 topic echo /odom    # (after bridging the odometry topic)
```

**Odometry** is the robot's estimate of its own position from wheel rotation — a fundamental input for navigation. You'll use it conceptually in the Day-22 project.

---

## 📝 Today's Task

1. Build `diff_drive.sdf` (start from the provided file) with chassis, two wheels, a caster, and the diff-drive plugin.
2. Launch it in your world and bridge `/cmd_vel`.
3. Drive it **forward**, then make it **turn**, then **spin in place** (wheels opposite → pure angular `z`).
4. Bridge and `echo /odom` — watch the position estimate update as you drive.
5. Tune `wheel_separation`/`wheel_radius` to wrong values and observe how the motion becomes inaccurate (why correct values matter).

---

## ✅ Key Takeaways

✓ **Differential drive** = two independently driven wheels + caster; the most common mobile base.

✓ You command it with a **`Twist`** on **`/cmd_vel`** (forward speed + turn rate) — the real-robot standard.

✓ The **diff-drive plugin** converts `/cmd_vel` into wheel velocities; `wheel_separation`/`radius` must match the model.

✓ The plugin also publishes **odometry** (`/odom`) — the robot's self-position estimate.

✓ You're now driving a simulated robot through the same interface used on physical robots.

---

## 📚 References & Resources

- [Gazebo: Moving a robot (diff drive tutorial)](https://gazebosim.org/docs/harmonic/moving_robot/)
- [geometry_msgs/Twist reference](https://docs.ros.org/en/api/geometry_msgs/html/msg/Twist.html)
- [Gazebo diff-drive plugin](https://gazebosim.org/api/sim/8/classgz_1_1sim_1_1systems_1_1DiffDrive.html)

---

## 🔭 What's Next?

**Day 20 — Sensors in Gazebo.** A driving robot is good; a *sensing* robot is useful. We'll add LiDAR, a camera, and an IMU so the robot can perceive its surroundings.

---

*"Two wheels and a Twist message — that's how most robots get around."*
