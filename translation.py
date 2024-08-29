# Two-way JSON to NetworkX translation
# Port from Anestis work
# v2

import networkx as nx
import json

def request2graph(data):

    # Initialize a directed graph
    # graph = nx.DiGraph()
    graph = nx.Graph()

    # Add nodes to the graph
    for node in data["services"]:
        graph.add_node(node['name'], cpu=node['cpu'], type=node['type'])

    # Add edges to the graph based on the connections
    for connection in data["connections"]:
        graph.add_edge(connection['from'], connection['to'], bandwidth=connection['bandwidth'])

    decorations = {
        "description": data["services"][0].get("description", "unknown"),
        "slice": data["services"][0].get("slice", "unknown"),
        "customer": data["services"][0].get("customer", "unknown"),
        "validation": data["services"][0].get("validation", "unknown"),
        "description_connection": data["connections"][0].get("description", "unknown"),
        "availability": data["qos"][0].get("availability", "unknown"),
        "latency": data["qos"][0].get("latency", "unknown"),
        "bandwidth": data["qos"][0].get("bandwidth", "unknown"),
    }

    return graph, decorations

def graph2request(graph, filename="outbox/output.json", data={}):

    # Extract Services
    nodes = []
    for node, attr in graph.nodes(data=True):
        nodes.append({
            "name": node,
            "cpu": attr.get("cpu", 0),  # Default to 0 if not found
            "type": attr.get("type", "unknown"),  # Default to 'unknown' if not found
            "slice": data.get("slice", "unknown"),
            "customer": data.get("customer", "unknown"),
            "validation": data.get("validation", "unknown"),
            "description": data.get("description", "unknown"),
        })

    # Extract Connections
    edges = []
    for from_node, to_node, attr in graph.edges(data=True):
        edges.append({
            "from": from_node,
            "to": to_node,
            "bandwidth": attr.get("bandwidth", 0),  # Default to 0 if not found
            "description": data.get("description_connection", "unknown")
        })

    # Extract QoS
    qos = []
    qos.append({
            "availability": data.get("availability", "unknown"),
            "latency": data.get("latency", "unknown"),
            "bandwidth": data.get("bandwidth", "unknown"),
        })

    # Construct the JSON structure
    data = {
        "version": "1.0",
        "services": nodes,
        "qos": qos,
        "connections": edges
    }

    # json.dumps(data, indent=4)

    # Save the data as a JSON file
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return json.dumps(data, indent=4)