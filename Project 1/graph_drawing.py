"""Generate visual representations of the graph instances and the
computed solutions."""


import matplotlib.pyplot as plt
import networkx as nx
import os
import pickle


def batch_draw(path):
    """Draw all graphs in path, colouring them if colours are saved."""

    for file in os.listdir(path):
        if file[-4:] != '.pkl':
            continue
        with open(f'{path}/{file}', 'rb') as f:
            adj_list = pickle.load(f)
            coords = pickle.load(f)
            try:
                chromatic_number = pickle.load(f)
                colours = pickle.load(f)
            except EOFError:
                chromatic_number = None
                colours = 'k'
        
        if 'greedy' in path:
            colours = [colours[node] for node in range(len(adj_list))]

        if chromatic_number:
            plt.title(f'Chromatic number: {chromatic_number}')

        G = nx.Graph(adj_list)
        nx.draw(G, pos=coords, node_color=colours, 
                edge_color='grey', with_labels=True)

        plt.savefig(f'{path}/{file[:-4]}.png')
        plt.clf()


path = './results/exhaustive_v2'
batch_draw(path)


# file = './graphs/13nodes_p50.pkl'
# with open(file, 'rb') as f:
#     adj_list = pickle.load(f)
#     coords = pickle.load(f)
# G = nx.Graph(adj_list)
# nx.draw(G, pos=coords, node_color='grey', edge_color='k', with_labels=True) 

# adj_str = '\n'.join([f'{node}: {adj_list[node]}' for node in adj_list])
# plt.text(7.5, 0.4, adj_str, size=8)
# plt.show()   