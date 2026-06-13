# Day 4 — Pendulum From Scratch

**Phase 2 · MuJoCo Fundamentals · ~2.5 hours**

## 🎯 Goal
Write your **own** MJCF file — a simple pendulum — add gravity and damping, and watch it swing. Your first model built by hand.

---

## The Model

A pendulum is one body on a single `hinge` joint. Save as `pendulum.xml` (provided in this folder):

```xml
<mujoco model="pendulum">
  <option gravity="0 0 -9.81" timestep="0.002"/>
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="2 2 0.1" rgba="0.8 0.9 0.8 1"/>

    <body name="arm" pos="0 0 1">
      <joint name="pivot" type="hinge" axis="0 1 0" damping="0.1"/>
      <geom type="capsule" fromto="0 0 0  0.5 0 0" size="0.03" rgba="0.2 0.4 0.9 1"/>
      <geom type="sphere" pos="0.5 0 0" size="0.06" rgba="0.9 0.3 0.2 1"/>
    </body>
  </worldbody>
</mujoco>
```

Key parts:
- `type="hinge"` — rotation about the `axis="0 1 0"` (the y-axis).
- `damping="0.1"` — friction in the joint, so the swing slowly dies out. Set it to `0` and it swings forever.
- The pendulum starts horizontal and falls under gravity.

---

## Run It

```bash
python -m mujoco.viewer --mjcf=pendulum.xml
```

Or step it in Python and watch the angle (`swing.py`):

```python
import time, mujoco, mujoco.viewer
model = mujoco.MjModel.from_xml_path("pendulum.xml")
data  = mujoco.MjData(model)
data.qpos[0] = 1.2   # start tilted
mujoco.mj_forward(model, data)
with mujoco.viewer.launch_passive(model, data) as v:
    while v.is_running():
        mujoco.mj_step(model, data); v.sync()
        time.sleep(model.opt.timestep)
```

---

## 📝 Experiment
- Set `damping="0"` → perpetual swing. Set `damping="2"` → it barely moves.
- Change the capsule length and mass (add `density=`) — note how the period changes.
- Set the start angle (`data.qpos[0]`) to different values.

---

## ✅ Checkpoint
**Your own `.xml` loads and swings.**

---

## 📚 Resources
- [MuJoCo XML reference — joint](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-joint)

---

## 🔭 Next
**Day 5 — Cart-pole with a motor, and your first Python control loop (read state, write controls).**
