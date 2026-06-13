"""
Day 15 — Mini-Project: CartPole Balance
A hand-tuned PD controller keeps the pole upright.

Run:  python cartpole_balance.py
"""

import time
import numpy as np
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("cartpole.xml")
data = mujoco.MjData(model)

# start slightly tilted so the controller has something to correct
data.qpos[1] = 0.1
mujoco.mj_forward(model, data)

Kp, Kd = 8.0, 1.5   # try Kp=2 (too weak) or Kp=30 (too strong)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        pole_angle = data.sensordata[1]   # 0 = upright
        pole_vel = data.sensordata[2]

        # PD feedback: push the cart to counter the tilt
        data.ctrl[0] = np.clip(Kp * pole_angle + Kd * pole_vel, -1, 1)

        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)
