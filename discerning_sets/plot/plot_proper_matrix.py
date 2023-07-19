import pickle
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


"""
This module visualize proper sets for given `n`
in a such way that every set is described by a binary number, 
e.g. {1, 4, 5, 7} -> 1001101. Only elements up to n // 2 are considered, 
as the sets' binary representations are perfectly symmetrical.
Visual guidelines in a form of vertical lines separating each 4 examples are added.
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

    n = 58

    with Path(f'../data/results_proper_62.pickle').open('rb') as f:
        result = pickle.load(f)

    _, sets, _ = result[n]
    matrix = create_matrix(n, sets)

    plt.figure()
    sns.heatmap(matrix, cbar=False, square=True, yticklabels=range(1, len(matrix) + 1))
    plt.xticks([])

    # guidelines
    ax = plt.gca()
    ax.vlines(range(4, matrix.shape[1], 4), *ax.get_ylim())

    plt.tight_layout()

    plt.savefig(f'../images/proper_matrix_{n}.pdf')
    plt.show()


if __name__ == '__main__':
    main()
