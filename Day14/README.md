# Day 14 — Sensors & Contacts in MuJoCo

## 🎯 Today's Goal
Add perception to your MuJoCo robot: declare sensors right in the MJCF, read them from Python, and inspect MuJoCo's precise contact information. This is the perception toolkit you'll use for control and RL rewards.

---

## Overview

On Day 9 you added sensors in PyBullet by calling functions. MuJoCo does it differently and elegantly: you **declare sensors in the model file**, and their readings appear automatically in `data.sensordata` every step. MuJoCo's contact data is also famously detailed — important because contacts are where reward signals and grasping logic come from.

---

## Declaring Sensors in MJCF

Sensors go in a `<sensor>` block and reference sites or bodies. First, you place a **`site`** (an invisible reference point) where you want to measure, then attach a sensor to it:

```xml
<worldbody>
  <body name="forearm" pos="0.5 0 0">
    <joint name="elbow" type="hinge" axis="0 1 0"/>
    <geom type="capsule" fromto="0 0 0  0.4 0 0" size="0.04"/>
    <site name="tip" pos="0.4 0 0" size="0.02"/>   <!-- measurement point -->
  </body>
</worldbody>

<sensor>
  <jointpos   name="elbow_angle" joint="elbow"/>
  <jointvel   name="elbow_speed" joint="elbow"/>
  <framepos   name="tip_position" objtype="site" objname="tip"/>
  <accelerometer name="tip_accel" site="tip"/>
</sensor>
```

---

## MuJoCo's Rich Sensor Suite

MuJoCo has many built-in sensors — far more than most simulators offer out of the box:

| Sensor | Measures |
|--------|----------|
| `jointpos` / `jointvel` | joint angle / speed |
| `framepos` / `framequat` | position / orientation of a body or site |
| `accelerometer` | linear acceleration (like a real IMU) |
| `gyro` | angular velocity (IMU) |
| `force` / `torque` | force/torque at a site |
| `touch` | contact pressure on a region |
| `rangefinder` | distance to first object (like LiDAR) |

You compose these to model almost any real sensor.

---

## Reading Sensors from Python

All sensor outputs land in one flat array, `data.sensordata`, in declaration order:

```python
import mujoco
model = mujoco.MjModel.from_xml_path("arm_sensors.xml")
data = mujoco.MjData(model)
mujoco.mj_step(model, data)

print("all sensors:", data.sensordata)

# look up a specific sensor by name (robust to ordering)
sid = model.sensor("elbow_angle").id
adr = model.sensor_adr[sid]
print("elbow angle:", data.sensordata[adr])
```

> 💡 Use the **named lookup** (`model.sensor("name")`) rather than hard-coded indices. When you add or reorder sensors later, named access won't silently break.

---

## Contacts: MuJoCo's Specialty

After a step, every contact lives in `data.contact`. This is more detailed than most engines:

```python
print("number of contacts:", data.ncon)
for i in range(data.ncon):
    c = data.contact[i]
    print("geoms:", c.geom1, c.geom2, " distance:", c.dist)

# the actual contact forces:
import numpy as np
force = np.zeros(6)
mujoco.mj_contactForce(model, data, 0, force)   # force on contact 0
print("contact force:", force[:3])
```

`data.ncon` tells you how many contacts exist this step; `mj_contactForce` gives the actual force vector. This precision is exactly why MuJoCo dominates contact-rich tasks like manipulation and walking — and why its contacts make great RL reward signals.

---

## 📝 Today's Task

1. Add the `<site>` and `<sensor>` block above to your Day-12 `arm.xml`; save as `arm_sensors.xml`.
2. Step it in Python and print `data.sensordata` — watch the elbow angle change as the arm moves.
3. Use **named lookup** to print just the tip's position (`framepos`) each second.
4. Drop the arm onto the floor (no actuation) and print `data.ncon` — watch contacts appear on impact.
5. Use `mj_contactForce` to print the impact force of the tip hitting the ground.

---

## ✅ Key Takeaways

✓ MuJoCo sensors are **declared in the MJCF** (`<sensor>` block), often anchored to a **`site`**.

✓ Readings appear automatically in **`data.sensordata`** every step — no per-step function calls.

✓ Rich built-in sensors: jointpos/vel, framepos/quat, accelerometer, gyro, force/torque, touch, rangefinder.

✓ Look sensors up **by name** (`model.sensor("name")`), not fragile indices.

✓ Contacts (`data.ncon`, `data.contact`, `mj_contactForce`) are detailed — ideal for manipulation & RL rewards.

---

## 📚 References & Resources

- [MuJoCo sensors reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html#sensor)
- [MuJoCo contacts & computation](https://mujoco.readthedocs.io/en/stable/computation/index.html)
- [MuJoCo Python API](https://mujoco.readthedocs.io/en/stable/python.html)

---

## 🔭 What's Next?

**Day 15 — Mini-Project: Balancing a CartPole.** You'll combine MJCF modeling, Python control, and sensing into the classic control challenge — and set the stage perfectly for reinforcement learning in Phase 5.

---

*"Declare what to sense, then just read the array. MuJoCo handles the rest."*
