"""
Day 10 — Offscreen camera rendering -> NumPy array -> OpenCV.
The bridge from physics to your vision pipeline.

Run:  python render_camera.py
Needs: pip install mujoco opencv-python numpy
Press 'q' in the window to quit.
"""
import time
import numpy as np
import mujoco
import cv2

XML = """
<mujoco model="cam_scene">
  <option gravity="0 0 -9.81" timestep="0.005"/>
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="2 2 0.1" rgba="0.85 0.85 0.85 1"/>
    <!-- a high-contrast strip on the floor, like our future seabed line -->
    <geom type="box" pos="0 0 0.001" size="0.05 1.5 0.001" rgba="1 0.2 0.1 1"/>
    <!-- a downward-looking camera mounted above, like the vehicle's -->
    <body name="vehicle" pos="0 0 1.0">
      <freejoint/>
      <geom type="box" size="0.15 0.1 0.05" rgba="0.2 0.4 0.9 1"/>
      <camera name="down" pos="0 0 0" xyaxes="1 0 0 0 1 0" mode="fixed" euler="3.14159 0 0"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(XML)
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)

t0 = time.time()
while time.time() - t0 < 30:
    mujoco.mj_step(model, data)
    renderer.update_scene(data, camera="down")
    img = renderer.render()                      # (240, 320, 3) RGB uint8
    bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("down camera", bgr)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
