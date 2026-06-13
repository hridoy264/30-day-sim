"""
Day 6 — PID balance of the cart-pole. The most important skill of the month.
Run:  python pid_cartpole.py   (needs cartpole.xml from Day 5 in this folder)
"""
import time
import numpy as np
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("cartpole.xml")
data = mujoco.MjData(model)
data.qpos[1] = 0.1                  # start the pole slightly tilted
mujoco.mj_forward(model, data)

Kp, Ki, Kd = 12.0, 0.0, 2.0        # <-- tune these by hand
integral, prev_err = 0.0, 0.0
dt = model.opt.timestep
errors = []

with mujoco.viewer.launch_passive(model, data) as v:
    while v.is_running():
        error = data.qpos[1]                  # pole angle, want 0 (upright)
        integral += error * dt
        deriv = (error - prev_err) / dt
        u = Kp * error + Ki * integral + Kd * deriv
        data.ctrl[0] = float(np.clip(u, -1, 1))
        prev_err = error
        errors.append(error)

        mujoco.mj_step(model, data)
        v.sync()
        time.sleep(dt)

# Optional: plot the error after closing the viewer window
try:
    import matplotlib.pyplot as plt
    plt.plot(errors); plt.xlabel("step"); plt.ylabel("pole angle error")
    plt.title("PID error over time"); plt.show()
except Exception:
    pass
