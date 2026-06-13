"""
Day 25 — Robust line detection.
Smoothing + line-lost handling + morphology + min-area + edge flag.
Exposes RobustDetector.errors(rgb) -> (found, cross, heading, near_edge).
Run:  python robust_detect.py   (needs auv_scene.xml here)
"""
import numpy as np
import mujoco
import cv2

W, H = 320, 240
LOWER = np.array([20, 100, 100]); UPPER = np.array([40, 255, 255])
KERNEL = np.ones((5, 5), np.uint8)
MIN_AREA = 80


class RobustDetector:
    def __init__(self):
        self.cross = 0.0
        self.heading = 0.0
        self.lost_frames = 0

    def errors(self, rgb):
        hsv = cv2.cvtColor(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER, UPPER)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if cv2.contourArea(c) > MIN_AREA]
        if not contours:
            self.lost_frames += 1
            return False, self.cross, self.heading, False   # keep last known

        biggest = max(contours, key=cv2.contourArea)
        ys, xs = np.where(mask > 0)
        cross_new = (xs.mean() - W / 2) / (W / 2)
        vx, vy, _, _ = cv2.fitLine(np.column_stack([xs, ys]).astype(np.float32),
                                   cv2.DIST_L2, 0, 0.01, 0.01).flatten()
        heading_new = float(np.arctan2(vx, vy))

        # low-pass smoothing
        self.cross = 0.7 * self.cross + 0.3 * cross_new
        self.heading = 0.7 * self.heading + 0.3 * heading_new
        self.lost_frames = 0
        near_edge = abs(self.cross) > 0.8
        return True, self.cross, self.heading, near_edge


if __name__ == "__main__":
    model = mujoco.MjModel.from_xml_path("auv_scene.xml")
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, height=H, width=W)
    det = RobustDetector()
    while True:
        data.ctrl[:] = [0.35, 0.35, 0.0, 0.0]
        mujoco.mj_step(model, data)
        renderer.update_scene(data, camera="down")
        rgb = renderer.render()
        found, cross, heading, edge = det.errors(rgb)
        vis = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        cv2.putText(vis, f"{found} cross={cross:+.2f} edge={edge}", (6, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
        cv2.imshow("robust", vis)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
