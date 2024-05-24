# Local Modules
import partition
import translation

# Modules
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
from rdflib import Graph
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

# Flask App
app = Flask(__name__)

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

# IBN (RDF) Endpoint

@app.route('/service_request', methods=['POST'])
def process_rdf():
    if 'request' not in request.files:
        return jsonify({'error': 'No RDF service request provided'})

    file = request.files['request']

    service_request = translation.rdf2request(file)

    print("s")
    print("Nodes:", service_request.nodes())
    print("Edges:", service_request.edges())

    s1, s2, s3 = partition.partition(service_request, n_domain=3)

    print("s1")
    print("Nodes:", s1.nodes())
    print("Edges:", s1.edges())

    print("s2")
    print("Nodes:", s2.nodes())
    print("Edges:", s2.edges())

    print("s3")
    print("Nodes:", s3.nodes())
    print("Edges:", s3.edges())

    translation.request2rdf(s1, "sp1.rdf")
    translation.request2rdf(s2, "sp2.rdf")
    translation.request2rdf(s3, "sp3.rdf")

    return jsonify("exported")

# SO Endpoint

# Monitoring Endpoint

# Functions

# MAIN
if __name__ == '__main__':
    app.run(debug=True, port=module_port)