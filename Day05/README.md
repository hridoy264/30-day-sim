# Day 5 — Cart-Pole + Actuation + Python Loop

**Phase 2 · MuJoCo Fundamentals · ~3 hours**

## 🎯 Goal
Build a cart-pole with a motor, then drive it from a **Python control loop**: read state (`qpos`, `qvel`) and write controls (`ctrl`) every step. This loop is the heartbeat of the entire project.

---

## The Model

A cart that slides (`slide` joint) with a pole hinged on top, plus a motor on the cart. Save as `cartpole.xml` (provided):

```xml
<mujoco model="cartpole">
  <option gravity="0 0 -9.81" timestep="0.01"/>
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="5 5 0.1" rgba="0.8 0.9 0.8 1"/>

    <body name="cart" pos="0 0 0.5">
      <joint name="slider" type="slide" axis="1 0 0"/>
      <geom type="box" size="0.2 0.15 0.1" rgba="0.2 0.4 0.9 1"/>
      <body name="pole" pos="0 0 0.1">
        <joint name="hinge" type="hinge" axis="0 1 0"/>
        <geom type="capsule" fromto="0 0 0  0 0 0.6" size="0.04" rgba="0.9 0.4 0.2 1"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <motor name="cart_motor" joint="slider" gear="50" ctrlrange="-1 1"/>
  </actuator>
</mujoco>
```

---

## The Control Loop (the key idea)

MuJoCo splits **`model`** (fixed blueprint) from **`data`** (live state). Each step you read state and write a control:

```python
import mujoco, mujoco.viewer, time
model = mujoco.MjModel.from_xml_path("cartpole.xml")
data  = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as v:
    while v.is_running():
        cart_x   = data.qpos[0]   # READ: cart position
        pole_ang = data.qpos[1]   # READ: pole angle
        # (no controller yet) push a tiny constant force:
        data.ctrl[0] = 0.1        # WRITE: control to the motor
        mujoco.mj_step(model, data)  # ADVANCE physics
        v.sync(); time.sleep(model.opt.timestep)
```

| Array | Meaning |
|-------|---------|
| `data.qpos` | joint **positions** — here `[cart_x, pole_angle]` |
| `data.qvel` | joint **velocities** |
| `data.ctrl` | the **control** you send to actuators |

That READ → WRITE → STEP cycle is *every* controller you'll write, including the line-follower on Day 26.

---

## 📝 Today's Task
- Build `cartpole.xml` and run `cartpole_loop.py`.
- Print `data.qpos` and `data.qvel` each step — watch them change.
- Send a constant `ctrl` and watch the cart accelerate; flip its sign.

---

## ✅ Checkpoint
**You can step the sim and apply controls in a Python loop.**

---

## 📚 Resources
- [MuJoCo Python API](https://mujoco.readthedocs.io/en/stable/python.html)

---

## 🔭 Next
**Day 6 — Your first PID controller. The single most important skill of the month.**
