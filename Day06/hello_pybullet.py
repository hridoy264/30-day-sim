"""
Day 6 — Hello PyBullet
Your first complete physics simulation.

Run:  python hello_pybullet.py
(Make sure your venv is active and `pip install pybullet` is done.)
"""

import time
import pybullet as p
import pybullet_data

# 1. CONNECT — p.GUI opens a window; use p.DIRECT for headless/fast runs
physicsClient = p.connect(p.GUI)

# 2. CONFIGURE
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # locate built-in models
p.setGravity(0, 0, -9.81)                               # Earth gravity (Z is up)

# 3. LOAD
plane_id = p.loadURDF("plane.urdf")                     # the ground
start_pos = [0, 0, 1]                                   # 1 meter above the floor
start_ori = p.getQuaternionFromEuler([0, 0, 0])        # no rotation
robot_id = p.loadURDF("r2d2.urdf", start_pos, start_ori)

# 4. STEP — run ~10 seconds at 240 Hz
for i in range(2400):
    p.stepSimulation()
    time.sleep(1.0 / 240.0)   # slow to real time so we can watch

# read the final pose
pos, ori = p.getBasePositionAndOrientation(robot_id)
print("Final position:", pos)

# 5. DISCONNECT
p.disconnect()
