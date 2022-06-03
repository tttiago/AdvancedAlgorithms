"""Generate all the plots used in the written report for the
empirical analysis."""


import matplotlib.pyplot as plt
import numpy as np
import pickle
from scipy.optimize import curve_fit


def organize_results_exhaustive(results):
    n_nodes = {'p25': [], 'p50': [], 'p75': []}
    e_time = {'p25': [], 'p50': [], 'p75': []}
    n_configs = {'p25': [], 'p50': [], 'p75': []}
    n_compars = {'p25': [], 'p50': [], 'p75': []}

    for file in results:
        if 'p25' in file:
            p_str = 'p25'
        elif 'p50' in file:
            p_str = 'p50'
        elif 'p75' in file:
            p_str = 'p75'
        n_nodes[p_str].append(int(file[:2]))
        e_time[p_str].append(results[file]['e_time'])
        n_configs[p_str].append(results[file]['n_configurations'])
        n_compars[p_str].append(results[file]['n_comparisons'])

    return n_nodes, e_time, n_configs, n_compars
    

def plot_analysis_v2():
    results_file = 'exhaustive_analysis_v2'
    alg_name = 'exhaustive_v2'

    with open(f'./results/{results_file}.pkl', 'rb') as f:
        results = pickle.load(f)
    n_nodes, e_time, n_configs, n_compars = organize_results_exhaustive(results)

    _, ax = plt.subplots()
    x_teo = np.linspace(min(n_nodes['p50']), max(n_nodes['p50']))
    y_teo = x_teo ** (x_teo - 1)
    ax.plot(x_teo, y_teo, '--', c='grey', linewidth=1, label='theoretical value')
    for p_str in ('p25', 'p50', 'p75'):
        ax.scatter(n_nodes[p_str], n_configs[p_str], label=f'p = 0.{p_str[-2:]}')
    ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    ax.set_title(f'Algorithm: {alg_name}')
    ax.set_ylabel('Number of configurations tested')
    ax.legend()
    plt.show(block=False)
    plt.savefig(f'./results/{alg_name}_n_configs.png')

    _, ax = plt.subplots()
    x_teo = np.linspace(min(n_nodes['p50']), max(n_nodes['p50']))
    y_min = x_teo ** (x_teo - 1)
    y_max = x_teo ** (x_teo + 1)
    ax.plot(x_teo, y_min, '--', c='green', linewidth=1, label='theoretical best case')
    ax.plot(x_teo, y_max, '--', c='red', linewidth=1, label='theoretical worst case')
    for p_str in ('p25', 'p50', 'p75'):
        ax.scatter(n_nodes[p_str], n_compars[p_str], label=f'p = 0.{p_str[-2:]}')
    ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    #ax.set_title(f'Algorithm: {alg_name}')
    ax.set_ylabel('Number of comparisons performed')
    ax.legend()
    plt.show(block=False)
    plt.savefig(f'./results/{alg_name}_n_compars.png')

    _, ax = plt.subplots()
    for p_str in ('p25', 'p50', 'p75'):
        ax.scatter(n_nodes[p_str], e_time[p_str], label=f'p = 0.{p_str[-2:]}')
    ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    #ax.set_title(f'Algorithm: {alg_name}')
    ax.set_ylabel('Execution time (s)')
    ax.legend()
    plt.show(block=False)
    plt.savefig(f'./results/{alg_name}_e_time.png')


    def objective(x, a, b): return a * x ** (x+b)
    _, ax = plt.subplots()
    x = np.array(n_nodes['p50'])
    y = np.array(e_time['p50'])
    popt, _ = curve_fit(objective, x, y)
    x_reg = np.linspace(min(x), max(x))
    x_pred = np.arange(max(x), max(x)+5)
    y_reg = objective(x, *popt)
    residuals = y - y_reg
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    reg_str = ('Regression Curve: t = ax^(x+b)' + 
            f'\na = {popt[0]:.2e}' + f'\nb = {popt[1]:.2f}')
    plt.scatter(x, y, label='empirical data')
    plt.plot(x_reg, objective(x_reg, *popt), c='grey', label='regression')
    plt.plot(x_pred, objective(x_pred, *popt), '--', c='grey', linewidth=0.5, label='prediction')
    ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    ax.set_title(f'Algorithm: {alg_name}, p = 0.50')
    ax.set_ylabel('Execution time (s)')
    ax.set_xticks(range(min(x), max(x)+5))
    ax.text(2, 0.1, reg_str)
    ax.legend()
    plt.savefig(f'./results/{alg_name}_e_time_regression.png')
    plt.show()


def plot_analysis_v3():
    results_file = 'exhaustive_analysis_v3'
    alg_name = 'exhaustive_v3'

    with open(f'./results/{results_file}.pkl', 'rb') as f:
        results = pickle.load(f)
    n_nodes, e_time, n_configs, n_compars = organize_results_exhaustive(results)

    _, ax = plt.subplots()
    x_teo = np.linspace(min(n_nodes['p50']), max(n_nodes['p50']))
    y_teo = x_teo ** (x_teo - 1)
    ax.plot(x_teo, y_teo, '--', c='grey', linewidth=1, label='max configurations of v2')
    for p_str in ('p25', 'p50', 'p75'):
        ax.scatter(n_nodes[p_str], n_configs[p_str], label=f'p = 0.{p_str[-2:]}')
    ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    ax.set_title(f'Algorithm: {alg_name}')
    ax.set_ylabel('Number of configurations tested')
    ax.set_xticks(range(min(n_nodes['p50']), max(n_nodes['p50'])+1))
    ax.legend()
    plt.show(block=False)
    plt.savefig(f'./results/{alg_name}_n_configs.png')

    _, ax = plt.subplots()
    x_teo = np.linspace(min(n_nodes['p50']), max(n_nodes['p50']))
    y_min = 0.5 * x_teo ** 2
    y_max = x_teo ** (x_teo + 1)
    ax.plot(x_teo, y_min, '--', c='green', linewidth=1, label='theoretical best case')
    ax.plot(x_teo, y_max, '--', c='red', linewidth=1, label='theoretical worst case')
    for p_str in ('p25', 'p50', 'p75'):
        ax.scatter(n_nodes[p_str], n_compars[p_str], label=f'p = 0.{p_str[-2:]}')
    ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    #ax.set_title(f'Algorithm: {alg_name}')
    ax.set_ylabel('Number of comparisons performed')
    ax.set_xticks(range(min(n_nodes['p50']), max(n_nodes['p50'])+1))
    ax.legend()
    plt.show(block=False)
    plt.savefig(f'./results/{alg_name}_n_compars.png')

    _, ax = plt.subplots()
    for p_str in ('p25', 'p50', 'p75'):
        ax.scatter(n_nodes[p_str], e_time[p_str], label=f'p = 0.{p_str[-2:]}')
    ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    #ax.set_title(f'Algorithm: {alg_name}')
    ax.set_ylabel('Execution time (s)')
    ax.set_xticks(range(min(n_nodes['p50']), max(n_nodes['p50'])+1))
    ax.legend()
    plt.show(block=False)
    plt.savefig(f'./results/{alg_name}_e_time.png')

    
    _, ax = plt.subplots()
    x = np.array(n_nodes['p50'])
    y = np.array(e_time['p50'])
    poly_coeffs = np.polyfit(x, np.log(y), 2)
    poly_f = np.poly1d(poly_coeffs)
    x_reg = np.linspace(min(x), max(x))
    x_pred = np.arange(max(x), max(x)+5)
    reg_str = ('Regression Curve: log(t) = ax^2+bx+c' + 
            f'\na = {poly_coeffs[0]:.2f}' + f'\nb = {poly_coeffs[1]:.2f}' 
            f'\nc = {poly_coeffs[2]:.2f}')
    plt.scatter(x, y, label='empirical data')
    plt.plot(x_reg, np.exp(poly_f(x_reg)), c='grey', label='regression')
    plt.plot(x_pred, np.exp(poly_f(x_pred)), '--', c='grey', linewidth=0.5, label='prediction')
    ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    ax.set_title(f'Algorithm: {alg_name}, p = 0.50')
    ax.set_ylabel('Execution time (s)')
    ax.set_xticks(range(min(x), max(x)+5))
    ax.text(2, 10, reg_str)
    ax.legend()
    plt.savefig(f'./results/{alg_name}_e_time_regression.png')
    plt.show()


def organize_results_greedy(results):
    n_nodes = {'p25': [], 'p50': [], 'p75': []}
    e_time = {'p25': [], 'p50': [], 'p75': []}
    n_checks = {'p25': [], 'p50': [], 'p75': []}

    for file in results:
        if 'p25' in file:
            p_str = 'p25'
        elif 'p50' in file:
            p_str = 'p50'
        elif 'p75' in file:
            p_str = 'p75'
        n_nodes[p_str].append(int(file[:2]))
        e_time[p_str].append(results[file]['e_time'])
        n_checks[p_str].append(results[file]['n_membership_checks'])

    return n_nodes, e_time, n_checks


def plot_analysis_greedy():
    results_file = 'greedy_analysis'
    alg_name = 'greedy_heuristic'

    with open(f'./results/{results_file}.pkl', 'rb') as f:
        results = pickle.load(f)
    n_nodes, e_time, n_checks = organize_results_greedy(results)

    _, ax = plt.subplots()
    x_teo = np.linspace(min(n_nodes['p50']), max(n_nodes['p50']))
    y_min = x_teo * np.log(x_teo)
    y_max = x_teo ** 2
    ax.plot(x_teo, y_min, '--', c='green', linewidth=1, label='theoretical best case')
    ax.plot(x_teo, y_max, '--', c='red', linewidth=1, label='theoretical worst case')
    for p_str in ('p25', 'p50', 'p75'):
        ax.scatter(n_nodes[p_str], n_checks[p_str], label=f'p = 0.{p_str[-2:]}')
    #ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    ax.set_title(f'Algorithm: {alg_name}')
    ax.set_ylabel('Number of membership checks performed')
    ax.set_xticks(range(min(n_nodes['p50']), max(n_nodes['p50'])+1))
    ax.legend()
    plt.show(block=False)
    plt.savefig(f'./results/{alg_name}_n_checks.png')

    _, ax = plt.subplots()
    for p_str in ('p25', 'p50', 'p75'):
        ax.scatter(n_nodes[p_str], 1000*np.array(e_time[p_str]), 
        label=f'p = 0.{p_str[-2:]}')
    #ax.set_yscale('log')
    ax.set_xlabel('Number of nodes')
    #ax.set_title(f'Algorithm: {alg_name}')
    ax.set_ylabel('Execution time (ms)')
    ax.set_xticks(range(min(n_nodes['p50']), max(n_nodes['p50'])+1))
    ax.legend()
    plt.savefig(f'./results/{alg_name}_e_time.png')
    plt.show(block=False)

    _, ax = plt.subplots()
    x = np.array(n_nodes['p50'])
    y = np.array(e_time['p50'])
    poly_coeffs = np.polyfit(x, y, 2)
    poly_f = np.poly1d(poly_coeffs)
    x_reg = np.linspace(min(x), max(x))
    x_pred = np.arange(max(x), max(x)+5)
    reg_str = ('Regression Curve: log(t) = ax^2+bx+c' + 
            f'\na = {poly_coeffs[0]:.2e}' + f'\nb = {poly_coeffs[1]:.2e}' 
            f'\nc = {poly_coeffs[2]:.2e}')
    plt.scatter(x, y*1000, label='empirical data')
    plt.plot(x_reg, poly_f(x_reg)*1000, c='grey', label='regression')
    plt.plot(x_pred, poly_f(x_pred)*1000, '--', c='grey', linewidth=0.5, label='prediction')
    ax.set_xlabel('Number of nodes')
    ax.set_title(f'Algorithm: {alg_name}, p = 0.50')
    ax.set_ylabel('Execution time (ms)')
    ax.set_xticks(range(min(x), max(x)+5))
    ax.text(2, 0.015, reg_str)
    ax.legend()
    plt.savefig(f'./results/{alg_name}_e_time_regression.png')
    plt.show()

#plot_analysis_v2()
#plot_analysis_v3()
plot_analysis_greedy()