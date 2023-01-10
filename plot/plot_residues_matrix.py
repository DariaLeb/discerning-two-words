import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from plot.plot_examples_matrix import create_matrix

"""
This modules plots colorful example matrix, where to each number present in example we assign its residue group.
We can see that due to the sum requirement |R_s(m, i)| = |R_s'(m, i)| + |R_s'(m, (sum - i) % m)|, 
where `s'` is smaller half of `s` and `sum` is the sum in this subset. Thus, we unite residues `i` and `(sum - i) % m`
into one group and say that is should have even cardinality in s' or i == (sum - i) % m for each non-maximal `m`.
We plot those matrices for every m from 3 to maximal one and trying to find some pattern in them.
"""


def main():

    n = 58

    with Path(f'../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    m, examples, _ = result[n]

    matrix = create_matrix(n, examples)
    n_ex = matrix.shape[1]

    # full matrix
    # first = matrix[:, :n_ex // 2]
    # second = matrix[:, n_ex // 2:]
    #
    # first = np.vstack([first, first[:-1, :][::-1, :], np.zeros(n_ex // 2).reshape((1, -1))])
    # second = np.vstack([second, second[::-1, :]])
    # matrix = np.hstack([first, second])

    for i in range(3, m + 1):

        # find residue groups for each half of examples and assign colors to them
        residues_n = [j for j in range(i) if j <= (n - j) % i]
        colors_n = {res: j for j, res in enumerate(residues_n)}
        colors_n.update({j: colors_n[(n - j) % i] for j in range(i) if j > (n - j) % i})

        # offset = 1 to save color for no number (0)
        colors_n = {j: c + 1 for j, c in colors_n.items()}

        residues_n1 = [j for j in range(i) if j <= (n + 1 - j) % i]
        colors_n1 = {res: j for j, res in enumerate(residues_n1)}
        colors_n1.update({j: colors_n1[(n + 1 - j) % i] for j in range(i) if j > (n + 1 - j) % i})

        # offset = 1 (no number) + len(residues_n) (used colors) + 1 (separator)
        colors_n1 = {j: c + 2 + len(residues_n) for j, c in colors_n1.items()}

        residues = matrix.copy()
        for j in range(matrix.shape[0]):
            for k in range(matrix.shape[1]):
                if residues[j][k] == 1:
                    residue = (j + 1) % i
                    residues[j][k] = colors_n[residue] if k < n_ex // 2 else colors_n1[residue]

        # custom colormap - different color for each residue group, white for 0 (no number)
        # and as a separator between groups in colorbar
        n_colors = 1 + len(residues_n) + 1 + len(residues_n1)
        cmap = sns.color_palette('tab20', n_colors - 2)
        cmap = [(1, 1, 1)] + cmap[:len(residues_n)] + [(1, 1, 1)] + cmap[len(residues_n):]

        # custom labels representing groups of residues "i + (sum - i) % m"
        tick_labels = []
        for j in residues_n:
            tick_labels.append(f'{j}+{(n - j) % i}')
        for j in residues_n1:
            tick_labels.append(f'{j}+{(n + 1 - j) % i}')

        plt.figure()

        # heatmap
        ax = sns.heatmap(
            residues,
            cbar=True, cbar_kws={'ticks': range(n_colors), 'orientation': 'horizontal'},
            square=True, linewidths=1,
            xticklabels=False, yticklabels=range(1, len(matrix) + 1), cmap=cmap
        )

        # colorbar with custom labels at the center of each color bar (except for the first and separator)
        cbar = ax.collections[0].colorbar
        ticks = [
            (n_colors - 1) / (2 * n_colors) + (n_colors - 1) / n_colors * i
            for i in range(n_colors)
            if i not in [0, len(residues_n) + 1]
        ]
        cbar.ax.set_xticks(ticks=ticks, labels=tick_labels, fontsize=6)

        # title & y-labels
        plt.title(f'{n}: m={i}')
        plt.yticks(fontsize=6)

        plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    main()
