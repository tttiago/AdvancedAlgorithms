"""Counter functions: deterministic counter and count-min sketch."""

import array
from collections import Counter
import hashlib
import math


def det_count(file):
    """Count words using a deterministic counter.
    Return a counter with all the words and their absolute frequency."""

    with open(file, 'r') as f:
        words = f.read().split()
    counter = Counter(words)

    return counter


def cm_sketch(file, k=3e2, d=5, m=None):
    """Count words using a CM Sketch counter."""

    # List of the words which appeared at least m/k times.
    top_words = []

    with open(file, 'r') as f:
        words = f.read().split()
    thresh = len(words) / k

    if m:
        cm_sketch = CountMinSketch(m=m, d=d)

    else:
        # Initialise with the recommended epsilon if m is not provided.
        epsilon = 1 / (2* k)
        cm_sketch = CountMinSketch(epsilon=epsilon, d=d)
    
    params = {'m': cm_sketch.m, 'd': d}

    # Update the CM Sketch with all the words and save the most frequent.
    for word in words:
        cm_sketch.update(word)
        if word in top_words:
            continue
        if cm_sketch.query(word) >= thresh:
            top_words.append(word)

    # Save also the frequency estimations for the evaluation of the method.
    res = {word: cm_sketch.query(word) for word in top_words}
    counter = Counter(res)

    return counter, params


# COUNT-MIN SKETCH:
# Rafael Carrascosa's Count-Min Sketch pure python implementation
# Adapted from https://github.com/rafacarrascosa/countminsketch
# Using delta and epsilon as suggested in https://github.com/AWNystrom/CountMinSketch
# J. Madeira --- December 2018
# Adapted by Tiago Fernandes

class CountMinSketch(object):
    """
    A class for counting hashable items using the Count-min Sketch strategy.

    The Count-min Sketch is a randomized data structure that uses a constant
    amount of memory and has constant insertion and lookup times at the cost
    of an arbitrarily small overestimation of the counts.

    It has two parameters:
     - `m` the size of the hash tables, larger implies smaller overestimation
     - `d` the number of hash tables, larger implies lower probability of
           overestimation.
    """

    def __init__(self, m=None, d=None, delta=None, epsilon=None):
        """
        Parameters
        ----------
        m : the number of columns in the count matrix
        d : the number of rows in the count matrix
        delta : (not applicable if m and d are supplied) the probability of 
                query error
        epsilon : (not applicable if w and d are supplied) the query error 
                   factor
        """

        if m:
            self.m = m
        elif epsilon:
            self.m = math.ceil(2.0 / epsilon)
        self.d = d

        self.tables = []
        for _ in range(self.d):
            table = array.array("l", (0 for _ in range(self.m)))   # signed long integers
            self.tables.append(table)

    def _hash(self, x):
        md5 = hashlib.md5(str(hash(x)).encode("utf-8"))     # handle bytes, not strings
        for i in range(self.d):
            md5.update(str(i).encode("utf-8"))              # concatenate
            yield int(md5.hexdigest(), 16) % self.m

    def update(self, x, value=1):
        """
        Count element `x` as if had appeared `value` times.
        Note : sketch.update(x) counts `x` as occurring once.
        """
        for table, i in zip(self.tables, self._hash(x)):
            table[i] += value

    def query(self, x):
        """
        Return an estimation of the amount of times `x` has occurred.
        """
        return min(table[i] for table, i in zip(self.tables, self._hash(x)))