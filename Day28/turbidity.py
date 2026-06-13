"""
Day 28 — Simulated turbidity / domain randomization.
Applies underwater effects to the camera feed, then runs detection on it.
Run:  python turbidity.py
Needs: auv_scene.xml and robust_detect.py in this folder.
Keys: 1/2/3 switch water condition, q quit.
"""
import numpy as np
import mujoco
import cv2
from robust_detect import RobustDetector

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)
det = RobustDetector()

CONDITIONS = {
    "1-clear":   dict(tint=(1.0, 1.0, 1.0), haze=0.05, noise=3,  blur=1),
    "2-murky":   dict(tint=(1.2, 1.0, 0.6), haze=0.35, noise=8,  blur=3),
    "3-dim":     dict(tint=(1.1, 0.9, 0.7), haze=0.25, noise=14, blur=5),
}
current = "2-murky"


def apply_water(img, tint, haze, noise, blur):
    out = img.astype(np.float32) * np.array(tint)
    fog = np.full_like(out, 180.0)
    out = (1 - haze) * out + haze * fog
    out += np.random.normal(0, noise, out.shape)
    out = np.clip(out, 0, 255).astype(np.uint8)
    if blur and blur % 2 == 1:
        out = cv2.GaussianBlur(out, (blur, blur), 0)
    return out


def allocate(surge, yaw, heave):
    return np.clip([surge + yaw, surge - yaw, heave, heave], -1, 1)


prev_cross = 0.0
while True:
    renderer.update_scene(data, camera="down")
    rgb = renderer.render()
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    murky = apply_water(bgr, **CONDITIONS[current])
    murky_rgb = cv2.cvtColor(murky, cv2.COLOR_BGR2RGB)

    found, cross, heading, edge = det.errors(murky_rgb)
    yaw = -(1.3 * cross + 0.3 * (cross - prev_cross))
    prev_cross = cross
    data.ctrl[:] = allocate(0.3 if found else 0.1, yaw, 0.0)
    mujoco.mj_step(model, data)

    cv2.putText(murky, f"{current} found={found} cross={cross:+.2f}", (6, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
    cv2.imshow("turbid water", murky)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'): break
    if k in (ord('1'), ord('2'), ord('3')):
        current = {ord('1'): "1-clear", ord('2'): "2-murky", ord('3'): "3-dim"}[k]

cv2.destroyAllWindows()
