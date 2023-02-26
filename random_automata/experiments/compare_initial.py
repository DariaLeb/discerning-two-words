import pickle
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

"""
This script is used to compare different automata experiments with fixed or various initial states.
It loads experiments' data and create a figure with two subplots for each number of changes there with all tried automata.
"""


path_fixed = [
    Path('../data') / f'res_1000_4583.pickle',
    Path('../data') / f'res_shifted_1000_3429.pickle',
    Path('../data') / f'res_cycle_shifted_1000_4420.pickle',
]

path_choose = [Path('../data') / f'res_1000_4650_choose.pickle']

result_fixed = None

for path in path_fixed:
    with path.open('rb') as f:
        res = pickle.load(f)
        result_fixed = result_fixed or res
        assert result_fixed['settings'] == res['settings']
        for key in ['permutation', 'random', 'shifted_permutation', 'cycle_shifted_permutation']:
            if res.get(key):
                result_fixed[key] = res[key]

print(result_fixed)

result_choose = None

for path in path_fixed:
    with path.open('rb') as f:
        res = pickle.load(f)
        result_choose = result_choose or res
        assert result_choose['settings'] == res['settings']
        for key in ['permutation', 'random', 'increased_permutation', 'shifted_permutation']:
            if res.get(key):
                result_choose[key] = res[key]

print(result_choose)

settings = result_choose['settings']
m = settings['m']
n_words = settings['n_words']
n_tries = settings['n_tries']
n_ns = settings['n_ns']
n_changes = settings['n_changes']
log_space = settings['logspace']

if log_space:
    ns = np.geomspace(1, m, num=n_ns, dtype=int)
else:
    ns = np.linspace(1, m, num=n_ns, dtype=int)

ns = sorted(set(ns))

tries = {
    'log(n)': int(math.log(m)),
    r'$\sqrt{n}$': int(m ** (1 / 2)),
    r'$\frac{n}{3}$': m // 3,
    r'$\frac{n}{2}$': m // 3,
    'n': m,
}

keys_fixed = ['permutation', 'random', 'shifted_permutation', 'cycle_shifted_permutation']
titles_fixed = ['permutation', 'random', 'increased permutation', 'shifted permutation']
styles_fixed = ['-', '--', 'dashdot', 'dotted']

keys_choose = ['permutation', 'random', 'increased_permutation', 'shifted_permutation']
titles_choose = ['permutation', 'random', 'increased permutation', 'shifted permutation']
styles_choose = ['-', '--', 'dashdot', 'dotted']

rand_key = np.random.randint(10000)

for i, n_change in enumerate(n_changes):
    fig, ax = plt.subplots(1, 2, figsize=(24, 8))

    plt.sca(ax[0])
    for key, title, style in zip(keys_fixed, titles_fixed, styles_fixed):
        if key not in result_fixed:
            continue

        avg = result_fixed[key][i].sum(axis=1) / (n_tries * n_words)
        n_log = [math.log(n) for n in ns]
        plt.plot(n_log, avg, linestyle=style, color='tab:blue', marker='.', label=title)

    for name, border in tries.items():
        plt.axvline(math.log(border), color='k', linestyle=':')

    plt.axhline(1, color='k', linestyle=':')

    plt.xticks(
        [math.log(val) for val in tries.values()],
        list(tries),
    )
    plt.legend()
    plt.ylabel('Ratio of distinguished pairs')
    plt.xlabel('Size of automaton [log]')

    plt.sca(ax[1])

    for key, title, style in zip(keys_choose, titles_choose, styles_choose):
        if key not in result_choose:
            continue

        avg = result_choose[key][i].sum(axis=1) / (n_tries * n_words)
        n_log = [math.log(n) for n in ns]
        plt.plot(n_log, avg, linestyle=style, color='tab:orange', marker='.', label=title)

    for name, border in tries.items():
        plt.axvline(math.log(border), color='k', linestyle=':')

    plt.axhline(1, color='k', linestyle=':')

    plt.xticks(
        [math.log(val) for val in tries.values()],
        list(tries),
    )
    plt.legend()
    plt.ylabel('Ratio of distinguished pairs')
    plt.xlabel('Size of automaton [log]')

    plt.title(f'{m = }, changes = {n_change}, {n_words = }, {n_ns = }, {log_space = }')
    plt.tight_layout()
    plt.savefig(f'../images/compare_initial_m_{m}_{n_change}_{rand_key}.pdf')

plt.show()
