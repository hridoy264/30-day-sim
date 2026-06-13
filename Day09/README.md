# Day 9 — Adding Sensors: Cameras, Rays & Contacts

## 🎯 Today's Goal
Give your robot **senses**. You'll attach a camera, cast rays (a simple LiDAR), and detect physical contacts — the three perception building blocks behind almost every robot behavior.

---

## Overview

A robot without sensors is just an animation. Sensing is what turns simulation into *robotics* — the robot perceives its world and reacts. Today you add the three most important sensor types in PyBullet. The same three concepts reappear in MuJoCo, Gazebo, and Isaac, so this knowledge transfers everywhere.

---

## Sensor 1 — The Camera

A simulated camera renders the scene from a viewpoint and hands you the pixels — exactly what a real camera-fed vision system would get.

```python
import pybullet as p

width, height = 320, 240

view = p.computeViewMatrix(
    cameraEyePosition=[1, 1, 1],     # where the camera is
    cameraTargetPosition=[0, 0, 0],  # what it looks at
    cameraUpVector=[0, 0, 1],        # which way is up
)
proj = p.computeProjectionMatrixFOV(
    fov=60, aspect=width/height, nearVal=0.1, farVal=10,
)

img = p.getCameraImage(width, height, view, proj)
rgb = img[2]          # color pixels  (H x W x 4)
depth = img[3]        # depth buffer  (H x W)   <- distance to each pixel!
seg = img[4]          # segmentation: which object each pixel belongs to
```

> 💡 A simulated camera gives you something real cameras can't: a **perfect depth image** and a **segmentation mask** (which object is which). This is gold for training vision models — a major reason simulation is used in AI.

To make the camera **follow the robot**, recompute the view matrix each step from the robot's current pose.

---

## Sensor 2 — Ray Casting (a simple LiDAR)

A ray is a virtual laser: shoot it from A to B, find the first thing it hits and how far. Many rays in a fan = a LiDAR scanner.

```python
start = [0, 0, 0.5]
end   = [2, 0, 0.5]
hit = p.rayTest(start, end)[0]
hit_object_id = hit[0]    # -1 means nothing hit
hit_fraction  = hit[2]    # 0..1 along the ray (distance)
hit_position  = hit[3]    # XYZ of the hit point
```

For a real LiDAR, cast many rays in a circle:

```python
import math
num_rays = 36
ray_len = 5.0
origin = [0, 0, 0.5]
ends = [[origin[0] + ray_len*math.cos(2*math.pi*i/num_rays),
         origin[1] + ray_len*math.sin(2*math.pi*i/num_rays),
         origin[2]] for i in range(num_rays)]
results = p.rayTestBatch([origin]*num_rays, ends)   # batch = fast!
distances = [r[2]*ray_len for r in results]
```

> 💡 Use **`rayTestBatch`**, not many `rayTest` calls — casting rays in one batch is dramatically faster. This matters when you simulate a 360-beam LiDAR every step.

---

## Sensor 3 — Contact Detection

Knowing *what is touching what* powers grasping, collision checking, and footstep detection.

```python
# all contact points involving the robot this step
contacts = p.getContactPoints(bodyA=robot)
for c in contacts:
    other_body = c[2]      # the other object's id
    contact_pos = c[5]     # where contact happens (world XYZ)
    normal_force = c[9]    # how hard they're pressing
    print("touching", other_body, "force", normal_force)
```

This is how a gripper "knows" it has grabbed an object (you'll use it in tomorrow's project), or how a walking robot detects its foot hit the ground.

---

## Putting It Together

See `sensors_demo.py` — it spawns objects, mounts a camera, sweeps a LiDAR fan, and prints contacts each step. Watching all three streams at once is the moment a "simulation" becomes a "robot."

---

## 📝 Today's Task

1. Run `sensors_demo.py`. Observe the camera window, printed LiDAR distances, and contact reports.
2. **Camera:** move the `cameraEyePosition` and re-render. Save an RGB frame with `matplotlib` (`plt.imsave`).
3. **LiDAR:** change `num_rays` to 8, then 72. Print the distance array — see your scanner's resolution change.
4. **Contacts:** drop a cube onto the floor and print `getContactPoints` — watch the normal force spike on impact.
5. Bonus: make the camera follow a moving object by recomputing the view matrix each step.

---

## ✅ Key Takeaways

✓ Three core sensors: **camera** (RGB + depth + segmentation), **rays** (LiDAR), **contacts** (touch/force).

✓ Simulated cameras hand you **perfect depth and segmentation** — a superpower for AI training.

✓ Cast many rays with **`rayTestBatch`** for speed; a fan of rays is a LiDAR.

✓ `getContactPoints` reveals what's touching and how hard — the basis of grasping & footstep detection.

✓ These same three sensor ideas reappear in every other simulator in this course.

---

## 📚 References & Resources

- [PyBullet Quickstart — camera, rays, contacts](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit)
- [Synthetic data for vision (why sim cameras matter)](https://developer.nvidia.com/blog/tag/synthetic-data/)
- [Bullet pybullet examples (GitHub)](https://github.com/bulletphysics/bullet3/tree/master/examples/pybullet/examples)

---

## 🔭 What's Next?

**Day 10 — Mini-Project!** You'll combine loading, control, and sensing into a single program: a robot arm that detects an object and picks it up. Your first real robotics task. 🛠

---

*"Control without sensing is a puppet. Sensing makes it a robot."*
