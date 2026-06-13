# Day 7 — Loading Robots & Worlds from URDF

## 🎯 Today's Goal
Go beyond a single falling object: load your own robots, **inspect** their joints and links programmatically, and build a small scene with multiple objects. Knowing how to interrogate a robot is what separates copying examples from real control.

---

## Overview

Yesterday you loaded a model and watched it fall. Today you learn to *understand* what you loaded. Every robot you control has joints and links with names and indices — and before you can command a robot, you must know what it's made of. This is a short but essential skill you'll use in every simulator.

---

## Loading: Position, Orientation & Options

`loadURDF` is more flexible than it first appears:

```python
robot = p.loadURDF(
    "r2d2.urdf",
    basePosition=[0, 0, 1],
    baseOrientation=p.getQuaternionFromEuler([0, 0, 0]),
    useFixedBase=False,   # True = bolt the base in place (great for robot arms)
    globalScaling=1.0,    # resize the whole model
)
```

> 💡 **`useFixedBase=True`** is one of the most useful flags. A robot arm should be bolted to the ground, not tip over. A mobile robot or a falling object should have `useFixedBase=False`.

---

## Inspecting Joints & Links

A loaded robot returns an integer **id**. From it you query everything:

```python
num_joints = p.getNumJoints(robot)
print("Number of joints:", num_joints)

for i in range(num_joints):
    info = p.getJointInfo(robot, i)
    joint_index = info[0]
    joint_name  = info[1].decode("utf-8")
    joint_type  = info[2]   # 0=revolute, 1=prismatic, 4=fixed, etc.
    link_name   = info[12].decode("utf-8")
    print(f"[{joint_index}] joint='{joint_name}' type={joint_type} link='{link_name}'")
```

This prints a map of the robot. **You need these indices** to control specific joints tomorrow. Get in the habit of printing the joint list whenever you load a new robot — it saves hours of guessing.

> ℹ️ In PyBullet, each **joint index also identifies the child link** attached by that joint. So "joint 3" and "the link moved by joint 3" share the same number.

---

## Reading a Joint's Current State

```python
state = p.getJointState(robot, jointIndex=2)
position = state[0]    # angle (rad) or distance (m)
velocity = state[1]    # rad/s or m/s
print("Joint 2 position:", position, "velocity:", velocity)
```

Reading state is how your control code "feels" the robot — the foundation of any feedback control.

---

## Building a Small Scene

Let's place several objects to make a proper world (see `load_and_inspect.py`):

```python
import pybullet as p, pybullet_data, time
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

p.loadURDF("plane.urdf")
p.loadURDF("table/table.urdf", [0, 0, 0])
tray = p.loadURDF("tray/tray.urdf", [0, 0, 0.65])
cube = p.loadURDF("cube_small.urdf", [0.1, 0, 0.8])
duck = p.loadURDF("duck_vhacd.urdf", [-0.1, 0, 0.8])

for _ in range(2400):
    p.stepSimulation(); time.sleep(1/240)
p.disconnect()
```

A table, a tray, a cube, and a duck — a real little scene you can later manipulate with a robot arm.

---

## Resetting & Repositioning

You can teleport a robot at any time (useful for resetting experiments):

```python
p.resetBasePositionAndOrientation(robot, [0, 0, 2], [0, 0, 0, 1])
p.resetJointState(robot, jointIndex=2, targetValue=0.0)  # snap a joint to an angle
```

`resetJointState` instantly sets a joint without physics — perfect for putting a robot in a known starting pose before a run.

---

## 📝 Today's Task

1. Run `load_and_inspect.py` to print the full joint/link map of R2D2.
2. Identify which joints are R2D2's **wheels** and **head** from the printout.
3. Load a **KUKA arm** with `useFixedBase=True`: `p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)` and print *its* joints — notice they're all revolute.
4. Build a scene with a table + tray + at least two objects (the snippet above).
5. Use `resetJointState` to set one KUKA joint to `1.0` rad before stepping, and watch the arm start bent.

---

## ✅ Key Takeaways

✓ `loadURDF` flags matter: **`useFixedBase=True`** bolts arms down; `globalScaling` resizes.

✓ Always **print the joint/link map** (`getNumJoints` + `getJointInfo`) when loading a new robot.

✓ In PyBullet a **joint index also names its child link** — same number.

✓ `getJointState` reads position & velocity — how your code "feels" the robot.

✓ `resetBasePositionAndOrientation` / `resetJointState` teleport for clean experiment resets.

---

## 📚 References & Resources

- [PyBullet Quickstart — loadURDF & joint info](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit)
- [pybullet_data model list (GitHub)](https://github.com/bulletphysics/bullet3/tree/master/data)
- [URDF Tutorials (ROS)](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html)

---

## 🔭 What's Next?

**Day 8 — Controlling Joints.** Now that you can load and inspect a robot, we make it *move*: position, velocity, and torque control. This is where robots come alive.

---

*"You can't control what you can't inspect. Today you learned to read a robot."*
