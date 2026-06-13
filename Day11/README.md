# Day 11 — Hello MuJoCo: Install & First Model

## 🎯 Today's Goal
Install MuJoCo, open the interactive viewer, and run your first model. Understand why MuJoCo is the simulator of choice for modern robotics research and reinforcement learning.

---

## Overview

Welcome to Phase 3! **MuJoCo** (Multi-Joint dynamics with Contact) is famous for its **accurate, stable physics** — especially how it handles contacts (things touching and pushing). Once expensive and closed, MuJoCo is now **free and open-source** (maintained by Google DeepMind) and installs with a single `pip` command. It's the engine behind a huge fraction of robotics and RL papers, so this phase makes you fluent in the research world's favorite tool.

---

## PyBullet vs. MuJoCo — Why Switch?

You already know PyBullet. Why learn another simulator?

| | PyBullet | MuJoCo |
|---|----------|--------|
| Ease of start | Very easy | Easy |
| Contact accuracy | Good | **Excellent** |
| Speed for RL | Good | **Excellent** |
| Used in research | Some | **Dominant** |
| Model format | URDF | MJCF (and imports URDF) |

The skills transfer: it's still bodies, joints, control, and sensors — just a cleaner, faster engine with its own XML flavor (MJCF, from Day 5).

---

## Step 1 — Install

With your course virtual environment active (Day 4):

```bash
pip install mujoco
```

That's it — no license files, no separate downloads anymore. Verify:

```bash
python -c "import mujoco; print(mujoco.__version__)"
```

---

## Step 2 — Launch the Interactive Viewer

MuJoCo ships a built-in viewer. The fastest way to see something is to load a model file:

```bash
python -m mujoco.viewer
```

This opens an empty viewer where you can drag in an MJCF (`.xml`) model. Or load one directly:

```bash
python -m mujoco.viewer --mjcf=my_first.xml
```

In the viewer you can rotate (drag), zoom (scroll), and — uniquely — **double-click a body and drag it** to apply forces with your mouse. Great for poking at your model to test it.

---

## Step 3 — Your First MJCF Model

MJCF is wonderfully compact. Here's a complete world: a floor and a falling ball. Save as `first.xml` (also in this folder):

```xml
<mujoco model="hello">
  <option gravity="0 0 -9.81"/>

  <worldbody>
    <!-- a light and the ground -->
    <light pos="0 0 3"/>
    <geom name="floor" type="plane" size="5 5 0.1" rgba="0.8 0.9 0.8 1"/>

    <!-- a ball that will fall -->
    <body name="ball" pos="0 0 2">
      <freejoint/>
      <geom name="ball" type="sphere" size="0.1" rgba="0.9 0.2 0.2 1"/>
    </body>
  </worldbody>
</mujoco>
```

Compare this to a URDF — MJCF is noticeably more compact. Note the familiar ideas: `gravity`, a `worldbody` (the world frame), `body` (a link), `geom` (geometry/shape), and `freejoint` (lets the body move freely, like an unattached object).

View it:

```bash
python -m mujoco.viewer --mjcf=first.xml
```

A red ball drops onto a green floor. You just wrote and ran a MuJoCo model.

---

## The MuJoCo Vocabulary (quick map from what you know)

| MuJoCo term | Means | PyBullet/URDF equivalent |
|-------------|-------|--------------------------|
| `worldbody` | the root world frame | the world |
| `body` | a rigid body | link |
| `geom` | a shape (collision + visual) | geometry |
| `joint` | connection / DOF | joint |
| `freejoint` | 6-DOF free motion | floating base |
| `actuator` | a motor/force source | joint motor |

---

## 📝 Today's Task

1. `pip install mujoco` and verify the version prints.
2. Save `first.xml` and open it with `python -m mujoco.viewer --mjcf=first.xml`.
3. In the viewer, **double-click the ball and drag** it around — feel the mouse-force interaction.
4. Change the ball to a `box` geom and give it a start rotation via the body's `euler="0 0.5 0"` attribute. Reload.
5. Add a second body at a different position so two objects fall.

---

## ✅ Key Takeaways

✓ **MuJoCo** is free, open-source (DeepMind), and installs with `pip install mujoco`.

✓ It's prized for **accurate contacts** and **speed**, making it the research/RL standard.

✓ Launch the viewer with `python -m mujoco.viewer`; you can drag bodies to apply forces.

✓ Models use **MJCF** XML — compact, with `worldbody`, `body`, `geom`, `joint`, `actuator`.

✓ All your simulation concepts carry over — it's the same ideas in a faster engine.

---

## 📚 References & Resources

- [MuJoCo documentation (home)](https://mujoco.readthedocs.io/en/stable/overview.html)
- [MuJoCo Python bindings](https://mujoco.readthedocs.io/en/stable/python.html)
- [MuJoCo on GitHub](https://github.com/google-deepmind/mujoco)
- [MuJoCo Menagerie — free high-quality robot models](https://github.com/google-deepmind/mujoco_menagerie)

---

## 🔭 What's Next?

**Day 12 — Building Models in MJCF.** We go deeper into MJCF: multi-body robots, joint types, and actuators, so you can describe a controllable robot from scratch.

---

*"MuJoCo is where research robots are born. Today you opened the door."*
