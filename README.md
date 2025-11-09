# 🤖 Warehouse Robot Navigation Project

### Task 2 – Robotics: Warehouse Robot Navigation  
**Scenario:** Robots navigate warehouse aisles and avoid obstacles autonomously.

---

## 🧠 Overview
This project develops an **autonomous warehouse robot system** capable of:
- Detecting and avoiding obstacles in real-time  
- Optimizing navigation paths using Reinforcement Learning (RL)  
- Deploying models for low-latency **edge inference**  
- Leveraging cloud services for **model retraining and monitoring**

---

## 🚩 Problem Identification
- **Slow deliveries** due to inefficient path planning  
- **Collisions** with shelves or other robots  
- **Manual monitoring** required to recover from navigation errors  

---

## 🧩 Solution Design
### **1. Data Collection**
- Sensors: **LIDAR** + **Camera (RGB)**  
- Data transmitted through **IoT Gateway** (MQTT/HTTP) to Cloud  

### **2. Preprocessing**
- Sensor normalization (distance scaling, filtering)  
- Image preprocessing (resizing, normalization, augmentation)

### **3. Modeling**
- **CNN** – Obstacle detection from camera frames  
- **RL (PPO Algorithm)** – Path optimization & obstacle avoidance  

### **4. Cloud Integration**
- Services: **AWS Greengrass / Azure IoT Hub / GCP AI Platform**  
- Cloud manages data ingestion, model retraining, and versioning  

### **5. Deployment**
- **Edge inference** using trained CNN + RL models  
- Deployed via containers (Docker / Greengrass) for on-device operation  

### **6. Monitoring**
- Edge-to-Cloud telemetry for collisions, drift, latency  
- Automatic alerts and retraining triggers  

---

## 🏗️ System Architecture

Sensors (LIDAR, Camera)
↓
IoT Gateway (Edge Device)
↓
Preprocessing (Sensor Normalization, Image Processing)
↓
CNN (Obstacle Detection) + RL (Path Optimization)
↓
Robot Actuators (Wheels, Motors)
↓
Cloud (IoT Core, SageMaker, Model Registry)
↑
Monitoring & Retraining Feedback Loop


> See detailed diagram in `deliverables/architecture_diagram.md`.

---

## 🧮 Model Details

| Component | Description |
|------------|--------------|
| CNN | Detects obstacles using camera image frames |
| RL (PPO) | Learns to navigate and optimize routes |
| Frameworks | PyTorch, Stable-Baselines3, OpenCV, Gymnasium |
| Training Steps | 50,000 timesteps (expandable) |
| Output | `warehouse_robot_rl.zip` model file |

---

## 🧰 Folder Structure

Warehouse_Robot_Navigation/
│
├── data/ → Raw or simulated sensor data
├── models/ → Saved CNN/RL model files
├── scripts/ → All Python scripts (training, simulation, etc.)
│ ├── obstacle_detection.py
│ ├── robot_simulation.py
│ ├── rl_env.py
│ ├── train_rl_agent.py
│ └── test_trained_agent.py
│
├── deliverables/ → Final report files
│ ├── architecture_diagram.md
│ └── summary.md
│
├── project_notes.md → Development log / notes
├── main.py → Environment verification script
└── README.md → This file


---

## 🧪 How to Run

### **1️⃣ Setup Environment**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt   # or install manually

2️⃣ Run Obstacle Detection Simulation
python scripts/obstacle_detection.py

3️⃣ Train the RL Model
python scripts/train_rl_agent.py

4️⃣ Test the Trained Model
python scripts/test_trained_agent.py

📈 Deliverables
Deliverable	Description	File
Architecture Diagram	End-to-end system design	deliverables/architecture_diagram.md
1-Page Summary	Concise project report	deliverables/summary.md
Code Implementation	Python scripts for full workflow	scripts/ folder
Logs & Models	Training outputs	models/ppo_nav/ folder
☁️ Cloud Deployment (Concept)
Layer	Example Platform	Role
IoT Edge	AWS Greengrass / Azure IoT Edge	Edge inference, local model
Cloud Core	AWS IoT Hub / GCP IoT Core	Device communication
Model Training	SageMaker / Azure ML / Vertex AI	Retraining and monitoring
Storage	S3 / Blob Storage / Cloud Storage	Sensor and model logs
🏁 Expected Outcomes

Autonomous obstacle avoidance with minimal collisions

Path optimization reduces travel time by >20% (simulated)

Scalable pipeline for retraining and continuous improvement

👨‍💻 Author

Developed by: Rehan Khan
Tools: Python, VS Code, OpenCV, PyTorch, Stable-Baselines3
Environment: Windows 11 + Virtual Environment (venv)
---

## ☁️ Cloud IoT Integration (AWS)

**Objective:** Connect the warehouse robot to AWS IoT Core for real-time telemetry and monitoring.

### 🔧 Setup
- AWS IoT Core endpoint:  
  `a37wis2tab9brj-ats.iot.ap-south-1.amazonaws.com`
- MQTT Topics:
  - Publish → `warehouse/robot1/status`
  - Subscribe → `warehouse/robot1/#`
- Certificates stored in:  
  `Warehouse_Robot_Navigation/secrets/robot1/`
- Policy: **warehouse-robot-policy**  
  (Allows `connect`, `publish`, `subscribe`, and `receive`)

### 🧠 Results
- ✅ Secure MQTT connection established (`rc=0`)
- ✅ Message published successfully:
  ```json
  {
    "device": "robot1",
    "status": "online",
    "battery": 87,
    "ts": 1762397342
  }

✅ Project Completed: Warehouse Robot Navigation (Task 2 – Robotics)

🗒️ Note

If you push this folder to GitHub, this README will automatically appear as your project’s main description.