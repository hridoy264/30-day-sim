"""
Day 23 — Altitude-hold using the downward depth image (Option A).
Reads distance to the seabed and P-controls heave to a target altitude.
Run:  python altitude_hold.py   (needs auv_scene.xml here)
Press 'q' to quit.
"""
import numpy as np
import mujoco
import cv2

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)

TARGET_ALT = 1.2     # desired meters above seabed
KP_ALT = 1.5


def read_altitude():
    renderer.enable_depth_rendering()
    renderer.update_scene(data, camera="down")
    depth = renderer.render()
    renderer.disable_depth_rendering()
    h, w = depth.shape[:2]
    return float(depth[h // 2, w // 2])


def allocate(surge, yaw, heave):
    return np.clip([surge + yaw, surge - yaw, heave, heave], -1, 1)


while True:
    alt = read_altitude()
    heave = KP_ALT * (TARGET_ALT - alt)            # P-control on height
    data.ctrl[:] = allocate(0.2, 0.0, heave)
    mujoco.mj_step(model, data)

    renderer.update_scene(data, camera="down")
    vis = cv2.cvtColor(renderer.render(), cv2.COLOR_RGB2BGR)
    cv2.putText(vis, f"alt={alt:.2f}m target={TARGET_ALT}m", (6, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
    cv2.imshow("altitude hold", vis)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
