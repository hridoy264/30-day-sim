"""
Day 24 — Train your first RL policy with Stable-Baselines3.
Trains PPO to balance CartPole, saves it, then shows it off.

Install:  pip install stable-baselines3[extra]
Run:      python train_cartpole.py
"""

import gymnasium as gym
from stable_baselines3 import PPO

# ---- TRAIN ----
env = gym.make("CartPole-v1")
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25_000)   # watch ep_rew_mean climb toward 500
model.save("cartpole_ppo")
env.close()
print("\nTraining complete. Saved to cartpole_ppo.zip\n")

# ---- WATCH ----
show = gym.make("CartPole-v1", render_mode="human")
model = PPO.load("cartpole_ppo")
obs, info = show.reset()
for _ in range(2000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = show.step(action)
    if terminated or truncated:
        obs, info = show.reset()
show.close()
