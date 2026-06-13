# Day 6 — Hello PyBullet: Your First Simulation

## 🎯 Today's Goal
Run a real, interactive physics simulation from scratch in PyBullet, and understand every line that makes it work. By the end you'll have a world with gravity, a floor, and falling objects you built yourself.

---

## Overview

Welcome to Phase 2! **PyBullet** is the friendliest simulator to start with: it's pure Python, installs with one `pip` command, runs on any OS, and gives you an interactive 3D window. It's built on the battle-tested **Bullet** physics engine used in films and games. Today you write your first complete simulation and learn the five-step pattern that *every* PyBullet program follows.

---

## The 5-Step PyBullet Pattern

Almost every PyBullet script has the same skeleton. Learn this and you can read any example:

```
1. CONNECT        → open the physics server (with or without a window)
2. CONFIGURE      → set gravity, search paths, time step
3. LOAD           → add the ground, objects, and robots
4. STEP           → run the simulation loop
5. DISCONNECT     → clean up
```

---

## Your First Simulation, Explained Line by Line

Save this as `hello_pybullet.py` (see `hello_pybullet.py` in this folder):

```python
import pybullet as p
import pybullet_data
import time

# 1. CONNECT — p.GUI opens a window; p.DIRECT runs invisibly (faster, for servers)
physicsClient = p.connect(p.GUI)

# 2. CONFIGURE
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # find built-in models
p.setGravity(0, 0, -9.81)                               # Earth gravity, downward

# 3. LOAD
planeId = p.loadURDF("plane.urdf")                      # the ground
startPos = [0, 0, 1]                                    # 1 meter up
startOri = p.getQuaternionFromEuler([0, 0, 0])         # no rotation
boxId = p.loadURDF("r2d2.urdf", startPos, startOri)    # a built-in robot model

# 4. STEP — run for ~10 seconds at 240 Hz
for i in range(2400):
    p.stepSimulation()
    time.sleep(1.0 / 240.0)   # slow to real time so you can watch

# read where the object ended up
pos, ori = p.getBasePositionAndOrientation(boxId)
print("Final position:", pos)

# 5. DISCONNECT
p.disconnect()
```

Run it: `python hello_pybullet.py`. A window opens, R2D2 drops onto the floor and settles. You just ran a physics simulation.

---

## Understanding the Key Pieces

- **`p.connect(p.GUI)`** — starts the physics engine *with* a 3D window. Use `p.DIRECT` for headless/fast runs (no graphics) — important later for training.
- **`pybullet_data`** — ships with ready-made models: `plane.urdf`, `r2d2.urdf`, `cube.urdf`, a KUKA arm, and more. Free robots to play with!
- **`setGravity(0, 0, -9.81)`** — recall Day 3: Z is up, so gravity is *negative* Z. Numbers are in m/s².
- **`getQuaternionFromEuler([...])`** — exactly the euler→quaternion idea from Day 3, built right in.
- **`stepSimulation()`** — advances the world by one time step (default `1/240` s). This is the loop from Day 2!
- **`time.sleep(1/240)`** — without it, the sim runs as fast as possible (good for training, too fast to watch).

---

## Exploring the GUI

Once the window is open, you can:

- **Rotate** the camera: hold **Ctrl + left-drag** (or just drag, depending on platform).
- **Zoom**: scroll wheel.
- **Pan**: Ctrl + middle-drag.

Try moving the camera while R2D2 falls. Getting comfortable navigating the 3D view pays off all course.

---

## 📝 Today's Task

1. Run `hello_pybullet.py` and watch R2D2 fall.
2. **Experiment** — change one thing at a time and observe:
   - Start position `[0, 0, 3]` (higher drop).
   - Gravity `setGravity(0, 0, -1.6)` (the Moon!).
   - Swap `"r2d2.urdf"` for `"duck_vhacd.urdf"` or load your `my_first_robot.urdf` from Day 5.
3. Load **two** objects at different positions and watch them both fall.
4. Print the final position and note how it changed with your tweaks.

---

## ✅ Key Takeaways

✓ Every PyBullet program follows: **connect → configure → load → step → disconnect**.

✓ `p.GUI` opens a window; `p.DIRECT` runs headless and fast (used for training later).

✓ `pybullet_data` provides free built-in models like `plane.urdf` and `r2d2.urdf`.

✓ `stepSimulation()` is the Day-2 simulation loop in code; `time.sleep` just slows it to watch.

✓ Gravity is **negative Z** because Z is up — the Day-3 conventions in action.

---

## 📚 References & Resources

- [PyBullet Quickstart Guide](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit)
- [PyBullet website & examples](https://pybullet.org/wordpress/)
- [Bullet physics GitHub (with examples)](https://github.com/bulletphysics/bullet3)

---

## 🔭 What's Next?

**Day 7 — Loading Robots & Worlds from URDF.** We go deeper into loading: spawning your own URDFs, inspecting a robot's joints and links, and setting up a proper scene.

---

*"Five lines stand between you and a working physics simulation. You just wrote them."*
