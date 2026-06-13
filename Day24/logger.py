"""
Day 24 — Logging: save frames + a CSV of errors/state/commands, and an mp4 clip.
Run:  python logger.py   (needs auv_scene.xml here)
Outputs to ./logs/. Press 'q' to quit.
"""
import os
import csv
import numpy as np
import mujoco
import cv2

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)
W = 320
LOWER = np.array([20, 100, 100]); UPPER = np.array([40, 255, 255])

os.makedirs("logs/frames", exist_ok=True)
log = open("logs/run.csv", "w", newline="")
writer = csv.writer(log)
writer.writerow(["t", "found", "cross", "heading", "surge", "yaw", "heave"])
clip = cv2.VideoWriter("logs/clip.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (W, 240))


def line_errors(rgb):
    hsv = cv2.cvtColor(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER, UPPER)
    ys, xs = np.where(mask > 0)
    if len(xs) < 10:
        return False, 0.0, 0.0
    cross = (xs.mean() - W / 2) / (W / 2)
    vx, vy, _, _ = cv2.fitLine(np.column_stack([xs, ys]).astype(np.float32),
                               cv2.DIST_L2, 0, 0.01, 0.01).flatten()
    return True, float(cross), float(np.arctan2(vx, vy))


for i in range(900):
    surge, yaw, heave = 0.35, 0.0, 0.0
    data.ctrl[:] = np.clip([surge + yaw, surge - yaw, heave, heave], -1, 1)
    mujoco.mj_step(model, data)

    renderer.update_scene(data, camera="down")
    rgb = renderer.render()
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    found, cross, heading = line_errors(rgb)

    if i % 5 == 0:
        cv2.imwrite(f"logs/frames/{i:05d}.png", bgr)
    writer.writerow([f"{data.time:.3f}", found, f"{cross:.3f}",
                     f"{heading:.3f}", surge, yaw, heave])
    clip.write(bgr)

    cv2.imshow("logging", bgr)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

clip.release(); log.close(); cv2.destroyAllWindows()
print("Saved logs/run.csv, logs/frames/, logs/clip.mp4")
