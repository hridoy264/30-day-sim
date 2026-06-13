# Day 23 — Intro to RL & the Gymnasium API

## 🎯 Today's Goal
Understand what reinforcement learning (RL) is, why simulation is essential to it, and learn the **Gymnasium** API — the standard interface that connects learning algorithms to simulated environments.

---

## Overview

Welcome to Phase 5 — where robots stop being *programmed* and start *learning*. On Day 15 you hand-tuned a CartPole controller and felt how fiddly it was. **Reinforcement learning** automates exactly that: the robot tries actions, gets rewards, and improves on its own. And here's the key connection — RL needs *millions* of trials, which is only practical in **simulation**. This is why everything you've learned matters: simulators are the training grounds of robot intelligence.

---

## What is Reinforcement Learning?

RL is learning by trial and error, formalized into a loop between an **agent** and an **environment**:

```
        ┌───────── action ─────────┐
   ┌─────────┐                ┌──────────────┐
   │  AGENT  │                │ ENVIRONMENT  │
   │ (brain) │                │ (simulator)  │
   └─────────┘                └──────────────┘
        └──── observation + reward ┘
```

- The **agent** observes the environment's **state**.
- It picks an **action**.
- The environment returns a new state and a **reward** (a number: good or bad).
- Over many tries, the agent learns a **policy** — a mapping from states to actions — that maximizes total reward.

For CartPole: state = pole angle & cart position; action = push left/right; reward = +1 for every step the pole stays up. Maximize reward → keep the pole balanced. The agent *discovers* the controller you hand-tuned on Day 15.

---

## Why Simulation is Essential for RL

RL agents learn from huge numbers of trials — often **millions** of steps, including many failures. You can't crash a real robot a million times. In simulation you can, faster than real time and in parallel. **Simulation is the enabling technology of modern robot learning.** Everything in this course has been preparing you for this.

---

## The Gymnasium API

**Gymnasium** (the maintained successor to OpenAI Gym) is the universal standard for RL environments. Every environment — from CartPole to a humanoid — exposes the same handful of methods. Learn this tiny API and you can use thousands of environments and every major RL library.

Install it (in your venv):

```bash
pip install gymnasium
```

The entire interface:

```python
import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")

observation, info = env.reset()       # start a new episode
for _ in range(1000):
    action = env.action_space.sample()           # pick an action (here: random)
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:                  # episode over (pole fell / time up)
        observation, info = env.reset()
env.close()
```

That's it. Five concepts power all of RL:

| Concept | Meaning |
|---------|---------|
| `reset()` | start a fresh episode, return first observation |
| `step(action)` | apply an action, get `(obs, reward, terminated, truncated, info)` |
| `observation_space` | the shape of what the agent sees |
| `action_space` | the set of actions the agent can take |
| **episode** | one attempt, from reset to termination |

---

## Reading the step() Return

`step()` returns five things — know them well:

- **observation** — the new state.
- **reward** — the signal to maximize.
- **terminated** — the task ended naturally (pole fell, goal reached).
- **truncated** — the episode hit a time limit.
- **info** — extra debug data (ignore for now).

---

## 📝 Today's Task

1. `pip install gymnasium` and run the random-action CartPole snippet above. Watch it flail — random actions can't balance the pole.
2. Print `env.observation_space` and `env.action_space` — understand what CartPole sees and can do.
3. Count how many steps the pole lasts with random actions (average over 10 episodes). This is your **baseline** to beat tomorrow.
4. Try another env: `gym.make("MountainCar-v0", render_mode="human")` — same API, new problem.
5. **Reflect:** write down the reward for CartPole and how it encourages balancing.

---

## ✅ Key Takeaways

✓ **RL** = learning by trial and error: agent picks **actions**, environment returns **rewards**; the agent learns a **policy** that maximizes reward.

✓ RL needs **millions of trials**, so it's only practical in **simulation** — the reason this whole course matters.

✓ **Gymnasium** is the universal RL environment API: `reset()`, `step(action)`, `observation_space`, `action_space`.

✓ `step()` returns **(observation, reward, terminated, truncated, info)**.

✓ Random actions are a **baseline**; learning should beat it dramatically (Day 24).

---

## 📚 References & Resources

- [Gymnasium documentation](https://gymnasium.farama.org/)
- [Gymnasium basic usage](https://gymnasium.farama.org/introduction/basic_usage/)
- [Sutton & Barto, *Reinforcement Learning* (free book)](http://incompleteideas.net/book/the-book-2nd.html)

---

## 🔭 What's Next?

**Day 24 — Training Your First Policy.** We bring in Stable-Baselines3 and actually *train* an agent to balance CartPole — automatically learning what you hand-tuned on Day 15.

---

*"On Day 15 you found the controller. Now you'll teach a machine to find it itself."*
