# Day 18 — Spawning a Robot & The ROS–Gazebo Bridge

## 🎯 Today's Goal
Put a robot into your Gazebo world and connect it to ROS 2 through the bridge, so your code can send commands and receive data. This is the moment Gazebo becomes *robotics*, not just a physics demo.

---

## Overview

You have a world (Day 17). Now you need a robot in it, talking to ROS 2. Today covers two essential skills: **spawning** a robot into a running simulation, and setting up the **`ros_gz` bridge** so ROS 2 topics flow to and from Gazebo. Once this works, everything you know about ROS 2 controls a simulated robot exactly like a real one.

---

## ROS 2 in 90 Seconds (the parts you need)

If you're new to ROS 2, here's the minimum:

- A **node** is a small program that does one job (e.g., "drive the wheels").
- Nodes talk over **topics** — named channels carrying **messages** (e.g., `/cmd_vel` carries velocity commands).
- **Publish** = send to a topic. **Subscribe** = receive from a topic.

A robot is many nodes exchanging messages. Gazebo joins this conversation through the bridge.

---

## Spawning a Robot

With a Gazebo world running, spawn a robot from an SDF or URDF using the ROS 2 service:

```bash
ros2 run ros_gz_sim create -world my_world -file robot.sdf -name my_robot -z 0.5
```

Or include it directly in the world's SDF (Day 17's `<include>`). Spawning at runtime is handy when you want to drop robots into an existing scene.

> 💡 You can convert the URDFs you wrote in Phase 1 into Gazebo robots — Gazebo understands URDF with some Gazebo-specific tags added. Reusing your earlier work is encouraged.

---

## The Bridge: Connecting Gazebo ↔ ROS 2

Gazebo has its own internal topics; ROS 2 has its own. The **`ros_gz_bridge`** translates between them. You start it and tell it which topics to connect and their types:

```bash
ros2 run ros_gz_bridge parameter_bridge \
  /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Read that mapping as: *bridge the topic `/cmd_vel`, which is a ROS `Twist` message (`@...Twist`) and a Gazebo `Twist` message (`@gz.msgs.Twist`).* The `@` symbols separate the topic name, the ROS type, and the Gazebo type.

Now anything published to `/cmd_vel` in ROS 2 reaches Gazebo, and vice versa.

---

## Verifying the Connection

Check that topics are flowing:

```bash
ros2 topic list                 # see /cmd_vel and others
ros2 topic echo /cmd_vel        # watch messages arrive
```

Send a test command to make the robot move (if it has a drive plugin — that's Day 19):

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.5}, angular: {z: 0.2}}"
```

If the robot moves in Gazebo from a ROS 2 command, your bridge works — a genuinely exciting milestone.

---

## Launch Files: Doing It All at Once

Typing all these commands every time is painful. ROS 2 **launch files** (Python) start the world, spawn the robot, and run the bridge in one command. A minimal sketch (`bringup.launch.py` in this folder shows a fuller version):

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'],
    )
    return LaunchDescription([bridge])
```

Run with `ros2 launch bringup.launch.py`. You'll build these up over the next days.

---

## 📝 Today's Task

1. Launch your Day-17 world: `gz sim my_world.sdf` (press play).
2. Spawn a simple robot model into it with `ros2 run ros_gz_sim create ...`.
3. Start a bridge for `/cmd_vel` and confirm with `ros2 topic list`.
4. `ros2 topic echo /cmd_vel` in one terminal while you `ros2 topic pub` in another — watch messages flow.
5. Write a minimal launch file that starts the bridge, and run it with `ros2 launch`.

---

## ✅ Key Takeaways

✓ ROS 2 basics: **nodes** talk over **topics** by **publishing** and **subscribing** to **messages**.

✓ Spawn robots with `ros2 run ros_gz_sim create ...` (or `<include>` in the world SDF).

✓ The **`ros_gz_bridge`** connects Gazebo topics to ROS 2 topics via `topic@ROStype@GZtype` mappings.

✓ Verify with `ros2 topic list / echo / pub` — seeing the robot move from a ROS command is the milestone.

✓ **Launch files** start the world, robot, and bridge together — your everyday workflow.

---

## 📚 References & Resources

- [ros_gz bridge documentation](https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_bridge)
- [ROS 2 topics tutorial](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
- [ROS 2 launch files](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html)
- [Gazebo + ROS 2 integration tutorials](https://gazebosim.org/docs/harmonic/ros2_integration/)

---

## 🔭 What's Next?

**Day 19 — A Differential-Drive Mobile Robot.** We build a proper two-wheeled robot with a drive plugin, so `/cmd_vel` commands actually make it roll around your world.

---

*"The bridge is where simulation meets software. Cross it, and your code runs robots."*
