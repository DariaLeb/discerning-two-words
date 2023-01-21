import pickle
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from discerning_sets.plot.plot_examples_matrix import create_matrix

"""
Analyze number of intervals of consecutive 1s and 0s in examples matrix, 
plot min and max number of them for given n.

We can see that both borders grow, but at the first sight they look pretty random.
"""


def main():

    with Path(f'../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    mins, maxs, ns = [], [], []

    for n, (m, examples, _) in result.items():

        print(n, m)

        matrix = create_matrix(n, examples)

        n_intervals = np.diff(matrix, axis=0).astype(bool).sum(axis=0) + 1  # number of intervals
        print(f'{n}: {min(n_intervals)}-{max(n_intervals)}, {n_intervals}')

        ns.append(n)
        mins.append(min(n_intervals))
        maxs.append(max(n_intervals))

    plt.figure()
    plt.plot(ns, mins, '.-', label='min number of intervals')
    plt.plot(ns, maxs, '.-', label='max number of intervals')

    plt.xlabel('n')

    plt.legend()
    plt.grid()

    # plt.savefig('images/number_unique.pdf')
    plt.show()


if __name__ == '__main__':
    main()
