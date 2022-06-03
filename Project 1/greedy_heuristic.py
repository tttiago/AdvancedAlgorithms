"""Tests a greedy heuristic algorithm for finding the chromatic number
of the previously generated graphs.
Creates a pickle file containing the adjacency list, the coordinates of the nodes,
the chromatic number and an optimal colouring solution for each graph. 
Also saves the empirical complexity data from running the algorithm for all
the graphs in a pickle file."""

import os
import pickle
import time

########## GREEDY HEURISTIC ALGORITHM #############

def chromatic_number_greedy(adj_list):
    """Returns the chromatic number of a given undirected graph
    represented by its adjacency list and one possible colour combination
    to obtain it."""
    # Sorts the nodes in non-increasing order.
    # Colours each node with the smallest colour that has not been given to 
    # its neighbours. 

    global n_membership_checks

    n_nodes = len(adj_list)
    # Sort nodes in non-increasing order of degree:
    nodes = sorted(adj_list, key=lambda node: len(adj_list[node]), reverse=True)
    
    colours = {} 
                                
    for node in nodes:
        # Store the different colours of the current node's neighbours:
        neighbour_colours = set() 
        for neighbour in adj_list[node]:
            n_membership_checks += 1
            if neighbour in colours:
                neighbour_colours.add(colours[neighbour])
        
        for colour in range(n_nodes):
            n_membership_checks += 1
            if colour not in neighbour_colours:
                colours[node] = colour
                break
    
    chromatic_number = len(set(colours.values()))

    return chromatic_number, colours


########## GREEDY HEURISTIC TESTING #############

def save_complexity_data(data):
    with open(f'./results/greedy_analysis.pkl', 'wb') as f:
        pickle.dump(data, f)
    print('\nUploaded complexity results to file.')


def run_tests(func = chromatic_number_greedy, max_nodes = 20):
    global n_membership_checks
    try:
        empirical_analysis = {}
        chromatic_number_func = func
        results_path = f'./results/greedy'

        print('Running greedy heuristic for all graphs, using {func_name}.\n')

        if not os.path.exists(results_path):
            os.makedirs(results_path)

        for file in os.listdir('./graphs/'):
            if int(file[:2]) > max_nodes:
                break
            if file.endswith('.png'):
                continue

            print(f'Searching graph {file[:-3]}...', end='', flush=True)
            with open(f'./graphs/{file}', 'rb') as f:
                adj_list = pickle.load(f)
                coords = pickle.load(f)    
            
            t_start = time.time()
            n_runs = 10000
            for _ in range(n_runs):
                n_membership_checks = 0
                chromatic_number, best_colours = chromatic_number_func(adj_list)
            t_end = time.time()
            elapsed_time = (t_end - t_start) / n_runs

            print(f' DONE in {1000*elapsed_time:.3f} ms')

            empirical_analysis[file] = {'n_membership_checks': n_membership_checks,
                                        'e_time': elapsed_time}

            with open(f'{results_path}/{file}', 'wb') as f:
                pickle.dump(adj_list, f)
                pickle.dump(coords, f)
                pickle.dump(chromatic_number, f)
                pickle.dump(best_colours, f)

        save_complexity_data(empirical_analysis)
            
    except KeyboardInterrupt:
        print(' CANCELLED')
        save_complexity_data()

n_membership_checks = 0
run_tests()