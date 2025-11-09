import os
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from rl_env import WarehouseNavEnv

# Make sure model directory exists
os.makedirs("models/ppo_nav", exist_ok=True)

# Create vectorized environment
env = make_vec_env(lambda: WarehouseNavEnv(render_mode=None), n_envs=4)

# Initialize PPO agent
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    gamma=0.99,
    tensorboard_log="./logs/",
)

# Train agent
TIMESTEPS = 50000  # You can increase this later (e.g., 200000+)
model.learn(total_timesteps=TIMESTEPS)

# Save trained model
model.save("models/ppo_nav/warehouse_robot_rl")

print("\n✅ Training complete! Model saved at models/ppo_nav/warehouse_robot_rl.zip")
