"""
Day 10 — Mini-Project: Pick and Place
A Franka Panda arm picks up a cube using inverse kinematics.

Run:  python pick_and_place.py
"""

import time
import pybullet as p
import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

p.loadURDF("plane.urdf")
p.loadURDF("table/table.urdf", [0.5, 0, -0.65])
cube = p.loadURDF("cube_small.urdf", [0.5, 0, 0.05])

arm = p.loadURDF("franka_panda/panda.urdf", [0, 0, 0], useFixedBase=True)
EE_LINK = 11
FINGER_JOINTS = [9, 10]
DT = 1.0 / 240.0


def move_to(xyz, steps=240):
    angles = p.calculateInverseKinematics(arm, EE_LINK, xyz)
    for j in range(7):
        p.setJointMotorControl2(arm, j, p.POSITION_CONTROL,
                                targetPosition=angles[j], force=200)
    for _ in range(steps):
        p.stepSimulation()
        time.sleep(DT)


def gripper(open_):
    target = 0.04 if open_ else 0.0
    for j in FINGER_JOINTS:
        p.setJointMotorControl2(arm, j, p.POSITION_CONTROL,
                                targetPosition=target, force=50)
    for _ in range(120):
        p.stepSimulation()
        time.sleep(DT)


def grasp_ok():
    """Day 9 idea: grasp is good if both fingers touch the cube."""
    touching = {c[3] for c in p.getContactPoints(bodyA=arm, bodyB=cube)}
    return all(f in touching for f in FINGER_JOINTS)


# --- pick sequence ---
gripper(open_=True)
move_to([0.5, 0, 0.25])   # approach above
move_to([0.5, 0, 0.02])   # descend
gripper(open_=False)      # grasp
print("Grasp successful!" if grasp_ok() else "Grasp missed - try adjusting.")
move_to([0.5, 0, 0.40])   # lift

# --- place sequence (challenge: extend this!) ---
move_to([0.3, 0.3, 0.40])
move_to([0.3, 0.3, 0.05])
gripper(open_=True)       # release
move_to([0.3, 0.3, 0.40])

for _ in range(1000):
    p.stepSimulation()
    time.sleep(DT)
p.disconnect()
