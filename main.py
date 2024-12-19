import os
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from datetime import datetime, timedelta, timezone
from threading import Timer

from _login import get_account_sync
from findmy import KeyPair
from findmy.reports import RemoteAnisetteProvider

# Initialize variables for Location Tracking
latitude = 0.0
longitude = 0.0
timestamp = datetime.now().isoformat()

# Secrets
PRIV_KEY = os.environ['PRIV_KEY'] 
ANISETTE_SERVER = os.environ['ANISETTE_SERVER']

app = Flask(__name__ , static_folder='static')
socketio = SocketIO(app, async_mode='gevent')

def get_tracker_location():
    global latitude, longitude, timestamp
    if (datetime.now() - datetime.fromisoformat(timestamp).replace(tzinfo=None)).total_seconds() > 5:
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

get_tracker_location()

@app.route('/')
def index():
    return render_template('index.html',latitude=latitude,longitude=longitude)

@socketio.on('request_location')
def handle_location_request():
    location = get_tracker_location()
    socketio.emit('location_update', location)

if __name__ == '__main__':
    socketio.run(app)