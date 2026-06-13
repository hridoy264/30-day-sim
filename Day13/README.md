# Day 13 — Buoyancy + ROS Concepts (light)

**Phase 3 · Marine Dynamics + MuJoCo Fluid · ~2.5 hours**

## 🎯 Goal
Make a body **neutrally buoyant** so it hovers, and skim ROS 2 concepts (on the Linux machine) for future use. Neutral buoyancy is what lets your vehicle "fly" through water.

---

## Block A — Buoyancy (1.5 hr)

A neutrally buoyant body neither sinks nor rises — it hovers, so thrusters only need to *move* it, not hold it up. Two ways to achieve it in MuJoCo:

### Option 1: `gravcomp` (simplest)
`gravcomp="1"` on a body cancels exactly its own weight (1.0 = full cancellation = neutral buoyancy):

```xml
<body name="rov" pos="0 0 1" gravcomp="1">
  <freejoint/>
  <geom type="box" size="0.2 0.15 0.1" density="1000"
        fluidshape="ellipsoid" fluidcoef="0.5 0.25 1.5 1.0 1.0"/>
</body>
```

- `gravcomp="1"` → neutral (hovers).
- `gravcomp="0.9"` → slightly negative buoyancy (sinks slowly — realistic for many ROVs).
- `gravcomp="1.1"` → positive (rises).

### Option 2: explicit buoyancy force (more physical)
Each step, apply an upward force equal to the displaced water's weight (`ρ_water · V · g`) at the center of buoyancy. See `buoyancy.py` for the pattern using `data.xfrc_applied`. This is more work but lets you place the center of buoyancy *above* the center of mass for self-righting (the weeble effect from Day 11).

```python
import numpy as np, mujoco
# ... each step:
rho, V, g = 1000.0, 0.006, 9.81           # water density, volume, gravity
F_buoy = rho * V * g                        # upward force (N)
data.xfrc_applied[body_id, :3] = [0, 0, F_buoy]   # apply to the body
mujoco.mj_step(model, data)
```

---

## Block B — ROS 2 Concepts, light (1 hr, on Linux, optional)

Not used in the Mac project, but useful for the future Stonefish/hardware step. Just skim:

- **Nodes** — small programs that do one job.
- **Topics** — named channels nodes use to exchange **messages**.
- **Publish / subscribe** — send to / receive from a topic.

A real robot is many nodes passing messages. You'll recognize this if you later port to Stonefish + ROS 2.

---

## 📝 Today's Task
- Make a body hover with `gravcomp="1"`; then make it slowly sink and rise.
- Try the explicit buoyancy force in `buoyancy.py` and place the buoyancy point above the COM — watch it self-right.
- (Optional, Linux) Read the ROS 2 nodes/topics tutorial intro.

---

## ✅ Checkpoint
**You can make a body neutrally buoyant.**

---

## 📚 Resources
- [MuJoCo `gravcomp` (body attribute)](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body)
- [ROS 2 tutorials](https://docs.ros.org)

---

## 🔭 Next
**Day 14 — Phase 4 begins: model the vehicle body on a 6-DOF free joint.**
