import pickle
from pathlib import Path

from analyze.analyze_similarities import get_similarities

"""
This module analyzes constraints resulted from (un)similarities - we try to answer 
the question if those constraints may help us significantly decrease computational 
complexity of finding examples if we know them (the constraints) in advance.

For now, the most powerful constraints are for n = 54 (with them, we analyze 2^18 times less subsets).
"""


def get_constraints(similar, unsimilar):

    groups = []
    constraints = {}

    for x, y in similar:
        for constr in groups:
            if x in constr or y in constr:
                constr.add(x)
                constr.add(y)
                break
        else:
            groups.append({x, y})

    groups = [tuple(sorted(group)) for group in groups]

    for group in groups:
        constraints[group] = tuple()

    for x, y in unsimilar:
        for constr in groups:
            if x in constr:
                assert y not in constr
                x_group = constr
                break
        else:
            x_group = (x, )
            groups.append(x_group)

        for constr in groups:
            if y in constr:
                assert x not in constr
                y_group = constr
                break
        else:
            y_group = (y, )
            groups.append(y_group)

        constraints[x_group] = y_group
        constraints[y_group] = x_group

    return constraints


def main():

    with Path(f'../data/results_unique_62.pickle').open('rb') as f:
        result = pickle.load(f)

    for n, (_, examples, _) in result.items():

        if len(examples) <= 8:
            continue

        for i, examples_ in enumerate((examples[:len(examples) // 2], examples[len(examples) // 2:])):
            similar, unsimilar = get_similarities(n, examples_)
            constraints = get_constraints(similar, unsimilar)

            print(f'{n}:{i} with {len(examples_)} examples')

            constraints = {
                g1: constraints[g1] for g1 in sorted(constraints)
                if not constraints[g1] or g1[0] < constraints[g1][0]
            }
            print(' '.join(map(str, constraints.keys())))
            print(' '.join(map(str, constraints.values())))

            print()

            max_x = n // 2 if i else n // 2 - 1

            combinations = max_x - 1

            for g1, g2 in constraints.items():
                combinations -= len(g1) + len(g2) - 1

            print(
                f'2^{max_x - 1} combinations in total, '
                f'2^{combinations} with constraints '
                f'(2^{(max_x - 1) - combinations} times less)'
            )
            print('---' * 30)


if __name__ == '__main__':
    main()
