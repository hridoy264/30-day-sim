# 📋 How to use this tracker

GitHub **Issues** have tap-to-tick checkboxes that save instantly and sync to every device (web + mobile app) — no commits needed.

**One-time setup:**
1. Push this repo to GitHub.
2. Go to the **Issues** tab → **New issue**.
3. Title it: `🌊 My 30-Day Underwater Sim Progress`
4. Copy *everything below the line* into the description and submit.
5. (Optional) **Pin** the issue so it's always at the top.

Now open that issue on any device and tap a box when you hit a day's checkpoint. GitHub even shows a progress bar (e.g. `7 of 30`).

⭐ = a make-or-break skill · Buffer days (7, 19, 24, 29) absorb slippage.

---

## Phase 1 — Orientation & MuJoCo Setup
- [ ] **Day 01** — Mental model + environment — *checkpoint: a MuJoCo window opens*
- [ ] **Day 02** — Frames, rigid bodies, marine 6-DOF — *checkpoint: explain why a too-large timestep destabilizes a sim*
- [ ] **Day 03** — MJCF format — *checkpoint: read an MJCF and name each element's role*

## Phase 2 — MuJoCo Fundamentals
- [ ] **Day 04** — Pendulum from scratch — *checkpoint: your own .xml loads and swings*
- [ ] **Day 05** — Cart-pole + Python loop — *checkpoint: step the sim and apply controls in Python*
- [ ] **Day 06** — Your first PID ⭐ — *checkpoint: a working closed control loop*
- [ ] **Day 07** — Buffer / consolidate — *checkpoint: Days 1–6 run; concepts written in your words*
- [ ] **Day 08** — LQR intuition — *checkpoint: you can say what Q and R do*
- [ ] **Day 09** — Contacts, sensors, the floor — *checkpoint: understand why contacts cause instability*
- [ ] **Day 10** — Offscreen camera rendering ⭐ — *checkpoint: grab a camera image as an array*

## Phase 3 — Marine Dynamics + MuJoCo Fluid
- [ ] **Day 11** — Marine dynamics theory — *checkpoint: explain why a vehicle glides after thrust stops*
- [ ] **Day 12** — MuJoCo fluid forces — *checkpoint: a body shows realistic drag*
- [ ] **Day 13** — Buoyancy + ROS concepts — *checkpoint: make a body neutrally buoyant*

## Phase 4 — Build the Underwater Vehicle
- [ ] **Day 14** — Vehicle body + free joint — *checkpoint: a 6-DOF body floats and responds to drag*
- [ ] **Day 15** — Thrusters + control allocation — *checkpoint: forward/yaw/vertical thrust moves it correctly*
- [ ] **Day 16** — Tune the dynamics — *checkpoint: feels like a vehicle, not a brick or balloon*
- [ ] **Day 17** — Mount two cameras — *checkpoint: two live camera streams from the moving vehicle*
- [ ] **Day 18** — Seabed + line — *checkpoint: the line is clearly visible in the downward camera*
- [ ] **Day 19** — Buffer + integration — *checkpoint: everything runs in one loop without choking the M4*

## Phase 5 — Teleoperation + Vision
- [ ] **Day 20** — Teleoperation ⭐ — *checkpoint: you can drive the vehicle manually*
- [ ] **Day 21** — OpenCV line detection — *checkpoint: draw a centroid/box on the detected line*
- [ ] **Day 22** — Error signals — *checkpoint: two clean numeric error signals as it moves*
- [ ] **Day 23** — Second camera use — *checkpoint: second camera contributes a usable signal*
- [ ] **Day 24** — Buffer + logging — *checkpoint: save frames + state; replay offline*
- [ ] **Day 25** — Robustness pass on detection — *checkpoint: detector is steady, not jumpy*

## Phase 6 — Autonomy + Robustness
- [ ] **Day 26** — Close the autonomy loop ⭐ — *checkpoint: follows a straight line autonomously*
- [ ] **Day 27** — Curves, loss, mode switch — *checkpoint: follows a curve; recovers from loss*
- [ ] **Day 28** — Turbidity / domain randomization — *checkpoint: survives 3+ water conditions*
- [ ] **Day 29** — Buffer + tuning — *checkpoint: one repeatable launch script*
- [ ] **Day 30** — Capstone + write-up 🏁 — *checkpoint: a reproducible end-to-end demo + notes*
