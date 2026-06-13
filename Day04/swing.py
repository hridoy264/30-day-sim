"""
Day 4 — Swing your hand-built pendulum.
Run:  python swing.py   (needs pendulum.xml in the same folder)
"""
import time
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("pendulum.xml")
data = mujoco.MjData(model)

data.qpos[0] = 1.2          # start tilted
mujoco.mj_forward(model, data)

with mujoco.viewer.launch_passive(model, data) as v:
    while v.is_running():
        mujoco.mj_step(model, data)
        v.sync()
        time.sleep(model.opt.timestep)
