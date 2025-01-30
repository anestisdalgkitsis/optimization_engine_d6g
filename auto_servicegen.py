# Service request generator
# v2.16

# Local Modules
import translation

# Modules
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import networkx as nx
import random
import requests
import argparse

# Arguments
parser = argparse.ArgumentParser("arguments")
parser.add_argument("counter", help="How many times to run.", type=int)
args = parser.parse_args()

# def print_graph(graph):
#     nx.draw(graph, with_labels=True)
#     plt.savefig("graph.png")  # Save the plot as an image file

# Port from Cyril's work
def request(length=(5, 10)):

    def gen_sfc(num_nodes):
        '''
        Generates a serial SFC with the given number of nodes
        '''
        G = nx.Graph()
    
        # Add nodes with resource requirements
        for i in range(num_nodes):
            cpu = random.randint(1, 10)  # CPU requirement
            G.add_node(f"{i}", cpu=cpu, type='vnf')
    
        # Add links with bandwidth
        for i in range(num_nodes - 1):
            bandwidth = random.randint(1, 10)  # Bandwidth requirement
            G.add_edge(f"{i}", f"{i+1}", bandwidth=bandwidth)
    
        return G

    nVNF = random.randint(*length)
    G = gen_sfc(nVNF)
    # print_graph(G)
    return G

for i in range(args.counter):
    sg = request((8, 12))
    data = {
        "description": "Evolved Node B (eNodeB) for handling radio communication at Site 1.",
        "slice": "x_slice",
        "customer": "customer_x",
        "validation": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description_connection": "Service1 forwards control plane information to Service1_control_plane.",
        "availability": "0.99",
        "latency": "13",
        "bandwidth": "1000",
    }
    service_request = translation.graph2request(sg, "inbox/sid85034.json", data)
    url = "http://127.0.0.1:5863/service_request"
    file_path = "inbox/sid85034.json"
    with open(file_path, "rb") as file:
        files = {"request": file}
        response = requests.post(url, files=files)
    print(str(i+1) + " / " + str(args.counter))