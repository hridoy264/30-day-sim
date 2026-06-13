"""
Day 13 — Controlling MuJoCo from Python
Drives the Day-12 two-link arm with sine waves, rendered live.

Put this next to Day12/arm.xml (or copy arm.xml here).
Run:  python control_arm.py
"""

import time
import numpy as np
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("arm.xml")   # fixed blueprint
data = mujoco.MjData(model)                        # live state

with mujoco.viewer.launch_passive(model, data) as viewer:
    start = time.time()
    while viewer.is_running() and time.time() - start < 30:
        t = data.time
        data.ctrl[0] = np.sin(t)            # shoulder waves
        data.ctrl[1] = 0.5 * np.sin(2 * t)  # elbow waves faster

        mujoco.mj_step(model, data)         # advance physics
        viewer.sync()                       # refresh window

        # report state once a second
        if int(t * 500) % 500 == 0:
            print(f"t={t:5.2f}  qpos={np.round(data.qpos, 3)}")

        time.sleep(model.opt.timestep)
