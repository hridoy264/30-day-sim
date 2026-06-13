# Day 15 — 🛠 Mini-Project: Balancing a CartPole

## 🎯 Today's Goal
Build the classic **CartPole** in MuJoCo and write a controller that balances the pole upright. You'll combine modeling, sensing, and feedback control — and create the exact environment you'll later solve with reinforcement learning.

---

## Overview

CartPole is the "hello world" of control and RL: a cart that slides left/right with a pole hinged on top. Push the cart correctly and the pole stays balanced; do nothing and it falls. It's simple to build, instantly visual, and teaches the single most important control idea — **feedback**. Building it yourself today makes Phase 5 (RL) click immediately, because you'll *understand* the problem the AI is solving.

---

## The Model

A cart (slides along X) with a pole (hinges) on top. Save as `cartpole.xml` (also in this folder):

```xml
<mujoco model="cartpole">
  <option gravity="0 0 -9.81" timestep="0.01"/>

  <worldbody>
    <light pos="0 0 3"/>
    <geom name="floor" type="plane" size="5 5 0.1" rgba="0.8 0.9 0.8 1"/>
    <geom name="rail" type="capsule" fromto="-3 0 0.5  3 0 0.5" size="0.02" rgba="0.5 0.5 0.5 1"/>

    <body name="cart" pos="0 0 0.5">
      <joint name="slider" type="slide" axis="1 0 0"/>
      <geom name="cart" type="box" size="0.2 0.15 0.1" rgba="0.2 0.4 0.9 1"/>

      <body name="pole" pos="0 0 0.1">
        <joint name="hinge" type="hinge" axis="0 1 0"/>
        <geom name="pole" type="capsule" fromto="0 0 0  0 0 0.6" size="0.04" rgba="0.9 0.4 0.2 1"/>
      </body>
    </body>
  </worldbody>

  <actuator>
    <motor name="cart_motor" joint="slider" gear="50" ctrlrange="-1 1"/>
  </actuator>

  <sensor>
    <jointpos name="cart_pos"  joint="slider"/>
    <jointpos name="pole_angle" joint="hinge"/>
    <jointvel name="pole_vel"  joint="hinge"/>
  </sensor>
</mujoco>
```

One actuator pushes the cart; three sensors report cart position, pole angle, and pole angular velocity — everything a controller needs.

---

## The Controller: Feedback in Action

A simple **proportional-derivative (PD)** rule balances the pole: push the cart in the direction the pole is *falling*, proportional to how far it's tilted and how fast it's tipping.

```python
# pole_angle: 0 = upright.  Push the cart to counter the tilt.
force = Kp * pole_angle + Kd * pole_velocity
data.ctrl[0] = clip(force, -1, 1)
```

That's the entire idea of feedback control: **measure the error, act to reduce it.** Two gains (`Kp`, `Kd`) and you can balance a pole.

---

## Full Program

See `cartpole_balance.py`:

```python
import time, numpy as np, mujoco, mujoco.viewer

model = mujoco.MjModel.from_xml_path("cartpole.xml")
data  = mujoco.MjData(model)

# start the pole slightly tilted so there's something to correct
data.qpos[1] = 0.1
mujoco.mj_forward(model, data)

Kp, Kd = 8.0, 1.5
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        pole_angle = data.sensordata[1]
        pole_vel   = data.sensordata[2]
        data.ctrl[0] = np.clip(Kp*pole_angle + Kd*pole_vel, -1, 1)
        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)
```

Run it. The pole wobbles, the cart darts to catch it, and it balances. **You just wrote a controller** — congratulations.

---

## Tuning (and why it matters for RL)

- **`Kp` too low** → the cart reacts too weakly, pole falls.
- **`Kp` too high** → the cart overshoots and oscillates.
- **`Kd`** damps the oscillation.

Hand-tuning these gains shows you how hard control can be even for a simple system. **This is exactly the problem reinforcement learning automates** — in Phase 5, an algorithm will *learn* a controller for this same CartPole without you tuning anything. Today you earn the right to appreciate that.

---

## 📝 Today's Task

1. Build `cartpole.xml` and run `cartpole_balance.py` — get the pole to balance.
2. **Break it:** set `Kp=2` (too weak) and `Kp=30` (too strong). Watch it fail in different ways.
3. Start with a bigger tilt (`data.qpos[1] = 0.4`) — can your gains still recover?
4. Add a disturbance: every few seconds add a random push to `data.ctrl` and see if the controller survives.
5. **Reflect:** write down how long it took to hand-tune good gains. Remember this on Day 24.

---

## 🏆 Phase 3 Complete!

You can now model robots in MJCF, drive and sense them from Python, and write a feedback controller. You've used the research world's favorite simulator end to end — and built the perfect launchpad for reinforcement learning.

---

## ✅ Key Takeaways

✓ **CartPole** = cart (slide joint) + pole (hinge joint) + one motor + three sensors.

✓ Feedback control = **measure the error, act to reduce it**; a PD rule balances the pole.

✓ Gains `Kp`/`Kd` must be tuned: too low fails, too high oscillates; `Kd` adds damping.

✓ Hand-tuning is fiddly — which is precisely the motivation for **reinforcement learning**.

✓ You've completed MuJoCo: modeling, control, sensing, and a real control task.

---

## 📚 References & Resources

- [CartPole problem background](https://gymnasium.farama.org/environments/classic_control/cart_pole/)
- [MuJoCo control samples](https://github.com/google-deepmind/mujoco/tree/main/model)
- [PID/PD control intro](https://en.wikipedia.org/wiki/PID_controller)

---

## 🔭 What's Next?

**Day 16 — Hello Gazebo.** New phase! We move to Gazebo and ROS 2, the industry-standard stack used to build real-world robots — and the most "professional robotics" part of the course.

---

*"You balanced a pole with two numbers. Next, you'll teach a machine to find them itself."*
