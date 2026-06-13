# Day 20 — Teleoperation

**Phase 5 · Teleoperation + Vision · ~3 hours**

## 🎯 Goal
Fly the vehicle by hand: map keyboard (or gamepad) input to your thrust-vector command and drive it around the scene live. **Teleop = done** is today's milestone.

---

## Why Teleop First

Manual control proves your whole pipeline works — thrusters, allocation, dynamics, cameras — *before* you hand control to an algorithm. It's also the fallback mode in your final demo (drive to the line by hand, then switch to autonomy on Day 26).

---

## Keyboard Teleop

The cleanest approach on the Mac is to read keys through the OpenCV window (no extra dependency) and feed them into your Day-15 `allocate()`. See `teleop_keyboard.py`:

```python
key = cv2.waitKey(1) & 0xFF
surge = yaw = heave = 0.0
if key == ord('w'): surge =  0.6     # forward
if key == ord('s'): surge = -0.6     # back
if key == ord('a'): yaw   =  0.5     # turn left
if key == ord('d'): yaw   = -0.5     # turn right
if key == ord('r'): heave =  0.5     # rise
if key == ord('f'): heave = -0.5     # dive
data.ctrl[:] = allocate(surge, yaw, heave)
```

Hold-to-move feel: keep applying the command for a short window after each keypress, or use the gamepad approach below for smooth analog control.

---

## Gamepad Teleop (smoother, optional)

A gamepad gives analog thrust via `pygame`:

```python
import pygame
pygame.init(); pygame.joystick.init()
js = pygame.joystick.Joystick(0); js.init()
# in the loop:
pygame.event.pump()
surge = -js.get_axis(1)     # left stick Y -> forward/back
yaw   = -js.get_axis(0)     # left stick X -> turn
heave = -js.get_axis(3)     # right stick Y -> up/down
```

Analog sticks feel far more like piloting an ROV than on/off keys.

---

## 📝 Today's Task
- Wire `teleop_keyboard.py` to your Day-18 scene and drive with `W/A/S/D/R/F`.
- Fly a lap of the scene; follow the line *manually* to confirm the camera shows it well.
- (Optional) Set up gamepad control with `pygame` for analog feel.
- Fix any inverted control (a sign flip in `allocate` or the key mapping).

---

## ✅ Checkpoint
**You can drive the vehicle manually. Teleop = DONE.**

---

## 📚 Resources
- [OpenCV `waitKey` (keyboard input)](https://docs.opencv.org)
- [pygame joystick docs](https://www.pygame.org/docs/ref/joystick.html)

---

## 🔭 Next
**Day 21 — OpenCV line detection: threshold the line and find it in the downward camera.**
