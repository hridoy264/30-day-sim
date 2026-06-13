# Day 10 — Offscreen Camera Rendering

**Phase 2 · MuJoCo Fundamentals · ~3 hours**

## 🎯 Goal
Render a MuJoCo `<camera>` to a **NumPy image array** in Python and display it with OpenCV/matplotlib. **This is the bridge to your vision pipeline** — without it, there's no line-following.

---

## Why This Is Pivotal

Your whole autonomy plan is: *camera sees line → compute error → drive thrusters*. That starts here, with turning what a camera "sees" into an array of pixels your code can process. Get this solid; everything in Phase 5 depends on it.

---

## The `Renderer` API

MuJoCo's `Renderer` renders any scene (from any declared camera) straight to a NumPy array — no window required (perfect for headless processing and for the Mac).

```python
import mujoco
import numpy as np

model = mujoco.MjModel.from_xml_path("scene_with_camera.xml")
data  = mujoco.MjData(model)
mujoco.mj_forward(model, data)

renderer = mujoco.Renderer(model, height=240, width=320)
renderer.update_scene(data, camera="onboard")   # use a named <camera>
img = renderer.render()          # -> (240, 320, 3) uint8 RGB array
print(img.shape, img.dtype)
```

That `img` is exactly what OpenCV expects. You now have eyes.

---

## Show It with OpenCV

```python
import cv2
# MuJoCo gives RGB; OpenCV expects BGR
bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
cv2.imshow("onboard camera", bgr)
cv2.waitKey(1)
```

A scene with a downward-looking camera over a colored strip is in `render_camera.py` — run it and you'll see a live camera feed rendered from inside the simulation.

> **Mac note:** the `Renderer` uses your M4's integrated GPU and works without a dedicated GPU. If you hit a context error, make sure you're on a recent `mujoco` version and rendering on the main thread.

---

## Depth & Segmentation (bonus)

The renderer can also output a **depth** image and a **segmentation** map:

```python
renderer.enable_depth_rendering()
depth = renderer.render()        # distance per pixel
renderer.disable_depth_rendering()
```

Depth will be handy for the Day-23 altitude-hold idea.

---

## 📝 Today's Task
- Build a small scene with a `<camera>` and render it to an array; print its shape.
- Display the feed live with OpenCV while the sim steps.
- Move the camera/scene and confirm the image updates.
- Bonus: render a depth image and visualize it.

---

## ✅ Checkpoint
**You can grab a camera image as an array** and display it.

---

## 📚 Resources
- [MuJoCo rendering docs](https://mujoco.readthedocs.io/en/stable/python.html#rendering)
- [OpenCV docs](https://docs.opencv.org)

---

## 🔭 Next
**Day 11 — Marine dynamics theory: added mass, drag, buoyancy, and the Fossen 6-DOF picture.**
