import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

"""
This module visualize each example for given `n` as a plot with numbers of example's first half on Y axis.
Multiple `n` can be placed on one or different subplots.
"""


def plot_ax(ax, exs, color, label):

    for i, ex in enumerate(exs):
        ex = ex[1:(len(ex) // 2)]
        ax.plot(range(len(ex)), ex, 'o-', color=color, label=None if i else label, alpha=0.7)

    ax.legend()
    ax.grid()


if __name__ == '__main__':
    with Path('../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    minimal_n = [n for n, (m, examples, _) in result.items() if len(examples) == 2]
    colors = list(mcolors.TABLEAU_COLORS)

    fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True, sharey=True)

    for n, color, ax in zip(list(result)[3:7], colors, axs):
        exs = [x[0] for x in result[n][1]]
        plot_ax(ax, exs, color, n)

    plt.tight_layout()
    plt.savefig('images/examples_12_18.pdf')
    plt.show()
    #
    # plt.figure()
    #
    # for n, color in zip(minimal_n[:5], colors):
    #     exs = [x[0] for x in result[n][1]]
    #     plot_ax(plt.gca(), exs, color, n)
    #
    # plt.tight_layout()
    # plt.savefig('images/minimal_examples_small_1.pdf')
    # plt.show()
    #
    # plt.figure()
    #
    # for n, color in zip(minimal_n[5:], colors[5:]):
    #     exs = [x[0] for x in result[n][1]]
    #     plot_ax(plt.gca(), exs, color, n)
    #
    # plt.tight_layout()
    # plt.savefig('images/minimal_examples_bigger_1.pdf')
    # plt.show()
