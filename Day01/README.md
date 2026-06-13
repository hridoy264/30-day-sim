# Day 1 — Mental Model + Environment

**Phase 1 · Orientation & MuJoCo Setup · ~3 hours**

## 🎯 Goal
Understand *why* we simulate, then get MuJoCo running on your Mac.

---

## Block A — Concepts (1 hr)

Before any code, build the mental model:

- **Why simulate at all?** Real underwater vehicles are expensive, slow to test, and hard to instrument. In sim you run hundreds of trials a day, for free, safely.
- **The sim-to-real gap.** A simulator is never a perfect copy of reality (approximated physics, clean sensors, imperfect models). Code that overfits the sim breaks on real hardware.
- **Domain randomization.** The fix for the gap: train/test across many randomized conditions (lighting, water color, noise) so your system is robust. You'll use this on Day 28.

Write a few sentences in your `notes/` on each — teaching it to yourself locks it in.

---

## Block B — Set up the Mac (1.5 hr)

```bash
xcode-select --install                 # if not already done
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install mujoco numpy opencv-python matplotlib
```

Verify and open the passive viewer on a built-in model:

```bash
python -c "import mujoco; print('MuJoCo', mujoco.__version__)"
python -m mujoco.viewer        # then drag in a model, or use the script below
```

A quick script that loads a built-in humanoid and opens a window — see `open_viewer.py`:

```python
import time, mujoco, mujoco.viewer
# minimal model so it runs with no external files
xml = """
<mujoco>
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="3 3 0.1"/>
    <body pos="0 0 1"><freejoint/><geom type="box" size="0.1 0.1 0.1"/></body>
  </worldbody>
</mujoco>
"""
model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)
with mujoco.viewer.launch_passive(model, data) as v:
    t0 = time.time()
    while v.is_running() and time.time() - t0 < 20:
        mujoco.mj_step(model, data); v.sync()
        time.sleep(model.opt.timestep)
```

---

## Block C — One Git Repo (0.5 hr)

Create your project structure and commit it:

```bash
mkdir -p mujoco-labs auv-project notes
git init
echo "venv/" > .gitignore
git add . && git commit -m "Day 1: project setup"
```

- `mujoco-labs/` — your daily MuJoCo experiments
- `auv-project/` — the underwater vehicle (Phase 4 onward)
- `notes/` — your written understanding

---

## ✅ Checkpoint
**A MuJoCo window opens on your Mac.**

---

## 📚 Resources
- [MuJoCo documentation (intro)](https://mujoco.readthedocs.io)

---

## 🔭 Next
**Day 2 — Frames, rigid bodies, and the marine 6-DOF naming (surge/sway/heave/roll/pitch/yaw).**
