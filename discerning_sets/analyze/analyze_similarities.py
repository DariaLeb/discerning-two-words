import pickle
from collections import defaultdict
from itertools import product
from pathlib import Path

"""
This module analyzes similar occurrences for pair of elements for given n.
We count example where both or none of X and Y are present and 
divide it by number of all examples.
"""


def get_similarities(n, examples):

    pair_occurrences = defaultdict(int)
    pair_disoccurrences = defaultdict(int)
    elements = set()

    for example, *_ in examples:
        example = example[:(len(example) // 2)]
        elements.update(example)

        for i in range(1, n // 2 + 1):
            for j in range(i + 1, n // 2 + 1):
                if i in example and j in example:
                    pair_occurrences[i, j] += 1
                elif i not in example and j not in example:
                    pair_disoccurrences[i, j] += 1

    similarities = {
        (x, y): (pair_occurrences[x, y] + pair_disoccurrences[x, y]) / len(examples)
        for x, y in product(elements, elements) if x < y
    }

    print(f'Different similarities values: {sorted(set(similarities.values()))}')

    unsimilar = [(x, y) for (x, y), value in similarities.items() if value == 0]
    similar = [(x, y) for (x, y), value in similarities.items() if value == 1]

    return similar, unsimilar


def main():

    with Path(f'../data/results_proper_62.pickle').open('rb') as f:
        result = pickle.load(f)

    for n, (_, examples, _) in result.items():

        if len(examples) <= 8:
            continue

        for examples_ in (examples[:len(examples) // 2], examples[len(examples) // 2:]):
            similar, unsimilar = get_similarities(n, examples_)
            print(n, f'{len(examples_)} examples processed')

            print(f'Unsimilar values (similarity = 0) - {len(unsimilar)} pairs:')
            for x, y in unsimilar:
                print(x, y)

            print(f'Similar values (similarity = 1): - {len(similar)} pairs:')
            for x, y in similar:
                print(x, y)

            print('---' * 30)


if __name__ == '__main__':
    main()
