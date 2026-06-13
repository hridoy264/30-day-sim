"""
Day 5 — Cart-pole + Python control loop.
Reads state (qpos/qvel) and writes a control (ctrl) each step.
Run:  python cartpole_loop.py   (needs cartpole.xml here)
"""
import time
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("cartpole.xml")
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as v:
    step = 0
    while v.is_running():
        cart_x = data.qpos[0]
        pole_ang = data.qpos[1]

        # no controller yet — just a tiny constant push to feel the motor
        data.ctrl[0] = 0.1

        mujoco.mj_step(model, data)
        v.sync()

        if step % 50 == 0:
            print(f"cart_x={cart_x:+.3f}  pole_ang={pole_ang:+.3f}")
        step += 1
        time.sleep(model.opt.timestep)
