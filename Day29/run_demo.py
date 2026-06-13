"""
Day 29 — One repeatable launch: teleop -> autonomy, optional water conditions.
This is your capstone demo entry point.

Run:  python run_demo.py
Needs: auv_scene.xml and robust_detect.py in this folder.

Keys:  W/A/S/D/R/F = teleop drive   |  m = toggle teleop/autonomy
       1/2/3 = water condition      |  q = quit
"""
import numpy as np
import mujoco
import cv2
from robust_detect import RobustDetector

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)
det = RobustDetector()

mode = "teleop"
prev_cross = 0.0
lost = 0
condition = "1-clear"
WATER = {
    "1-clear": dict(tint=(1.0, 1.0, 1.0), haze=0.05, noise=3, blur=1),
    "2-murky": dict(tint=(1.2, 1.0, 0.6), haze=0.35, noise=8, blur=3),
    "3-dim":   dict(tint=(1.1, 0.9, 0.7), haze=0.25, noise=14, blur=5),
}


def allocate(s, y, h):
    return np.clip([s + y, s - y, h, h], -1, 1)


def apply_water(img, tint, haze, noise, blur):
    out = img.astype(np.float32) * np.array(tint)
    out = (1 - haze) * out + haze * np.full_like(out, 180.0)
    out += np.random.normal(0, noise, out.shape)
    out = np.clip(out, 0, 255).astype(np.uint8)
    return cv2.GaussianBlur(out, (blur, blur), 0) if blur % 2 else out


def teleop(key):
    s = y = h = 0.0
    if key == ord('w'): s = 0.5
    elif key == ord('s'): s = -0.5
    if key == ord('a'): y = 0.5
    elif key == ord('d'): y = -0.5
    if key == ord('r'): h = 0.5
    elif key == ord('f'): h = -0.5
    return s, y, h


def autonomy(rgb):
    global prev_cross, lost
    found, cross, heading, edge = det.errors(rgb)
    if not found:
        lost += 1
        return (0.1, 0.4 * np.sign(prev_cross or 1.0), 0.0)
    lost = 0
    yaw = -(1.4 * cross + 0.35 * (cross - prev_cross) + 0.5 * heading)
    prev_cross = cross
    return (0.3, yaw, 0.0)


print(__doc__)
while True:
    renderer.update_scene(data, camera="down")
    raw = cv2.cvtColor(renderer.render(), cv2.COLOR_RGB2BGR)
    shown = apply_water(raw, **WATER[condition])
    shown_rgb = cv2.cvtColor(shown, cv2.COLOR_BGR2RGB)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    if key == ord('m'): mode = "auto" if mode == "teleop" else "teleop"
    if key in (ord('1'), ord('2'), ord('3')):
        condition = {ord('1'): "1-clear", ord('2'): "2-murky", ord('3'): "3-dim"}[key]

    cmd = teleop(key) if mode == "teleop" else autonomy(shown_rgb)
    data.ctrl[:] = allocate(*cmd)
    mujoco.mj_step(model, data)

    cv2.putText(shown, f"MODE={mode}  WATER={condition}  (m/1-3/q)", (6, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
    cv2.imshow("AUV line-following demo", shown)

cv2.destroyAllWindows()
