# Two-way RDF to NetworkX translation
# Port from Anestis work

# from rdflib import Graph, Literal, RDF, URIRef, Namespace
# from rdflib.namespace import FOAF, XSD
import networkx as nx
import json
import yaml

def request2graph(data):

    # Initialize the directed graph
    # graph = nx.DiGraph()
    graph = nx.Graph()

    # Parse the YAML content
    data = yaml.safe_load(data)

    # Extract service nodes and add them to the graph
    service_nodes = data.get("services nodes", [])
    for node in service_nodes:
        graph.add_node(node["name"], **node)

    # Extract node connections and add them as edges to the graph
    node_connections = data.get("node connections", [])
    for connection in node_connections:
        from_node = connection["from"]
        to_node = connection["to"]
        graph.add_edge(from_node, to_node, **connection)

    return graph

def graph2request(graph, output_file="output.rdf"):
    
    # Initialize the structure of the request file
    request_data = {
        "version": "1.0",
        "services": {
            "RAN": [],
            "Core": []
        },
        "connections_user_plane": [],
        "connections_control_plane": []
    }

    # Categorize the nodes into RAN and Core services
    for node, attributes in graph.nodes(data=True):
        service_info = {
            "name": attributes.get("name", node),
            "type": attributes.get("category", "network_element"),
            "service_type": attributes.get("service_type", ""),
            "slice_type": attributes.get("slice_type", ""),
            "customer_name": attributes.get("customer_name", ""),
            "validation_time": attributes.get("validation_time", ""),
            "general_description": attributes.get("description", "")
        }
        
        qos_specification = {
            "Availability": attributes.get("availability", "xx%"),
            "Latency": attributes.get("latency", "yy ms"),
            "Bandwidth": attributes.get("bandwidth", "zz mbps")
        }

        if attributes.get("service_type", "").lower() == "radio_access":
            service_entry = {"QoS_Specification": qos_specification, **service_info}
            request_data["services"]["RAN"].append(service_entry)
        else:
            service_entry = {"QoS_Specification": qos_specification, **service_info}
            request_data["services"]["Core"].append(service_entry)
    
    # Categorize edges into user plane and control plane connections
    for u, v, attributes in graph.edges(data=True):
        connection = {
            "from": u,
            "to": v,
            "description": attributes.get("description", "")
        }
        
        if attributes.get("plane", "").lower() == "user_plane":
            request_data["connections_user_plane"].append(connection)
        else:
            request_data["connections_control_plane"].append(connection)

    # Convert the Python dictionary to a JSON-formatted string
    request_json = json.dumps(request_data, indent=2)
    
    return request_json

# OUTDATED, THIS WILL BE PHASED OUT IN THE NEXT VERSION
# def request2rdf(graph, output_file="output.rdf"):
#     # Create a new RDF graph
#     rdf_graph = Graph()
    
#     # Define a namespace for our nodes and edges
#     EX = Namespace("http://example.org/")
    
#     # Bind our namespace to a prefix for easier reading
#     rdf_graph.bind("ex", EX)
    
#     # Iterate over nodes and add them to the RDF graph
#     for node, data in graph.nodes(data=True):
#         node_uri = EX[f"node{node}"]
#         rdf_graph.add((node_uri, RDF.type, EX.VNF))
#         rdf_graph.add((node_uri, EX.cpu, Literal(data['cpu'], datatype=XSD.int)))
#         rdf_graph.add((node_uri, EX.type, Literal(data['type'], datatype=XSD.string)))
    
#     # Iterate over edges and add them to the RDF graph
#     for source, target, data in graph.edges(data=True):
#         edge_uri = EX[f"link{source}_{target}"]
#         rdf_graph.add((edge_uri, RDF.type, EX.Link))
#         rdf_graph.add((edge_uri, EX.source, EX[f"node{source}"]))
#         rdf_graph.add((edge_uri, EX.target, EX[f"node{target}"]))
#         rdf_graph.add((edge_uri, EX.bandwidth, Literal(data['bandwidth'], datatype=XSD.int)))
    
#     # Serialize the RDF graph to a file
#     rdf_graph.serialize(destination=output_file, format='xml')

# OUTDATED, THIS WILL BE PHASED OUT IN THE NEXT VERSION
# def rdf2request(input_file="input.rdf"):
#     # Create an empty graph
#     G = nx.Graph()

#     # Load the RDF graph from file
#     rdf_graph = Graph()
#     rdf_graph.parse(input_file, format="xml")

#     # Define the namespace used in the RDF file
#     EX = Namespace("http://example.org/")

#     # Iterate over nodes in the RDF graph
#     for node_uri in rdf_graph.subjects(RDF.type, EX.VNF):
#         node_id = int(node_uri.split("node")[-1])  # Extract node ID
#         cpu = None
#         node_type = None

#         # # Extract CPU and type information for the node
#         # for _, _, value in rdf_graph.triples((node_uri, None, None)):
#         #     if value.startswith(EX):
#         #         predicate = value.split("/")[-1]
#         #         if predicate == "cpu":
#         #             cpu = int(rdf_graph.value(subject=node_uri, predicate=EX.cpu, default=None))
#         #         elif predicate == "type":
#         #             node_type = str(rdf_graph.value(subject=node_uri, predicate=EX.type, default=None))
        
#         # Extract CPU and type information for the node
#         for name, attr, value in rdf_graph.triples((node_uri, None, None)):
#             predicate = attr.split("/")[-1]
#             if predicate == "cpu":
#                 cpu = int(rdf_graph.value(subject=node_uri, predicate=EX.cpu, default=None))
#             elif predicate == "type":
#                 node_type = str(rdf_graph.value(subject=node_uri, predicate=EX.type, default=None))

#         # Add node to the graph
#         if cpu is not None and node_type is not None:
#             G.add_node(node_id, cpu=cpu, type=node_type)

#     # Iterate over edges in the RDF graph
#     for edge_uri in rdf_graph.subjects(RDF.type, EX.Link):
#         source_uri = rdf_graph.value(subject=edge_uri, predicate=EX.source, default=None)
#         target_uri = rdf_graph.value(subject=edge_uri, predicate=EX.target, default=None)
#         bandwidth = int(rdf_graph.value(subject=edge_uri, predicate=EX.bandwidth, default=None))

#         # Extract source and target node IDs
#         source_id = int(source_uri.split("node")[-1])
#         target_id = int(target_uri.split("node")[-1])

#         # Add edge to the graph
#         if source_id is not None and target_id is not None:
#             G.add_edge(source_id, target_id, bandwidth=bandwidth)

#     return G