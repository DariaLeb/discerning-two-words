import pickle
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
This module also visualize examples as a matrix, only unique canonical examples with sums n or n + 1 are considered.
However, we sort the rows of the matrix (elements) according to the patterns they have - 
we realize, that first 4 cells of each row forms a pattern which is then copied as-is or inverted. 
We distinguish rows by order of copies and inversions they have. Groups are separated by horizontal lines.
Vertical lines separating each 4 cells are added for clarity.
"""


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
        # if len(examples) > 2:
        #     continue

        print(n, m)

        matrix = np.zeros((len(examples), n // 2), dtype=int)
        for ii, (example, m_, i, counts) in enumerate(examples):
            for x in example[:len(example) // 2]:
                matrix[ii, x - 1] = 1

        n_ex = len(examples)
        matrix = np.vstack((sort_matrix(matrix[:n_ex // 2, :]), sort_matrix(matrix[n_ex // 2:, :])))
        # indicies = [idx for idx in [1, 8, 10, 12, 17, 26] if idx < matrix.shape[1]]
        # matrix = matrix[:, indicies]

        for matrix in [matrix[:n_ex // 2, :], matrix[n_ex // 2:, :]]:
            matrix = matrix.T
            print(matrix)

            indicies = range(0, len(matrix) + 1)
            patterns = []
            for i in range(len(matrix)):
                pattern = []
                for j in range(4, matrix.shape[1], 4):
                    pattern.append((matrix[i, j:j + 4] == matrix[i, j - 4:j]).all())
                patterns.append(pattern)

            indicies = [x for _, x in sorted(zip(patterns, indicies))]
            matrix = matrix[indicies, :]
            labels = np.array(indicies) + 1

            plt.figure()
            sns.heatmap(matrix, cbar=False, square=True, xticklabels=np.sum(matrix, axis=0), yticklabels=labels)
            plt.title(n)
            plt.xticks(rotation=90, fontsize=6)
            plt.yticks(fontsize=6)
            ax = plt.gca()
            ax.vlines(range(4, matrix.shape[1], 4), *ax.get_ylim())

            patterns = sorted(patterns)
            idxs = [i + 1 for i in range(len(matrix) - 1) if patterns[i] != patterns[i + 1]]
            ax.hlines(idxs, *ax.get_xlim())
            plt.tight_layout()
            break

    plt.show()


if __name__ == '__main__':
    main()
