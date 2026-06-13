"""
Day 25 — A custom Gymnasium environment (PyBullet).
A KUKA arm learns to move its end-effector toward a target.

Validate:  python -c "from stable_baselines3.common.env_checker import check_env; from custom_env import ReachEnv; check_env(ReachEnv())"
Train:     see the snippet at the bottom (uncomment).
"""

import gymnasium as gym
import numpy as np
import pybullet as p
import pybullet_data


class ReachEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Box(-1, 1, shape=(2,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(
            -np.inf, np.inf, shape=(4,), dtype=np.float32)
        p.connect(p.DIRECT)          # headless = fast training
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.steps = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        self.robot = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)
        # randomize the target so the policy generalizes
        self.target = self.np_random.uniform([0.3, -0.3], [0.6, 0.3])
        self.steps = 0
        return self._obs(), {}

    def step(self, action):
        for i in range(2):
            p.setJointMotorControl2(self.robot, i, p.VELOCITY_CONTROL,
                                    targetVelocity=float(action[i]) * 2.0)
        p.stepSimulation()
        self.steps += 1

        ee = np.array(p.getLinkState(self.robot, 6)[0][:2])
        dist = float(np.linalg.norm(ee - self.target))
        reward = -dist
        terminated = dist < 0.05
        if terminated:
            reward += 10.0                 # bonus for reaching
        truncated = self.steps >= 300
        return self._obs(), reward, terminated, truncated, {}

    def _obs(self):
        j0 = p.getJointState(self.robot, 0)[0]
        j1 = p.getJointState(self.robot, 1)[0]
        return np.array([j0, j1, self.target[0], self.target[1]],
                        dtype=np.float32)


if __name__ == "__main__":
    from stable_baselines3.common.env_checker import check_env
    check_env(ReachEnv())
    print("Environment passes check_env!")

    # --- to train, uncomment: ---
    # from stable_baselines3 import PPO
    # model = PPO("MlpPolicy", ReachEnv(), verbose=1)
    # model.learn(total_timesteps=100_000)
    # model.save("reach_ppo")
