# Day 26 — Sim-to-Real & Domain Randomization

## 🎯 Today's Goal
Understand the central challenge of using simulation for real robots — the **reality gap** — and the powerful technique that bridges it: **domain randomization**. This is the concept that makes everything you've learned matter for physical robots.

---

## Overview

You've trained agents in simulation. But the whole point is usually a *real* robot. Does a policy learned in sim actually work on hardware? Sometimes yes, often no — and understanding *why* (and how to fix it) is one of the most valuable ideas in modern robotics. This is a concept-focused day; no big install, but it ties the entire course to the real world.

---

## The Reality Gap

Simulation is never a perfect copy of reality. The differences — the **reality gap** — include:

- **Physics approximations** — friction, contact, and motor dynamics are simplified.
- **Imperfect models** — the real robot's masses, dimensions, and joint play differ slightly from your URDF.
- **Sensor noise** — real cameras and LiDARs are noisy, laggy, and sometimes wrong; sim sensors are often too clean.
- **Unmodeled effects** — cable drag, gear backlash, air currents, wear.

A policy that overfits to the simulator's *exact* physics can fail on a real robot that behaves even slightly differently. This is the #1 reason naive sim-to-real transfer fails.

---

## The Key Insight: Don't Train for One World

If a policy only works in one perfect simulation, it's brittle. The fix is counterintuitive but powerful: **train across many randomized variations** so the policy learns to be robust to *uncertainty itself*. If it can handle a thousand slightly different physics, the real world is just one more variation it can handle.

---

## Domain Randomization

**Domain randomization** means randomizing the simulator's parameters every episode during training. Instead of one fixed world, the agent trains on a whole distribution of worlds:

| Randomize... | Examples |
|--------------|----------|
| **Physics** | friction, mass, motor strength, damping |
| **Visuals** | textures, colors, lighting (for camera-based policies) |
| **Sensors** | add noise, delay, dropouts |
| **Geometry** | small size/position variations |

A policy trained this way doesn't depend on any single exact value — so when it meets the real robot (yet another variation), it adapts. This single idea has powered many landmark sim-to-real results, including dexterous robot-hand manipulation and quadruped locomotion.

---

## What It Looks Like in Code

Conceptually, you randomize inside `reset()` of your Day-25 environment:

```python
def reset(self, seed=None, options=None):
    super().reset(seed=seed)
    p.resetSimulation()
    p.setGravity(0, 0, -9.81)
    self.robot = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

    # --- domain randomization ---
    friction = self.np_random.uniform(0.5, 1.5)
    p.changeDynamics(self.robot, -1, lateralFriction=friction)
    mass_scale = self.np_random.uniform(0.8, 1.2)
    # ... vary masses, add sensor noise to observations, etc.
    return self._obs(), {}
```

Each episode, the world is a little different. The agent is forced to learn a policy that works *across* the range — exactly what real-world robustness requires.

---

## Other Bridges Across the Gap

Domain randomization is the headline, but the toolbox also includes:

- **System identification** — measure the real robot carefully and make the sim match it.
- **Better simulators** — higher-fidelity physics (a reason MuJoCo and Isaac exist).
- **Real-world fine-tuning** — train mostly in sim, then a little on the real robot.
- **Sim-to-real-to-sim loops** — use real data to improve the sim, repeat.

In practice, teams combine several of these.

---

## 📝 Today's Task

This is a thinking day:

1. Add **domain randomization** to your Day-25 `custom_env.py`: randomize friction and the robot's base mass each `reset()`.
2. Train two policies — one *without* randomization, one *with* — and compare how they behave when you then change the friction to a new value at test time. The randomized one should cope better.
3. Write a short paragraph: list three reality-gap sources for *your* environment and how you'd randomize each.
4. Read one sim-to-real case study (see references) and note the randomizations they used.
5. **Reflect:** why does training on *more* variation make a policy *more* robust, not less?

---

## ✅ Key Takeaways

✓ The **reality gap** = differences between sim and reality (physics, models, sensor noise, unmodeled effects).

✓ Policies that overfit one perfect sim are **brittle** on real robots — the main sim-to-real failure.

✓ **Domain randomization** trains across many randomized worlds so the policy is robust to uncertainty — the real world becomes "just another variation."

✓ Randomize physics, visuals, sensors, and geometry — often inside `reset()`.

✓ Other bridges: **system identification**, higher-fidelity sims, and real-world fine-tuning — usually combined.

---

## 📚 References & Resources

- [OpenAI: Solving Rubik's Cube with a Robot Hand (domain randomization)](https://openai.com/research/solving-rubiks-cube)
- [Sim-to-Real overview (NVIDIA Isaac)](https://developer.nvidia.com/isaac/sim)
- [Domain Randomization paper (Tobin et al., 2017)](https://arxiv.org/abs/1703.06907)

---

## 🔭 What's Next?

**Day 27 — NVIDIA Isaac Sim.** Final phase! We look at the GPU-accelerated frontier of simulation, where thousands of robots train in parallel — the cutting edge that makes large-scale domain randomization practical.

---

*"The trick isn't to make sim perfect. It's to make your robot ready for imperfection."*
