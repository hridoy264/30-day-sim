# Day 6 — Your First PID

**Phase 2 · MuJoCo Fundamentals · ~3 hours**

## 🎯 Goal
Write a PID controller that balances the cart-pole (or holds a joint angle). Tune it by hand and plot the error. **This is the most important skill of the month** — every autonomous behavior you build is a control loop.

---

## What is PID?

PID turns an **error** (how far you are from where you want to be) into a **control action**. Three terms, each fixing a different problem:

| Term | Reacts to | Effect |
|------|-----------|--------|
| **P** (proportional) | the current error | push harder the further off you are |
| **I** (integral) | accumulated past error | eliminate steady offset that P leaves behind |
| **D** (derivative) | rate of change of error | damp oscillation, anticipate |

```
output = Kp*error + Ki*∫error dt + Kd*(d error/dt)
```

For balancing the pole, the error is the pole angle (0 = upright). For your AUV later, the error will be "how far the line is from the camera center." Same controller, different error.

---

## The Controller

See `pid_cartpole.py`:

```python
import numpy as np, mujoco, mujoco.viewer, time

model = mujoco.MjModel.from_xml_path("cartpole.xml")  # reuse Day 5's model
data  = mujoco.MjData(model)
data.qpos[1] = 0.1                 # start the pole tilted
mujoco.mj_forward(model, data)

Kp, Ki, Kd = 12.0, 0.0, 2.0        # tune these by hand
integral, prev_err = 0.0, 0.0
dt = model.opt.timestep
errors = []

with mujoco.viewer.launch_passive(model, data) as v:
    while v.is_running():
        error = data.qpos[1]                 # pole angle (want 0)
        integral += error * dt
        deriv = (error - prev_err) / dt
        u = Kp*error + Ki*integral + Kd*deriv
        data.ctrl[0] = np.clip(u, -1, 1)     # send to motor
        prev_err = error
        errors.append(error)
        mujoco.mj_step(model, data); v.sync()
        time.sleep(dt)
```

---

## Tuning by Hand (the craft)

A practical recipe:

1. Start with `Ki=Kd=0`. Raise **`Kp`** until the pole *almost* balances but oscillates.
2. Add **`Kd`** to damp the oscillation until it's smooth.
3. Add a little **`Ki`** only if there's a stubborn steady offset.

- `Kp` too low → too weak, pole falls. Too high → violent oscillation.
- `Kd` too high → sluggish, jittery from noise.

Plot the error over time with matplotlib to *see* your tuning improve — a settling, shrinking curve means good gains.

---

## ✅ Checkpoint
**A working closed control loop.** (The pole balances; your error plot settles toward zero.)

---

## 📚 Resources
- Brian Douglas — *PID Control* video series (YouTube)
- [PID controller (overview)](https://en.wikipedia.org/wiki/PID_controller)

---

## 🔭 Next
**Day 7 — Buffer / consolidate. Fix breakage and write the core concepts in your own words.**
