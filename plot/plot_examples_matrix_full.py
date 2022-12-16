import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
This module plots example matrix similar to the one in `plot_examples_matrix.py`,
but it takes into account all canonical examples. Examples are divided into groups, separated by vertical lines.
First, ale example which do not satisfy the sum requirement are plotted. 
Every other group consists of examples with the same sum. 
Last two groups are unique examples for n, second to last - for n - 2 and so on.
"""


def sort_matrix(matrix):

    matrix = [''.join(map(str, x)) for x in matrix]
    matrix = np.array([list(map(int, x)) for x in sorted(matrix)])

    return matrix


def main():

    with Path(f'../data/results_34.pickle').open('rb') as f:
        result = pickle.load(f)

    result = {n: result[n] for n in [28]}

    for n, (m, examples, _) in result.items():

        print(n, m, len(examples))
        canonical = []
        canonical_diff = set()

        idxs = defaultdict(list)
        for ex, _, _, _ in examples:
            diff = tuple(next_ - prev for prev, next_ in zip(ex[:-1], ex[1:]))
            if diff not in canonical_diff:
                canonical.append(ex)
                canonical_diff.add(diff)

                ss = {ex[len(ex) - i - 1] + ex[i] for i in range(len(ex) // 2)}
                if len(ss) == 1:
                    idxs[ex[len(ex) - 1] + ex[0]].append(len(canonical) - 1)
                else:
                    idxs[-1].append(len(canonical) - 1)

        matrix = np.zeros((len(canonical), n), dtype=int)
        for ii, example in enumerate(canonical):
            for x in example:
                matrix[ii, x - 1] = 1

        matricies = []
        for ss, idxs_ in sorted(idxs.items()):
            matricies.append(sort_matrix(matrix[idxs_, :]))

        matrix = np.vstack(matricies)
        # indicies = [idx for idx in [1, 8, 10, 12, 17, 26] if idx < matrix.shape[1]]
        # matrix = matrix[:, indicies]

        matrix = matrix.T
        print(matrix)

        labels = range(1, len(matrix) + 1)
        groups = np.cumsum([len(idxs_) for ss, idxs_ in sorted(idxs.items())])

        plt.figure()
        sns.heatmap(matrix, cbar=False, square=True, xticklabels=np.sum(matrix, axis=0), yticklabels=labels)
        plt.title(n)
        plt.xticks(rotation=90, fontsize=6)
        plt.yticks(fontsize=6)
        ax = plt.gca()
        ax.vlines(groups, *ax.get_ylim())

        plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    main()
