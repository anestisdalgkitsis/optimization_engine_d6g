# Dr. Anestis Dalgkitsis
# Version 4.85.34

# Local Modules
import translation

# Modules
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import networkx as nx
import argparse
import socket
import json
import time

# Model Pool
import models.partition as partition
import models.autologic as autologic
import models.greedysplit as greedysplit

# Selector Pool
import selectors.spinwheel as spinwheel

# In-Memory Variables
status = "standby"
start_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
request_count = 0
algorithms = { # this should be changed to modular
    "partition.py (Default)": {"enabled": True},
    "autologic.py": {"enabled": False},
    "greedysplit.py": {"enabled": False},
}

# Module Info
module_name = "Optimization Engine Module"
module_version = "1.28 Beta"
module_ip = socket.gethostbyname(socket.gethostname())
module_port = "5863"


# Load Config files
# TBD


# ARGUMENTS
parser = argparse.ArgumentParser(description="A script that processes command-line arguments.")
# parser.add_argument('input', type=str, help='Input file or value')
parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
args = parser.parse_args()


# ROUTES

# Flask App
app = Flask(__name__)
# socketio = SocketIO(app)

# Web-UI Dashboard  
@app.route('/')
def home():
    return render_template('index.html', algorithms=algorithms)

@app.route('/api/start', methods=['POST'])
def start():
    global status
    status = "standby"
    return jsonify({"status": status})

@app.route('/api/stop', methods=['POST'])
def stop():
    global status
    status = "disabled"
    return jsonify({"status": status})

@app.route('/api/status', methods=['GET'])
def status():
    global start_time
    global status
    global request_count

    uptime = int(time.time() - start_time)

    return jsonify({"status": status, "uptime": str(uptime), "requests": str(request_count)})

@app.route('/toggle_algorithm', methods=['POST'])
def toggle_algorithm():
    algorithm_name = request.form['algorithm']
    if algorithm_name in algorithms:
        algorithms[algorithm_name]['enabled'] = not algorithms[algorithm_name]['enabled']
    return redirect('/')

# IBN Endpoint

@app.route('/service_request', methods=['POST'])
def incoming_request():
    global request_count
    global status

    if status == "disabled":
        return

    # Activate busy indicator
    status = "busy"

    # Check if it is a request indeed
    if 'request' not in request.files:
        return jsonify({'error': 'No service request provided'})
    else:
        request_count += 1
        if args.verbose:
            print("Received request! req: " + str(request_count))
    file_storage = request.files['request']

    # Decode
    file_content = file_storage.read().decode('utf-8')

    # Clean file
    data = json.loads(file_content)

    # Send file for translation
    graph, data = translation.request2graph(data)

    # Parition Service
    s1, s2, s3 = partition.partition(graph, n_domain=3)

    # Encode
    s1e = translation.graph2request(s1, "outbox/sid85034_s0.json", data)
    s2e = translation.graph2request(s2, "outbox/sid85034_s1.json", data)
    s3e = translation.graph2request(s3, "outbox/sid85034_s2.json", data)

    # Combine Response
    combined_response = {
        "s1e": s1e,
        "s2e": s2e,
        "s3e": s3e
    }

    # Deactivate busy indicator
    status = "standby"

    return jsonify(combined_response)


# MAIN
if __name__ == '__main__':
    print(f"Verbose mode: {'on' if args.verbose else 'off'}")
    app.run(debug=True, port=module_port)