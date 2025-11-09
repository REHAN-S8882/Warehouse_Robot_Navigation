# scripts/robot_publisher.py
import json, ssl, time, random, signal, sys
from pathlib import Path
import paho.mqtt.client as mqtt

# ==== AWS IoT settings ====
ENDPOINT = "a37wis2tab9brj-ats.iot.ap-south-1.amazonaws.com"
PORT = 8883
CLIENT_ID = "robot1"  # must exactly match policy condition
TOPIC_PUB = "warehouse/robot1/status"
TOPIC_SUB = "warehouse/robot1/#"  # optional subscribe for echoes

# ==== Cert paths (same layout you used) ====
BASE = Path(r"C:\Users\16reh\OneDrive\Desktop\Warehouse_Robot_Navigation\secrets\robot1")
CA1 = BASE / "AmazonRootCA1.pem"
CA3 = BASE / "AmazonRootCA3.pem"
CA_PATH = CA1 if CA1.exists() else CA3
CERT_PATH    = BASE / "1ddb11e352cb087eb8b14ff8025ae5ba6773ade49f196f0c22b92e7022c14ef4-certificate.pem.crt"
PRIVKEY_PATH = BASE / "1ddb11e352cb087eb8b14ff8025ae5ba6773ade49f196f0c22b92e7022c14ef4-private.pem.key"

for p in [CA_PATH, CERT_PATH, PRIVKEY_PATH]:
    if not p.exists():
        raise FileNotFoundError(f"Missing required file: {p}")

# ==== MQTT callbacks ====
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[CONNECT] rc={rc}")
    if rc == 0:
        client.subscribe(TOPIC_SUB, qos=1)

def on_message(client, userdata, msg):
    try:
        print(f"[MSG] {msg.topic} -> {msg.payload.decode('utf-8')}")
    except Exception:
        print(f"[MSG-raw] {msg.topic} -> {msg.payload}")

def on_disconnect(client, userdata, rc, properties=None):
    print(f"[DISCONNECT] rc={rc}")

# ==== Build client ====
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv5, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.tls_set(
    ca_certs=str(CA_PATH),
    certfile=str(CERT_PATH),
    keyfile=str(PRIVKEY_PATH),
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)
client.tls_insecure_set(False)

# Graceful stop
_running = True
def _stop(*_):
    global _running
    _running = False
signal.signal(signal.SIGINT, _stop)
if hasattr(signal, "SIGTERM"):
    signal.signal(signal.SIGTERM, _stop)

# ==== Connect + publish loop ====
PUBLISH_INTERVAL = 5  # seconds
battery = 100

print(f"Connecting to {ENDPOINT}:{PORT} ...")
client.connect(ENDPOINT, PORT, keepalive=60)
client.loop_start()

print("Publishing every", PUBLISH_INTERVAL, "seconds. Press Ctrl+C to stop.")
while _running:
    # fake telemetry
    battery = max(0, battery - random.randint(0, 2))
    payload = {
        "device": "robot1",
        "status": "online" if battery > 0 else "shutdown",
        "battery": battery,
        "speed": round(random.uniform(0.2, 1.0), 2),
        "collisions": random.choice([0, 0, 1]),   # occasional 1 for testing
        "ts": int(time.time())
    }
    result = client.publish(TOPIC_PUB, json.dumps(payload), qos=1)
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print("[WARN] publish rc:", result.rc)
    else:
        print("[PUB]", payload)
    time.sleep(PUBLISH_INTERVAL)

print("Stopping…")
client.loop_stop()
client.disconnect()
print("Done.")
