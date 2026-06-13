# Day 19 — Buffer + Integration

**Phase 4 · Build the Underwater Vehicle · ~2.5 hours (buffer)**

## 🎯 Goal
Get everything from Phase 4 running together in **one Python loop** — dynamics + thrusters + two cameras + the full scene — without choking the M4. This is your integration checkpoint before autonomy.

---

## Why This Day Matters

You've built the pieces across Days 14–18. Before adding vision and autonomy, prove they all run *together* smoothly. A clean, single integrated loop now saves you from debugging tangled problems later. This is also a buffer day — use spare time to fix anything still rough.

---

## The Integrated Loop

`run_all.py` loads `auv_scene.xml` (your Day-18 base), steps physics, renders both cameras, and applies thrust through the Day-15 allocation — all in one loop:

```python
import mujoco, numpy as np, cv2, time

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data  = mujoco.MjData(model)
renderer = mujoco.Renderer(model, 240, 320)

def allocate(surge, yaw, heave):
    return np.clip([surge+yaw, surge-yaw, heave, heave], -1, 1)

def grab(cam):
    renderer.update_scene(data, camera=cam); return renderer.render()

while True:
    data.ctrl[:] = allocate(0.4, 0.0, 0.0)     # gentle forward
    mujoco.mj_step(model, data)
    down  = grab("down")
    front = grab("front")
    cv2.imshow("down|front", np.hstack([
        cv2.cvtColor(down,  cv2.COLOR_RGB2BGR),
        cv2.cvtColor(front, cv2.COLOR_RGB2BGR)]))
    if cv2.waitKey(1) & 0xFF == ord('q'): break
```

---

## Performance Checklist (keep the M4 happy)

- **One `Renderer`**, reused — never recreate it per frame.
- **Modest camera resolution** (320×240 is plenty for line-following).
- You don't need the interactive 3D viewer *and* OpenCV windows at once — for autonomy, the camera feeds are enough.
- If it's slow, render the cameras every N steps instead of every step (the control loop can run faster than the vision loop).
- Watch CPU/thermals; the M4 handles this easily at these settings.

---

## 📝 Today's Task
- Run `run_all.py`: physics + both cameras + thrust in one loop.
- Confirm a stable, smooth frame rate on the Mac.
- Fix any leftover issues from Days 14–18 (camera aim, drag feel, line visibility).
- Commit this as your working Phase-4 base.

---

## ✅ Checkpoint
Dynamics + thrusters + two cameras + scene all run together in one Python loop without choking the M4.

---

## 🔭 Next
**Day 20 — Teleoperation: fly the vehicle by hand with the keyboard or a gamepad.**
