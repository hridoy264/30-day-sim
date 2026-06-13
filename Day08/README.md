# Day 8 — Controlling Joints: Position, Velocity & Torque

## 🎯 Today's Goal
Make a robot **move on command**. You'll learn the three fundamental ways to control any robot joint — position, velocity, and torque — and feel the difference between them hands-on.

---

## Overview

This is the day robots stop falling and start *doing*. All robot control, in every simulator, comes down to commanding joints. PyBullet exposes three **control modes**, and understanding when to use each is a genuinely important robotics skill — not just a PyBullet detail.

---

## The One Function: `setJointMotorControl2`

Almost all joint commands go through one function:

```python
p.setJointMotorControl2(
    bodyUniqueId=robot,
    jointIndex=2,
    controlMode=p.POSITION_CONTROL,   # or VELOCITY_CONTROL, or TORQUE_CONTROL
    targetPosition=1.57,              # what you want (meaning depends on mode)
    force=50,                         # max force/torque the motor may use
)
```

The `controlMode` changes everything about what `target*` and `force` mean. Let's take each mode.

---

## Mode 1 — Position Control (most common)

*"Go to this angle and hold it."* You give a **target position** and a **max force**; the simulator's built-in motor figures out the rest.

```python
p.setJointMotorControl2(robot, 2, p.POSITION_CONTROL,
                        targetPosition=1.57, force=50)
```

This is what you'll use most. It's how you command a robot arm to a pose, or a gripper to close. The `force` caps how hard the motor pushes — too low and it can't reach the target against gravity; too high and it can be violent.

---

## Mode 2 — Velocity Control

*"Spin at this speed."* Perfect for **wheels** and conveyor-like motion.

```python
p.setJointMotorControl2(robot, wheel_joint, p.VELOCITY_CONTROL,
                        targetVelocity=10.0, force=20)
```

A mobile robot drives by setting wheel velocities. `force` here is the max torque available to reach that speed.

---

## Mode 3 — Torque Control

*"Apply exactly this much torque."* The most direct and lowest-level mode — you supply the raw force, and physics does the rest. Used in advanced control and reinforcement learning.

```python
# IMPORTANT: first disable the default motor, or it fights your torque
p.setJointMotorControl2(robot, j, p.VELOCITY_CONTROL, force=0)
# then apply torque
p.setJointMotorControl2(robot, j, p.TORQUE_CONTROL, force=1.5)
```

> ⚠️ **Classic gotcha:** PyBullet enables a *default velocity motor* on every joint. For torque control you must first disable it by setting `VELOCITY_CONTROL` with `force=0`. Forget this and your torques seem to do nothing — the default motor is silently holding the joint still.

---

## Controlling Many Joints at Once

For arms, command all joints together with `setJointMotorControlArray`:

```python
joints = [0, 1, 2, 3, 4, 5, 6]
targets = [0.0, 0.5, -0.5, 1.0, 0.0, 0.5, 0.0]
p.setJointMotorControlArray(robot, joints, p.POSITION_CONTROL,
                            targetPositions=targets)
```

---

## A Complete Example: Make a KUKA Arm Wave

See `joint_control.py` in this folder:

```python
import pybullet as p, pybullet_data, time, math
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")
arm = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

t = 0.0
while t < 20:
    # oscillate joint 3 with a sine wave -> smooth waving motion
    target = math.sin(t) * 1.0
    p.setJointMotorControl2(arm, 3, p.POSITION_CONTROL,
                            targetPosition=target, force=200)
    p.stepSimulation(); time.sleep(1/240); t += 1/240
p.disconnect()
```

A sine wave fed into a position target produces smooth, lifelike motion. This little trick — `sin(t)` into a joint — is the "hello world" of robot motion.

---

## 📝 Today's Task

1. Run `joint_control.py` and watch the KUKA arm wave.
2. **Position control:** change joint `3` to a fixed `targetPosition=1.0` and watch it move there and hold.
3. **Velocity control:** load R2D2 and spin its wheel joints with `VELOCITY_CONTROL` — make it drive.
4. **Torque control:** pick one joint, disable its default motor (`force=0`), then apply a small constant torque and observe.
5. Use `setJointMotorControlArray` to send all 7 KUKA joints to a custom pose at once.

---

## ✅ Key Takeaways

✓ Joint control goes through `setJointMotorControl2` (or `...Array` for many joints).

✓ **Position control** = "go to this angle and hold" — your everyday mode for arms & grippers.

✓ **Velocity control** = "spin at this speed" — perfect for wheels.

✓ **Torque control** = "apply exactly this force" — low-level, used in RL/advanced control.

✓ For torque mode you must first **disable the default velocity motor** (`force=0`) or it fights you.

✓ A `sin(t)` target produces smooth oscillating motion — the classic motion demo.

---

## 📚 References & Resources

- [PyBullet Quickstart — setJointMotorControl2](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit)
- [Position vs. velocity vs. torque control (overview)](https://control.com/technical-articles/an-introduction-to-control-systems/)
- [Bullet examples (GitHub)](https://github.com/bulletphysics/bullet3/tree/master/examples/pybullet/examples)

---

## 🔭 What's Next?

**Day 9 — Adding Sensors.** A robot that can't sense is blind. We'll add cameras, ray (LiDAR-style) sensors, and contact detection so your robot can perceive its world.

---

*"Control is just three questions: what angle, what speed, or what force?"*
