# Day 17 — Mount Two Cameras

**Phase 4 · Build the Underwater Vehicle · ~3 hours**

## 🎯 Goal
Add two `<camera>` elements to the vehicle — one **downward** (for line-following) and one **forward** — and render both offscreen to image arrays at the same time.

---

## Adding the Cameras

Cameras are children of the vehicle body, so they move with it. Add to your tuned `auv` model (see `auv_cameras.xml`):

```xml
<body name="rov" pos="0 0 0" gravcomp="1">
  <freejoint/>
  <geom type="box" size="0.23 0.15 0.10" .../>
  ...thrusters...

  <!-- downward camera: looks at the seabed for the line -->
  <camera name="down" pos="0 0 -0.10" euler="3.14159 0 0" fovy="70"/>
  <!-- forward camera: looks ahead -->
  <camera name="front" pos="0.24 0 0" euler="1.5708 0 -1.5708" fovy="60"/>
</body>
```

- `pos` is relative to the vehicle body (it rides along).
- `euler` aims the camera — `down` points at the seabed; `front` points along the vehicle's forward axis.
- `fovy` is the vertical field of view in degrees.

> Aiming cameras is fiddly. Render, look, adjust `euler`, repeat. The downward camera **must** clearly see the floor beneath the vehicle.

---

## Rendering Both Feeds

Use one `Renderer` and switch the camera each call (see `two_cameras.py`):

```python
import mujoco, numpy as np, cv2
renderer = mujoco.Renderer(model, 240, 320)

def grab(cam):
    renderer.update_scene(data, camera=cam)
    return renderer.render()                 # RGB array

while running:
    mujoco.mj_step(model, data)
    down  = grab("down")
    front = grab("front")
    # show side by side
    combo = np.hstack([cv2.cvtColor(down,  cv2.COLOR_RGB2BGR),
                       cv2.cvtColor(front, cv2.COLOR_RGB2BGR)])
    cv2.imshow("down | front", combo); cv2.waitKey(1)
```

> One `Renderer` reused for both cameras is fine and efficient on the M4. Avoid creating a new `Renderer` every frame — that leaks memory.

---

## 📝 Today's Task
- Add `down` and `front` cameras to the vehicle.
- Render both and show them side by side.
- Drive the vehicle (Day 15 command) and confirm both feeds move with it.
- Adjust `down` until the floor directly below is centered in its view.

---

## ✅ Checkpoint
**Two live camera image streams from the moving vehicle.**

---

## 📚 Resources
- [MuJoCo camera (XML)](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-camera)
- [MuJoCo rendering](https://mujoco.readthedocs.io/en/stable/python.html#rendering)

---

## 🔭 Next
**Day 18 — Build the seabed and a high-contrast line for the downward camera to follow.**
