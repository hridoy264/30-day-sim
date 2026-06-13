# Day 12 — MuJoCo Fluid Forces in Practice

**Phase 3 · Marine Dynamics + MuJoCo Fluid · ~3 hours**

## 🎯 Goal
Make MuJoCo model water. Set medium **density** and **viscosity**, enable the **ellipsoid fluid model** on a geom, drop a body in "water," and tune the drag.

---

## How MuJoCo Does Fluids

MuJoCo can simulate a body moving through a fluid medium using two layers:

### 1. The medium (global, in `<option>`)
Set the surrounding fluid's properties:

```xml
<option gravity="0 0 -9.81" timestep="0.002"
        density="1000"        <!-- water ≈ 1000 kg/m³ (air ≈ 1.2) -->
        viscosity="0.001"/>   <!-- water's viscosity -->
```

Density alone already gives you **buoyancy and basic drag** via MuJoCo's inertia-box model.

### 2. The ellipsoid fluid model (per-geom, more realistic)
For richer, tunable drag, enable the ellipsoid model on a geom with `fluidshape`:

```xml
<geom type="box" size="0.2 0.15 0.1" density="1000"
      fluidshape="ellipsoid"
      fluidcoef="0.5 0.25 1.5 1.0 1.0"/>
```

The five `fluidcoef` numbers control blunt drag, slender drag, angular drag, and lift terms. You **tune these** until the body's drag looks right.

---

## Experiment: Drop a Body in Water

See `water_drag.xml`. Drop a body with the medium set to water and watch it sink *slowly* (drag) instead of falling fast:

```bash
python -m mujoco.viewer --mjcf=water_drag.xml
```

Compare: temporarily set `density="1.2"` (air) and it falls fast; `density="1000"` (water) and it drifts down gently. That difference *is* fluid drag.

---

## Tuning the 5 Ellipsoid Parameters

There's no single correct set — tune for the behavior you want:

- Body falls/accelerates too fast → increase drag coefficients.
- Body stops too abruptly → decrease them.
- Spins too freely → increase the angular drag term.

Study MuJoCo's `balloons.xml` example to see fluid parameters used in a working model.

> Keep notes on which `fluidcoef` values give a "watery" feel — you'll reuse them on the vehicle in Phase 4.

---

## ✅ Checkpoint
**A body experiences realistic-looking drag in your sim** (sinks/glides like it's underwater, not in air).

---

## 📚 Resources
- [MuJoCo fluid forces docs](https://mujoco.readthedocs.io/en/stable/computation/fluid.html)
- `balloons.xml` example (in the MuJoCo model set) for fluid usage

---

## 🔭 Next
**Day 13 — Buoyancy: make a body neutrally buoyant (hover), plus a light ROS 2 concepts skim.**
