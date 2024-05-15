# Two-way RDF to NetworkX translation
# Port from Anestis work

from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD
import networkx as nx

def request2rdf(graph, output_file="output.rdf"):
    # Create a new RDF graph
    rdf_graph = Graph()
    
    # Define a namespace for our nodes and edges
    EX = Namespace("http://example.org/")
    
    # Bind our namespace to a prefix for easier reading
    rdf_graph.bind("ex", EX)
    
    # Iterate over nodes and add them to the RDF graph
    for node, data in graph.nodes(data=True):
        node_uri = EX[f"node{node}"]
        rdf_graph.add((node_uri, RDF.type, EX.VNF))
        rdf_graph.add((node_uri, EX.cpu, Literal(data['cpu'], datatype=XSD.int)))
        rdf_graph.add((node_uri, EX.type, Literal(data['type'], datatype=XSD.string)))
    
    # Iterate over edges and add them to the RDF graph
    for source, target, data in graph.edges(data=True):
        edge_uri = EX[f"link{source}_{target}"]
        rdf_graph.add((edge_uri, RDF.type, EX.Link))
        rdf_graph.add((edge_uri, EX.source, EX[f"node{source}"]))
        rdf_graph.add((edge_uri, EX.target, EX[f"node{target}"]))
        rdf_graph.add((edge_uri, EX.bandwidth, Literal(data['bandwidth'], datatype=XSD.int)))
    
    # Serialize the RDF graph to a file
    rdf_graph.serialize(destination=output_file, format='xml')

def rdf2request(input_file="input.rdf"):
    # Create an empty graph
    G = nx.Graph()

    # Load the RDF graph from file
    rdf_graph = Graph()
    rdf_graph.parse(input_file, format="xml")

    # Define the namespace used in the RDF file
    EX = Namespace("http://example.org/")

    # Iterate over nodes in the RDF graph
    for node_uri in rdf_graph.subjects(RDF.type, EX.VNF):
        node_id = int(node_uri.split("node")[-1])  # Extract node ID
        cpu = None
        node_type = None

        # Extract CPU and type information for the node
        for _, _, value in rdf_graph.triples((node_uri, None, None)):
            if value.startswith(EX):
                predicate = value.split("/")[-1]
                if predicate == "cpu":
                    cpu = int(rdf_graph.value(subject=node_uri, predicate=EX.cpu, default=None))
                elif predicate == "type":
                    node_type = str(rdf_graph.value(subject=node_uri, predicate=EX.type, default=None))

        # Add node to the graph
        if cpu is not None and node_type is not None:
            G.add_node(node_id, cpu=cpu, type=node_type)

    # Iterate over edges in the RDF graph
    for edge_uri in rdf_graph.subjects(RDF.type, EX.Link):
        source_uri = rdf_graph.value(subject=edge_uri, predicate=EX.source, default=None)
        target_uri = rdf_graph.value(subject=edge_uri, predicate=EX.target, default=None)
        bandwidth = int(rdf_graph.value(subject=edge_uri, predicate=EX.bandwidth, default=None))

        # Extract source and target node IDs
        source_id = int(source_uri.split("node")[-1])
        target_id = int(target_uri.split("node")[-1])

        # Add edge to the graph
        if source_id is not None and target_id is not None:
            G.add_edge(source_id, target_id, bandwidth=bandwidth)

    return G