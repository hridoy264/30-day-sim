"""
Day 21 — OpenCV line detection on the downward camera.
Thresholds the line in HSV and marks its centroid.
Run:  python line_detect.py   (needs auv_scene.xml here)
Press 'q' to quit.
"""
import numpy as np
import mujoco
import cv2

model = mujoco.MjModel.from_xml_path("auv_scene.xml")
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)

# yellow line HSV range -- TUNE to your line color
LOWER = np.array([20, 100, 100])
UPPER = np.array([40, 255, 255])


def detect_line(rgb):
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER, UPPER)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, mask
    biggest = max(contours, key=cv2.contourArea)
    M = cv2.moments(biggest)
    if M["m00"] == 0:
        return None, mask
    cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
    return (cx, cy), mask


while True:
    data.ctrl[:] = [0.35, 0.35, 0.0, 0.0]      # drift forward over the line
    mujoco.mj_step(model, data)

    renderer.update_scene(data, camera="down")
    rgb = renderer.render()
    vis = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    center, mask = detect_line(rgb)
    if center:
        cv2.circle(vis, center, 6, (0, 0, 255), -1)

    cv2.imshow("detection", vis)
    cv2.imshow("mask", mask)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
