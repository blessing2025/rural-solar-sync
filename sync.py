import time
import requests

DATA = {"village": "Bamenda", "power_kw": 120}

for attempt in range(5):  # retry logic
    try:
        r = requests.post("https://central-server/api/solar", json=DATA, timeout=5)
        if r.status_code == 200:
            print("Sync successful")
            break
    except:
        print("Network error, retrying...")
        time.sleep(10)