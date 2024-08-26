# Dr. Anestis Dalgkitsis
# Version 2.0

# Local Modules
import partition
import translation

# Modules
from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import networkx as nx
import datetime
import socket
import random
import time
import json
import yaml
import pprint as pprint

# Global Settings
active_partition_algorithm = "default"

# Global Variables
status = "standby"
partition_algorithms_list = ["default", "random", "auto"]
automation_list = ["partition"]

# Module Info
module_name = "Network Optimization Module"
module_version = "0.35 Alpha"
module_ip = socket.gethostbyname(socket.gethostname())
module_port = "5863"
module_start_time = time.time()
module_endpoints = ["management", "service_request"]


# ROUTES

# Flask App
app = Flask(__name__)

# Web-UI Dashboard
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start():
    # Your logic for starting
    return jsonify({"status": "Running"})

@app.route('/api/stop', methods=['POST'])
def stop():
    # Your logic for stopping
    return jsonify({"status": "Standby"})

# @app.route('/api/status', methods=['GET'])
# def status():
#     # Your logic for getting status
#     return jsonify({"status": "running"})  # or "stopped"

# Management API (will be merged with Web-UI)

@app.route('/management', methods=['POST'])
def management():

    incoming_message = request.json
    command_list = incoming_message.get('command', [])

    # Verbose
    print("Management -> Incoming message:", incoming_message)

    # Decoder
    if "algorithm" in command_list:
        if "partition" in command_list:
            # Set here algorithm name to default
            pass
        pass

    if "list" in command_list:
        if "automation" in command_list:
            return jsonify(automation_list)
        elif "partition" in command_list:
            return jsonify(partition_algorithms_list)

    if "status" in command_list:
        report = {
            "status": status,
            "name": module_name,
            "version": module_version,
            "ip": module_ip,
            "port": module_port,
            "uptime": str(datetime.timedelta(seconds=(time.time() - module_start_time))).split('.')[0],
            "endpoints": module_endpoints,
            "active partition algorithm": active_partition_algorithm,
        }
        return jsonify(report)

    # Return
    return jsonify("ok")

# IBN Endpoint

@app.route('/service_request', methods=['POST'])
def incoming_request():

    # Check if it is a request indeed
    if 'request' not in request.files:
        return jsonify({'error': 'No service request provided'})
    else:
        print("Received request!")
    file_storage = request.files['request']

    # Decode
    file_content = file_storage.read().decode('utf-8')

    # Clean file
    data = json.loads(file_content)

    # print("JSON data check:\n---")
    # pprint.pprint(data)
    # print("---")
    # exit()

    # Send file for translation
    graph = translation.request2graph(data)

    print("---\nGraph Report:")
    print("-Nodes:", graph.nodes())
    for node in graph.nodes(data=True):
        print(f"Node: {node[0]}, CPU: {node[1].get('cpu')}")
    print("-Edges:", graph.edges())
    for edge in graph.edges(data=True):
        print(f"Edge from {edge[0]} to {edge[1]}, Bandwidth: {edge[2].get('bandwidth')}")
    print("---")

    # Parition Service
    s1, s2, s3 = partition.partition(graph, n_domain=3)

    # print("s1 Sub-Graph Report:")
    # print("-Nodes:", s1.nodes())
    # print("-Edges:", s1.edges())

    # print("s2 Sub-Graph Report:")
    # print("-Nodes:", s2.nodes())
    # print("-Edges:", s2.edges())

    # print("s3 Sub-Graph Report:")
    # print("-Nodes:", s3.nodes())
    # print("-Edges:", s3.edges())

    # Return Service
    translation.graph2request(s1, "outbox/sid85034_s0.json")
    translation.graph2request(s2, "outbox/sid85034_s1.json")
    translation.graph2request(s3, "outbox/sid85034_s2.json")

    return jsonify("exported")

# SO Endpoint

# Monitoring Endpoint

# UTILITY FUNCTIONS

def orchestration():
    # move the graph process thing here
    pass


# MAIN
if __name__ == '__main__':
    app.run(debug=True, port=module_port)