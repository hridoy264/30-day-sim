"""
Day 13 — Explicit buoyancy force -> neutral buoyancy / self-righting.
Applies an upward force each step at the body (center of buoyancy).
Run:  python buoyancy.py
"""
import time
import mujoco
import mujoco.viewer

XML = """
<mujoco model="buoyant">
  <option gravity="0 0 -9.81" timestep="0.002" density="1000" viscosity="0.001"/>
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="3 3 0.1" rgba="0.3 0.5 0.7 1"/>
    <body name="rov" pos="0 0 1.5">
      <freejoint/>
      <geom type="box" size="0.2 0.15 0.1" density="1000"
            fluidshape="ellipsoid" fluidcoef="0.5 0.25 1.5 1.0 1.0"
            rgba="0.9 0.7 0.2 1"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(XML)
data = mujoco.MjData(model)
body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "rov")

# upward buoyancy force ~ weight of displaced water (tune V for neutral)
rho, g = 1000.0, 9.81
V = 0.006                       # displaced volume (m^3) -> tune for neutral
F_buoy = rho * V * g

with mujoco.viewer.launch_passive(model, data) as v:
    while v.is_running():
        # apply upward force; offsetting it from COM would add self-righting torque
        data.xfrc_applied[body_id, :3] = [0.0, 0.0, F_buoy]
        mujoco.mj_step(model, data)
        v.sync()
        time.sleep(model.opt.timestep)
