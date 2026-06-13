# 30 Days of Simulation 🦾🌍

A free, beginner-friendly, project-based course that takes you from **zero** to building and controlling your own simulated robots. No expensive hardware required — just a laptop and curiosity.

Simulation is where modern robotics, reinforcement learning, and AI are built and tested. Before a robot ever moves in the real world, it is born, trained, and debugged inside a simulator. This 30-day journey teaches you the four most important simulation tools used in industry and research today, one clean step at a time.

---

## Who This Is For

- Complete beginners who know a little Python (or are willing to learn as they go)
- Robotics, AI, or game-dev students who want hands-on simulation skills
- Hardware tinkerers who want to test ideas in software first
- Anyone curious about how robots are trained before they touch the real world

**Prerequisites:** Basic computer skills and a willingness to type commands. We explain everything else. Python basics help but are taught along the way.

---

## What You'll Learn

By Day 30 you will be able to:

- Explain how physics simulators work under the hood
- Describe robots and worlds using URDF, SDF, and MJCF
- Build and control robots in **PyBullet**, **MuJoCo**, and **Gazebo (with ROS 2)**
- Add sensors — cameras, LiDAR, IMU, contact sensors — to simulated robots
- Train a robot to balance and walk using **reinforcement learning**
- Understand **sim-to-real** and why simulation matters for real robots
- Know when and why to reach for **NVIDIA Isaac Sim** and digital twins
- Ship a capstone project: a sensored robot in a world that you built and controlled

---

## The 30-Day Roadmap

### Phase 1 — Foundations (Days 1–5)
Build the mental model before touching tools.

| Day | Topic |
|-----|-------|
| 01 | What is Simulation & Why It Matters |
| 02 | How Physics Engines Work (rigid bodies, time steps, collisions) |
| 03 | The Math You Need: Frames, Transforms & Units |
| 04 | Setting Up Your Simulation Environment |
| 05 | Describing Robots & Worlds: URDF, SDF & MJCF |

### Phase 2 — PyBullet: Your First Simulator (Days 6–10)
The easiest entry point. Pure Python, runs anywhere.

| Day | Topic |
|-----|-------|
| 06 | Hello PyBullet: Your First Simulation |
| 07 | Loading Robots & Worlds from URDF |
| 08 | Controlling Joints: Position, Velocity & Torque |
| 09 | Adding Sensors: Cameras, Rays & Contacts |
| 10 | 🛠 Mini-Project: A Robot Arm That Picks Things Up |

### Phase 3 — MuJoCo: Accurate Physics for Learning (Days 11–15)
The simulator behind most modern robotics research.

| Day | Topic |
|-----|-------|
| 11 | Hello MuJoCo: Install & First Model |
| 12 | Building Models in MJCF |
| 13 | Simulating & Controlling from Python |
| 14 | Sensors & Contacts in MuJoCo |
| 15 | 🛠 Mini-Project: Balancing a CartPole |

### Phase 4 — Gazebo + ROS 2: Industry-Standard Robotics (Days 16–22)
The simulator used to build real robots, connected to ROS 2.

| Day | Topic |
|-----|-------|
| 16 | Hello Gazebo: Install & The Simulator Tour |
| 17 | Building Worlds with SDF |
| 18 | Spawning a Robot & The ROS–Gazebo Bridge |
| 19 | A Differential-Drive Mobile Robot |
| 20 | Sensors in Gazebo: LiDAR, Camera & IMU |
| 21 | Teleop & Visualizing in RViz |
| 22 | 🛠 Mini-Project: A Robot That Explores a World |

### Phase 5 — Reinforcement Learning in Simulation (Days 23–26)
Teach robots to learn by themselves.

| Day | Topic |
|-----|-------|
| 23 | Intro to RL & the Gymnasium API |
| 24 | Training Your First Policy with Stable-Baselines3 |
| 25 | Wrapping Your Own Simulator as a Gym Environment |
| 26 | Sim-to-Real & Domain Randomization |

### Phase 6 — Advanced & Capstone (Days 27–30)
The frontier, then put it all together.

| Day | Topic |
|-----|-------|
| 27 | NVIDIA Isaac Sim & GPU-Accelerated Simulation |
| 28 | Digital Twins & High-Fidelity Rendering |
| 29 | 🏁 Capstone: Build, Sensor & Control Your Own Robot |
| 30 | Wrap-Up, Portfolio & Where to Go Next |

---

## How to Use This Course

1. **One day at a time.** Each `DayXX/` folder has a `README.md` with a clear goal, the concepts, and a short hands-on task. Don't rush — consistency beats speed.
2. **Always do the "Today's Task."** Reading is not learning. Type the code, break it, fix it.
3. **Keep a log.** A sentence a day about what you learned compounds fast.
4. **Share progress.** Post with **#30DaysOfSimulation** and connect with others learning alongside you.

Each day is designed to take **30–90 minutes**.

---

## Tools You'll Install (all free)

| Tool | Used In | Why |
|------|---------|-----|
| **Python 3.10+** | Everything | The glue language of simulation |
| **PyBullet** | Days 6–10 | Easiest simulator to start with |
| **MuJoCo** | Days 11–15 | Accurate physics, research standard |
| **Gazebo (Harmonic) + ROS 2** | Days 16–22 | Industry robotics simulation |
| **Gymnasium + Stable-Baselines3** | Days 23–26 | Reinforcement learning |
| **NVIDIA Isaac Sim** | Days 27–28 | GPU sim (overview; optional GPU) |

> 💡 **Operating system tip:** Ubuntu Linux (22.04/24.04) gives the smoothest experience, especially for ROS 2 and Gazebo. On Windows, use **WSL2**. On macOS, PyBullet and MuJoCo work natively; use a cloud/Linux machine for the Gazebo days.

---

## A Note From Your Instructor

This material is written as if a senior simulation engineer were sitting next to you — explaining not just *what* to type, but *why* it works and *where* it breaks. Simulation has a reputation for being fiddly. The secret is to start simple, build one concept at a time, and never skip the hands-on part.

You don't need a powerful computer or a real robot to become genuinely good at this. You need 30 days and the willingness to keep going.

Let's build. 🚀

---

*"The best way to predict the behavior of a robot is to simulate it first."*
