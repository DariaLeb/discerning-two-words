import pickle
from pathlib import Path

"""
This module analyzes differences between consequent elements of the examples subsets for given `n`.
It sorts the first and second half of the examples separately (with sums n and n + 1 respectively).
"""


def sort_examples(examples):

    # sort examples according to the appearance of elements in them.
    # I.e. {1, 4, 5} -> 10011, those string are sorted lexicographically.

    max_i = examples[0][0][-1] // 2  # last element of the first subset
    return sorted(examples, key=lambda x: [i in x[0] for i in range(1, max_i + 1)])


def main():

    n = 58

    with Path('../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    result = {n: result[n]}

    for n, (m, examples, _) in result.items():

        print(n, m)
        k = len(examples)
        examples = sort_examples(examples[:k // 2]) + sort_examples(examples[k // 2:])

        for ii, (example, m_, i, counts) in enumerate(examples):

            example = example[:len(example) // 2]
            differences = tuple(next_ - prev for prev, next_ in zip(example[:-1], example[1:]))

            print('...' * 5)
            print(example)
            print(differences)

        print('---' * 3)


if __name__ == '__main__':
    main()
