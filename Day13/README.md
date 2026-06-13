# Day 13 — Simulating & Controlling from Python

## 🎯 Today's Goal
Drive a MuJoCo model entirely from Python: load a model, step the physics, read state, and send control commands in a loop. This is the core pattern behind every MuJoCo behavior and RL environment.

---

## Overview

The viewer sliders were fun, but real work happens in code. Today you learn MuJoCo's Python API — and the great news is it mirrors the PyBullet loop you already know (connect/load → step → read/command). Master this small pattern and you can build anything in MuJoCo.

---

## The Two Core Objects: `model` and `data`

MuJoCo splits everything into two pieces — a distinction worth understanding:

- **`model`** — the *unchanging* description: bodies, joints, masses (loaded from your MJCF). It doesn't change as the sim runs.
- **`data`** — the *changing* state: current positions, velocities, forces, time. This updates every step.

```python
import mujoco

model = mujoco.MjModel.from_xml_path("arm.xml")   # the fixed description
data  = mujoco.MjData(model)                       # the live state
```

Think: `model` = the robot's blueprint; `data` = the robot right now.

---

## The Simulation Loop

Stepping is one call — `mj_step` — which is the Day-2 loop under the hood:

```python
for _ in range(1000):
    mujoco.mj_step(model, data)     # advance physics by one timestep
    print(data.time, data.qpos)     # qpos = joint positions
```

Key state arrays on `data`:

| Array | Meaning |
|-------|---------|
| `data.qpos` | joint **positions** (generalized coordinates) |
| `data.qvel` | joint **velocities** |
| `data.ctrl` | the **control** signal you set (drives actuators) |
| `data.time` | current sim time |
| `data.sensordata` | sensor readings (Day 14) |

---

## Sending Commands

You control the robot by writing to `data.ctrl` — one entry per actuator (in the order you defined them in the MJCF):

```python
data.ctrl[0] = 0.5   # shoulder target (it's a position actuator)
data.ctrl[1] = -0.3  # elbow target
```

That's the whole control interface. Set `ctrl`, step, repeat.

---

## A Complete Controlled Run (with viewer)

See `control_arm.py`. It loads the Day-12 arm and drives it with a sine wave, rendered live:

```python
import time, mujoco, mujoco.viewer, numpy as np

model = mujoco.MjModel.from_xml_path("arm.xml")
data  = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    start = time.time()
    while viewer.is_running() and time.time() - start < 30:
        t = data.time
        data.ctrl[0] = np.sin(t)          # shoulder waves
        data.ctrl[1] = 0.5 * np.sin(2*t)  # elbow waves faster
        mujoco.mj_step(model, data)
        viewer.sync()                     # update the window
        time.sleep(model.opt.timestep)
```

`launch_passive` opens a viewer that *doesn't* block your loop, so your code controls the robot while you watch. Run it and the arm dances to your sine waves — the same `sin(t)` trick from Day 8, now in MuJoCo.

---

## Resetting the Simulation

For experiments and RL you'll reset often:

```python
mujoco.mj_resetData(model, data)   # back to the model's initial state
data.qpos[0] = 0.3                  # optionally set a custom start
mujoco.mj_forward(model, data)      # recompute derived quantities
```

`mj_resetData` is your "start over" button — essential for the RL phase.

---

## 📝 Today's Task

1. Run `control_arm.py` and watch your Day-12 arm move under Python control.
2. Print `data.qpos` and `data.qvel` each step — watch the numbers change as it moves.
3. Replace the sine waves with a **step command**: hold `ctrl = [1.0, -1.0]` and watch the arm move to that pose and settle.
4. Add `mj_resetData` every 500 steps so the arm repeatedly restarts — preview of RL episodes.
5. Run *without* the viewer (just the loop) and time 10,000 steps — notice how fast headless MuJoCo is.

---

## ✅ Key Takeaways

✓ MuJoCo splits **`model`** (fixed blueprint) from **`data`** (live state) — blueprint vs. right now.

✓ `mujoco.mj_step(model, data)` advances physics one timestep (the Day-2 loop).

✓ Read state from `data.qpos` / `data.qvel`; command actuators by writing `data.ctrl`.

✓ `launch_passive` gives a non-blocking viewer so your code drives while you watch.

✓ `mj_resetData` restarts the sim — the foundation of RL episodes (Phase 5).

---

## 📚 References & Resources

- [MuJoCo Python API](https://mujoco.readthedocs.io/en/stable/python.html)
- [MuJoCo programming guide](https://mujoco.readthedocs.io/en/stable/programming/index.html)
- [mj_step / data structures reference](https://mujoco.readthedocs.io/en/stable/APIreference/index.html)

---

## 🔭 What's Next?

**Day 14 — Sensors & Contacts in MuJoCo.** We add perception: MuJoCo's rich built-in sensor suite and its precise contact information, so your code can feel the world.

---

*"model is the blueprint, data is the heartbeat. Step, read, command — repeat."*
