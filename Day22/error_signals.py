"""
Day 22 — Cross-track + heading error from the downward camera.
Exposes line_errors(rgb) -> (found, cross_track, heading).
Run:  python error_signals.py   (needs auv_scene.xml here)
Press 'q' to quit.
"""
import numpy as np
import mujoco
import cv2

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)
W = 320

LOWER = np.array([20, 100, 100])
UPPER = np.array([40, 255, 255])


def line_errors(rgb):
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER, UPPER)

    ys, xs = np.where(mask > 0)
    if len(xs) < 10:
        return False, 0.0, 0.0, mask

    cx = xs.mean()
    cross_track = (cx - W / 2) / (W / 2)          # normalized [-1, 1]

    vx, vy, _, _ = cv2.fitLine(np.column_stack([xs, ys]).astype(np.float32),
                               cv2.DIST_L2, 0, 0.01, 0.01).flatten()
    heading = float(np.arctan2(vx, vy))           # radians vs vertical
    return True, float(cross_track), heading, mask


while True:
    data.ctrl[:] = [0.35, 0.35, 0.0, 0.0]
    mujoco.mj_step(model, data)

    renderer.update_scene(data, camera="down")
    rgb = renderer.render()
    vis = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    found, cross, heading, mask = line_errors(rgb)
    cv2.line(vis, (W // 2, 0), (W // 2, 240), (255, 255, 255), 1)
    cv2.putText(vis, f"found={found} cross={cross:+.2f} head={heading:+.2f}",
                (6, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

    cv2.imshow("errors", vis)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
