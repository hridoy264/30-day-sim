# Day 15 — Thrusters

**Phase 4 · Build the Underwater Vehicle · ~3 hours**

## 🎯 Goal
Add thrusters to the vehicle and map a high-level **thrust-vector command** (forward / yaw / vertical) to individual thruster forces. This mapping is called **control allocation**, and it's how you'll command the vehicle for the rest of the project.

---

## Thrusters in MuJoCo

A thruster is a force applied at a point on the body. You place a `<site>` where each thruster sits and attach a force `<actuator>` to it. Start with 4–6 thrusters in a vectored layout. See `auv_thrusters.xml`:

```xml
<body name="rov" pos="0 0 0" gravcomp="1">
  <freejoint/>
  <geom type="box" size="0.23 0.15 0.10" density="1000"
        fluidshape="ellipsoid" fluidcoef="0.5 0.25 1.5 1.0 1.0"/>
  <!-- two horizontal thrusters (left & right rear) for surge + yaw -->
  <site name="t_left"  pos="-0.2  0.12 0" zaxis="1 0 0"/>
  <site name="t_right" pos="-0.2 -0.12 0" zaxis="1 0 0"/>
  <!-- two vertical thrusters for heave -->
  <site name="t_vup_f" pos=" 0.15 0 0.06" zaxis="0 0 1"/>
  <site name="t_vup_b" pos="-0.15 0 0.06" zaxis="0 0 1"/>
</body>
...
<actuator>
  <!-- 'thruster' actuators apply force along the site's z-axis -->
  <thruster site="t_left"  name="m_left"  gear="5" ctrlrange="-1 1"/>
  <thruster site="t_right" name="m_right" gear="5" ctrlrange="-1 1"/>
  <thruster site="t_vup_f" name="m_vf"    gear="5" ctrlrange="-1 1"/>
  <thruster site="t_vup_b" name="m_vb"    gear="5" ctrlrange="-1 1"/>
</actuator>
```

The `zaxis` of each site sets the direction the thruster pushes. The horizontal pair (`t_left`, `t_right`) pushes forward; the vertical pair lifts.

---

## Control Allocation (the key skill)

You don't want to think in individual motors — you want to command **surge** (forward), **yaw** (turn), and **heave** (up/down). Control allocation converts those into motor commands:

```
m_left  = surge + yaw          # differential -> turning
m_right = surge - yaw
m_vf    = heave
m_vb    = heave
```

See `thrust_allocation.py`:

```python
def allocate(surge, yaw, heave):
    return [
        surge + yaw,   # m_left
        surge - yaw,   # m_right
        heave,         # m_vf
        heave,         # m_vb
    ]
# each step:
data.ctrl[:] = np.clip(allocate(surge, yaw, heave), -1, 1)
```

Now "drive forward and turn left" is just `allocate(0.6, 0.3, 0)`. Every later command — teleop *and* autonomy — goes through this function.

---

## 📝 Today's Task
- Add thruster sites + actuators (`auv_thrusters.xml`).
- Write `allocate(surge, yaw, heave)` and verify:
  - `allocate(1,0,0)` → drives straight forward.
  - `allocate(0,1,0)` → spins in place (yaw).
  - `allocate(0,0,1)` → rises (heave).
- Fix any direction that comes out backwards (swap a sign).

---

## ✅ Checkpoint
**Commanding forward/yaw/vertical thrust moves the vehicle correctly.**

---

## 📚 Resources
- [MuJoCo actuators (thruster, force)](https://mujoco.readthedocs.io/en/stable/XMLreference.html#actuator)

---

## 🔭 Next
**Day 16 — Tune the dynamics so it handles like an ROV, not a brick or a balloon.**
