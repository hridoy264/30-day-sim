# Day 4 — Setting Up Your Simulation Environment

## 🎯 Today's Goal
Get your computer ready for the whole course: a working Python, a clean **virtual environment**, and the habits that prevent 90% of "it doesn't work on my machine" problems.

---

## Overview

A good setup is invisible — you never think about it. A bad setup costs you hours. Today we install the foundation that every later day builds on. We'll keep it simple and robust. Do this carefully once and you won't fight your tools later.

---

## Choosing Your Operating System

Simulation tools have different OS support. Here's the honest guidance:

| Your OS | Recommendation |
|---------|----------------|
| **Ubuntu Linux 22.04 / 24.04** | ✅ Best experience. Everything works, especially Gazebo + ROS 2. |
| **Windows** | Use **WSL2** (Windows Subsystem for Linux) running Ubuntu. Near-native Linux inside Windows. |
| **macOS** | PyBullet & MuJoCo work natively. For the Gazebo/ROS 2 days, use a cloud Linux VM or dual-boot. |

> 💡 If you're on Windows, installing **WSL2** now is the single best thing you can do for this course. One command in PowerShell (as admin): `wsl --install`, then reboot. You get a real Ubuntu terminal.

---

## Step 1 — Install Python 3.10+

Most systems have Python. Check your version:

```bash
python3 --version
```

You want **3.10 or newer**. If you don't have it:

- **Ubuntu/WSL:** `sudo apt update && sudo apt install python3 python3-pip python3-venv`
- **macOS:** install [Homebrew](https://brew.sh), then `brew install python`
- **Windows (native):** download from [python.org](https://www.python.org/downloads/) and check "Add to PATH."

---

## Step 2 — Create a Virtual Environment (Important!)

A **virtual environment** is an isolated sandbox for this course's Python packages. It stops different projects from breaking each other — a real engineering best practice.

```bash
# create a project folder and enter it
mkdir ~/sim-course && cd ~/sim-course

# create a virtual environment named "venv"
python3 -m venv venv

# activate it
source venv/bin/activate        # Linux / macOS / WSL
# venv\Scripts\activate         # Windows PowerShell
```

When active, your prompt shows `(venv)`. **Activate it every time** you work on the course. To leave it: `deactivate`.

> 💡 Why this matters: without a venv, a package one day needs can silently break a package from another day. The venv keeps everything clean and reproducible.

---

## Step 3 — Install Your First Simulation Packages

With the venv active, install the lightweight tools we'll use early. These run on any OS:

```bash
pip install --upgrade pip
pip install numpy scipy matplotlib   # the math & plotting toolkit
pip install pybullet                 # our Day 6 simulator
```

> ℹ️ Heavier tools (MuJoCo, Gazebo, RL libraries) are installed in their own phases so you only install what you need, when you need it.

---

## Step 4 — Verify It Works

Let's confirm PyBullet runs. Save this as `test_setup.py`:

```python
import pybullet as p
import pybullet_data

# connect with a graphical window
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# load the ground and a falling box
p.loadURDF("plane.urdf")
p.loadURDF("r2d2.urdf", [0, 0, 1])

# run for a few seconds
import time
for _ in range(2400):
    p.stepSimulation()
    time.sleep(1/240)
p.disconnect()
```

Run it:

```bash
python test_setup.py
```

If a window opens and an R2D2 model drops onto a floor — **congratulations, your environment works!** If you're on a headless server (no display), change `p.GUI` to `p.DIRECT` to run without a window.

---

## A Recommended Editor

Use **VS Code** (free, cross-platform) with the Python extension. On WSL, install the "WSL" extension so VS Code edits files inside Linux seamlessly. Any editor works, but good tooling makes debugging far easier.

---

## 📝 Today's Task

1. Confirm `python3 --version` shows 3.10+.
2. Create and **activate** a virtual environment called `venv`.
3. Install `numpy`, `scipy`, `matplotlib`, and `pybullet`.
4. Run the `test_setup.py` verification script and watch R2D2 fall.
5. Save the working folder — you'll use it all course. Note in your log how to activate your venv (you'll forget at least once!).

---

## ✅ Key Takeaways

✓ Ubuntu (native or via **WSL2** on Windows) gives the smoothest simulation experience.

✓ Always work inside a **virtual environment** — it keeps packages isolated and reproducible.

✓ `python3 -m venv venv` then `source venv/bin/activate` is the pattern you'll repeat all course.

✓ Heavy tools are installed per-phase; today you set up Python + PyBullet.

✓ A successful `test_setup.py` run (R2D2 falling) means your foundation is solid.

---

## 📚 References & Resources

- [Python venv official guide](https://docs.python.org/3/library/venv.html)
- [Install WSL2 on Windows](https://learn.microsoft.com/en-us/windows/wsl/install)
- [PyBullet Quickstart Guide (PDF)](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit)
- [VS Code Python setup](https://code.visualstudio.com/docs/python/python-tutorial)

---

## 🔭 What's Next?

**Day 5 — Describing Robots & Worlds.** Before we control a robot, we have to *describe* one. We'll learn the three file formats — URDF, SDF, and MJCF — that tell a simulator what your robot and world look like.

---

*"A clean setup is a gift you give your future self."*
