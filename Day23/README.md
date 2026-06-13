# Day 23 — Second Camera Use

**Phase 5 · Teleoperation + Vision · ~2.5 hours**

## 🎯 Goal
Put the forward/second camera to work — for **altitude-hold** over the seabed (keeping a steady height) or as a forward situational view. Keep it simple; one usable signal is the goal.

---

## Why a Second Camera?

The downward camera follows the line. The second camera adds a second sense — most usefully, *how high above the seabed am I?* Holding a steady altitude keeps the line in focus and at a consistent scale, which makes the Day-21 detection more reliable.

Pick **one** simple use; don't over-engineer:

### Option A — Altitude-hold via depth (simplest)
You already enabled depth rendering on Day 10. Render the downward (or forward-down) depth image and read the distance to the seabed at the image center:

```python
renderer.enable_depth_rendering()
renderer.update_scene(data, camera="down")
depth = renderer.render()
altitude = float(depth[depth.shape[0]//2, depth.shape[1]//2])   # meters to seabed
renderer.disable_depth_rendering()
```

Then a simple P-controller on `heave` holds a target altitude:

```python
heave = Kp_alt * (target_altitude - altitude)
```

### Option B — Rough stereo / known-baseline trick
If you mounted a forward stereo pair, estimate distance from disparity. This is more involved — only attempt if Option A bores you.

### Option C — Forward view only
Just display the forward camera for situational awareness (no signal). Perfectly fine if you're short on time — the line-follower works without it.

---

## Keep It Simple

The plan's guidance: **keep it simple.** Altitude-hold (Option A) gives the most value for the least code and directly improves line detection. Get one clean signal and move on — Phase 6 autonomy is where the time should go.

See `altitude_hold.py` for the Option-A pattern.

---

## 📝 Today's Task
- Implement altitude-hold (Option A): read seabed distance from the depth image, P-control `heave` to a target.
- Confirm the vehicle settles to and holds a steady height.
- (Or) wire the forward camera as a view, if you choose Option C.

---

## ✅ Checkpoint
**Second camera contributes a usable signal** (e.g., altitude-hold holds a steady height).

---

## 📚 Resources
- [MuJoCo depth rendering](https://mujoco.readthedocs.io/en/stable/python.html#rendering)
- [Stereo disparity basics (OpenCV)](https://docs.opencv.org/4.x/dd/d53/tutorial_py_depthmap.html)

---

## 🔭 Next
**Day 24 — Buffer + logging: save frames and state to debug detection offline.**
