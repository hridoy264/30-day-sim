"""
Day 15 — Thrusters + control allocation.
Maps high-level (surge, yaw, heave) commands to the 4 thruster forces.
Run:  python thrust_allocation.py   (needs auv_thrusters.xml here)
"""
import time
import numpy as np
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("auv_thrusters.xml")
data = mujoco.MjData(model)


def allocate(surge, yaw, heave):
    """High-level command -> [m_left, m_right, m_vf, m_vb]."""
    return np.array([
        surge + yaw,   # m_left
        surge - yaw,   # m_right
        heave,         # m_vf
        heave,         # m_vb
    ])


# demo: drive forward for a bit, then turn, then rise
def command(t):
    if t < 4:    return (0.6, 0.0, 0.0)   # forward (surge)
    if t < 8:    return (0.2, 0.4, 0.0)   # forward + turn (yaw)
    return (0.0, 0.0, 0.4)                # rise (heave)


with mujoco.viewer.launch_passive(model, data) as v:
    while v.is_running():
        surge, yaw, heave = command(data.time)
        data.ctrl[:] = np.clip(allocate(surge, yaw, heave), -1, 1)
        mujoco.mj_step(model, data)
        v.sync()
        time.sleep(model.opt.timestep)
