# scripts/preprocess.py
import numpy as np
import cv2

def normalize_scalar(x, min_v, max_v):
    x = float(x)
    return max(0.0, min(1.0, (x - min_v) / (max_v - min_v + 1e-9)))

def preprocess_telemetry(msg):
    return {
        "battery_norm": normalize_scalar(msg["battery"], 0, 100),
        "speed_norm":   normalize_scalar(msg["speed"],   0.0, 1.5),
        "collisions":   int(msg.get("collisions", 0)),
        "ts":           int(msg["ts"])
    }

def preprocess_frame(frame_bgr, size=(84,84)):
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    gray = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)
    gray = gray.astype(np.float32) / 255.0
    # CHW for CNN
    return np.expand_dims(gray, 0)
