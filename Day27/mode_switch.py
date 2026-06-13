"""
Day 27 — Teleop <-> Autonomy toggle + line-loss recovery.
Both modes produce the same (surge, yaw, heave); press 'm' to switch, 'q' to quit.
Run:  python mode_switch.py
Needs: auv_scene.xml and robust_detect.py in this folder.
"""
import numpy as np
import mujoco
import cv2
from robust_detect import RobustDetector

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)
det = RobustDetector()

Kp_yaw, Kd_yaw = 1.4, 0.35
prev_cross = 0.0
lost = 0
mode = "teleop"


def allocate(surge, yaw, heave):
    return np.clip([surge + yaw, surge - yaw, heave, heave], -1, 1)


def autonomy_command(rgb):
    global prev_cross, lost
    found, cross, heading, edge = det.errors(rgb)
    if not found:
        lost += 1
        if lost > 10:                       # search toward last known side
            return 0.1, 0.4 * np.sign(prev_cross or 1.0), 0.0
        return 0.1, 0.0, 0.0
    lost = 0
    yaw = -(Kp_yaw * cross + Kd_yaw * (cross - prev_cross)
            + 0.5 * heading)                # blend heading for curves
    prev_cross = cross
    return 0.3, yaw, 0.0


def teleop_command(key):
    s = y = h = 0.0
    if key == ord('w'): s = 0.5
    elif key == ord('s'): s = -0.5
    if key == ord('a'): y = 0.5
    elif key == ord('d'): y = -0.5
    if key == ord('r'): h = 0.5
    elif key == ord('f'): h = -0.5
    return s, y, h


while True:
    renderer.update_scene(data, camera="down")
    rgb = renderer.render()
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('m'):
        mode = "auto" if mode == "teleop" else "teleop"

    if mode == "teleop":
        cmd = teleop_command(key)
    else:
        cmd = autonomy_command(rgb)

    data.ctrl[:] = allocate(*cmd)
    mujoco.mj_step(model, data)

    vis = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    cv2.putText(vis, f"MODE={mode}  (m=switch)", (6, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow("mode switch", vis)

cv2.destroyAllWindows()
