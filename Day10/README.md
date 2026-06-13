# Day 10 — 🛠 Mini-Project: A Robot Arm That Picks Things Up

## 🎯 Today's Goal
Combine everything from Phase 2 — loading, joint control, and sensing — into one complete program: a robot arm that moves to an object, grasps it, and lifts it. Your first end-to-end robotics task.

---

## Overview

This is your first **mini-project**, and it's a big milestone. You've learned the pieces; today you assemble them. A pick-and-place is the "hello world" of manipulation and appears in real warehouses worldwide. We'll build it step by step so every part is clear, then give you challenges to extend it.

Don't worry about perfection. The goal is a working pipeline you understand end to end.

---

## What We're Building

A **KUKA arm with a gripper** that:

1. Starts above a table with a cube on it.
2. Moves its end-effector down to the cube (using **inverse kinematics**).
3. Closes the gripper to grasp it (using **contact** feedback ideas from Day 9).
4. Lifts the cube back up.

---

## New Concept: Inverse Kinematics (IK)

Until now we set joint angles directly (*forward* — "given angles, where's the hand?"). But for picking, we want the opposite: *"I want the hand at this XYZ — what joint angles achieve that?"* That's **inverse kinematics**, and PyBullet solves it for you:

```python
target_xyz = [0.5, 0, 0.3]
joint_angles = p.calculateInverseKinematics(arm, end_effector_link, target_xyz)
# then command those angles with POSITION_CONTROL
```

This one function turns "go here in space" into joint commands. It's one of the most useful tools in manipulation.

---

## The Project, Step by Step

See `pick_and_place.py` for the full program. Here's the logic:

```python
import pybullet as p, pybullet_data, time

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")
p.loadURDF("table/table.urdf", [0.5, 0, -0.65])
cube = p.loadURDF("cube_small.urdf", [0.5, 0, 0.05])

# a gripper-equipped arm
arm = p.loadURDF("franka_panda/panda.urdf", [0, 0, 0], useFixedBase=True)
ee_link = 11          # panda end-effector link index
finger_joints = [9, 10]

def move_to(xyz, steps=240):
    angles = p.calculateInverseKinematics(arm, ee_link, xyz)
    for j in range(7):
        p.setJointMotorControl2(arm, j, p.POSITION_CONTROL, angles[j], force=200)
    for _ in range(steps):
        p.stepSimulation(); time.sleep(1/240)

def gripper(open_):
    target = 0.04 if open_ else 0.0
    for j in finger_joints:
        p.setJointMotorControl2(arm, j, p.POSITION_CONTROL, target, force=50)
    for _ in range(120):
        p.stepSimulation(); time.sleep(1/240)

# the pick sequence
gripper(open_=True)
move_to([0.5, 0, 0.25])     # above the cube
move_to([0.5, 0, 0.02])     # down to it
gripper(open_=False)        # grasp
move_to([0.5, 0, 0.4])      # lift!

for _ in range(2000):
    p.stepSimulation(); time.sleep(1/240)
p.disconnect()
```

Run it and watch the arm pick up the cube. This is real robotic manipulation — the same structure used in industry, just simplified.

---

## Why This Works (the recipe)

Every manipulation task follows this pattern, and you just built it:

1. **Perceive** the target's location (here we know it; with vision you'd detect it).
2. **Plan** waypoints: approach → reach → grasp → lift.
3. **Execute** each waypoint with IK + position control.
4. **Verify** the grasp (check contacts / that the object lifted with the hand).

---

## 📝 Today's Task

1. Run `pick_and_place.py` and get the arm to lift the cube.
2. **Move it:** after lifting, add waypoints to carry the cube to `[0.3, 0.3, 0.4]` and release it — a full pick *and place*.
3. **Verify the grasp:** use `getContactPoints` between the fingers and the cube to print "Grasp successful!" only when both fingers touch it.
4. **Make it robust:** move the cube's start position and confirm IK still reaches it.
5. **Reflect:** write 2–3 sentences in your log on what was hardest. (Grasp timing? IK reach? Gripper force?)

---

## 🏆 Phase 2 Complete!

You can now load robots, inspect them, control joints three ways, read sensors, and chain it all into a real task. That's a genuine simulation skill set. Take a moment — you've come a long way from a falling R2D2 on Day 6.

---

## ✅ Key Takeaways

✓ A pick-and-place = **perceive → plan waypoints → execute with IK → verify**.

✓ **Inverse kinematics** (`calculateInverseKinematics`) turns a target XYZ into joint angles.

✓ Grasping combines **position control** (fingers) with **contact feedback** (did we grab it?).

✓ Complex robot behaviors are just **sequences of simple, verified steps**.

✓ You've completed a full Phase — loading, control, and sensing now work together.

---

## 📚 References & Resources

- [PyBullet inverse kinematics docs](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit)
- [Franka Panda model (in pybullet_data)](https://github.com/bulletphysics/bullet3/tree/master/data/franka_panda)
- [Pick-and-place overview](https://en.wikipedia.org/wiki/Pick-and-place_machine)

---

## 🔭 What's Next?

**Day 11 — Hello MuJoCo.** New phase, new tool. We move to MuJoCo, the high-accuracy physics engine behind most modern robotics research and reinforcement learning.

---

*"You didn't just animate an arm — you built a pipeline. That's engineering."*
