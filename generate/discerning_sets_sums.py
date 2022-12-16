import pickle
from itertools import chain, combinations
from pathlib import Path

"""
This module generates canonical example subsets satisfying the sum requirement for even ns in the given interval.
Maximum computed number was n=62 (runs over a day on my laptop).

For this, it tests all subset of [n] with sum `s` constructed as 
{1} + randomly generated first half from [2..(s-1)/2] + compliment second half.

It is sufficient to test only sums `n` and `n + 1` for canonical subsets.

For each n, it stores generated examples in `data/results_unique_{n}.pickle` for reproducibility. 
Format of the pickle file is described in `discerning_sets.py`.
"""


def subsets(s):

    max_half = (s - 1) // 2

    for half_set in _subsets(max_half):
        yield (1, ) + half_set + tuple(s - x for x in half_set)[::-1] + (s - 1, )


def _subsets(n):

    s = list(range(2, n + 1))

    return chain.from_iterable(combinations(s, r) for r in range(1, n))


def residue_counts(s, m):

    counts = [0 for _ in range(m)]
    for el in s:
        counts[el % m] += 1

    return counts


def test_residues(counts):

    for i, c in enumerate(counts):
        if c % 2 == 1:
            return i


def analyze_n(n):

    max_m = 0
    c = 0
    examples = []

    for sum_ in [n, n + 1]:
        for s in subsets(sum_):

            c += 1
            for m in range(2, n):
                counts = residue_counts(s, m)
                i = test_residues(counts)

                if i is not None:
                    # print(f'{s=}: {m=}, {i=}, {counts=}')
                    if m == max_m:
                        examples.append((s, m, i, counts))
                    elif m > max_m:
                        max_m = m
                        examples = [(s, m, i, counts)]
                    break

            else:
                if max_m == n:
                    examples.append((s, None, None, None))
                elif n > max_m:
                    max_m = n
                    examples = [(s, None, None, None)]

    return max_m, examples, c


def main():

    result = {}

    for n in range(62, 100, 2):
        max_m, examples, c = analyze_n(n)
        result[n] = max_m, examples, c

        print('---' * 3)
        print(f'for {n = } max m is {max_m}, we have {len(examples)} examples')
        for s, m, i, counts in examples:
            print(f's = {[x for x in s[:len(s) // 2]]} | {[x for x in s[len(s) // 2:]]}')
        print()

        if n > 30:
            with Path(f'../data/results_unique_{n}.pickle').open('wb') as f:
                pickle.dump(result, f)


if __name__ == '__main__':

    main()
