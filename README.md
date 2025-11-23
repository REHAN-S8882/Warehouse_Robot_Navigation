# 🤖 Warehouse Robot Navigation System(https://ai-medical-diagnosis-mz8yefsch5xwtsqq28ftru.streamlit.app/)

An intelligent **autonomous warehouse robot simulation** that uses **Computer Vision (OpenCV)** and **Reinforcement Learning (RL)** for path optimization — integrated with **AWS IoT Core** for real-time telemetry, data logging, and collision alerts.

---

## 🧠 Overview

Modern warehouses face challenges such as **slow deliveries**, **collisions**, and **manual monitoring**.  
This project demonstrates how AI and IoT can solve these problems by enabling a robot to:
- Detect obstacles using vision-based sensing.
- Learn optimal navigation through RL (PPO algorithm).
- Send telemetry data (battery, speed, collisions) to AWS IoT.
- Trigger alerts via **AWS SNS** and store data in **S3** for analytics.

---

## ⚙️ System Architecture

Sensors (LIDAR / Camera)
↓
Preprocessing (OpenCV)
↓
CNN Model → Obstacle Detection
↓
Reinforcement Learning (PPO Agent)
↓
IoT Core → MQTT Telemetry
↓
AWS S3 (Data Logging) + AWS SNS (Collision Alerts)
↓
Edge Deployment / Robot Actuators

markdown
Copy code

🗂 **Key AWS Services Used:**
- **AWS IoT Core** → Secure MQTT communication  
- **AWS S3** → Stores telemetry logs (`iot/robot1/{timestamp}.json`)  
- **AWS SNS** → Sends email alerts on collision  
- **IAM Roles & Certificates** → For secure device authentication

---

## 📁 Project Structure

Warehouse_Robot_Navigation/
│
├── data/ # sensor or simulation data
├── models/ # trained RL or CNN models
├── scripts/ # preprocessing, detection, simulation
│ ├── robot_publisher.py
│ ├── robot_simulation.py
│ ├── train_rl_agent.py
│ ├── test_trained_agent.py
│
├── deliverables/ # architecture diagram, 1-page summary
├── secrets/ # AWS certs (ignored in git)
├── main.py # main entry point
├── requirements.txt # all dependencies
├── README.md # this file
└── project_notes.md # step-by-step documentation

yaml
Copy code

---

## 🚀 Features

✅ **Autonomous Simulation** using OpenCV  
✅ **Obstacle Detection & Collision Avoidance**  
✅ **Reinforcement Learning (PPO)** for Path Optimization  
✅ **Cloud Integration via MQTT (AWS IoT Core)**  
✅ **Automated Data Logging to S3**  
✅ **Email Alerts on Collisions (AWS SNS)**  

---

## 🧩 Tech Stack

| Category | Technologies |
|-----------|---------------|
| Programming | Python 3.12 |
| Simulation | OpenCV, NumPy |
| ML / RL | PyTorch, Stable-Baselines3 |
| IoT | MQTT (paho-mqtt), AWS IoT Core |
| Cloud | AWS S3, AWS SNS, IAM |
| Tools | VS Code, Streamlit (optional UI) |

---

## 💡 Example Outputs

**IoT Published Data:**
```json
{
  "device": "robot1",
  "status": "online",
  "battery": 92,
  "speed": 0.65,
  "collisions": 0,
  "ts": 17624113221
}
AWS SNS Alert Example:

json
Copy code
{"device": "robot1", "status": "shutdown", "battery": 0, "speed": 0.32, "collisions": 1, "ts": 1762415237}
🧠 How to Run
1️⃣ Setup Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
2️⃣ Run Obstacle Simulation
bash
Copy code
python scripts/robot_simulation.py
3️⃣ Train RL Agent
bash
Copy code
python scripts/train_rl_agent.py
4️⃣ Publish IoT Telemetry to AWS
bash
Copy code
python scripts/robot_publisher.py
☁️ Cloud Integration Steps
Create an AWS IoT Thing (robot1)

Attach the certificates + policy

Create an IoT Rule → S3 for telemetry storage

SQL: SELECT * FROM 'warehouse/robot1/status'

Create an IoT Rule → SNS for alerts

Condition: collisions = 1

Subscribe via email and confirm the link.

🖼️ Architecture Diagram

🧾 Deliverables
📜 deliverables/architecture_diagram.md

📄 deliverables/summary.md

🧠 project_notes.md — full stepwise documentation

👨‍💻 Author
Rehan Khan
AI & Machine Learning Enthusiast | IoT Developer
📍 India
📧 16rehan687@gmail.com
🌐 LinkedIn Profile:https://www.linkedin.com/in/rehan-khan-b413a7200/
