import pickle
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

"""
This script is used to compare different automata from multiple symbols experiments in one figure.
It loads experiments' data and create a figure for each number of changes there with all tried automata.
"""


paths = [
    Path('../data/res_1000_4583.pickle'),
    Path('../data/res_shifted_1000_3429.pickle'),
    Path('../data/res_cycle_shifted_1000_4420.pickle'),
]

result = None

for path in paths:
    with path.open('rb') as f:
        res = pickle.load(f)
        result = result or res
        assert result['settings'] == res['settings']
        for key in ['permutation', 'random', 'shifted_permutation', 'cycle_shifted_permutation']:
            if res.get(key):
                result[key] = res[key]

settings = result['settings']
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

keys = ['permutation', 'random', 'shifted_permutation', 'cycle_shifted_permutation']
titles = ['permutation', 'random', 'increased permutation', 'shifted permutation']
styles = ['-', '--', 'dashdot', 'dotted']

rand_key = np.random.randint(10000)

for i, n_change in enumerate(n_changes):
    plt.figure(figsize=(12, 8))

    for key, title, style in zip(keys, titles, styles):
        if key not in result:
            continue

        avg = result[key][i].sum(axis=1) / (n_tries * n_words)
        n_log = [math.log(n) for n in ns]
        plt.plot(n_log, avg, linestyle=style, marker='.', label=title)

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

    plt.title(f'{m = }, changes = {n_change}, {n_words = }, {n_tries = }, {n_ns = }, {log_space = }')
    plt.tight_layout()
    plt.savefig(f'../images/compare_m_{m}_{n_change}_{rand_key}.pdf')

    print(rand_key)

plt.show()
