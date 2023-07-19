import pickle
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


"""
This module visualize proper matrices for given interval of ns combined together in one figure.
Smaller matrices are padded with zeros to preserve symmetry.
"""


def create_matrix(n, sets):

    matrix = np.zeros((len(sets), n // 2), dtype=int)
    for ii, (set_, m_, i, counts) in enumerate(sets):
        for x in set_[:len(set_) // 2]:
            matrix[ii, x - 1] = 1

    matrix = sort_matrix(matrix)

    return matrix.T


def sort_matrix(matrix):

    matrix = [''.join(map(str, x)) for x in matrix]
    matrix = np.array([list(map(int, x)) for x in sorted(matrix)])

    return matrix


def main():

    n_from = 33
    n_to = 42

    ns = range(n_from, n_to + 1)

    with Path(f'../data/results_proper_62.pickle').open('rb') as f:
        result = pickle.load(f)

    matrices = []
    sizes = []

    n_rows = n_to // 2

    for n in ns:
        _, sets, _ = result[n]

        matrix = create_matrix(n, sets)
        matrix = np.vstack((matrix, np.zeros((n_rows - matrix.shape[0], matrix.shape[1]))))
        matrices.append(matrix)

        sizes.append(matrix.shape[1])

    matrix = np.hstack(matrices)

    borders = np.cumsum(sizes)
    ticks = borders - np.array(sizes) / 2

    plt.figure(figsize=(10, 6.6))
    sns.heatmap(matrix, cbar=False, square=True, yticklabels=range(1, len(matrix) + 1))

    plt.xticks(ticks, ns, rotation=0)

    # guidelines
    ax = plt.gca()
    ax.vlines(borders[:-1], *ax.get_ylim())

    plt.tight_layout()

    plt.savefig(f'../images/proper_matrix_{n_from}_{n_to}.pdf')
    plt.show()


if __name__ == '__main__':
    main()
