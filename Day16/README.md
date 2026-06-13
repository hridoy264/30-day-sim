# Day 16 — Hello Gazebo: Install & The Simulator Tour

## 🎯 Today's Goal
Install Gazebo, understand how it pairs with ROS 2, and take a guided tour of the simulator that professional roboticists use to build real-world robots.

---

## Overview

Welcome to Phase 4 — the most "industry robotics" part of the course. **Gazebo** is the open-source simulator at the heart of the ROS ecosystem. Where PyBullet and MuJoCo are great for quick experiments and RL, Gazebo is what teams use to develop and test the full software stack of a *real robot* before deployment. It's deeply integrated with **ROS 2**, the standard middleware that runs modern robots.

This phase is more involved to set up (it really wants Linux), but it's where your skills become directly job-relevant.

---

## A Note on Names & Versions

Gazebo has a confusing history. Here's the clear version:

- The modern simulator is called **Gazebo** (formerly "Ignition Gazebo"). The old one is now "Gazebo Classic" (retired).
- Releases are named alphabetically. **Gazebo Harmonic** is the current **LTS** (long-term support) release — recommended for this course.
- It connects to ROS 2 via a bridge package called **`ros_gz`**.

> 💡 If unsure which version to use: install the **default Gazebo that comes with your ROS 2 version**. ROS 2 Humble/Jazzy pair cleanly with Gazebo Harmonic. Matching versions avoids 90% of setup pain.

---

## What You Need

- **Ubuntu Linux** (22.04 or 24.04) — native, or via **WSL2** on Windows (Day 4). Gazebo + ROS 2 on Linux is by far the smoothest path.
- **ROS 2** (Humble on 22.04, or Jazzy on 24.04).

---

## Step 1 — Install ROS 2

Follow the official ROS 2 install guide for your Ubuntu version (link in references). The short version for Humble on Ubuntu 22.04:

```bash
# (after adding the ROS 2 apt repository per the official guide)
sudo apt update
sudo apt install ros-humble-desktop
```

Then **source ROS 2** in every new terminal (add to your `~/.bashrc` to automate):

```bash
source /opt/ros/humble/setup.bash
```

---

## Step 2 — Install Gazebo + the ROS Bridge

Install Gazebo and the `ros_gz` bridge that connects it to ROS 2:

```bash
sudo apt install ros-humble-ros-gz
```

This pulls in Gazebo and the integration packages together — the recommended way.

---

## Step 3 — Launch Gazebo

Open the simulator with an empty world:

```bash
gz sim
```

Or jump straight into a demo world:

```bash
gz sim shapes.sdf
```

The Gazebo window opens with a 3D scene, a play/pause control, and panels for entities and components.

---

## Tour of the Interface

| Area | What it does |
|------|--------------|
| **3D viewport** | the simulated world; orbit/zoom like other sims |
| **Play/Pause** (bottom) | start/stop time — *Gazebo starts paused!* |
| **Entity tree** | every model/light in the world |
| **Component inspector** | pose, mass, and properties of the selected entity |
| **Insert panel** | drag in built-in shapes and models |

> ⚠️ **First gotcha for everyone:** Gazebo opens **paused**. If "nothing is happening," press the **play button** at the bottom-left. Everyone hits this once.

---

## How Gazebo + ROS 2 Fit Together

This is the key mental model for the phase:

- **Gazebo** simulates the physics, sensors, and world.
- **ROS 2** is the robot's "nervous system" — nodes that send commands and receive sensor data over **topics**.
- **`ros_gz` bridge** translates messages between them.

So your ROS 2 code controls a Gazebo robot *exactly* as it would control a real one. That's the magic: the same code runs in sim and on hardware. We build toward this over the next six days.

---

## 📝 Today's Task

1. Ensure you're on Ubuntu (native or WSL2). Install **ROS 2** and **`ros-humble-ros-gz`**.
2. Source ROS 2 and run `gz sim shapes.sdf`.
3. **Press play** and watch the shapes settle.
4. Click a shape and explore the **Component Inspector** — find its pose and mass.
5. Use the **Insert** panel to drag a new sphere into the world and let it fall.

> 💻 **No Linux handy?** Read through this phase to understand the concepts, and use a free cloud Linux VM (or [The Construct's](https://www.theconstruct.ai/) browser-based ROS environment) to do the hands-on parts. The concepts transfer fully.

---

## ✅ Key Takeaways

✓ **Gazebo** is the open-source simulator for developing *real* robots, tightly tied to **ROS 2**.

✓ Use the modern **Gazebo** (Harmonic LTS), not the retired "Gazebo Classic."

✓ Easiest install: `ros-<distro>-ros-gz`, matching your ROS 2 version; Linux/WSL2 strongly preferred.

✓ Launch with `gz sim`; remember it **starts paused** — press play.

✓ Mental model: **Gazebo simulates**, **ROS 2 commands/senses**, the **`ros_gz` bridge** connects them — same code as on a real robot.

---

## 📚 References & Resources

- [Gazebo: Getting Started](https://gazebosim.org/docs/harmonic/getstarted/)
- [Install Gazebo with ROS](https://gazebosim.org/docs/latest/ros_installation/)
- [ROS 2 installation](https://docs.ros.org/en/humble/Installation.html)
- [ros_gz bridge](https://github.com/gazebosim/ros_gz)

---

## 🔭 What's Next?

**Day 17 — Building Worlds with SDF.** We use SDF (from Day 5) to construct custom Gazebo worlds — ground, lighting, and obstacles — the stage your robots will perform on.

---

*"PyBullet and MuJoCo are the lab. Gazebo is the factory floor."*
