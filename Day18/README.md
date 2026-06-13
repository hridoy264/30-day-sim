# Day 18 — Build the Seabed + Line

**Phase 4 · Build the Underwater Vehicle · ~2.5 hours**

## 🎯 Goal
Add a textured seabed and a high-contrast line/pipe for the vehicle to follow, plus enough lighting/brightness that the downward camera sees it clearly. This is the scene your autonomy will run in.

---

## The Seabed

A textured floor reads as a seabed and gives the camera visual variety (so the line stands out). Use a checker texture via `<asset>`:

```xml
<asset>
  <texture name="seabed" type="2d" builtin="checker"
           rgb1="0.2 0.3 0.35" rgb2="0.25 0.4 0.45" width="300" height="300"/>
  <material name="seabed_mat" texture="seabed" texrepeat="20 20"/>
</asset>
...
<geom name="seabed" type="plane" size="10 10 0.1" pos="0 0 -1.5"
      material="seabed_mat"/>
```

---

## The Line

The line is a long, thin, **high-contrast** geom laid on the seabed. Bright yellow on a blue-grey seabed is easy for the camera to threshold (Day 21):

```xml
<!-- straight line segment; add more segments later for curves -->
<geom name="line" type="box" pos="0 0 -1.49" size="0.06 5 0.005"
      rgba="1 0.85 0.1 1"/>
```

> For Day 27 (curves), you'll add several rotated/offset segments to form a curved path. A straight line is enough to get autonomy working first.

---

## Lighting / Vehicle Brightness

Underwater scenes are dark. Make sure the downward camera sees the line by adding light — either a scene light or a "vehicle light" that rides with the ROV:

```xml
<body name="rov" ...>
  ...
  <light name="headlight" pos="0 0 -0.05" dir="0 0 -1" diffuse="0.8 0.8 0.8"/>
</body>
```

A downward light attached to the vehicle keeps the line lit no matter where the ROV goes — exactly like a real ROV's lamps.

---

## Full Scene

`auv_scene.xml` (provided) combines: tuned vehicle + thrusters + two cameras + seabed texture + line + vehicle light. **This file is your project base from here on.** Render the down camera and confirm the line is unmistakable.

---

## 📝 Today's Task
- Build `auv_scene.xml`: seabed texture + bright line + vehicle light.
- Render the `down` camera; confirm the line is clearly visible and high-contrast.
- Drive over the line and watch it pass through the downward view.
- Tweak line color/width and lighting until detection will be easy.

---

## ✅ Checkpoint
**The line is clearly visible in the downward camera.**

---

## 📚 Resources
- [MuJoCo assets — textures & materials](https://mujoco.readthedocs.io/en/stable/XMLreference.html#asset)
- [MuJoCo lights](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-light)

---

## 🔭 Next
**Day 19 — Buffer + integration: get dynamics + thrusters + two cameras + scene all running in one loop.**
