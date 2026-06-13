# Day 26 — Close the Autonomy Loop

**Phase 6 · Autonomy + Robustness · ~3 hours**

## 🎯 Goal
Connect vision to control: cross-track + heading error → two PID loops (yaw + lateral) → thrust vector, with constant forward thrust. **The vehicle follows the line by itself.** This is the payoff of the whole month.

---

## The Complete Loop

Everything you've built clicks together here:

```
   down camera ─▶ robust detector ─▶ (cross, heading) ─▶ PID ─▶ allocate() ─▶ thrusters
        ▲                                                                         │
        └──────────────────────── vehicle moves ◀────────────────────────────────┘
```

It's the **sense → think → act** loop, underwater. Sense = Day 25 detector. Think = PID. Act = Day 15 allocation.

---

## The Controller

Two PIDs convert the two errors into a steering command, plus constant surge to keep moving (`autonomy_loop.py`):

```python
from robust_detect import RobustDetector
det = RobustDetector()

# yaw PID drives the line to image center (cross-track -> 0)
Kp_yaw, Kd_yaw = 1.2, 0.3
prev_cross = 0.0
FORWARD = 0.35                      # constant surge

while running:
    mujoco.mj_step(model, data)
    rgb = grab("down")
    found, cross, heading, edge = det.errors(rgb)

    # steering: combine cross-track and heading error
    d_cross = cross - prev_cross
    yaw = -(Kp_yaw * cross + Kd_yaw * d_cross)   # turn toward the line
    prev_cross = cross

    surge = FORWARD if found else 0.1            # slow if unsure
    data.ctrl[:] = allocate(surge, yaw, 0.0)
```

> **Sign check:** if the line is to the *right* (`cross > 0`), the vehicle must yaw right to center it. If it veers *away* from the line, flip the sign on `yaw`. This one sign is the most common bug — expect to fix it.

---

## Tuning Tips

- Start with only the P term on cross-track. Raise `Kp_yaw` until it tracks but wobbles.
- Add `Kd_yaw` to smooth the wobble (your Day-6 PID skills, applied).
- Keep `FORWARD` modest at first — slower = more forgiving while tuning.
- Blend in heading error once cross-track works, for smoother tracking on angled segments.

---

## 📝 Today's Task
- Wire the Day-25 detector into a yaw PID and constant forward thrust.
- Get the vehicle to follow a **straight** line autonomously, staying centered.
- Fix the yaw sign if it runs away from the line.
- Tune `Kp_yaw`/`Kd_yaw` for steady, centered tracking.

---

## ✅ Checkpoint
**Vehicle follows a straight line autonomously.** 🎉

---

## 📚 Resources
- Revisit Day 6 (PID), Day 15 (allocation), Day 25 (robust detector).

---

## 🔭 Next
**Day 27 — Curves, line loss, and a clean teleop↔autonomy mode switch.**
