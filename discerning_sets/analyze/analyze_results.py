import pickle
from pathlib import Path

from analyze_differences import sort_examples

"""
This module is used to perform different analyses of the generated subsets according to current needs.
For now, it analyses canonical examples in all generated ones - how much of them satisfy the sum requirement.
"""


def check_subset(subset):

    s = subset[0] + subset[-1]
    t = True
    for i in range(len(subset) // 2):
        t = t and subset[i] + subset[-(i + 1)] == s

    return t


def main():

    with Path(f'../data/results_34.pickle').open('rb') as f:
        result = pickle.load(f)

    # result = {58: result[58]}

    for n, (m, examples, _) in result.items():

        # k = len(examples)
        # examples = sort_examples(examples[:k // 2]) + sort_examples(examples[k // 2:])

        print(n, m)

        examples = [ex for ex, m_, i, counts in examples if ex[0] == 1 and ex[-1] in [n, n - 1]]
        sum_examples = [ex for ex in examples if check_subset(ex)]

        print(
            f'Canonical examples = {len(examples)}, '
            f'satisfying = {len(sum_examples)}, '
            f'not = {len(examples) - len(sum_examples)}'
        )
        print('---' * 3)


if __name__ == '__main__':
    main()
