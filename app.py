# Dr. Anestis Dalgkitsis
# Version 2.0

# Local Modules
import partition
import translation

# Modules
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import matplotlib.pyplot as plt
import networkx as nx
# import threading
import datetime
import socket
import random
import time
import json
import yaml
import pprint as pprint

# Global Settings
active_partition_algorithm = "default"

# In-Memory Variables
status = "standby"
# partition_algorithms_list = ["default", "random", "auto"]
# automation_list = ["partition"]
start_time = time.time()
request_count = 0
algorithms = {
    "partition.py": {"enabled": True},
    "test1": {"enabled": False},
    "test2": {"enabled": False},
}

# Module Info
module_name = "Network Optimization Module"
module_version = "1.28 Beta"
module_ip = socket.gethostbyname(socket.gethostname())
module_port = "5863"
module_start_time = time.time()
module_endpoints = ["management", "service_request"]


# Load Config files
# TBD


# Arguments Input
# TBD


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
    # Your logic for starting
    return jsonify({"status": "Running"})

@app.route('/api/stop', methods=['POST'])
def stop():
    # Your logic for stopping
    return jsonify({"status": "Standby"})

@app.route('/api/status', methods=['GET'])
def status():
    # Your logic for getting status
    return jsonify({"status": "running"})  # or "stopped"

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

    # Check if it is a request indeed
    if 'request' not in request.files:
        return jsonify({'error': 'No service request provided'})
    else:
        request_count += 1
        print("Received request! req: " + str(request_count))
    file_storage = request.files['request']

    # Decode
    file_content = file_storage.read().decode('utf-8')

    # Clean file
    data = json.loads(file_content)

    # Send file for translation
    graph = translation.request2graph(data)

    # Parition Service
    s1, s2, s3 = partition.partition(graph, n_domain=3)

    # Encode
    s1e = translation.graph2request(s1, "outbox/sid85034_s0.json")
    s2e = translation.graph2request(s2, "outbox/sid85034_s1.json")
    s3e = translation.graph2request(s3, "outbox/sid85034_s2.json")

    # Combine Response
    combined_response = {
        "s1e": s1e,
        "s2e": s2e,
        "s3e": s3e
    }

    return jsonify(combined_response)


# MAIN
if __name__ == '__main__':
    app.run(debug=True, port=module_port)