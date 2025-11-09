import json, ssl, time
from pathlib import Path
import paho.mqtt.client as mqtt

# ==== AWS IoT Core Settings ====
ENDPOINT = "a37wis2tab9brj-ats.iot.ap-south-1.amazonaws.com"
PORT = 8883
CLIENT_ID = "robot1"  # must exactly match policy condition
TOPIC_PUB = "warehouse/robot1/status"
TOPIC_SUB = "warehouse/robot1/#"

# ==== File Paths ====
BASE = Path(r"C:\Users\16reh\OneDrive\Desktop\Warehouse_Robot_Navigation\secrets\robot1")

CA1 = BASE / "AmazonRootCA1.pem"
CA3 = BASE / "AmazonRootCA3.pem"
CA_PATH = CA1 if CA1.exists() else CA3

CERT_PATH    = BASE / "1ddb11e352cb087eb8b14ff8025ae5ba6773ade49f196f0c22b92e7022c14ef4-certificate.pem.crt"
PRIVKEY_PATH = BASE / "1ddb11e352cb087eb8b14ff8025ae5ba6773ade49f196f0c22b92e7022c14ef4-private.pem.key"

# ==== Debugging File Checks ====
print("[DEBUG] CA exists?:", CA_PATH.exists(), "->", CA_PATH)
print("[DEBUG] CERT exists?:", CERT_PATH.exists(), "->", CERT_PATH)
print("[DEBUG] KEY exists?:", PRIVKEY_PATH.exists(), "->", PRIVKEY_PATH)

for p in [CA_PATH, CERT_PATH, PRIVKEY_PATH]:
    if not p.exists():
        raise FileNotFoundError(f"Missing required file: {p}")

# ==== MQTT Event Callbacks ====
def on_connect(client, userdata, flags, rc):
    print(f"[CONNECT] rc={rc}")
    if rc == 0:
        print("[INFO] Connection successful ✅")
        client.subscribe(TOPIC_SUB, qos=1)
    else:
        print("[ERROR] Connection failed ❌")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
    except Exception:
        payload = str(msg.payload)
    print(f"[MSG] {msg.topic} -> {payload}")

# ==== Create MQTT Client ====
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message

# ==== Configure TLS ====
client.tls_set(
    ca_certs=str(CA_PATH),
    certfile=str(CERT_PATH),
    keyfile=str(PRIVKEY_PATH),
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)
client.tls_insecure_set(False)

# ==== Connect and Publish ====
print(f"Connecting to {ENDPOINT}:{PORT} ...")
client.connect(ENDPOINT, PORT, keepalive=60)
client.loop_start()
time.sleep(2)

payload = {"device": "robot1", "status": "online", "battery": 87, "ts": int(time.time())}
print("Publishing:", payload)
client.publish(TOPIC_PUB, json.dumps(payload), qos=1)

time.sleep(5)
client.loop_stop()
client.disconnect()
print("Done.")
