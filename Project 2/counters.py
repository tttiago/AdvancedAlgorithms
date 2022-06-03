"""Counter functions: deterministic, with fixed probability and
with decreasing probability."""

from math import sqrt
import random


ord_A = ord('A')
ord_Z = ord('Z')

def det_count(file):
    """Deterministic counter."""

    results = {chr(i): 0 for i in range(ord_A, ord_Z+1)}
    with open(file, 'r') as f:
        contents = f.read()
    for char in contents:
        results[char] += 1

    return results


def fix_prob_count(file, prob=1/16, n_counts=1_000):
    """Fixed probability counter."""

    results = {chr(i): [0]*n_counts for i in range(ord_A, ord_Z+1)}
    with open(file, 'r') as f:
        contents = f.read()
    
    for n_try in range(n_counts):
        for char in contents:
            if random.random() < prob:
                results[char][n_try] += 1

    return results


def dec_prob_count(file, denominator=sqrt(3), n_counts=1_000):
    """Decreasing probability counter."""
    
    dec_probs = [1/(denominator**k) for k in range(128)]

    results = {chr(i): [0]*n_counts for i in range(ord_A, ord_Z+1)}
    with open(file, 'r') as f:
        contents = f.read()
    
    for n_try in range(n_counts):
        for char in contents:
            k = results[char][n_try]
            if random.random() < dec_probs[k]:
                results[char][n_try] += 1

    return results


