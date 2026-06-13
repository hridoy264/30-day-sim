"""
Day 17 — Render two onboard cameras (down + front) side by side.
Run:  python two_cameras.py   (needs auv_cameras.xml here)
Press 'q' to quit.
"""
import time
import numpy as np
import mujoco
import cv2

model = mujoco.MjModel.from_xml_path("auv_cameras.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)


def grab(cam):
    renderer.update_scene(data, camera=cam)
    return renderer.render()


t0 = time.time()
while time.time() - t0 < 30:
    # gentle forward thrust so the feeds move
    data.ctrl[:] = [0.4, 0.4, 0.0, 0.0]
    mujoco.mj_step(model, data)

    down = cv2.cvtColor(grab("down"), cv2.COLOR_RGB2BGR)
    front = cv2.cvtColor(grab("front"), cv2.COLOR_RGB2BGR)
    cv2.imshow("down | front", np.hstack([down, front]))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
