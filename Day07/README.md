# Day 7 — Buffer / Consolidate

**Phase 2 · MuJoCo Fundamentals · ~1.5 hours (light)**

## 🎯 Goal
Catch your breath. Fix anything broken from Days 1–6 and write the core ideas in your own words so they stick.

---

## Why a Buffer Day?

The first six days moved fast: setup, frames, MJCF, pendulum, cart-pole, PID. Buffer days exist so falling behind doesn't break the plan. There are four (Days 7, 19, 24, 29) — use them. If you're on track, this is a consolidation day, not a day off.

---

## 📝 Today's Task

**1. Fix breakage.** Revisit anything that didn't quite work — a model that wouldn't load, a PID that wouldn't settle. Get Days 1–6 all running cleanly.

**2. Write it in your own words** (in `notes/`). Explain each, briefly, as if teaching a friend:

- **State** — what `data.qpos` / `data.qvel` represent.
- **Control** — what `data.ctrl` does and how it reaches the physics.
- **Timestep** — what `dt` is and why too large breaks the sim.
- **Control loop** — the READ → compute → WRITE → STEP cycle.
- **PID** — what P, I, and D each fix.

If you can write these clearly, you own the foundation the rest of the project stands on.

---

## ✅ Checkpoint
Days 1–6 all run cleanly, and you have a short written explanation of state, control, timestep, the control loop, and PID.

---

## 🔭 Next
**Day 8 — LQR intuition: a smarter controller, and what Q and R do.**
