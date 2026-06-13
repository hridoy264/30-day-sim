# Appendix A — Optional Stonefish Track (when you get GPU access)

Do this *after* the MuJoCo project, when you have a GPU. **Your control + vision code ports over; only the simulator host changes.** Stonefish gives photorealistic water and high-fidelity camera/sonar simulation that MuJoCo doesn't.

## Why It's Separate

Stonefish's camera simulation needs **OpenGL 4.3+**, which macOS does not provide (Apple caps at OpenGL 4.1). So the M4 Mac can't run it natively. This is purely a rendering-host limitation — your algorithms are unaffected.

## Where to Run It

- **Cloud GPU (recommended):** rent an hourly Linux GPU instance, install Ubuntu + ROS 2 + Stonefish there. Cleanest path; costs a few dollars/hour only while in use.
- **Your Core i5 Linux laptop (free, slow):** the Intel iGPU + Mesa drivers expose OpenGL 4.3+, so Stonefish *may* run. Keep scenes minimal and camera resolution low (e.g., 320×240); expect low FPS. Fine for slow development, frustrating for real-time.
- **Not viable:** the M4 Mac natively (OpenGL 4.1 ceiling). Asahi Linux reaches OpenGL 4.6 on Apple Silicon, but M4 support is bleeding-edge/experimental — don't count on it.

## What Ports Over

| From your MuJoCo project | In Stonefish |
|--------------------------|--------------|
| HSV line detector + error signals | unchanged (it's just OpenCV on an image) |
| PID + control allocation | unchanged (still surge/yaw/heave) |
| Teleop/autonomy logic | unchanged |
| The vehicle model & scene | re-described in Stonefish's format |
| Camera feed source | Stonefish camera (via ROS 2 topics) |

You'd typically run Stonefish + ROS 2, bridge the camera and thruster topics, and drop in your existing controller — now with realistic water.

## Resources

- Docs: https://stonefish.readthedocs.io
- Library: https://github.com/patrykcieslak/stonefish
- ROS 2 interface: https://github.com/patrykcieslak/stonefish_ros2
- BlueROV2 + ArduSub + QGroundControl example: https://github.com/bvibhav/stonefish_bluerov2
- ArduSub: https://www.ardusub.com  ·  QGroundControl: https://qgroundcontrol.com

---

# Appendix B — Master Resource List

**MuJoCo / control**
- Docs: https://mujoco.readthedocs.io
- Tutorial notebook: `google-deepmind/mujoco` → `python/tutorial.ipynb`
- Fluid forces: https://mujoco.readthedocs.io/en/stable/computation/fluid.html
- *Underactuated Robotics* (Tedrake): https://underactuated.mit.edu
- Steve Brunton "Control Bootcamp"; Brian Douglas control videos (YouTube)
- Reference that MuJoCo can model AUVs: "Learning to Swim" (arXiv:2410.00120)

**Marine dynamics**
- Fossen, *Handbook of Marine Craft Hydrodynamics and Motion Control*
- Python Vehicle Simulator: https://github.com/cybergalactic/PythonVehicleSimulator

**Vision**
- OpenCV docs: https://docs.opencv.org

**ROS 2 (optional / Linux machine)**
- https://docs.ros.org
