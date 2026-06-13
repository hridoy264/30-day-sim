# Day 21 — OpenCV Line Detection (Part 1)

**Phase 5 · Teleoperation + Vision · ~3 hours**

## 🎯 Goal
Take the downward camera array, convert it to OpenCV, **threshold the line in HSV**, and find its contour/centroid. This is the perception half of autonomy.

---

## The Vision Pipeline (3 steps)

1. **Convert to HSV.** HSV (hue, saturation, value) separates *color* from *brightness*, so a color threshold survives lighting changes far better than RGB. Essential for the murky-water robustness on Day 28.
2. **Threshold** the line's color → a binary mask (white = line, black = everything else).
3. **Find contours** in the mask, pick the biggest, compute its **centroid** (the line's position in the image).

See `line_detect.py`:

```python
import cv2, numpy as np

def detect_line(rgb):
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    # yellow line -> tune these ranges to YOUR line color
    lower = np.array([20, 100, 100])
    upper = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, mask
    biggest = max(contours, key=cv2.contourArea)
    M = cv2.moments(biggest)
    if M["m00"] == 0:
        return None, mask
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy), mask
```

---

## Tuning the HSV Range

This is the make-or-break step:

- Print HSV values of line pixels (click in a window, or sample the center) to find the right `lower`/`upper`.
- Too narrow → line disappears under lighting changes. Too wide → it grabs the seabed too.
- For a yellow line, hue ~20–40; raise saturation/value minimums to reject the dull seabed.

Draw the detection back on the image so you can *see* it working:

```python
center, mask = detect_line(rgb)
if center:
    cv2.circle(vis, center, 6, (0, 0, 255), -1)   # red dot on the line
cv2.imshow("detection", vis)
cv2.imshow("mask", mask)
```

---

## 📝 Today's Task
- Run `line_detect.py` on the live downward feed.
- Tune the HSV range until the mask cleanly isolates the line.
- Draw the centroid (and a bounding box) on the line as the vehicle moves.
- Drive (teleop) over the line and watch the dot track it.

---

## ✅ Checkpoint
**Your code draws a box/centroid on the detected line.**

---

## 📚 Resources
- [OpenCV — color spaces & thresholding](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
- [OpenCV — contours](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html)

---

## 🔭 Next
**Day 22 — Turn the detection into clean numeric error signals (cross-track + heading).**
