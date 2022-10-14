from itertools import chain, combinations


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
    examples = []

    for s in even_subsets(n):

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

    for n in range(6, 32, 2):
        max_m, examples, c = analyze_n(n)

        print('---' * 3)
        print(f'for {n = } {c} subsets were processed')
        print(f'for {n = } max m is {max_m}')
        for s, m, i, counts in examples:
            print(f'{s = }, {m = }, {i = }, {counts = }')
        print()


if __name__ == '__main__':

    main()
