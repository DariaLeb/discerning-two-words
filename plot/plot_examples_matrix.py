import pickle
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


"""
This module visualize examples for one or multiple given ns 
in a such way that every example is described by a binary number, 
e.g. {1, 4, 5, 7} -> 1001101, examples within their sum group are sorted 
and displayed as a matrix in a separate figure.
Visual guidelines in a form of vertical lines separating each 8 examples are added.
"""


def create_matrix(n, examples):

    matrix = np.zeros((len(examples), n // 2), dtype=int)
    for ii, (example, m_, i, counts) in enumerate(examples):
        for x in example[:len(example) // 2]:
            matrix[ii, x - 1] = 1

    n_ex = len(examples)
    matrix = np.vstack((sort_matrix(matrix[:n_ex // 2, :]), sort_matrix(matrix[n_ex // 2:, :])))

    return matrix.T


def sort_matrix(matrix):

    matrix = [''.join(map(str, x)) for x in matrix]
    matrix = np.array([list(map(int, x)) for x in sorted(matrix)])

    return matrix


def main():

    n = 58

    with Path(f'../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    result = {n: result[n]}

    for n, (m, examples, _) in result.items():

        print(n, m)

        matrix = create_matrix(n, examples)
        n_ex = len(examples)

        for matrix in [matrix[:, :n_ex // 2], matrix[:, n_ex // 2:]]:
            # print(matrix)

            xlabels = np.sum(matrix, axis=0)  # number of elements in the subset
            # xlabels = np.diff(matrix, axis=0).astype(bool).sum(axis=0) + 1  # number of intervals
            ylabels = range(1, len(matrix) + 1)

            plt.figure()
            sns.heatmap(matrix, cbar=False, square=True, xticklabels=xlabels, yticklabels=ylabels)
            plt.title(n)
            plt.xticks(rotation=90, fontsize=6)
            plt.yticks(fontsize=6)
            ax = plt.gca()
            ax.vlines(range(8, matrix.shape[1], 8), *ax.get_ylim())

            plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    main()
