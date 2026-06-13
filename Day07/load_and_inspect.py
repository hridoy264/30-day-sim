"""
Day 7 — Loading & Inspecting Robots
Prints a robot's joint/link map and builds a small scene.

Run:  python load_and_inspect.py
"""

import time
import pybullet as p
import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# --- a small scene ---
p.loadURDF("plane.urdf")
p.loadURDF("table/table.urdf", [0, 0, 0])
p.loadURDF("tray/tray.urdf", [0, 0, 0.65])
p.loadURDF("cube_small.urdf", [0.1, 0, 0.8])
p.loadURDF("duck_vhacd.urdf", [-0.1, 0, 0.8])

# --- a robot to inspect ---
robot = p.loadURDF("r2d2.urdf", [0.6, 0, 0.7])

# --- print the joint/link map ---
num_joints = p.getNumJoints(robot)
print(f"\nRobot has {num_joints} joints:\n")
type_names = {0: "REVOLUTE", 1: "PRISMATIC", 2: "SPHERICAL",
              3: "PLANAR", 4: "FIXED"}
for i in range(num_joints):
    info = p.getJointInfo(robot, i)
    jname = info[1].decode("utf-8")
    jtype = type_names.get(info[2], str(info[2]))
    lname = info[12].decode("utf-8")
    print(f"[{i:2d}] joint='{jname}'  type={jtype}  link='{lname}'")

# --- run ---
for _ in range(2400):
    p.stepSimulation()
    time.sleep(1.0 / 240.0)

p.disconnect()
