# Day 12 — Building Models in MJCF

## 🎯 Today's Goal
Build a real, controllable robot in MJCF from scratch: multiple bodies, proper joints, and **actuators** (motors). By the end you'll have a 2-link arm you can drive.

---

## Overview

Yesterday you dropped a ball. Today you build a robot. MJCF's nested structure makes multi-body robots intuitive: bodies contain bodies, joints connect them, and actuators provide the motors. This is the same links-and-joints idea from Day 5, expressed in MuJoCo's clean style.

---

## Nesting = Kinematic Tree

In MJCF, you build a robot by **nesting** `<body>` tags. A child body is automatically attached to its parent — the nesting *is* the kinematic tree:

```xml
<body name="upper_arm">          <!-- attached to world -->
  <joint name="shoulder" .../>
  <geom .../>
  <body name="forearm">          <!-- attached to upper_arm -->
    <joint name="elbow" .../>
    <geom .../>
  </body>
</body>
```

This visual nesting makes the robot's structure obvious at a glance — a real strength of MJCF.

---

## Joint Types in MJCF

| MJCF joint | Motion | Like |
|------------|--------|------|
| `hinge` | rotation about an axis | revolute (elbow) |
| `slide` | linear sliding | prismatic |
| `ball` | 3-DOF rotation | spherical |
| `free` | 6-DOF (whole-body) | floating base |

A `hinge` is the workhorse — it's the elbow/shoulder of robot arms.

---

## Actuators: The Motors

Bodies and joints define *structure*; **actuators** make it *move*. They live in a separate `<actuator>` block and reference a joint by name:

```xml
<actuator>
  <motor name="shoulder_motor" joint="shoulder" gear="1" ctrlrange="-2 2"/>
  <position name="elbow_pos" joint="elbow" kp="50"/>
</actuator>
```

- **`motor`** applies raw torque (like Day 8 torque control).
- **`position`** is a position servo with stiffness `kp` (like Day 8 position control).

> 💡 This separation — structure in `worldbody`, motors in `actuator` — is a clean idea. You define *what the robot is* and *how it's driven* independently.

---

## A Complete 2-Link Arm

Here's a full controllable arm. Save as `arm.xml` (also in this folder):

```xml
<mujoco model="two_link_arm">
  <option gravity="0 0 -9.81"/>

  <worldbody>
    <light pos="0 0 3"/>
    <geom name="floor" type="plane" size="3 3 0.1" rgba="0.8 0.9 0.8 1"/>

    <body name="upper_arm" pos="0 0 1">
      <joint name="shoulder" type="hinge" axis="0 1 0"/>
      <geom type="capsule" fromto="0 0 0  0.5 0 0" size="0.05" rgba="0.2 0.4 0.9 1"/>

      <body name="forearm" pos="0.5 0 0">
        <joint name="elbow" type="hinge" axis="0 1 0"/>
        <geom type="capsule" fromto="0 0 0  0.4 0 0" size="0.04" rgba="0.9 0.4 0.2 1"/>
      </body>
    </body>
  </worldbody>

  <actuator>
    <position name="shoulder_pos" joint="shoulder" kp="100"/>
    <position name="elbow_pos"    joint="elbow"    kp="100"/>
  </actuator>
</mujoco>
```

Note the `capsule fromto` — capsules are MuJoCo's favorite shape because they collide stably and cheaply (remember Day 2: simple collision shapes!).

View it:

```bash
python -m mujoco.viewer --mjcf=arm.xml
```

Without gravity holding it, the arm hangs. The viewer even gives you sliders to move the actuators — try them!

---

## Useful MJCF Extras

- **`<default>`** — set default properties once (e.g., default geom size) so you don't repeat yourself.
- **`<option timestep="0.002">`** — set the time step (Day 2!). MuJoCo's default is 0.002 s.
- **`euler` / `quat`** on a body — set its orientation (Day 3 frames).
- **`mass` / `density`** on geoms — MuJoCo auto-computes inertia for you (a nice convenience over URDF).

---

## 📝 Today's Task

1. Save `arm.xml` and open it in the viewer.
2. Use the viewer's **actuator sliders** to move the shoulder and elbow.
3. Add a **third link** (a "hand") nested inside the forearm, with its own hinge and actuator.
4. Change a `position` actuator to a `motor` (torque) and feel the difference when you drag the arm.
5. Set `<option timestep="0.01">` and observe whether the arm gets less stable (bigger step = Day 2 lesson).

---

## ✅ Key Takeaways

✓ In MJCF you build a robot by **nesting `<body>` tags** — the nesting *is* the kinematic tree.

✓ Joint types: **`hinge`** (revolute), **`slide`** (prismatic), **`ball`**, **`free`**.

✓ **Actuators** (in a separate block) drive joints: `motor` (torque) or `position` (servo with `kp`).

✓ **Capsules** are the preferred shape — cheap and stable to collide.

✓ MuJoCo **auto-computes inertia** from mass/density — less manual work than URDF.

---

## 📚 References & Resources

- [MJCF (XML) reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)
- [MuJoCo modeling guide](https://mujoco.readthedocs.io/en/stable/modeling.html)
- [MuJoCo Menagerie (study real robot models)](https://github.com/google-deepmind/mujoco_menagerie)

---

## 🔭 What's Next?

**Day 13 — Simulating & Controlling from Python.** We leave the viewer's sliders behind and drive the arm from Python code — the way you'll actually build behaviors and RL environments.

---

*"Nest the bodies, name the joints, wire the motors. That's a robot in MJCF."*
