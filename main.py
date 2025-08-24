import os
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from datetime import datetime, timedelta, timezone
from threading import Timer,Thread
from time import sleep
import asyncio
from NovaApi.ExecuteAction.LocateTracker.location_request import return_get_location_data_for_device

# Initialize variables for Location Tracking
latitude = 0.0
longitude = 0.0
timestamp = datetime.now().isoformat()

reports = return_get_location_data_for_device("68a847d6-0000-268b-a6f6-34c7e9210863","GoogleFindMyTools µC")
report = sorted(reports, key=lambda loc: loc['timestamp'], reverse=True)[0]  # Fixed: reports not loc
latitude = report["lat"]
longitude = report["lng"]
timestamp = report["timestamp"]
sleep(2)

app = Flask(__name__ , static_folder='static')
socketio = SocketIO(app, async_mode='gevent')

def get_tracker_location():
    global latitude, longitude, timestamp
    if (datetime.now() - datetime.fromisoformat(timestamp).replace(tzinfo=None)).total_seconds() > 5:
        try:
            # Create event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            reports = return_get_location_data_for_device("68a847d6-0000-268b-a6f6-34c7e9210863","GoogleFindMyTools µC")
            report = sorted(reports, key=lambda loc: loc['timestamp'], reverse=True)[0]  # Fixed: reports not loc
            latitude = report["lat"]
            longitude = report["lng"]
            timestamp = report["timestamp"]
            
            loop.close()  # Clean up
        except Exception as e:
            print(f"Error: {e}")
    
    return {
        'lat': float(latitude),
        'lng': float(longitude),
        'timestamp': str(timestamp)
    }

def fetch_loc():
    return {
    'lat': float(latitude),
    'lng': float(longitude),
    'timestamp': str(timestamp)
    }


def update_loc_thread():
    while True:
        report = get_tracker_location()
        print("Got tracker loc:",report)
        sleep(10)

thread = Thread(target=update_loc_thread)
thread.start()

@app.route('/')
def index():
    return render_template('index.html',latitude=latitude,longitude=longitude)

@socketio.on('request_location')
def handle_location_request():
    location = fetch_loc()
    socketio.emit('location_update', location)

if __name__ == '__main__':
    socketio.run(app)