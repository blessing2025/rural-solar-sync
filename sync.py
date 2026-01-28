import time
import os
import requests
import sys
import json
from datetime import datetime

# Rural Solar Grid Configuration
VILLAGE_ID = os.getenv("VILLAGE_ID", "Bamenda")
POWER_KW = float(os.getenv("POWER_KW", "120"))
LOCAL_CACHE = os.getenv("LOCAL_CACHE_PATH", "/tmp/solar_sync_cache.json")
CENTRAL_API_URL = os.getenv("API_URL", "http://central-server:8000/api/solar")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))
RETRY_INTERVAL = int(os.getenv("RETRY_INTERVAL", "10"))

DATA = {
    "village_id": VILLAGE_ID,
    "power_kw": POWER_KW,
    "timestamp": datetime.utcnow().isoformat(),
    "sync_attempt": 1
}

def save_to_local_cache(data, cache_path=LOCAL_CACHE):
    """Save sync data to local cache for intermittent connectivity"""
    try:
        with open(cache_path, 'w') as f:
            json.dump(data, f)
        print(f"[CACHE] Data saved locally at {cache_path}")
        return True
    except Exception as e:
        print(f"[CACHE_ERROR] Failed to save cache: {e}")
        return False

def sync_to_central(data, api_url=CENTRAL_API_URL):
    """Attempt to sync data to central server with retry logic"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[SYNC] Attempt {attempt}/{MAX_RETRIES} to {api_url}")
            r = requests.post(api_url, json=data, timeout=15)
            
            if r.status_code == 200:
                print(f"[SUCCESS] Sync successful on attempt {attempt}")
                print(f"[RESPONSE] {r.json()}")
                return True
            else:
                print(f"[HTTP_ERROR] Status {r.status_code}: {r.text}")
                
        except requests.exceptions.Timeout:
            print(f"[TIMEOUT] Network timeout on attempt {attempt}")
        except requests.exceptions.ConnectionError:
            print(f"[CONNECTION_ERROR] Cannot reach {api_url} on attempt {attempt}")
        except requests.exceptions.RequestException as e:
            print(f"[REQUEST_ERROR] {type(e).__name__}: {e}")
        
        if attempt < MAX_RETRIES:
            wait_time = RETRY_INTERVAL * attempt  # Exponential backoff
            print(f"[RETRY] Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
        else:
            print(f"[FAILED] Max retries ({MAX_RETRIES}) exceeded")
            return False
    
    return False

# Main execution
if __name__ == "__main__":
    print("="*60)
    print("[RURAL SOLAR GRID SYNC] Starting sync operation")
    print(f"[CONFIG] Village: {VILLAGE_ID}, Power: {POWER_KW}kW")
    print(f"[CONFIG] Max Retries: {MAX_RETRIES}, Interval: {RETRY_INTERVAL}s")
    print(f"[CONFIG] Central API: {CENTRAL_API_URL}")
    print("="*60)
    
    # Step 1: Save to local cache (ensures data is not lost)
    print("\n[STEP 1] Saving data to local cache...")
    save_to_local_cache(DATA)
    
    # Step 2: Attempt sync with retry logic
    print("\n[STEP 2] Attempting to sync to central database...")
    success = sync_to_central(DATA)
    
    # Step 3: Exit with appropriate code
    if success:
        print("\n[RESULT] ✓ Sync completed successfully")
        sys.exit(0)
    else:
        print("\n[RESULT] ✗ Sync failed - data cached locally for retry")
        sys.exit(1)