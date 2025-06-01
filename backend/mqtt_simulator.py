import time
import random
import json
import requests

API_URL = "http://127.0.0.1:5000/api/data"
NUM_DEVICES = 10
INTERVAL = 20  # seconds
DURATION = 4 * 60  # 4 minutes
REPEAT = DURATION // INTERVAL

# Generate fixed data for each device
device_payloads = {
    device_id: {
        "device_id": device_id,
        "heart_rate": random.randint(60, 100),
        "temperature": round(random.uniform(36.5, 38.5), 1)
    }
    for device_id in range(1, NUM_DEVICES + 1)
}

print(f"🚀 Simulating {NUM_DEVICES} devices every {INTERVAL}s for {DURATION // 60} minutes...")

for round_num in range(1, REPEAT + 1):
    print(f"\n🕒 Round {round_num}/{REPEAT}")
    for device_id, payload in device_payloads.items():
        data = payload.copy()
        data["timestamp"] = time.time()
        try:
            response = requests.post(API_URL, json=data)
            print(f"[Device {device_id}] Sent → Status {response.status_code}")
        except Exception as e:
            print(f"[Device {device_id}] ❌ Error: {e}")
    time.sleep(INTERVAL)

print("\n✅ Simulation complete.")
