import math
import pickle
from pathlib import Path

import matplotlib.pyplot as plt


"""
This module is used to plot simple line charts with evolution of some variable for different ns.
It could be maximum m, number of examples, min/max sum etc.
"""

if __name__ == '__main__':

    with Path('../data/results_proper_62.pickle').open('rb') as f:
        result = pickle.load(f)

    ns = list(result)
    ms = [val[0] for val in result.values()]

    size = [int(math.log2(len(val[1]))) for val in result.values()]

    min_s = [min(len(ex[0]) for ex in val[1]) for val in result.values()]
    max_s = [max(len(ex[0]) for ex in val[1]) for val in result.values()]

    number_of_s = [len(val[1]) for val in result.values()]

    log = [math.log(n) for n in ns]
    sqrt = [math.sqrt(n) for n in ns]
    half = [n / 2 for n in ns]
    square = [n / 4 for n in ns]
    fives = [n / 5 for n in ns]
    sixs = [n / 6 for n in ns]

    plt.figure()
    # plt.plot(ns, ms, '.-', label='m')
    plt.plot(ns, size, '.-', label='log number of unique examples')
    # plt.plot(ns, min_s, label='min |s|')
    # plt.plot(ns, max_s, label='max |s|')
    # plt.plot(ns, log, label='log')
    # plt.plot(ns, sqrt, label='sqrt')
    # plt.plot(ns, square, label='n/4')
    # plt.plot(ns, fives, label='n/5')
    # plt.plot(ns, sixs, label='n/6')
    # plt.plot(ns, half, label='n/2')
    # plt.plot(ns, number_of_s, label='number of S')

    plt.xlabel('n')

    plt.legend()
    plt.grid()

    # plt.savefig('images/number_unique.pdf')
    plt.show()
