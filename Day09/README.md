# Day 9 — Contacts, Sensors & the Floor

**Phase 2 · MuJoCo Fundamentals · ~2.5 hours**

## 🎯 Goal
Add a floor, drop a box, tune friction, and read MuJoCo's built-in sensors. Understand why **contacts cause most sim instability** — knowledge you'll need when your vehicle meets the seabed.

---

## Contacts: Where Sims Go Wrong

A "contact" is two geoms touching. Resolving contacts is the hardest, stiffest part of physics — and the usual cause of jitter, sinking, or "exploding" sims. Common culprits:

- **Timestep too large** for the contact stiffness → instability (Day 2).
- **Bad friction or solver settings** → objects slide wrong or vibrate.
- **Complex collision meshes** → slow and unstable; prefer simple shapes (boxes, capsules, spheres).

Drop a box on a floor and experiment (`contacts_sensors.xml`):

```xml
<mujoco model="drop">
  <option gravity="0 0 -9.81" timestep="0.002"/>
  <worldbody>
    <light pos="0 0 3"/>
    <geom name="floor" type="plane" size="3 3 0.1" friction="1 0.005 0.0001"/>
    <body name="box" pos="0 0 1">
      <freejoint/>
      <geom type="box" size="0.1 0.1 0.1" density="500"/>
      <site name="imu_site" pos="0 0 0"/>
    </body>
  </worldbody>
  <sensor>
    <gyro name="gyro" site="imu_site"/>
    <accelerometer name="acc" site="imu_site"/>
    <framepos name="pos" objtype="site" objname="imu_site"/>
  </sensor>
</mujoco>
```

The `friction` attribute is `(sliding, torsional, rolling)`. Tune the first number and watch how the box slides on landing.

---

## Sensors

MuJoCo sensors are **declared in the model** and read from `data.sensordata`:

| Sensor | Measures | Used later for |
|--------|----------|----------------|
| `gyro` | angular velocity | heading/attitude (IMU) |
| `accelerometer` | linear acceleration | IMU |
| `framepos` / `framequat` | position / orientation | knowing where the vehicle is |

```python
import mujoco
model = mujoco.MjModel.from_xml_path("contacts_sensors.xml")
data  = mujoco.MjData(model)
for _ in range(500):
    mujoco.mj_step(model, data)
print("sensordata:", data.sensordata)
print("num contacts this step:", data.ncon)
```

`data.ncon` is the number of contacts in the current step — watch it jump from 0 to nonzero the instant the box lands.

---

## 📝 Today's Task
- Drop the box; tune `friction` and the timestep; find a setting that's stable vs one that jitters.
- Read `gyro`, `accelerometer`, and `framepos` from `data.sensordata`.
- Print `data.ncon` over time and note when contacts appear.

---

## ✅ Checkpoint
**You understand why contacts cause most sim instability**, and you can read MuJoCo sensors.

---

## 📚 Resources
- [MuJoCo sensors reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html#sensor)
- [MuJoCo computation / contacts](https://mujoco.readthedocs.io/en/stable/computation/index.html)

---

## 🔭 Next
**Day 10 — Offscreen camera rendering: grab a camera image as a NumPy array. The bridge to your vision pipeline.**
