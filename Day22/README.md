# Day 22 — Error Signals

**Phase 5 · Teleoperation + Vision · ~3 hours**

## 🎯 Goal
Turn the detected line into two clean numbers your controller will use: **cross-track error** (how far off-center the line is) and **heading error** (how angled the line is). These two signals *are* the input to your autonomy.

---

## The Two Errors

A line-follower needs to know two things from the camera:

### 1. Cross-track error — "am I left or right of the line?"
The horizontal offset of the line's centroid from the image center:

```python
cross_track = cx - (image_width / 2)
# negative = line is left of center; positive = right
# normalize to [-1, 1] so gains are resolution-independent:
cross_track /= (image_width / 2)
```

### 2. Heading error — "is the line angled relative to me?"
The line's tilt in the image. Fit a line to the masked pixels and read its angle:

```python
# fit a straight line through the mask points
ys, xs = np.where(mask > 0)
if len(xs) > 10:
    vx, vy, x0, y0 = cv2.fitLine(np.column_stack([xs, ys]),
                                 cv2.DIST_L2, 0, 0.01, 0.01).flatten()
    heading = np.arctan2(vx, vy)   # angle of the line vs image vertical
```

See `error_signals.py` for the full version.

---

## Why Normalize?

Dividing by half the image width makes `cross_track` range about `[-1, 1]` regardless of camera resolution. That means the PID gains you tune on Day 26 won't break if you change the image size — a small habit that saves real pain.

---

## Expose Them Cleanly

Wrap detection so it returns just the two errors plus a "found" flag:

```python
def line_errors(rgb):
    # ... detect, compute ...
    return found, cross_track, heading
```

Your Day-26 controller will call exactly this. Keep it clean: vision in, two numbers out.

---

## Visualize to Trust It

Overlay both errors on the image — a vertical center line, the detected centroid, and a printed `cross_track` / `heading`. Drive (teleop) and confirm:
- Line drifts right → `cross_track` goes positive.
- You yaw so the line tilts → `heading` changes sign.

If the numbers move sensibly as you drive, they're ready to drive the vehicle back.

---

## 📝 Today's Task
- Compute and normalize `cross_track` from the centroid.
- Compute `heading` with `cv2.fitLine` on the mask.
- Wrap it as `line_errors(rgb) -> (found, cross_track, heading)`.
- Overlay the values and drive around to confirm both behave correctly.

---

## ✅ Checkpoint
**Two clean numeric error signals as the vehicle moves.**

---

## 📚 Resources
- [OpenCV — `fitLine`](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html)
- [OpenCV — moments / centroids](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)

---

## 🔭 Next
**Day 23 — Use the second (forward/stereo) camera for an altitude-hold or forward-view signal.**
