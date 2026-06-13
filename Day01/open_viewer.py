"""
Day 1 — Open the MuJoCo passive viewer on a tiny built-in model.
Run:  python open_viewer.py
"""
import time
import mujoco
import mujoco.viewer

xml = """
<mujoco>
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="3 3 0.1" rgba="0.8 0.9 0.8 1"/>
    <body pos="0 0 1">
      <freejoint/>
      <geom type="box" size="0.1 0.1 0.1" rgba="0.2 0.4 0.9 1"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as v:
    t0 = time.time()
    while v.is_running() and time.time() - t0 < 20:
        mujoco.mj_step(model, data)
        v.sync()
        time.sleep(model.opt.timestep)
