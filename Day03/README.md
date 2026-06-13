# Day 3 — MJCF: The MuJoCo XML Format

**Phase 1 · Orientation & MuJoCo Setup · ~2.5 hours**

## 🎯 Goal
Be able to read any MJCF (`.xml`) file and name what each element does. This is the format you'll write the whole vehicle in.

---

## The Core Elements

MJCF describes a world by nesting bodies. The elements you'll use constantly:

| Element | Role |
|---------|------|
| `<worldbody>` | the root; everything lives inside it |
| `<body>` | a rigid body (a link); nest bodies to build a tree |
| `<joint>` | how a body moves relative to its parent (`hinge`, `slide`, `ball`, `free`) |
| `<geom>` | a shape — used for **both** collision and visuals (mass too, via density) |
| `<inertial>` | mass & inertia (optional — MuJoCo can compute it from geoms) |
| `<actuator>` | a motor/force source that drives a joint or applies force at a site |
| `<camera>` | a viewpoint you can render from (key for Phase 5 vision!) |
| `<site>` | an invisible reference point (for sensors, thrusters, cameras) |
| `<option>` | global settings: gravity, timestep, **and later: fluid density/viscosity** |

---

## Read a Real Model

Open MuJoCo's tutorial notebook and a built-in model, orbit it, and find each element above in the XML:

```bash
python -m mujoco.viewer        # drag in a model, or load one in Python
```

```python
import mujoco
model = mujoco.MjModel.from_xml_path("your_model.xml")
print("bodies:", model.nbody, " joints:", model.njnt,
      " geoms:", model.ngeom, " actuators:", model.nu, " cameras:", model.ncam)
```

---

## A Tiny Annotated MJCF

```xml
<mujoco model="demo">
  <option gravity="0 0 -9.81" timestep="0.002"/>   <!-- world settings -->
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="3 3 0.1"/>            <!-- the ground -->
    <body name="block" pos="0 0 1">                <!-- a rigid body -->
      <freejoint/>                                 <!-- 6-DOF free motion -->
      <geom type="box" size="0.1 0.1 0.1" density="500"/>
      <camera name="onboard" pos="0 -0.3 0" xyaxes="1 0 0 0 0 1"/>
      <site name="tip" pos="0.1 0 0"/>
    </body>
  </worldbody>
</mujoco>
```

Read it aloud: *"A world with gravity and a ground. A free-floating box of density 500, carrying a camera and a reference site."* If you can do that, you've hit today's checkpoint.

---

## ✅ Checkpoint
**You can read an MJCF file and name each element's role.**

---

## 📚 Resources
- MuJoCo Python tutorial notebook: `google-deepmind/mujoco` → `python/tutorial.ipynb`
- [MuJoCo XML (MJCF) reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)

---

## 🔭 Next
**Day 4 — Write your own pendulum MJCF from scratch and watch it swing.**
