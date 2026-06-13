# Day 24 — Buffer + Logging

**Phase 5 · Teleoperation + Vision · ~2.5 hours (buffer)**

## 🎯 Goal
Add logging so you can debug detection failures *offline*: save camera frames and state to disk, and record a few test clips. Plus catch up on anything outstanding.

---

## Why Log?

When the line-follower misbehaves on Day 26–27, you won't be able to debug it live — it moves too fast and fails intermittently. Logged frames + state let you replay exactly what the camera saw the moment it failed. Good logging turns "it sometimes breaks" into "it breaks on frame 412, here's why."

---

## What to Log

For each step (or every Nth step), save:
- the **downward camera frame** (so you can re-run detection on it),
- the **detected errors** (`cross_track`, `heading`, `found`),
- the **vehicle state** (`data.qpos`, `data.time`),
- the **command** sent (`surge`, `yaw`, `heave`).

See `logger.py`:

```python
import os, csv, cv2
os.makedirs("logs/frames", exist_ok=True)
log = open("logs/run.csv", "w", newline="")
w = csv.writer(log); w.writerow(["t","found","cross","heading","surge","yaw","heave"])

# in the loop, every few steps:
cv2.imwrite(f"logs/frames/{frame_i:05d}.png", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
w.writerow([data.time, found, cross, heading, surge, yaw, heave])
```

---

## Save Test Clips

Record short videos of representative runs (straight line, near a curve, line briefly lost) with OpenCV's `VideoWriter`:

```python
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("logs/clip.mp4", fourcc, 30, (320, 240))
# each frame:
out.write(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
```

These clips are gold for Day 25 robustness work *and* for your Day-30 capstone demo.

---

## Offline Replay

A tiny script that re-runs `line_errors()` over saved frames lets you tune HSV/detection without launching the sim each time — much faster iteration.

---

## 📝 Today's Task
- Add `logger.py`: write frames + a CSV of errors/state/commands each run.
- Record 2–3 short clips of different situations.
- Write a 5-line replay script that runs detection over saved frames.
- Use the buffer time to fix any lingering Phase-5 issues.

---

## ✅ Checkpoint
You can save camera frames + state to disk and replay them offline; a few test clips saved.

---

## 📚 Resources
- [OpenCV — VideoWriter](https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html)
- [Python csv module](https://docs.python.org/3/library/csv.html)

---

## 🔭 Next
**Day 25 — Robustness pass: make the detector survive occlusion and brief line loss.**
