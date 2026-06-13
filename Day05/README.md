# Day 5 — Describing Robots & Worlds: URDF, SDF & MJCF

## 🎯 Today's Goal
Learn how a simulator knows what your robot looks like. You'll understand the three description formats — **URDF**, **SDF**, and **MJCF** — and write your very first robot description by hand.

---

## Overview

A simulator can't simulate a robot it doesn't know about. You have to *describe* the robot: its body parts, how they connect, their sizes, masses, and sensors. This description lives in a special file. Today you learn the three formats you'll meet across this course and write a tiny one yourself. This is the bridge between "understanding simulation" and "doing simulation."

---

## The Core Idea: Links and Joints

Every robot description, in every format, is built from two things:

- **Links** — the rigid bodies (a wheel, an arm segment, the chassis). Each has a shape, a mass, and inertia.
- **Joints** — the connections between links that define how they move relative to each other.

Common joint types:

| Joint type | Motion | Example |
|------------|--------|---------|
| **Fixed** | none | a sensor bolted to the chassis |
| **Revolute** | rotates within limits | an elbow, a steering hinge |
| **Continuous** | rotates freely (no limit) | a wheel |
| **Prismatic** | slides in a line | a linear actuator, a gripper finger |

A robot is just a **tree of links connected by joints**. Once you see it that way, every description format reads the same.

---

## The Three Formats

### 1. URDF — Unified Robot Description Format
The **most common** format in robotics. It's XML, used by **ROS** and supported by PyBullet and Gazebo. Great for describing a single robot (its links and joints). Its limitation: it can't easily describe a *whole world* (multiple objects, lights, physics settings) — that's what SDF is for.

### 2. SDF — Simulation Description Format
**Gazebo's native format**, also XML. More powerful than URDF: it can describe robots **and** complete worlds — lighting, multiple models, physics parameters, sensors. You'll use SDF heavily in the Gazebo phase (Days 16–22).

### 3. MJCF — MuJoCo XML Format (`.xml`)
**MuJoCo's native format**. Compact and excellent for the high-accuracy physics and reinforcement-learning work in Days 11–15. It describes bodies, joints, actuators, and sensors very concisely.

> 💡 The good news: all three are XML and built from the same **links + joints** idea. Learn one and the others are easy. Tools exist to convert between them (e.g., URDF → SDF in Gazebo).

---

## Your First URDF (read it like a sentence)

Here's a minimal robot: a single box body. Notice the three sub-parts of a link — **visual** (what you see), **collision** (what physics uses), and **inertial** (mass properties).

```xml
<?xml version="1.0"?>
<robot name="my_first_robot">

  <link name="base_link">
    <!-- what you SEE -->
    <visual>
      <geometry>
        <box size="0.4 0.4 0.2"/>
      </geometry>
    </visual>

    <!-- what PHYSICS uses for contact -->
    <collision>
      <geometry>
        <box size="0.4 0.4 0.2"/>
      </geometry>
    </collision>

    <!-- mass & inertia -->
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

</robot>
```

Read it top to bottom: *"This robot has one link called base_link. It looks like a 0.4×0.4×0.2 m box, collides as that same box, weighs 1 kg, and has this inertia."* That's a complete (if boring) robot.

---

## Adding a Second Link with a Joint

To make it move, add another link and a **joint** connecting them:

```xml
  <link name="wheel">
    <visual>
      <geometry><cylinder radius="0.1" length="0.05"/></geometry>
    </visual>
  </link>

  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel"/>
    <origin xyz="0.2 0 0" rpy="1.5708 0 0"/>  <!-- position + rotation -->
    <axis xyz="0 0 1"/>                         <!-- spins about this axis -->
  </joint>
```

Notice `rpy="1.5708 0 0"` — that's **roll = π/2 radians = 90°**, exactly the frames-and-radians knowledge from Day 3 in action.

---

## 📝 Today's Task

1. Create a file `my_first_robot.urdf` and paste the single-box URDF above.
2. **Load it in PyBullet** to see your own robot appear (uses your Day 4 setup):
   ```python
   import pybullet as p, pybullet_data, time
   p.connect(p.GUI)
   p.setAdditionalSearchPath(pybullet_data.getDataPath())
   p.setGravity(0, 0, -9.81)
   p.loadURDF("plane.urdf")
   p.loadURDF("my_first_robot.urdf", [0, 0, 1])   # your robot!
   for _ in range(2400):
       p.stepSimulation(); time.sleep(1/240)
   p.disconnect()
   ```
3. Change the box `size` and re-run. Watch your robot change shape.
4. Add the wheel link + joint and reload. Congratulations — you've described a robot.

---

## ✅ Key Takeaways

✓ A simulator needs a **description file**; every robot is a **tree of links connected by joints**.

✓ Joint types: **fixed, revolute, continuous, prismatic** — they define how links move.

✓ **URDF** (ROS standard), **SDF** (Gazebo, can describe whole worlds), **MJCF** (MuJoCo, compact, RL).

✓ Each link has **visual** (seen), **collision** (physics), and **inertial** (mass) parts.

✓ All three formats are XML built on the same idea — learn one, learn them all.

---

## 📚 References & Resources

- [URDF Tutorials (ROS)](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html)
- [SDFormat specification](http://sdformat.org/spec)
- [MuJoCo MJCF (XML) reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)
- [PyBullet loadURDF docs](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit)

---

## 🔭 What's Next?

**Day 6 — Hello PyBullet.** Foundations complete! Now the fun begins. We dive into PyBullet, build a simulation from scratch, and start making robots move. 🎉

---

*"Before a robot can move, it must be described. You just learned the language."*
