"""Find the cases where the greedy heuristic returned a wrong solution and
calculate the average precision of the greedy algorithm."""

from functools import wraps
import numpy as np
import os
import pickle


exact_results = np.zeros((3, 13))
for file in sorted(os.listdir('./results/exhaustive_v3')):
    if file[-4:] != '.pkl':
        continue
    n_nodes = int(file[:2])
    if 'p25' in file:
        row = 0
    elif 'p50' in file:
        row = 1
    elif 'p75' in file:
        row = 2
    with open(f'./results/exhaustive_v3/{file}', 'rb') as f:
        _ = pickle.load(f)
        _ = pickle.load(f)
        chromatic_number = pickle.load(f)
    
    exact_results[row][n_nodes-2] = chromatic_number

greedy_results = np.zeros((3, 13))
for file in sorted(os.listdir('./results/greedy')):
    n_nodes = int(file[:2])
    if n_nodes > 14:
        break
    if file[-4:] != '.pkl':
        continue
    if 'p25' in file:
        row = 0
    elif 'p50' in file:
        row = 1
    elif 'p75' in file:
        row = 2
    with open(f'./results/greedy/{file}', 'rb') as f:
        _ = pickle.load(f)
        _ = pickle.load(f)
        chromatic_number = pickle.load(f)
    
    greedy_results[row][n_nodes-2] = chromatic_number
    

wrong = greedy_results-exact_results
print(wrong)
print(np.sum(wrong))
avg_precision = np.sum(exact_results)/np.sum(greedy_results)
print(avg_precision)