# Day 29 — Buffer + Tuning

**Phase 6 · Autonomy + Robustness · ~2.5 hours (buffer)**

## 🎯 Goal
Final polish. Do your last tuning pass and build **one repeatable launch script** that runs the whole demo: build the sim → teleop to the line → switch to autonomy. This makes tomorrow's capstone recording effortless.

---

## Final Tuning Pass

Go through the system one last time:

- **Controller gains** — re-tune `Kp_yaw`/`Kd_yaw` for smooth, centered tracking on both straight and curved lines.
- **Detector** — confirm the HSV range + morphology handle your turbidity conditions (Day 28).
- **Speeds** — pick a `FORWARD` thrust that's brisk but keeps the line reliably in frame.
- **Recovery** — verify line-loss search actually re-acquires the line.
- **Performance** — confirm a smooth frame rate on the M4 throughout.

---

## One Repeatable Launch

A single script should run the entire demo flow so you (and anyone you show) can reproduce it with one command (`run_demo.py`):

```python
# 1. build the sim from auv_scene.xml
# 2. start in TELEOP   -> you fly the vehicle onto the line
# 3. press 'm'         -> AUTONOMY takes over, follows the line
# 4. (optional) press a key to cycle water conditions
# 5. 'q' quits
```

This is essentially your Day-27 `mode_switch.py` cleaned up: clear on-screen instructions, a tidy HUD (mode, errors), and sensible defaults. The goal is a polished, one-command experience.

> Put `run_demo.py`, `auv_scene.xml`, and `robust_detect.py` together in your `auv-project/` folder so the demo runs standalone.

---

## Pre-Capstone Checklist

- [ ] Teleop flies smoothly.
- [ ] Autonomy follows a straight line, centered.
- [ ] Autonomy handles a curve.
- [ ] Line-loss recovery works.
- [ ] Survives 3+ water conditions.
- [ ] One command launches the whole demo.
- [ ] No crashes during a full run.

If every box is checked, you're ready to record.

---

## 📝 Today's Task
- Final-tune gains, detector, and speeds.
- Build `run_demo.py`: one command → teleop → autonomy → (water conditions).
- Run the pre-capstone checklist and fix any gaps.
- Do a full dry-run of the demo end to end.

---

## ✅ Checkpoint
A single script reproducibly runs: build sim → teleop to line → switch to autonomy, with no crashes.

---

## 🔭 Next
**Day 30 — Capstone: record the full demo and write it up.**
