# Day 2 — Frames, Rigid Bodies & Marine 6-DOF

**Phase 1 · Orientation & MuJoCo Setup · ~2.5 hours**

## 🎯 Goal
Get fluent in the spatial language you'll use all month: frames, rotations, and the six marine degrees of freedom — plus why the timestep matters.

---

## Frames & Rotations

- **Body frame vs world frame.** Every object has its own frame; the world frame is the fixed reference. "Where is the vehicle?" always means *relative to the world frame*. "Where is the camera?" usually means *relative to the body frame*.
- **Rotation matrices** — a 3×3 matrix describing orientation (used internally).
- **Quaternions** `(w, x, y, z)` — four numbers, the robust glitch-free standard MuJoCo uses for orientation. You rarely write them by hand; libraries convert from euler angles for you.

> MuJoCo quaternion order is **`(w, x, y, z)`** — note the `w` is first, unlike some libraries. This trips people up.

---

## The Marine 6-DOF (memorize these)

A free-floating underwater vehicle has **6 degrees of freedom** — 3 translations + 3 rotations — and marine engineering has specific names for each:

| Motion | Axis | Name |
|--------|------|------|
| Translation | forward/back (x) | **surge** |
| Translation | left/right (y) | **sway** |
| Translation | up/down (z) | **heave** |
| Rotation | about x | **roll** |
| Rotation | about y | **pitch** |
| Rotation | about z | **yaw** |

You'll command your vehicle in these terms: "forward thrust" = surge, "turn" = yaw, "dive" = heave. Learn them now; the whole project uses this vocabulary.

---

## Numerical Integration & the Timestep

A simulator advances time in small steps of size `dt` (the **timestep**). Each step it integrates forces → accelerations → velocities → positions.

- **Smaller `dt`** → more accurate and stable, slower.
- **Larger `dt`** → faster, but the integration error grows; objects jitter, pass through each other, or "explode."

MuJoCo's default is `0.002 s`. Underwater dynamics (added mass, drag) can be stiff, so a stable timestep matters even more here.

---

## 📝 Today's Task
- Watch 3Blue1Brown on quaternions and a Steve Brunton control intro.
- In `notes/`, write the 6-DOF table from memory.
- Write one sentence explaining why a too-large timestep destabilizes a sim.

---

## ✅ Checkpoint
**You can explain why a too-large timestep destabilizes a sim**, and name all six marine DOFs.

---

## 📚 Resources
- 3Blue1Brown — *Quaternions* (YouTube / [interactive](https://eater.net/quaternions))
- Steve Brunton — *Control Bootcamp* (YouTube)

---

## 🔭 Next
**Day 3 — MJCF, the MuJoCo XML format: `body`, `joint`, `geom`, `inertial`, `actuator`, `camera`.**
