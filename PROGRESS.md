# Progress Tracker — 30 Days of Underwater Simulation

Check off each day as you finish it (tick the box when you hit the **Checkpoint**).
For an interactive version that saves automatically, open `progress-tracker.html` in your browser.

---

## Phase 1 — Orientation & MuJoCo Setup
- [ ] **Day 01** — Mental model + environment · *Checkpoint: a MuJoCo window opens*
- [ ] **Day 02** — Frames, rigid bodies, marine 6-DOF · *Checkpoint: explain why a too-large timestep destabilizes a sim*
- [ ] **Day 03** — MJCF format · *Checkpoint: read an MJCF and name each element's role*

## Phase 2 — MuJoCo Fundamentals
- [ ] **Day 04** — Pendulum from scratch · *Checkpoint: your own .xml loads and swings*
- [ ] **Day 05** — Cart-pole + Python loop · *Checkpoint: step the sim and apply controls in Python*
- [ ] **Day 06** — Your first PID · *Checkpoint: a working closed control loop* ⭐
- [ ] **Day 07** — Buffer / consolidate · *Checkpoint: Days 1–6 run; concepts written in your words*
- [ ] **Day 08** — LQR intuition · *Checkpoint: you can say what Q and R do*
- [ ] **Day 09** — Contacts, sensors, the floor · *Checkpoint: understand why contacts cause instability*
- [ ] **Day 10** — Offscreen camera rendering · *Checkpoint: grab a camera image as an array* ⭐

## Phase 3 — Marine Dynamics + MuJoCo Fluid
- [ ] **Day 11** — Marine dynamics theory · *Checkpoint: explain why a vehicle glides after thrust stops*
- [ ] **Day 12** — MuJoCo fluid forces · *Checkpoint: a body shows realistic drag*
- [ ] **Day 13** — Buoyancy + ROS concepts · *Checkpoint: make a body neutrally buoyant*

## Phase 4 — Build the Underwater Vehicle
- [ ] **Day 14** — Vehicle body + free joint · *Checkpoint: a 6-DOF body floats and responds to drag*
- [ ] **Day 15** — Thrusters + control allocation · *Checkpoint: forward/yaw/vertical thrust moves it correctly*
- [ ] **Day 16** — Tune the dynamics · *Checkpoint: feels like a vehicle, not a brick or balloon*
- [ ] **Day 17** — Mount two cameras · *Checkpoint: two live camera streams from the moving vehicle*
- [ ] **Day 18** — Seabed + line · *Checkpoint: the line is clearly visible in the downward camera*
- [ ] **Day 19** — Buffer + integration · *Checkpoint: everything runs in one loop without choking the M4*

## Phase 5 — Teleoperation + Vision
- [ ] **Day 20** — Teleoperation · *Checkpoint: you can drive the vehicle manually* ⭐
- [ ] **Day 21** — OpenCV line detection · *Checkpoint: draw a centroid/box on the detected line*
- [ ] **Day 22** — Error signals · *Checkpoint: two clean numeric error signals as it moves*
- [ ] **Day 23** — Second camera use · *Checkpoint: second camera contributes a usable signal*
- [ ] **Day 24** — Buffer + logging · *Checkpoint: save frames + state; replay offline*
- [ ] **Day 25** — Robustness pass on detection · *Checkpoint: detector is steady, not jumpy*

## Phase 6 — Autonomy + Robustness
- [ ] **Day 26** — Close the autonomy loop · *Checkpoint: follows a straight line autonomously* ⭐
- [ ] **Day 27** — Curves, loss, mode switch · *Checkpoint: follows a curve; recovers from loss*
- [ ] **Day 28** — Turbidity / domain randomization · *Checkpoint: survives 3+ water conditions*
- [ ] **Day 29** — Buffer + tuning · *Checkpoint: one repeatable launch script*
- [ ] **Day 30** — Capstone + write-up · *Checkpoint: a reproducible end-to-end demo + notes* 🏁

---

⭐ = a make-or-break skill · 🏁 = the finish line

**Buffer days (7, 19, 24, 29) absorb slippage — falling behind is normal and planned for.**
