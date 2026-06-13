"""
Day 26 — Close the autonomy loop: vision -> PID -> thrust.
Vehicle follows the line autonomously.
Run:  python autonomy_loop.py
Needs: auv_scene.xml and robust_detect.py (from Day 25) in this folder.
Press 'q' to quit.
"""
import numpy as np
import mujoco
import cv2
from robust_detect import RobustDetector

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)
det = RobustDetector()

Kp_yaw, Kd_yaw = 1.2, 0.3
FORWARD = 0.35
prev_cross = 0.0


def allocate(surge, yaw, heave):
    return np.clip([surge + yaw, surge - yaw, heave, heave], -1, 1)


def grab(cam):
    renderer.update_scene(data, camera=cam)
    return renderer.render()


while True:
    mujoco.mj_step(model, data)
    rgb = grab("down")
    found, cross, heading, edge = det.errors(rgb)

    d_cross = cross - prev_cross
    yaw = -(Kp_yaw * cross + Kd_yaw * d_cross)   # flip sign if it runs away
    prev_cross = cross
    surge = FORWARD if found else 0.1            # slow when unsure

    data.ctrl[:] = allocate(surge, yaw, 0.0)

    vis = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    cv2.line(vis, (160, 0), (160, 240), (255, 255, 255), 1)
    cv2.putText(vis, f"AUTO found={found} cross={cross:+.2f} yaw={yaw:+.2f}",
                (6, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
    cv2.imshow("autonomy", vis)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
