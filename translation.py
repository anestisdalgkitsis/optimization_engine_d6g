# Two-way RDF to NetworkX translation
# Port from Anestis work

# from rdflib import Graph, Literal, RDF, URIRef, Namespace
# from rdflib.namespace import FOAF, XSD
import networkx as nx
import json
# import yaml

def request2graph(data):

    # Initialize a directed graph
    # graph = nx.DiGraph()
    graph = nx.Graph()

    # Add nodes to the graph
    for node in data["services nodes"]:
        # print(node['name'], node['cpu'], node['type'])
        # graph.add_node(node["name"], **node)
        graph.add_node(node['name'], cpu=node['cpu'], type=node['type'])
        # G.add_node(node_id, cpu=cpu, type=node_type)

    # Add edges to the graph based on the connections
    for connection in data["node connections"]:
        # print(connection['from'], connection['to'], connection['bandwidth'])
        # graph.add_edge(connection["from"], connection["to"], **connection)
        graph.add_edge(connection['from'], connection['to'], bandwidth=connection['bandwidth'])
        # G.add_edge(source_id, target_id, bandwidth=bandwidth)

    return graph

def graph2request(graph, filename="outbox/output.json"):

    # # Prepare the data to be saved as JSON
    # data = {
    #     "version": "1.0",
    #     "services nodes": [],
    #     "node connections": []
    # }

    # # Add nodes to the JSON structure
    # for node, node_data in graph.nodes(data=True):
    #     data["services nodes"].append({
    #         "name": "id_" + node,
    #         **{k: v for k, v in node_data.items() if k != "name"}
    #     })

    # # Add edges to the JSON structure
    # for from_node, to_node, edge_data in graph.edges(data=True):
    #     connection = {
    #         "from": from_node,
    #         "to": to_node,
    #         **{k: v for k, v in edge_data.items() if k not in ["from", "to"]}
    #     }
    #     data["node connections"].append(connection)

    # Extract nodes
    nodes = []
    for node, attr in graph.nodes(data=True):
        nodes.append({
            "name": node,
            "cpu": attr.get("cpu", 0),  # Default to 0 if not found
            "type": attr.get("type", "unknown")  # Default to 'unknown' if not found
        })

    # Extract edges
    edges = []
    for from_node, to_node, attr in graph.edges(data=True):
        edges.append({
            "from": from_node,
            "to": to_node,
            "bandwidth": attr.get("bandwidth", 0)  # Default to 0 if not found
        })

    # Construct the JSON structure
    data = {
        "version": "1.0",
        "services nodes": nodes,
        "node connections": edges
    }

    # json.dumps(data, indent=4)

    # Save the data as a JSON file
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return json.dumps(data, indent=4)