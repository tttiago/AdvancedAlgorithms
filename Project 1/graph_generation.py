"""Generate the graph files to be used on the computational experiments.
Graphs are stored in the chosen directory, as pickle files containing
the adjacency list and the coordinates of the nodes of each graph."""

import networkx as nx
import pickle
import os
import random


def generate_coords(n_nodes):
    """Generate a set of different (x, y) coordinates for the nodes.
    Coordinates are integers between 1 and 9 (inclusive).
    Avoids adding an (x, y) if it is one of the four nearest neighbours (left,
    right, up, down) of a coordinate already accepted."""
    
    coords = {}
    i = 0
    while i < n_nodes:
        x = random.randint(1, 9)
        y = random.randint(1, 9)
        if (x, y) in coords.values():
            continue
        nearest_neighbours = ((x+1, y), (x-1, y), (x, y+1), (x,y-1))
        if any((x, y) in coords.values() for (x, y) in nearest_neighbours):
            continue
        coords[i] = (x, y)
        i += 1
    
    return coords


def generate_connected_graph(n_nodes, p):
    """Generate a connected graph with n_nodes using the Erdős–Rényi model.
    To ensure connectedness, an edge between two random nodes belonging
    to different connected components is added until the graph is 
    fully connected."""

    G = nx.erdos_renyi_graph(n_nodes, p, seed=SEED, directed=False)
    while not nx.is_connected(G):
        connected_components = list(nx.connected_components(G))
        from_connected_component = random.choice(connected_components)
        while True:
            to_connected_component = random.choice(connected_components)
            if from_connected_component != to_connected_component:
                break        
        from_node = random.choice(list(from_connected_component))
        to_node = random.choice(list(to_connected_component))
        G.add_edge(from_node, to_node)
    return G


SEED = 88784
MAX_N_NODES = 20
EDGE_PERCENTAGES = (0.25, 0.50, 0.75)
GRAPH_PATH = './graphs'

random.seed(SEED)
if not os.path.exists(GRAPH_PATH):
    os.makedirs(GRAPH_PATH)

for edge_percentage in EDGE_PERCENTAGES:
    print('\n   ######################################')
    print(f'Generating graphs with {edge_percentage*100:.0f}%' +
            f' of maximum edges.')
    print('   ######################################\n')
    for n_nodes in range(2, MAX_N_NODES + 1):

        coords = generate_coords(n_nodes)
        G = generate_connected_graph(n_nodes, p=edge_percentage)   
        adj_list = nx.to_dict_of_lists(G)

        max_edges = n_nodes * (n_nodes - 1) / 2
        n_edges = G.number_of_edges()
        print(f'Generated graph with {n_nodes:<2} nodes and {n_edges:^3} edges' + 
        f' ({n_edges/max_edges*100:.2f}% of max edges).')
        
        str_n_nodes = str(n_nodes).zfill(2)
        str_p = f'{edge_percentage*100:.0f}'
        with open(f'{GRAPH_PATH}/{str_n_nodes}nodes_p{str_p}.pkl', 'wb') as f:
            pickle.dump(adj_list, f)
            pickle.dump(coords, f)