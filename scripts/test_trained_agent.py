import time
import numpy as np
from stable_baselines3 import PPO
from rl_env import WarehouseNavEnv

# Load the trained model
model_path = "models/ppo_nav/warehouse_robot_rl.zip"
print(f"Loading model from: {model_path}")
model = PPO.load(model_path)

# Initialize environment in human (visual) mode
env = WarehouseNavEnv(render_mode="human")
obs, _ = env.reset(seed=42)

print("\n🚀 Running trained agent in warehouse simulation...")
time.sleep(1)

total_reward = 0
for step in range(300):  # Run for 300 steps (adjust as needed)
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(int(action))
    total_reward += reward
    if terminated or truncated:
        print("\n🏁 Episode finished early!")
        break

env.close()
print(f"\n✅ Simulation finished. Total reward: {round(total_reward, 2)}")
