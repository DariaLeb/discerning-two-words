import pickle
from collections import defaultdict
from itertools import product
from pathlib import Path

"""
This module analyze similar occurrences for pair of elements for given n.
We count example where both ore none of X and Y are present and 
divide it by number of all examples.
"""


def main():

    n = 58

    with Path(f'../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    _, examples, _ = result[n]

    for examples_ in (examples[:len(examples) // 2], examples[len(examples) // 2:]):
        pair_occurrences = defaultdict(int)
        pair_disoccurrences = defaultdict(int)
        elements = set()

        for example, *_ in examples_:
            example = example[:(len(example) // 2)]
            elements.update(example)

            for i in range(1, n // 2 + 1):
                for j in range(i + 1, n // 2 + 1):
                    if i in example and j in example:
                        pair_occurrences[i, j] += 1
                    elif i not in example and j not in example:
                        pair_disoccurrences[i, j] += 1

        similarities = {
            (x, y): (pair_occurrences[x, y] + pair_disoccurrences[x, y]) / len(examples_)
            for x, y in product(elements, elements)
            if pair_disoccurrences[x, y] or pair_occurrences[x, y]
        }

        print(similarities)
        print(set(similarities.values()))

        print('Similar values:')
        for (x, y), value in similarities.items():
            if value == 1:
                print(x, y)

        print('---' * 30)


if __name__ == '__main__':
    main()
