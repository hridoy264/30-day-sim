# Day 2 — How Physics Engines Work

## 🎯 Today's Goal
Understand the engine at the heart of every simulator: how it represents objects, advances time, and computes collisions and forces. This is the single most useful mental model in the whole course.

---

## Overview

Yesterday you learned *what* simulation is. Today we look inside the **physics engine** — the part that makes a virtual world behave like the real one. You don't need advanced math here. You need the right intuition, and by the end of today you'll have it.

Every simulator in this course (PyBullet, MuJoCo, Gazebo, Isaac) is, at its core, a physics engine with extras bolted on. Learn this once, and you understand all of them.

---

## What a Physics Engine Actually Does

A physics engine answers one question, over and over, very fast:

> *"Given where everything is right now and the forces acting on it, where will everything be a tiny moment later?"*

It does this by repeating a loop thousands of times per second. Each repetition is one **time step**.

---

## Rigid Bodies: The Building Blocks

Most robotics simulation uses **rigid bodies** — objects that don't bend or squish. A robot is modeled as a set of rigid bodies (called **links**) connected by **joints**.

Each rigid body has physical properties the engine needs:

- **Mass** — how heavy it is.
- **Center of mass** — the balance point.
- **Inertia** — how hard it is to start or stop rotating (the rotational version of mass).
- **Collision shape** — the geometry used to detect contact (often a simple box, sphere, or cylinder for speed).
- **Visual shape** — the geometry you *see* (can be more detailed than the collision shape).

> 💡 A pro habit: collision shapes are kept *simple* (boxes, capsules) even when the visual mesh is detailed. Complex collision geometry is slow and unstable. You'll see this everywhere.

---

## The Simulation Loop & Time Steps

Here is the heartbeat of every simulator:

```
loop forever:
    1. read forces (gravity, motors, contacts)
    2. compute accelerations from forces  (F = ma)
    3. update velocities    (velocity += acceleration × dt)
    4. update positions     (position += velocity × dt)
    5. detect & resolve collisions
    6. render the new frame
```

The key value is **`dt`** — the **time step**, the small slice of time each loop advances. A typical value is `1/240` second (PyBullet's default) or `0.002` s.

**The golden rule of time steps:**

- **Smaller `dt`** → more accurate and stable, but slower (more loops per second of sim time).
- **Larger `dt`** → faster, but objects can pass through each other, jitter, or "explode."

Most beginner instability ("my robot flew off the screen!") comes from a time step that's too large for the situation. This is the #1 thing to check when a simulation misbehaves.

---

## Collision Detection & Response

Two jobs the engine does every step:

1. **Detection** — figuring out *which* objects are touching or overlapping. The engine first does a cheap "broad phase" (rough bounding-box check) then an exact "narrow phase" only on pairs that might collide.
2. **Response** — applying forces so objects push apart realistically instead of sinking into each other. This is governed by parameters like **restitution** (bounciness) and **friction**.

When you place a box on the floor, it doesn't fall through because, each step, the engine detects the overlap and applies an upward contact force. Get this wrong (bad `dt`, bad parameters) and objects sink, bounce forever, or jitter.

---

## Why Different Engines Exist

You'll meet several engines. They make different trade-offs:

- **Bullet** (in PyBullet) — fast, general-purpose, great for games and robotics prototyping.
- **MuJoCo** — extremely accurate contact handling, the favorite for research and reinforcement learning.
- **DART / Bullet / others** (in Gazebo) — robotics-focused, integrate with ROS.
- **PhysX** (in NVIDIA Isaac) — GPU-accelerated, runs thousands of robots at once.

None is "best" — each is best *for a purpose*. By the end of the course you'll have hands-on feel for the trade-offs.

---

## 📝 Today's Task

No coding yet — build the mental model:

1. Re-read the **simulation loop** above and explain it out loud in your own words. If you can teach it, you know it.
2. Look around your room and pick one object. Estimate its **mass**, identify its **center of mass**, and imagine the simplest **collision shape** (box? cylinder?) that would represent it.
3. Write a one-line answer: *"Why does a too-large time step make a simulation unstable?"*
4. Optional: watch a short video on "how game physics engines work" — robotics uses the same ideas.

---

## ✅ Key Takeaways

✓ A physics engine repeatedly answers: "where will everything be a tiny moment later?"

✓ Robots are modeled as **rigid bodies (links)** with mass, inertia, and collision shapes, connected by **joints**.

✓ The simulation advances in small **time steps (`dt`)**; smaller is more stable, larger is faster.

✓ Most "exploding robot" bugs come from a time step that's too large.

✓ Collision = **detection** (who's touching) + **response** (push apart with friction & restitution).

✓ Keep **collision shapes simple** even when visuals are detailed.

---

## 📚 References & Resources

- [Bullet Physics Documentation](https://pybullet.org/wordpress/)
- [MuJoCo: Computation overview](https://mujoco.readthedocs.io/en/stable/computation/index.html)
- [Gazebo Physics concepts](https://gazebosim.org/docs)
- Search: *"How physics engines work"* (Gaffer On Games: "Integration Basics" is a classic intro)

---

## 🔭 What's Next?

**Day 3 — The Math You Need: Frames, Transforms & Units.** Every simulator describes *where* things are using coordinate frames. We'll demystify positions, rotations, and the small bit of math that makes the rest of the course easy.

---

*"Understand the loop, and every simulator becomes the same simulator."*
