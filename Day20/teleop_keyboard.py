"""
Day 20 — Keyboard teleoperation of the AUV.
Drive with W/A/S/D (surge/yaw), R/F (rise/dive), Q to quit.
Run:  python teleop_keyboard.py   (needs auv_scene.xml here)
"""
import numpy as np
import mujoco
import cv2

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)


def allocate(surge, yaw, heave):
    return np.clip([surge + yaw, surge - yaw, heave, heave], -1, 1)


def grab(cam):
    renderer.update_scene(data, camera=cam)
    return cv2.cvtColor(renderer.render(), cv2.COLOR_RGB2BGR)


print("Teleop: W/S surge, A/D yaw, R/F heave, Q quit")
while True:
    key = cv2.waitKey(1) & 0xFF
    surge = yaw = heave = 0.0
    if key == ord('w'): surge = 0.6
    elif key == ord('s'): surge = -0.6
    if key == ord('a'): yaw = 0.5
    elif key == ord('d'): yaw = -0.5
    if key == ord('r'): heave = 0.5
    elif key == ord('f'): heave = -0.5
    if key == ord('q'): break

    data.ctrl[:] = allocate(surge, yaw, heave)
    mujoco.mj_step(model, data)

    view = np.hstack([grab("down"), grab("front")])
    cv2.imshow("down | front  (drive me)", view)

cv2.destroyAllWindows()
