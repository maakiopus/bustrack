import os
import json
from time import sleep
from datetime import datetime, timezone, time

from _login import get_account_sync
from findmy import KeyPair
from findmy.reports import RemoteAnisetteProvider

sleep_sec = 6

# Initialize variables for Location Tracking
latitude = 0.0
longitude = 0.0
timestamp = datetime.now().isoformat()
oldtime = None
# Secrets
PRIV_KEY = os.environ['PRIV_KEY'] 
ANISETTE_SERVER = os.environ['ANISETTE_SERVER']

def get_tracker_location():
    global latitude, longitude, timestamp
    try:
        reports = acc.fetch_last_reports(key)
        report = sorted(reports, reverse=True)[0]
        latitude = report.latitude
        longitude = report.longitude
        timestamp = report.timestamp.isoformat()
    except:
        pass
    return {
        'lat': float(latitude),
        'lng': float(longitude),
        'timestamp': str(timestamp)
    }

key = KeyPair.from_b64(PRIV_KEY)
acc = get_account_sync(
    RemoteAnisetteProvider(ANISETTE_SERVER),
)

print(f"Logged in as: {acc.account_name} ({acc.first_name} {acc.last_name})")

while True:
    now = datetime.now()
    # if (now.hour > 18) or (now.hour < 6):
    if (1 == 1):
        oldtime = timestamp
        get_tracker_location()

        if oldtime == timestamp:
            sleep(sleep_sec)
            continue

        data = {
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude
        }
        
        json_path = "locstore/" + now.strftime('%d-%m-%Y') + ".json"
        
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        if os.path.exists(json_path):
            with open(json_path, 'r') as jsonfile:
                try:
                    jsondata = json.load(jsonfile)
                    if not isinstance(jsondata, list):
                        jsondata = [jsondata]
                except json.JSONDecodeError:
                    jsondata = []
            
            jsondata.append(data)
            with open(json_path, 'w') as jsonfile:
                json.dump(jsondata, jsonfile, indent=4)
        else:
            with open(json_path, 'w') as jsonfile:
                json.dump([data], jsonfile, indent=4)

        print(f"Appended telemetry time:{timestamp} lat:{latitude} lng:{longitude}")
    sleep(sleep_sec)