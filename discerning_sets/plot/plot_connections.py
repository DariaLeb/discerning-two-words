import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from plot_occurrences import count_occurrences

"""
This module plots a connection graph for pairs of elements for one or multiple given ns.
We count critical sets where X and Y occurs simultaneously and 
divide it by number of sets where at least one of them occurs.

We plot all numbers except for 1 (it occurs everywhere). 
We can also introduce a threshold to plot only extreme cases as otherwise graph tends to be cluttered.
"""


def main():

    with Path(f'../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    n = 52

    result = {n: result[n]}

    pair_occurrences = defaultdict(int)
    elements = set()

    for n, (_, examples, _) in result.items():

        for example, *_ in examples:
            example = example[:(len(example) // 2)]
            elements.update(example)

            for i, x in enumerate(example):
                for y in example[i + 1:]:
                    pair_occurrences[x, y] += 1

    single_occurrences = count_occurrences(result)

    for x, y in pair_occurrences:
        pair_occurrences[x, y] /= (single_occurrences[x] + single_occurrences[y] - pair_occurrences[x, y])

    print(pair_occurrences)

    # apply threshold?
    values = np.array(list(pair_occurrences.values()))
    quantile = 18
    bound = np.quantile(values, quantile / 100)
    print(bound, max(values))

    # create graph
    edges_list = []
    for (x, y), val in pair_occurrences.items():
        if x == 1:
            continue
        edges_list.append((x, y, val))

    weights = list(zip(*edges_list))[2]
    print(max(weights))

    G = nx.Graph()
    G.add_weighted_edges_from(edges_list)

    # plot
    pos = nx.circular_layout(sorted(G.nodes()))

    nx.draw_networkx_nodes(G, pos, node_size=200)
    nx.draw_networkx_labels(G, pos, font_size=10)

    edges = nx.draw_networkx_edges(G, pos, edge_color=weights)
    plt.colorbar(edges)

    plt.axis('off')

    # plt.title(f'Threshold {bound:.2f}')
    # plt.savefig(f'images/connections_n_{n}.pdf')
    plt.show()


if __name__ == '__main__':
    main()
