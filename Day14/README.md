# Day 14 — Vehicle Body + Free Joint

**Phase 4 · Build the Underwater Vehicle · ~2.5 hours**

## 🎯 Goal
Model a BlueROV2-like vehicle as a single rigid body on a 6-DOF `freejoint`, give it mass/inertia, and place it in your water world so it responds to drag and buoyancy.

---

## The Vehicle Body

Start simple: one rigid body (we'll add thrusters tomorrow, cameras on Day 17). A `freejoint` gives it all 6 DOF (surge/sway/heave/roll/pitch/yaw). Save as `auv_body.xml` (provided):

```xml
<mujoco model="auv">
  <option gravity="0 0 -9.81" timestep="0.004" density="1000" viscosity="0.001"/>

  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="10 10 0.1" pos="0 0 -3" rgba="0.25 0.35 0.45 1"/>

    <body name="rov" pos="0 0 0" gravcomp="1">     <!-- neutral buoyancy -->
      <freejoint/>
      <!-- main hull -->
      <geom type="box" size="0.23 0.15 0.10" density="1000"
            fluidshape="ellipsoid" fluidcoef="0.5 0.25 1.5 1.0 1.0"
            rgba="0.95 0.65 0.15 1"/>
      <!-- a small nose marker so you can see its heading -->
      <geom type="capsule" fromto="0.23 0 0  0.30 0 0" size="0.02" rgba="0.1 0.1 0.1 1"/>
    </body>
  </worldbody>
</mujoco>
```

Key choices:
- **`gravcomp="1"`** — neutral buoyancy from Day 13, so it hovers.
- **`fluidshape="ellipsoid"`** — drag from Day 12, so it glides like an ROV.
- **`timestep="0.004"`** — a stable step for fluid dynamics on the Mac (tune if unstable).
- The nose marker lets you *see* which way it's pointing — essential once it moves.

---

## Run & Poke It

```bash
python -m mujoco.viewer --mjcf=auv_body.xml
```

In the viewer, **double-click the body and drag** to apply a force. It should:
- Hover (not sink or float away) — buoyancy is right.
- Glide and slow to a stop — drag is right.
- Not spin forever — if it does, you'll add angular damping on Day 16.

---

## 📝 Today's Task
- Build `auv_body.xml`; confirm it hovers in water.
- Drag it around in the viewer — does it glide and settle like a vehicle?
- Adjust hull `size`/`density` and `gravcomp` until it feels neutrally buoyant.

---

## ✅ Checkpoint
**A 6-DOF body floats in water and responds to drag.**

---

## 📚 Resources
- [MuJoCo freejoint & body](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-freejoint)

---

## 🔭 Next
**Day 15 — Thrusters: add force actuators and map a thrust-vector command to them (control allocation).**
