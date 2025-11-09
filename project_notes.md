# 🧠 Warehouse Robot Navigation Project Notes

## Step Summary So Far

### ✅ Environment Setup (Completed)
- Installed **VS Code** and configured Python 3.12.7
- Created virtual environment `venv`
- Installed required libraries:
  - numpy, pandas, matplotlib, opencv-python
  - torch, torchvision, torchaudio
  - gymnasium, stable-baselines3
- Verified everything with `main.py` test script

### 📁 Project Structure
Warehouse_Robot_Navigation/
│
├── data/ → sensor data or simulation input files
├── models/ → trained CNN/RL models
├── scripts/ → helper modules for preprocessing, detection, etc.
├── venv/ → virtual environment
├── main.py → main driver script
└── project_notes.md → documentation and progress notes


### 🧩 Next Steps
1. Build the **Obstacle Detection Simulation** (using OpenCV + CNN-style logic)
2. Integrate Reinforcement Learning (path optimization)
3. Add Cloud IoT integration and edge inference simulation
4. Create architecture diagram and 1-page summary

---
### 🚗 Step 7 (B): Automatic Robot Simulation (Completed)
- Added `robot_simulation.py` in the **scripts** folder to simulate an autonomous robot in a 2D warehouse.
- The robot moves automatically, detects obstacles, and avoids collisions using OpenCV-based vision.
- Inflated gray regions represent safe buffer zones around obstacles.
- A green robot continuously scans the environment with detection rays.
- A red trail marks the robot’s past movement path.
- The robot dynamically adjusts its direction to navigate freely.
- Press `q` to exit the simulation window.

✅ **Outcome:** The environment and robot movement simulation are now fully functional.

---

### 🧭 Next Milestone
**Step 8: Path Optimization using Reinforcement Learning (RL)**  
Goal: Enable the robot to learn and optimize its path to reach a target efficiently.  
We'll create a training environment using **Stable Baselines3** and integrate a simple **reward-based navigation model**.

### 🤖 Step 8 (C): RL-Trained Robot Navigation — Simulation (Completed)
- Trained PPO agent using `scripts/train_rl_agent.py` (50k timesteps).
- Saved model to: `models/ppo_nav/warehouse_robot_rl.zip`.
- Ran live simulation with `scripts/test_trained_agent.py` using the trained policy.
- Result: Agent navigates around obstacles toward the goal; episode ends on success or collision.
- Example output: `✅ Simulation finished. Total reward: 3746.38` (varies per run).

**How to rerun**
```bash
# train (can increase timesteps later)
python scripts/train_rl_agent.py

# visual test with trained model
python scripts/test_trained_agent.py


### 🧩 Step 9 Deliverables Added
- [x] Architecture diagram → `deliverables/architecture_diagram.md`
- [x] 1-Page summary → `deliverables/summary.md`


### ☁️ Step 10: AWS IoT Cloud Integration (Completed)
**Goal:** Connect the trained warehouse robot simulation to AWS IoT Core for real-time monitoring, message exchange, and cloud-based data logging.

#### ✅ Setup Summary
- Created and activated a new AWS IoT certificate (`1ddb11e352cb087eb8b14ff8025ae5ba6773ade49f196f0c22b92e7022c14ef4`).
- Attached custom policy: **warehouse-robot-policy**
  - Allows connect, publish, subscribe, and receive for topic `warehouse/robot1/*`.
- Downloaded and stored certificate files in:  
  `Warehouse_Robot_Navigation/secrets/robot1/`
  - `AmazonRootCA1.pem`  
  - `AmazonRootCA3.pem`  
  - `*-certificate.pem.crt`  
  - `*-private.pem.key`  
  - `*-public.pem.key`

#### 🧠 Python MQTT Client Setup
- Script: `scripts/aws_iot_test.py`
- Libraries: `paho-mqtt`, `ssl`, `json`, `time`
- Endpoint used:
a37wis2tab9brj-ats.iot.ap-south-1.amazonaws.com

bash
Copy code
- Topics:
- Publish → `warehouse/robot1/status`
- Subscribe → `warehouse/robot1/#`

#### 🧩 Test Results
- Successfully connected to AWS IoT Core via MQTT (`rc=0` ✅)
- Message published:
```json
{
  "device": "robot1",
  "status": "online",
  "battery": 87,
  "ts": 1762397342
}
Message received and displayed in AWS IoT Test Client in real-time.

✅ Outcome: Local robot script now communicates securely with AWS IoT Core over MQTT, sending live telemetry to the cloud.

☁️ Step 11 (Next): Cloud Data Logging and Analytics
Goal: Configure AWS IoT Rule to automatically store all incoming messages into an S3 bucket.
This enables persistent logging, later analysis, and dashboard visualization.

Planned Steps:
Create an S3 bucket — e.g., warehouse-robot-logs-ap-south-1

Define IoT Rule:

sql
Copy code
SELECT *, topic() as msg_topic, timestamp() as msg_ts
FROM 'warehouse/+/status'
Add S3 action:

Bucket: warehouse-robot-logs-ap-south-1

Object key: iot/${msg_topic}/${msg_ts}.json

Test by rerunning the MQTT publisher — verify logs in S3.

🧩 Step 12 (Planned)
Continuous Simulation & Multi-Robot Expansion

Modify script to simulate multiple robots (robot1, robot2, etc.)

Each device will publish unique telemetry to its own topic.

Subscribe to warehouse/# to monitor all robots together in AWS IoT Test Client.

### ☁️ Monitoring: Collision Alert System (AWS SNS Integration)

Implemented real-time monitoring using AWS IoT Core and SNS.  
When the robot publishes a message with `"collisions": 1`,  
an IoT rule automatically triggers an SNS topic (`wrn-collision-alerts`)  
that sends an email notification to the operator for immediate action.

✅ IoT Rule: collision_alert_rule  
✅ SNS Topic: wrn-collision-alerts  
✅ Status: Successfully tested with live alerts

### ✅ Step 10: Monitoring and Cloud Alerts (Completed)
- Created IoT Rule → S3 (for data logging)
- Created IoT Rule → SNS (for collision alerts)
- Subscribed email via AWS SNS
- Verified alerts successfully triggered:
{"device": "robot1", "status": "shutdown", "battery": 0, "speed": 0.32, "collisions": 1}

diff
Copy code
- Data and alert systems fully functional