# Day 27 — Curves, Loss & Mode Switch

**Phase 6 · Autonomy + Robustness · ~3 hours**

## 🎯 Goal
Level up the autonomy: follow **curved** lines, recover when the line is briefly **lost**, and add a clean **teleop ↔ autonomy toggle** (same vehicle, swappable command source).

---

## 1. A Curved Line

A straight line is easy to follow because the error stays small. Curves test your controller. Build a curved path from several offset/rotated segments (see `curved_scene.xml`), or replace the single line geom with a few angled boxes forming an S-curve.

Tune for curves:
- Raise `Kp_yaw` a bit so it turns sharply enough — but not so much it oscillates.
- Lean more on the **heading** error (line angle) on curves; cross-track alone lags on tight turns.
- Slow `FORWARD` on sharp curves so the camera keeps the line in frame.

---

## 2. Line-Loss Recovery

When the detector reports `found=False` for several frames, don't just stop — **search**:

```python
if not found:
    lost += 1
    if lost > 10:
        # search: creep forward and yaw toward last known side
        surge = 0.1
        yaw = 0.4 * np.sign(last_cross)   # turn back toward where it was
    else:
        surge, yaw = 0.1, last_yaw         # briefly hold course
else:
    lost = 0
```

A simple "turn toward where the line last was" recovers most losses on curves and edges.

---

## 3. Teleop ↔ Autonomy Toggle

Make the command **source** swappable so you can fly to the line, then hand off to autonomy — exactly your capstone demo flow. Press a key to toggle:

```python
if key == ord('m'):
    mode = "auto" if mode == "teleop" else "teleop"

if mode == "teleop":
    surge, yaw, heave = read_keys()
else:
    surge, yaw, heave = autonomy_command(rgb)

data.ctrl[:] = allocate(surge, yaw, heave)   # same vehicle, either source
```

See `mode_switch.py`. The key idea: both modes produce the same `(surge, yaw, heave)` tuple, so the vehicle doesn't care which is driving.

---

## 📝 Today's Task
- Build a curved line; tune the controller to follow it (lean on heading error).
- Add line-loss recovery (search behavior) and test by driving off the line.
- Implement the `m`-key teleop↔autonomy toggle.
- Demo the flow: teleop onto the line → press `m` → autonomy takes over a curve.

---

## ✅ Checkpoint
**Follows a curved line; recovers when the line briefly disappears**; teleop↔autonomy toggle works.

---

## 📚 Resources
- Revisit Day 20 (teleop), Day 25 (robust detector), Day 26 (autonomy).

---

## 🔭 Next
**Day 28 — Simulated turbidity & domain randomization: make it survive different water conditions.**
