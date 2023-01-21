import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

"""
This module plots a bar chart with relative occurrences of each element in example subsets.
For each number X, we count a number of subsets where is can possibly appear in the first half
and use it as a denominator for actual occurrences. 
We then subtract 0.5 from each number and plot the results for all xs except for 1.
"""


def possible_appearances(result, xs):

    # given x can appear in all examples for n < 2x and in half of examples for n = 2x

    example_count = {n: len(examples) // 2 for n, (m, examples, _) in result.items()}
    example_cumsum = np.cumsum(list(example_count.values())[::-1])
    example_cumsum = {n: val for n, val in zip(example_count, example_cumsum[::-1])}

    min_, max_ = min(result), max(result)

    possible_appearance = {}
    for x in xs:
        if x <= min_ // 2 - 1:
            possible_appearance[x] = example_cumsum[min_] * 2
        elif x >= max_ // 2:
            possible_appearance[x] = example_cumsum[max_]
        else:
            possible_appearance[x] = example_cumsum[x * 2 + 2] * 2 + example_count[x * 2]

    return possible_appearance


def count_occurrences(result):

    occurrences = defaultdict(int)

    for n, (m, examples, _) in result.items():

        for ii, (example, m_, i, counts) in enumerate(examples):
            for x in example[:(len(example) // 2)]:
                occurrences[x] += 1

    return occurrences


def main():

    with Path(f'../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    occurrences = count_occurrences(result)
    possible_appearance = possible_appearances(result, list(occurrences))

    # print(sorted(occurrences.items())[1:])
    # print(sorted(possible_appearance.items())[1:])

    occurrences = {x: y / possible_appearance[x] for x, y in occurrences.items()}
    occurrences = sorted(occurrences.items())
    x, y = zip(*occurrences)
    y = np.array(y) - 0.5

    plt.figure()
    plt.bar(x[1:], y[1:])

    # plt.savefig('images/occurrences.pdf')
    plt.show()


if __name__ == '__main__':
    main()
