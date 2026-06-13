# Day 24 — Training Your First Policy with Stable-Baselines3

## 🎯 Today's Goal
Actually *train* an RL agent. Using **Stable-Baselines3**, you'll teach a neural network to balance CartPole from scratch — automating the controller you hand-tuned on Day 15 — and watch it go from clueless to expert.

---

## Overview

Yesterday you saw random actions fail. Today you'll train an agent that succeeds. **Stable-Baselines3 (SB3)** is the most popular, beginner-friendly RL library — it implements proven algorithms so you don't have to. With about ten lines of code, you'll train a real policy. This is the "wow" moment of the course: a machine learning a skill on its own.

---

## What is Stable-Baselines3?

SB3 is a Python library of reliable, ready-to-use RL **algorithms** (the "brains" that learn). You pick an algorithm, point it at a Gymnasium environment, and call `.learn()`. It handles the neural networks, the trial-and-error, and the math.

Install it (in your venv):

```bash
pip install stable-baselines3[extra]
```

---

## Choosing an Algorithm

A few you'll hear about:

| Algorithm | Good for | Note |
|-----------|----------|------|
| **PPO** | almost everything | robust, the great default — use this |
| **DQN** | discrete actions | classic, good for CartPole |
| **SAC** | continuous control | strong for robot arms/locomotion |

> 💡 When unsure, **start with PPO**. It's stable, widely used, and works on a huge range of problems with little tuning. It's the sensible default for beginners and experts alike.

---

## Training in ~10 Lines

See `train_cartpole.py`. The whole thing:

```python
import gymnasium as gym
from stable_baselines3 import PPO

# 1. the environment (the Day-23 Gymnasium API)
env = gym.make("CartPole-v1")

# 2. the agent: an MLP (neural network) policy with PPO
model = PPO("MlpPolicy", env, verbose=1)

# 3. LEARN — this is the training. ~25k steps is plenty for CartPole
model.learn(total_timesteps=25_000)

# 4. save the trained brain
model.save("cartpole_ppo")
```

Run it. You'll see training stats scroll by — watch `ep_rew_mean` (average episode reward) climb from ~20 toward CartPole's max of 500. The agent is *learning*.

---

## Watching Your Trained Agent

After training, load the policy and watch it perform:

```python
import gymnasium as gym
from stable_baselines3 import PPO

env = gym.make("CartPole-v1", render_mode="human")
model = PPO.load("cartpole_ppo")

obs, info = env.reset()
for _ in range(2000):
    action, _ = model.predict(obs, deterministic=True)   # the learned policy
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
env.close()
```

The pole stays balanced — beautifully, indefinitely. **You trained that.** No gains to tune (Day 15), no rules to code: the agent discovered the controller from reward alone.

---

## Understanding What Happened

The neural network started random (like Day 23's flailing). Through thousands of trials, PPO nudged its weights toward actions that earned more reward. The end result is a **policy**: feed it the current state, it outputs the best action. This same recipe — define env + reward, pick PPO, call `.learn()` — scales to robot arms, walking robots, and drones. You now know the core workflow of modern robot learning.

---

## 📝 Today's Task

1. `pip install stable-baselines3[extra]` and run `train_cartpole.py`. Watch `ep_rew_mean` rise.
2. Run the "watch" script and see your trained agent balance the pole.
3. **Compare to Day 23:** random lasted ~20 steps; your agent should hit ~500. Note the difference.
4. **Experiment:** train with only `5_000` steps — is it good yet? Then `50_000` — better? See how training time affects skill.
5. Train `"MountainCar-v0"` or `"LunarLander-v2"` (needs `[extra]`) with PPO — same five lines, harder problem.

---

## ✅ Key Takeaways

✓ **Stable-Baselines3** provides ready-made RL algorithms; you just point them at a Gym env and call `.learn()`.

✓ **PPO** is the robust default — start there before anything fancier.

✓ Training is `PPO("MlpPolicy", env).learn(total_timesteps=...)` — watch **`ep_rew_mean`** climb.

✓ A trained **policy** maps state → best action; use `model.predict(obs)` to run it.

✓ The agent **discovers** the Day-15 controller from reward alone — no manual tuning. This recipe scales to real robots.

---

## 📚 References & Resources

- [Stable-Baselines3 documentation](https://stable-baselines3.readthedocs.io/)
- [SB3 Getting Started](https://stable-baselines3.readthedocs.io/en/master/guide/quickstart.html)
- [SB3 on GitHub](https://github.com/DLR-RM/stable-baselines3)
- [RL Baselines3 Zoo (trained agents & tuned hyperparameters)](https://github.com/DLR-RM/rl-baselines3-zoo)

---

## 🔭 What's Next?

**Day 25 — Custom Gym Environments.** You'll wrap your *own* simulator (PyBullet or MuJoCo) in the Gymnasium API, so you can train RL on robots *you* design — not just the built-in examples.

---

*"Ten lines of code, and a neural network taught itself to balance a pole. Welcome to robot learning."*
