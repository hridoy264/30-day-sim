"""
Day 19 — Integration: physics + thrusters + two cameras + scene in one loop.
Run:  python run_all.py     (needs auv_scene.xml from Day 18 in this folder)
Press 'q' to quit.
"""
import time
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
    return renderer.render()


t0 = time.time()
frames = 0
while time.time() - t0 < 30:
    data.ctrl[:] = allocate(0.4, 0.0, 0.0)        # gentle forward
    mujoco.mj_step(model, data)

    down = cv2.cvtColor(grab("down"), cv2.COLOR_RGB2BGR)
    front = cv2.cvtColor(grab("front"), cv2.COLOR_RGB2BGR)
    cv2.imshow("down | front", np.hstack([down, front]))
    frames += 1
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

dt = time.time() - t0
print(f"Rendered {frames} frames in {dt:.1f}s  (~{frames/dt:.0f} FPS)")
cv2.destroyAllWindows()
