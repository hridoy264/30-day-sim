"""
Day 8 — LQR intuition for the cart-pole.
Goal is intuition (what Q and R do), not mastery. Requires scipy.

This builds a linear model by finite-differencing MuJoCo around the upright
point, solves the continuous-time LQR, and balances with u = -K x.

Run:  python lqr_cartpole.py   (needs cartpole.xml from Day 5 here)
"""
import time
import numpy as np
import mujoco
import mujoco.viewer
from scipy.linalg import solve_continuous_are

model = mujoco.MjModel.from_xml_path("cartpole.xml")
data = mujoco.MjData(model)
dt = model.opt.timestep

# --- crude linearization A, B via finite differences around upright (x=0) ---
nx = 2 * model.nv          # state = [qpos, qvel]
nu = model.nu


def f(x, u):
    d = mujoco.MjData(model)
    d.qpos[:] = x[:model.nv]
    d.qvel[:] = x[model.nv:]
    d.ctrl[:] = u
    mujoco.mj_step(model, d)
    return np.concatenate([d.qpos, d.qvel])


x0 = np.zeros(nx)
u0 = np.zeros(nu)
eps = 1e-5
A = np.zeros((nx, nx))
B = np.zeros((nx, nu))
base = f(x0, u0)
for i in range(nx):
    dx = x0.copy(); dx[i] += eps
    A[:, i] = (f(dx, u0) - base) / eps
for i in range(nu):
    du = u0.copy(); du[i] += eps
    B[:, i] = (f(x0, du) - base) / eps
# convert discrete-step deltas to rough continuous dynamics
A = (A - np.eye(nx)) / dt
B = B / dt

# --- the design knobs: Q penalizes state error, R penalizes control effort ---
Q = np.diag([1.0, 10.0, 1.0, 1.0])   # try raising the pole-angle weight (index 1)
R = np.array([[0.1]])                 # try raising R for gentler control

P = solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P
print("LQR gain K =", np.round(K, 2))

# --- run u = -K x ---
data.qpos[1] = 0.1
mujoco.mj_forward(model, data)
with mujoco.viewer.launch_passive(model, data) as v:
    while v.is_running():
        x = np.concatenate([data.qpos, data.qvel])
        data.ctrl[:] = np.clip(-K @ x, -1, 1)
        mujoco.mj_step(model, data); v.sync()
        time.sleep(dt)
