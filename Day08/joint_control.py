"""
Day 8 — Joint Control
A KUKA arm waves using position control driven by a sine wave.

Run:  python joint_control.py
"""

import time
import math
import pybullet as p
import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

p.loadURDF("plane.urdf")
arm = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

t = 0.0
dt = 1.0 / 240.0
while t < 20.0:
    # smooth waving: sine wave -> joint position target
    target = math.sin(t) * 1.0
    p.setJointMotorControl2(arm, jointIndex=3,
                            controlMode=p.POSITION_CONTROL,
                            targetPosition=target, force=200)
    p.stepSimulation()
    time.sleep(dt)
    t += dt

p.disconnect()
