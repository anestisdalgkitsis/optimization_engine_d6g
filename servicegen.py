# Service request generator

# Local Modules
import translation

# Modules
import networkx as nx
import random

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
    return G

sg = request((8, 12))
rdf_request = translation.request2rdf(sg, "gen_service.rdf")
