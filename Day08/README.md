# Day 8 — LQR Intuition

**Phase 2 · MuJoCo Fundamentals · ~3 hours**

## 🎯 Goal
Meet a smarter controller: linearize the cart-pole, design an **LQR**, and compare it to your PID. Aim for *intuition*, not mastery — specifically, understand what **Q** and **R** do.

---

## Why Look Beyond PID?

PID is one error → one output. But the cart-pole has *four* states (cart position & velocity, pole angle & velocity) that all interact. **LQR (Linear-Quadratic Regulator)** handles all of them at once and computes optimal gains automatically — no hand-tuning of three numbers. For a multi-DOF underwater vehicle, this kind of thinking scales better.

You won't master LQR today. You just need the intuition.

---

## The Idea in Three Steps

1. **Linearize.** Around the upright balance point, approximate the system as `ẋ = A x + B u` (a linear model). `x` is the state vector, `u` the control.
2. **Define what you care about** via two matrices:
   - **Q** — penalizes *state error* (how much you dislike the pole tilting or the cart drifting).
   - **R** — penalizes *control effort* (how much you dislike using big forces).
3. **Solve** for the gain matrix `K` that minimizes the total cost. The controller is simply `u = -K x`.

---

## What Q and R Actually Do (the key takeaway)

- **Bigger Q** → "I really care about staying on target" → aggressive, tighter control.
- **Bigger R** → "I want to use gentle, cheap control" → smoother, lazier control.
- It's a **trade-off dial**: Q vs R balances *performance* against *effort*. That intuition transfers to every optimal-control problem.

---

## Try It

Use `scipy` to solve the LQR (`lqr_cartpole.py` sketches this). You'll define `A`, `B`, `Q`, `R`, solve the Riccati equation for `K`, then run `u = -K x` in your Day-5 loop. Compare against your Day-6 PID:

- Does LQR settle faster or smoother?
- Crank `Q` up — more aggressive? Crank `R` up — gentler?

> Don't worry if the matrices feel abstract. The goal is to *feel* the Q/R trade-off, not derive control theory.

---

## ✅ Checkpoint
**You can say what Q and R do** (Q penalizes state error; R penalizes control effort; together they trade performance vs. effort).

---

## 📚 Resources
- Tedrake — *Underactuated Robotics*, LQR chapter ([underactuated.mit.edu](https://underactuated.mit.edu))
- Steve Brunton — *Control Bootcamp* (LQR videos)

---

## 🔭 Next
**Day 9 — Contacts, sensors, and the floor: why contacts cause most sim instability.**
