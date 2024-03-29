import pickle
from itertools import chain, combinations
from pathlib import Path

"""
This module generates critical sets for ns in the given interval. 
For this, it tests all subset of [n] with even number of elements and founds ones with maximum `m`.
Maximum computed number was n=34 (runs over a day on my laptop).

For each n, it stores generated sets in `data/results_{n}.pickle` for reproducibility.
In pickle file, there is a dictionary, where for each n list of critical sets in the following format is stored:
n -> (max_m, examples, c), 
where `examples` is the list of examples and `c` is a number of processed subsets. 
Critical sets are stored in the following format:
[(s, m, i, counts)], 
where `s` is a set, `m` is m for this set, `i` is the residue where violation for given `m` occurs and 
`counts` is a list with number of elements in each residue class.
"""


def even_subsets(n):

    s = list(range(1, n + 1))

    return chain.from_iterable(combinations(s, r) for r in range(4, n, 2))


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
    sets = []

    for s in even_subsets(n):

        c += 1
        for m in range(2, n):
            counts = residue_counts(s, m)
            i = test_residues(counts)

            if i is not None:
                # print(f'{s=}: {m=}, {i=}, {counts=}')
                if m == max_m:
                    sets.append((s, m, i, counts))
                elif m > max_m:
                    max_m = m
                    sets = [(s, m, i, counts)]
                break

        else:
            if max_m == n:
                sets.append((s, None, None, None))
            elif n > max_m:
                max_m = n
                sets = [(s, None, None, None)]

    return max_m, sets, c


def main():

    result = {}

    for n in range(6, 40):
        max_m, sets, c = analyze_n(n)
        result[n] = max_m, sets, c

        print('---' * 3)
        print(f'for {n = } {c} subsets were processed')
        print(f'for {n = } max m is {max_m}')
        for s, m, i, counts in sets:
            print(f'{s = }, {m = }, {i = }, {counts = }')
        print()

        with Path(f'../data/results_{n}.pickle').open('wb') as f:
            pickle.dump(result, f)


if __name__ == '__main__':

    main()
