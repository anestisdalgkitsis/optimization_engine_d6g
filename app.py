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

# Global Settings
active_partition_algorithm = "default"

# Global Variables
status = "standby"
partition_algorithms_list = ["default", "random", "auto"]
automation_list = ["partition"]

# Module Info
module_name = "Network Optimization Module"
module_version = "0.28 Alpha"
module_ip = socket.gethostbyname(socket.gethostname())
module_port = "5863"
module_start_time = time.time()
module_endpoints = ["management", "service_request"]


# TEMP
temp_graph = None

def print_temp_graph():
    nx.draw(temp_graph, with_labels=True)
    plt.savefig("graph.png")  # Save the plot as an image file


# ROUTES

# Flask App
app = Flask(__name__)

# Web-UI
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start():
    # Your logic for starting
    return jsonify({"status": "started"})

@app.route('/api/stop', methods=['POST'])
def stop():
    # Your logic for stopping
    return jsonify({"status": "stopped"})

@app.route('/api/status', methods=['GET'])
def status():
    # Your logic for getting status
    return jsonify({"status": "running"})  # or "stopped"

# Management API

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
    data = request.files['request']

    # Send file for translation
    graph = translation.request2graph(data)

    # print("s")
    # print("Nodes:", graph.nodes())
    # print("Edges:", graph.edges())

    s1, s2, s3 = partition.partition(graph, n_domain=3)

    # print("s1")
    # print("Nodes:", s1.nodes())
    # print("Edges:", s1.edges())

    # print("s2")
    # print("Nodes:", s2.nodes())
    # print("Edges:", s2.edges())

    # print("s3")
    # print("Nodes:", s3.nodes())
    # print("Edges:", s3.edges())

    translation.graph2request(s1, "sp1.rdf")
    translation.graph2request(s2, "sp2.rdf")
    translation.graph2request(s3, "sp3.rdf")

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