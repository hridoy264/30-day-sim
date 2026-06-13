# Day 16 — Tune the Dynamics

**Phase 4 · Build the Underwater Vehicle · ~2.5 hours**

## 🎯 Goal
Balance buoyancy, drag, and thrust so the vehicle **handles like an ROV** — some glide, but controllable. Not a brick (over-damped, no glide), not a balloon (under-damped, drifts forever).

---

## The Feel You're Aiming For

A good ROV:
- **Hovers** when thrusters are off (neutral buoyancy).
- **Accelerates smoothly**, with a little lag (added mass).
- **Glides briefly** then settles when you cut thrust (drag).
- **Doesn't spin freely** — rotation also damps out.

This is a *tuning* day. There's no single right answer; you adjust until it feels right when you drive it.

---

## The Knobs

| Symptom | Knob to adjust |
|---------|----------------|
| Sinks or floats away | `gravcomp` (toward 1.0 for neutral) |
| Falls/accelerates too fast | increase `fluidcoef` drag terms (Day 12) |
| Coasts forever / too floaty | increase drag terms |
| Stops too abruptly (brick) | decrease drag terms |
| Spins freely after a turn | add **angular damping** (raise the angular `fluidcoef` term, or add joint `damping`) |
| Sim jitters / explodes | reduce `timestep` (e.g., 0.004 → 0.002) |

Add light rotational resistance if it over-rotates — bump the 3rd `fluidcoef` value (angular drag) or add a small damping on the freejoint's rotational DOFs.

---

## Tuning Method

1. Drive with `thrust_allocation.py` (Day 15) using a fixed command pattern.
2. Cut thrust mid-run and watch how it coasts. Too far? More drag. Stops dead? Less drag.
3. Command a yaw, then zero — does it keep spinning? Add angular damping.
4. Repeat until forward, turn, and dive all feel deliberate and controllable.
5. Save the tuned values — this `auv` model becomes the base for the rest of the project.

> Keep a copy of your tuned numbers in `notes/`. You'll thank yourself when a later change breaks the feel and you need to revert.

---

## ✅ Checkpoint
**The vehicle feels like an underwater vehicle, not a brick or a balloon.**

---

## 📚 Resources
- [MuJoCo fluid forces (tuning `fluidcoef`)](https://mujoco.readthedocs.io/en/stable/computation/fluid.html)

---

## 🔭 Next
**Day 17 — Mount two cameras (downward for line-following, forward for view) and render both.**
