"""Tests an exhaustive search algorithm for finding the chromatic number
of the previously generated graphs.
Creates a pickle file containing the adjacency list, the coordinates of the nodes,
the chromatic number and an optimal colouring solution for each graph. 
Also saves the empirical complexity data from running the algorithm for all
the graphs in a pickle file."""

from itertools import product
from math import inf as inf
import os
import pickle
import time

########## EXHAUSTIVE SEARCH ALGORITHMS #############

def generate_all_configs(n_nodes, n_colours=None):
    """Generate all possible n_colours colour configurations 
    for a graph with n_nodes. If n_colours is not given, it is assumed that
    n_colours = n_nodes. Returns an iterator."""
    
    if not n_colours:
        n_colours = n_nodes

    colours = range(n_colours)
    colour_combinations = product(colours, repeat=n_nodes)
    
    return colour_combinations


def valid_config(adj_list, colour_config):
    """Returns True if the graph is properly coloured (no two adjacent 
    vertices have the same colour). Returns False otherwise."""
    global n_comparisons

    for node in adj_list:
        for neighbour in adj_list[node]:
            n_comparisons += 1
            if colour_config[node] == colour_config[neighbour]:
                return False 
    return True


def chromatic_number_exhaustive_v1(adj_list):
    """Returns the chromatic number of a given undirected graph
    represented by its adjacency list and one possible colour combination
    to obtain it."""
    # Iterates through ALL (n^n) possibilities of colouring n nodes with
    # n colours and finds the one using less colours.

    global n_configurations
    global n_comparisons

    n_nodes = len(adj_list)
    colour_combinations = generate_all_configs(n_nodes)
    chromatic_number = inf  # current best chromatic number
    best_colours = None     # current best colour configuration

    for colour_config in colour_combinations:
        n_configurations += 1
        if valid_config(adj_list, colour_config):
            n_comparisons += 1
            if (cur_c_number:=len(set(colour_config))) < chromatic_number:
                chromatic_number = cur_c_number
                best_colours = list(colour_config)
    
    return chromatic_number, best_colours


def chromatic_number_exhaustive_v2(adj_list):
    """Returns the chromatic number of a given undirected graph
    represented by its adjacency list and one possible colour combination
    to obtain it."""
    # Improves on the v1 algorithm by iterating the first (sorted) n^(n-1) 
    # possibilities of colouring n nodes with n colours 
    # and finds the one using less colours.

    global n_configurations
    global n_comparisons

    n_nodes = len(adj_list)
    max_configs = n_nodes ** (n_nodes - 1)  # last configuration to be checked
    colour_combinations = generate_all_configs(n_nodes)
    chromatic_number = inf  # current best chromatic number
    best_colours = None     # current best colour configuration

    for colour_config in colour_combinations:
        # == because n_configurations starts at 0
        if n_configurations == max_configs:
            break
        n_configurations += 1
        if valid_config(adj_list, colour_config):
            n_comparisons += 1
            if (cur_number:=len(set(colour_config))) < chromatic_number:
                chromatic_number = cur_number
                best_colours = list(colour_config)
    
    return chromatic_number, best_colours


def chromatic_number_exhaustive_v3(adj_list):
    """Returns the chromatic number of a given undirected graph
    represented by its adjacency list and one possible colour combination
    to obtain it."""
    # Starts with just n_colours=2 colours and iterates through the first 
    # (sorted) n_colours^(n_nodes-1) possibilities of colouring n_nodes nodes
    # using n_colours colours. 
    # Stops if a valid solution is found and adds one colour otherwise.

    global n_configurations

    n_nodes = len(adj_list)
    max_configs = 0  # last configuration to be checked

    for n_colours in range(2, n_nodes + 1):    
        max_configs += n_colours ** (n_nodes - 1)
        colour_combinations = generate_all_configs(n_nodes, n_colours)
        
        for colour_config in colour_combinations:
            if n_configurations == max_configs:
                # == because n_configurations starts at 0
                break

            n_configurations += 1
            if valid_config(adj_list, colour_config):
                # If we find a valid configuration for the current
                # n_colours, it must be an optimal solution.
                chromatic_number = len(set(colour_config))
                best_colours = list(colour_config)
                return chromatic_number, best_colours      


########## EXHAUSTIVE SEARCH TESTING #############

def save_complexity_data():
    with open(f'./results/exhaustive_analysis_{func_name[-2:]}.pkl', 'wb') as f:
        pickle.dump(empirical_analysis, f)
    print('\nUploaded complexity results to file.')

MAX_NODES = 13

try:
    empirical_analysis = {}
    chromatic_number_func = chromatic_number_exhaustive_v3
    func_name = chromatic_number_func.__name__
    results_path = f'./results/exhaustive_{func_name[-2:]}'

    print('Performing exhaustive search for all graphs' + 
          f', using {func_name}.\n')

    if not os.path.exists(results_path):
        os.makedirs(results_path)

    for file in os.listdir('./graphs/'):
        if int(file[:2]) > MAX_NODES:
            break
        if file.endswith('.png'):
            continue

        print(f'Searching graph {file[:-3]}...', end='', flush=True)
        with open(f'./graphs/{file}', 'rb') as f:
            adj_list = pickle.load(f)
            coords = pickle.load(f)

        n_configurations = 0
        n_comparisons = 0

        t_start = time.time()
        chromatic_number, best_colours = chromatic_number_func(adj_list)
        t_end = time.time()
        elapsed_time = t_end - t_start

        if elapsed_time < 1e-3:
            n_runs = 1000
            t_start = time.time()
            for _ in range(n_runs):
                n_configurations = 0
                n_comparisons = 0
                chromatic_number, best_colours = chromatic_number_func(adj_list)
            t_end = time.time()
            elapsed_time = (t_end - t_start) / n_runs
            print(f' DONE in {1000*elapsed_time:.3f} ms')
        else:
            print(f' DONE in {elapsed_time:.3f} s')

        empirical_analysis[file] = {'n_configurations': n_configurations,
                                    'n_comparisons': n_comparisons,
                                    'e_time': elapsed_time}

        with open(f'{results_path}/{file}', 'wb') as f:
            pickle.dump(adj_list, f)
            pickle.dump(coords, f)
            pickle.dump(chromatic_number, f)
            pickle.dump(best_colours, f)

    save_complexity_data()    
except KeyboardInterrupt:
    print(' CANCELLED')
    save_complexity_data()
