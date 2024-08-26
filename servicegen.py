# Service request generator
# v2.16

# Local Modules
import translation

# Modules
import matplotlib.pyplot as plt
import networkx as nx
import random

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

sg = request((8, 12))
service_request = translation.graph2request(sg, "inbox/sid85034.json")
