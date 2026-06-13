# 30 Days of Underwater Simulation 🌊🤖

Build an **autonomous underwater line-following vehicle** in simulation — from zero to a full demo — in 30 focused days, entirely in **MuJoCo**, on hardware you already own.

By Day 30 you'll have a MuJoCo underwater vehicle with two cameras that you can **teleoperate** (keyboard/gamepad) and that **autonomously follows a line on the seabed** using classic computer vision, tested under varied (simulated) water conditions.

---

## Why This Plan (and This Tool)

This course is deliberately built around real hardware constraints:

- **Primary machine: M4 MacBook Air.** All MuJoCo work, vision, and Python live here. MuJoCo runs natively on Apple Silicon, models underwater dynamics (buoyancy + fluid drag + thrusters), and renders two cameras — **no dedicated GPU required**.
- **Secondary machine: Core i5 Linux laptop.** Used for practicing ROS 2 concepts and *optionally* attempting the Stonefish photorealistic track later.
- **Stonefish is an optional follow-on** (see `APPENDIX_Stonefish.md`) because its camera sim needs OpenGL 4.3+, which macOS doesn't provide. Your control + vision code ports over when you get GPU access — only the simulator host changes.

**Time budget:** ~2.5–3 focused hours/day, split into blocks. Skip "Stretch" items to compress.

---

## What You'll Build, Phase by Phase

| Phase | Days | Outcome |
|-------|------|---------|
| **1 — Orientation & Setup** | 1–3 | MuJoCo running on your Mac; you can read an MJCF file |
| **2 — MuJoCo Fundamentals** | 4–10 | Pendulum, cart-pole, **a working PID loop**, contacts, sensors, **camera→NumPy rendering** |
| **3 — Marine Dynamics + Fluid** | 11–13 | Realistic drag, and a **neutrally buoyant** body in "water" |
| **4 — Build the Vehicle** | 14–19 | A thruster-driven 6-DOF ROV with two cameras over a seabed line |
| **5 — Teleop + Vision** | 20–25 | **Manual flight** + an OpenCV line detector producing clean error signals |
| **6 — Autonomy + Robustness** | 26–30 | **Autonomous line-following**, curve/loss recovery, turbidity testing, capstone demo |

---

## The Three Skills That Carry the Whole Project

1. **The control loop** (Day 6 PID) — *the most important skill of the month.* Everything downstream is a control loop.
2. **Camera → image array** (Day 10) — the bridge between physics and your vision pipeline.
3. **Error signal → controller** (Days 22 & 26) — turning what the camera sees into thrust commands.

If you nail these three, the project works.

---

## How to Use This Course

1. **One day at a time.** Each `DayXX/` folder has a `README.md` with the day's blocks, a clear **Checkpoint**, resources, and starter code/MJCF where useful.
2. **Hit the Checkpoint before moving on.** Each day ends with a concrete, testable checkpoint. That's your gate.
3. **Use the buffer days** (7, 19, 24, 29) to absorb slippage — falling behind is normal and planned for.
4. **Track your progress.** Open `progress-tracker.html` in your browser to check off days and checkpoints (it saves automatically), or use `PROGRESS.md`.

---

## Setup Before Day 1

- **Mac (primary):** Install Xcode Command Line Tools, Python 3, a virtual environment, and Git.
- **Linux (secondary):** Only needed for optional ROS 2 practice / Stonefish later.
- **Skills assumed:** comfortable Python and terminal. **No C++ required** for the MuJoCo path.

```bash
# on the Mac
xcode-select --install
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install mujoco numpy opencv-python matplotlib
```

---

## Adapting the Plan

- **Behind schedule?** Buffer days (7, 19, 24, 29) absorb slippage.
- **Already know control/ROS?** Compress Phases 2–3, spend the saved days on Phase 5–6 robustness.
- **MuJoCo water looks unrealistic?** Expected — it's the tradeoff for running on your hardware. Photorealism is the Stonefish track's job, later.

---

## Repository Layout

```
30daysim/
├── README.md                     ← you are here
├── PROGRESS.md                   ← checkbox tracker (markdown)
├── progress-tracker.html         ← interactive tracker (saves your progress)
├── APPENDIX_Stonefish.md         ← optional photorealistic track (needs GPU)
├── Day01/ … Day30/               ← daily lessons + starter code
└── 30-day-underwater-sim-plan(1).md   ← your original source plan
```

---

*"You don't need a pool, a robot, or a GPU to build an autonomous submarine. You need MuJoCo and 30 days."* 🌊
