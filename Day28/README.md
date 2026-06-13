# Day 28 — Simulated Turbidity / Domain Randomization

**Phase 6 · Autonomy + Robustness · ~3 hours**

## 🎯 Goal
Fake real underwater conditions — murky water, color casts, changing light, noise — and make your line-follower survive them. This is **domain randomization** (Day 1's concept) made concrete, and it's what would make your system transfer to reality.

---

## Why Murky Water Matters

Real underwater images are nothing like your clean sim: they're blue-green, low-contrast, hazy with suspended particles ("turbidity"), and unevenly lit. A detector tuned to one perfect look is brittle. By testing across many faked conditions, you force the detector to be robust — exactly the sim-to-real insight from Day 1.

---

## Faking Underwater Conditions

Apply these effects to the rendered camera image before detection (see `turbidity.py`):

```python
def apply_water(img, tint=(1.1, 1.0, 0.7), haze=0.3, noise=8, blur=3):
    out = img.astype(np.float32)
    out *= np.array(tint)                          # blue-green color cast (BGR)
    fog = np.full_like(out, 180)                    # hazy grey
    out = (1 - haze) * out + haze * fog             # turbidity / haze
    out += np.random.normal(0, noise, out.shape)    # sensor noise
    out = np.clip(out, 0, 255).astype(np.uint8)
    if blur: out = cv2.GaussianBlur(out, (blur, blur), 0)
    return out
```

| Effect | Simulates |
|--------|-----------|
| color tint | blue-green absorption of water |
| haze blend | turbidity / suspended particles |
| Gaussian noise | camera sensor noise |
| blur | water scattering, soft focus |
| varied lighting | depth & sun position |

You can also vary the MuJoCo scene light intensity and the seabed/line colors between runs.

---

## The Robustness Test

1. Run autonomy under 3+ different `apply_water` settings (clear, murky-green, dim+noisy).
2. Where the detector fails, **widen/adjust the HSV range** and lean on the morphology cleanup (Day 25).
3. Goal: the *same* detector and gains follow the line across all conditions — no per-condition retuning.

> If you must retune HSV for each condition, your range is too tight. Robustness means *one* setting that tolerates the whole range — that's the domain-randomization payoff.

---

## 📝 Today's Task
- Add `apply_water()` and run it on the camera feed before detection.
- Test autonomy under at least 3 distinct "water" conditions.
- Adjust the detector (HSV width, morphology) until one setting handles all of them.
- Save a clip of the vehicle tracking the line in murky water — great for the capstone.

---

## ✅ Checkpoint
**Line-follower survives 3+ different "water" conditions.**

---

## 📚 Resources
- Day 1 (domain randomization concept); Day 25 (robust detection).
- [OpenCV — image arithmetic & blur](https://docs.opencv.org/4.x/d2/de8/group__core__array.html)

---

## 🔭 Next
**Day 29 — Buffer + tuning: one repeatable launch script (build → teleop → autonomy).**
