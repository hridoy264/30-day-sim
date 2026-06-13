# Day 17 — Building Worlds with SDF

## 🎯 Today's Goal
Build a custom Gazebo world from scratch using SDF: a ground plane, lighting, physics settings, and obstacles. You'll create the stage your robot will explore in later days.

---

## Overview

On Day 5 you met **SDF** (Simulation Description Format) — Gazebo's native XML for describing *entire worlds*, not just robots. Today you write one. A "world" in Gazebo is everything: the ground, the sky, lights, physics parameters, and any static objects. Building one yourself demystifies every Gazebo demo you'll ever open.

---

## Anatomy of an SDF World

An SDF world file has a clear structure:

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="my_world">

    <!-- physics: the time step from Day 2! -->
    <physics name="default" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- a light source -->
    <light name="sun" type="directional">
      <pose>0 0 10 0 0 0</pose>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- the ground -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>20 20</size></plane></geometry>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

Notice the familiar pieces: `physics` (your Day-2 time step), `light`, and a `model` with `collision` + `visual` (Day 5). The `<static>true</static>` tag means the ground never moves — important for fixed scenery.

---

## Adding Obstacles

Let's add a box obstacle the robot will later avoid. Inside `<world>`:

```xml
<model name="box_obstacle">
  <static>true</static>
  <pose>2 0 0.5 0 0 0</pose>   <!-- x y z roll pitch yaw -->
  <link name="link">
    <collision name="collision">
      <geometry><box><size>1 1 1</size></box></geometry>
    </collision>
    <visual name="visual">
      <geometry><box><size>1 1 1</size></box></geometry>
      <material><ambient>0.8 0.2 0.2 1</ambient></material>
    </visual>
  </link>
</model>
```

The `<pose>` is the same 6 numbers you know: x, y, z, roll, pitch, yaw (Day 3). `<material>` sets its color.

---

## Reusing Models with `<include>`

You rarely build everything by hand. Gazebo has an online model library (Fuel) you can pull from:

```xml
<include>
  <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Construction Cone</uri>
  <pose>3 1 0 0 0 0</pose>
</include>
```

`<include>` lets you drop in pre-made, high-quality models (cones, tables, buildings, even robots) instead of writing them. This is how real worlds are assembled quickly.

---

## Running Your World

Save your file as `my_world.sdf` (a starter is in this folder) and launch:

```bash
gz sim my_world.sdf
```

Press **play**. You should see your ground, your lighting, and your red box obstacle. You built a world.

---

## 📝 Today's Task

1. Create `my_world.sdf` with a ground plane, a sun light, and physics settings.
2. Launch it with `gz sim my_world.sdf` and press play.
3. Add **two box obstacles** at different poses and colors.
4. Add a **cylinder** obstacle (swap `<box>` for `<cylinder><radius>...<length>...`).
5. Try an `<include>` to pull a model from Gazebo Fuel (needs internet). Arrange a small "course" your future robot can navigate.

---

## ✅ Key Takeaways

✓ **SDF worlds** describe everything: physics, lights, ground, and objects.

✓ `<physics>` holds your **time step** (Day 2); `<static>true</static>` fixes scenery in place.

✓ Objects use the same **`collision` + `visual` + `pose`** pattern as Day 5, with `<material>` for color.

✓ **`<include>`** pulls ready-made models from Gazebo **Fuel** — assemble worlds fast.

✓ Launch any world with `gz sim <file>.sdf` (and remember to press play).

---

## 📚 References & Resources

- [SDFormat specification](http://sdformat.org/spec)
- [Gazebo: Building your own world](https://gazebosim.org/docs/harmonic/sdf_worlds/)
- [Gazebo Fuel model library](https://app.gazebosim.org/fuel)

---

## 🔭 What's Next?

**Day 18 — Spawning a Robot & The ROS–Gazebo Bridge.** We put a robot into your world and connect it to ROS 2, so your code can finally talk to a Gazebo robot.

---

*"A robot needs a stage. Today you built one."*
