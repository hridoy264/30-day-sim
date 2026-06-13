"""
Day 9 — Sensors Demo
Camera + LiDAR-style ray fan + contact detection, all at once.

Run:  python sensors_demo.py
"""

import time
import math
import pybullet as p
import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

p.loadURDF("plane.urdf")
robot = p.loadURDF("r2d2.urdf", [0, 0, 0.5])
p.loadURDF("cube_small.urdf", [1.0, 0, 0.1])
p.loadURDF("duck_vhacd.urdf", [0, 1.0, 0.1])

W, H = 320, 240
proj = p.computeProjectionMatrixFOV(fov=60, aspect=W / H, nearVal=0.1, farVal=10)


def lidar_scan(origin, num_rays=36, ray_len=5.0):
    ends = [[origin[0] + ray_len * math.cos(2 * math.pi * i / num_rays),
             origin[1] + ray_len * math.sin(2 * math.pi * i / num_rays),
             origin[2]] for i in range(num_rays)]
    results = p.rayTestBatch([origin] * num_rays, ends)
    return [round(r[2] * ray_len, 2) for r in results]


for step in range(2000):
    p.stepSimulation()

    if step % 240 == 0:   # once per simulated second
        # --- camera ---
        view = p.computeViewMatrix([1.5, 1.5, 1.5], [0, 0, 0], [0, 0, 1])
        p.getCameraImage(W, H, view, proj)

        # --- LiDAR ---
        print("LiDAR distances:", lidar_scan([0, 0, 0.5], num_rays=12))

        # --- contacts ---
        contacts = p.getContactPoints(bodyA=robot)
        if contacts:
            print(f"  {len(contacts)} contact point(s); "
                  f"max force = {max(c[9] for c in contacts):.2f} N")

    time.sleep(1.0 / 240.0)

p.disconnect()
