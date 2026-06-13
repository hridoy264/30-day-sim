# Day 21 — Teleop & Visualizing in RViz

## 🎯 Today's Goal
Drive your robot with the keyboard (teleoperation) and use **RViz** — ROS 2's visualization tool — to *see* its sensor data: LiDAR scans, the camera feed, and the robot model, all in real time.

---

## Overview

So far you've driven the robot by typing `ros2 topic pub` commands — clumsy. Today you get two professional tools: **teleop** for live keyboard driving, and **RViz** for visualizing everything the robot senses. RViz is the window every roboticist keeps open; learning it now makes you far more effective for the rest of the course and beyond.

---

## Teleoperation: Drive With Your Keyboard

ROS 2 ships a keyboard teleop node that publishes `/cmd_vel` from your keypresses:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Keep that terminal focused and use the on-screen keys (`i`/`,` forward/back, `j`/`l` turn, `k` stop). Your robot drives live around the world. Much nicer than typing Twist messages by hand.

> 💡 If the robot doesn't move, confirm: the teleop node publishes `/cmd_vel`, the **bridge** for `/cmd_vel` is running, and Gazebo is **playing** (not paused). Those three together are 95% of teleop problems.

---

## What is RViz?

**RViz** is a 3D visualizer for ROS 2 data. Crucially, RViz does **not** simulate anything — it *displays* whatever is on ROS topics. So it shows the same data whether it comes from Gazebo or a real robot. That's why it's the universal robotics dashboard.

Launch it:

```bash
rviz2
```

---

## Setting Up RViz Displays

RViz starts empty. You add **Displays**, each subscribing to a topic:

1. Set the **Fixed Frame** (top-left) to a frame that exists, e.g. `odom` or `base_link`. (Wrong fixed frame = the #1 RViz beginner error; you'll see "no transform" warnings.)
2. Click **Add → By topic** and pick:
   - **LaserScan** on `/scan` → see the LiDAR hits as a ring of points.
   - **Image** on `/camera` → see the camera feed in a panel.
   - **Imu** on `/imu` → visualize orientation.
   - **RobotModel** / **TF** → see the robot and its coordinate frames.

Now drive with teleop and watch the LiDAR points sweep across obstacles and the camera feed update. This is the moment robotics feels real.

---

## Understanding TF in RViz

Remember **transforms** from Day 3? ROS 2's **TF** system broadcasts the live relationships between frames (`odom → base_link → lidar → ...`). RViz uses TF to place every piece of data correctly in 3D. If displays appear in the wrong place or RViz complains about transforms, it's almost always a TF/fixed-frame issue — exactly the Day-3 concepts in practice.

```bash
ros2 run tf2_tools view_frames   # generates a diagram of your TF tree
```

---

## Saving Your RViz Config

Once your displays are set up, save the configuration (File → Save Config As) so you don't rebuild it each time. You can launch RViz preloaded with it:

```bash
rviz2 -d my_robot.rviz
```

---

## 📝 Today's Task

1. Run `teleop_twist_keyboard` and drive your robot around the world with the keyboard.
2. Open `rviz2`, set the **Fixed Frame** correctly.
3. Add a **LaserScan** display on `/scan` and drive toward an obstacle — watch the points cluster on it.
4. Add an **Image** display for the camera and a **TF** display for the frames.
5. Save your RViz config and reopen it with `rviz2 -d`.

---

## ✅ Key Takeaways

✓ **Teleop** (`teleop_twist_keyboard`) publishes `/cmd_vel` from your keyboard for live driving.

✓ **RViz** *visualizes* ROS topics — it doesn't simulate; it shows sim or real data identically.

✓ Add **Displays** (LaserScan, Image, Imu, RobotModel) subscribed to your topics.

✓ Set the correct **Fixed Frame**; most RViz problems are **TF/frame** issues — the Day-3 transforms at work.

✓ Save your RViz **config** and reload with `rviz2 -d` to avoid rebuilding it.

---

## 📚 References & Resources

- [teleop_twist_keyboard](https://github.com/ros-teleop/teleop_twist_keyboard)
- [RViz user guide](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-Main.html)
- [ROS 2 TF2 tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html)

---

## 🔭 What's Next?

**Day 22 — Mini-Project!** You'll tie the whole Gazebo phase together: a mobile robot that uses its LiDAR to explore a world and avoid obstacles on its own.

---

*"RViz is the roboticist's eyes. Once you can see what the robot senses, debugging becomes easy."*
