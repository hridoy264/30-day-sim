# Day 25 — Robustness Pass on Detection

**Phase 5 · Teleoperation + Vision · ~2.5 hours**

## 🎯 Goal
Make the detector steady, not jumpy: survive partial occlusion and brief line loss, and handle the line leaving the frame edge. A robust detector is what makes autonomy stable tomorrow.

---

## Real Detectors Fail — Plan For It

Up to now you tested on a clean line. In motion, detection gets messy: the line partly leaves the frame, glare/shadow breaks the mask, or the vehicle briefly loses it on a turn. If your controller reacts to every jumpy reading, it'll wobble. Today you make detection *graceful*.

---

## Robustness Techniques

### 1. Smooth the error (low-pass filter)
Don't trust a single noisy reading — blend with the previous value:

```python
cross_smooth = 0.7 * cross_smooth + 0.3 * cross_new
```

This kills jitter while staying responsive.

### 2. Handle "line lost"
When no contour is found, **don't return garbage** — return the last known direction and a `lost` flag so the controller can act sensibly (slow down, search):

```python
if not found:
    lost_frames += 1
    return False, last_cross, last_heading
else:
    lost_frames = 0
    last_cross, last_heading = cross, heading
```

### 3. Clean the mask (morphology)
Remove speckle and fill gaps so contours are solid:

```python
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # remove noise
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # fill holes
```

### 4. Ignore tiny blobs
Reject contours below a minimum area so a stray pixel cluster doesn't masquerade as the line.

### 5. Edge handling
If the line's centroid is near the frame edge, that's a sign it's leaving — flag it so the controller can turn harder to recover.

See `robust_detect.py` for all of these combined.

---

## Test It Hard

- Drive so the line briefly exits the frame — does the detector hold steady and recover?
- Add a temporary occluder over part of the line — does morphology + min-area keep it tracking?
- Confirm the error signal is smooth (no spikes) on your logged plot from Day 24.

---

## 📝 Today's Task
- Add smoothing, line-lost handling, morphology, min-area, and edge flags to your detector.
- Replay your Day-24 logs and confirm the error trace is smooth and gap-tolerant.
- Drive through occlusion/loss scenarios and verify steady recovery.

---

## ✅ Checkpoint
**Detector is steady, not jumpy** (survives partial occlusion and brief line loss).

---

## 📚 Resources
- [OpenCV — morphological transforms](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
- [Low-pass / exponential smoothing](https://en.wikipedia.org/wiki/Exponential_smoothing)

---

## 🔭 Next
**Day 26 — Close the autonomy loop: errors → PID → thrust. The vehicle follows the line itself.**
