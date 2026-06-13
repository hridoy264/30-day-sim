# Day 25 — Wrapping Your Own Simulator as a Gym Environment

## 🎯 Today's Goal
Build a **custom Gymnasium environment** around a simulator you control, so you can train RL on robots *you* design. This is the bridge between "running examples" and "doing your own RL research."

---

## Overview

Until now you trained on built-in environments. But the real power comes when *you* define the task: your robot, your reward, your goal. Today you learn the small recipe for turning any simulator into a Gym environment. Once you can do this, you can apply Stable-Baselines3 (Day 24) to anything you build in PyBullet, MuJoCo, or even Gazebo.

---

## What a Custom Environment Must Provide

A Gymnasium environment is just a Python class with a few required pieces (from the Day-23 API):

| Piece | What it defines |
|-------|-----------------|
| `__init__` | set `action_space` and `observation_space` |
| `reset()` | start an episode, return first observation |
| `step(action)` | apply action, return (obs, reward, terminated, truncated, info) |
| `render()` | (optional) show it |

Fill in those four and your simulator becomes trainable.

---

## The Three Design Decisions

Building an RL environment is really about three choices. These matter far more than the code:

1. **Observation** — what does the agent *see*? (joint angles, positions, sensor readings). Too little and it can't learn; too much and it learns slowly.
2. **Action** — what can the agent *do*? (joint torques, target velocities). Match your control mode from Day 8/12.
3. **Reward** — what makes an action *good*? This is the heart of RL. A good reward gently guides the agent toward the goal.

> 💡 **Reward shaping is an art.** "Reward = +1 per step upright" works for CartPole. For reaching a target, reward = `-distance_to_target` pulls the arm closer each step. Sparse rewards (1 only at success) are hard to learn; shaped rewards (a hint every step) learn faster. Most RL failures are reward-design problems, not algorithm problems.

---

## A Minimal Custom Environment (PyBullet)

See `custom_env.py`. A skeleton for training a robot arm to reach a target:

```python
import gymnasium as gym
import numpy as np
import pybullet as p
import pybullet_data

class ReachEnv(gym.Env):
    def __init__(self):
        super().__init__()
        # 1. spaces
        self.action_space = gym.spaces.Box(-1, 1, shape=(2,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape=(4,), dtype=np.float32)
        p.connect(p.DIRECT)          # headless = fast for training (Day 6!)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        self.robot = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)
        self.target = np.array([0.5, 0.0])
        return self._obs(), {}

    def step(self, action):
        # 2. apply action (velocity on two joints)
        for i in range(2):
            p.setJointMotorControl2(self.robot, i, p.VELOCITY_CONTROL,
                                    targetVelocity=float(action[i]) * 2)
        p.stepSimulation()
        obs = self._obs()
        # 3. reward = closer is better
        ee = np.array(p.getLinkState(self.robot, 6)[0][:2])
        dist = np.linalg.norm(ee - self.target)
        reward = -dist
        terminated = dist < 0.05      # reached!
        return obs, reward, terminated, False, {}

    def _obs(self):
        j0 = p.getJointState(self.robot, 0)[0]
        j1 = p.getJointState(self.robot, 1)[0]
        return np.array([j0, j1, *self.target], dtype=np.float32)
```

Note `p.connect(p.DIRECT)` — headless mode from Day 6, which makes training fast because there's no rendering. This is why we learned both `GUI` and `DIRECT` early.

---

## Training On Your Environment

Because it follows the Gym API, Day 24's code *just works* on it:

```python
from stable_baselines3 import PPO
from custom_env import ReachEnv

model = PPO("MlpPolicy", ReachEnv(), verbose=1)
model.learn(total_timesteps=100_000)
model.save("reach_ppo")
```

You designed the robot, the task, and the reward — and an agent learned to solve it. That's real RL engineering.

---

## Validating Your Environment

Before training for hours, sanity-check the env:

```python
from stable_baselines3.common.env_checker import check_env
check_env(ReachEnv())   # flags shape/space bugs early
```

`check_env` catches the most common mistakes (wrong shapes, bad return types). Always run it on a new environment — it saves enormous debugging time.

---

## 📝 Today's Task

1. Build `custom_env.py` (the ReachEnv above) and run `check_env` on it — fix any complaints.
2. Train it with PPO for `100_000` steps; watch `ep_rew_mean` (less negative = closer to target).
3. **Tune the reward:** add a bonus `+10` when `terminated` (reached). Does it learn faster?
4. **Change the task:** randomize the target position each `reset()` so the agent generalizes.
5. **Reflect:** write down your three design choices (observation, action, reward) and why.

---

## ✅ Key Takeaways

✓ A custom Gym env is a class with **`__init__` (spaces), `reset()`, `step()`** — fill these and any sim is trainable.

✓ The three real decisions are **observation, action, and reward** — they matter more than code.

✓ **Reward shaping** (a hint every step, e.g. `-distance`) learns far faster than sparse rewards; most RL bugs are reward bugs.

✓ Train headless (`p.DIRECT`) for speed — the reason Day 6 taught both GUI and DIRECT.

✓ Run **`check_env`** before long training runs to catch common mistakes early.

---

## 📚 References & Resources

- [Gymnasium: Make your own custom environment](https://gymnasium.farama.org/introduction/create_custom_env/)
- [SB3 custom environments guide](https://stable-baselines3.readthedocs.io/en/master/guide/custom_env.html)
- [Reward shaping overview](https://gymnasium.farama.org/introduction/basic_usage/)

---

## 🔭 What's Next?

**Day 26 — Sim-to-Real & Domain Randomization.** The big question: does a policy trained in simulation work on a *real* robot? We'll cover the reality gap and the clever trick that bridges it.

---

*"When you can wrap your own robot as an environment, the entire RL toolkit becomes yours."*
