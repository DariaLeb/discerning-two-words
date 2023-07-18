import pickle
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

"""
This script is used to compare different automata experiments with fixed or various initial states.
It loads experiments' data and create a figure for each number of changes with all tried automata
Tries with fixed initial state are distinguished from those with various by color, 
while automata types are distinguished by line style.

We store the figures in `images/compare_initial_m_{m}_{n_change}_{rand_key}.pdf`, 
where random suffix is added to avoid collisions.
"""


path_fixed = Path('../data') / f'res_multiple_1000_8386.pickle'
path_choose = Path('../data') / f'res_1000_4650_choose.pickle'

with path_fixed.open('rb') as f:
    result_fixed = pickle.load(f)

with path_choose.open('rb') as f:
    result_choose = pickle.load(f)

settings = result_choose['settings']
m = settings['m']
n_words = settings['n_words']
n_tries_choose = settings['n_tries']
n_ns = settings['n_ns']
n_changes = settings['n_changes']

n_tries_fixed = result_fixed['settings']['n_tries']

ns = np.geomspace(1, m, num=n_ns, dtype=int)
ns = sorted(set(ns))

tries = {
    'log(n)': int(math.log(m)),
    r'$\sqrt{n}$': int(m ** (1 / 2)),
    r'$\frac{n}{2}$': m // 2,
    'n': m,
}

keys_fixed = ['permutation', 'random', 'shifted_permutation']
titles_fixed = ['fixed: permutation', 'fixed: random', 'fixed: shifted']
styles_fixed = ['-', '--', 'dotted']

keys_choose = ['permutation', 'random', 'shifted_permutation']
titles_choose = ['various: permutation', 'various: random', 'various: shifted']
styles_choose = ['-', '--', 'dotted']

rand_key = np.random.randint(10000)

for i, n_change in enumerate(n_changes):
    plt.figure(figsize=(8, 5.3))

    for key, title, style in zip(keys_fixed, titles_fixed, styles_fixed):
        if key not in result_fixed:
            continue

        avg = result_fixed[key][i].sum(axis=1) / (n_tries_fixed * n_words)
        n_log = [math.log(n) for n in ns]
        plt.plot(n_log, avg, linestyle=style, color='tab:blue', marker='.', label=title, alpha=0.7)

    for key, title, style in zip(keys_choose, titles_choose, styles_choose):
        if key not in result_choose:
            continue

        avg = result_choose[key][i].sum(axis=1) / (n_tries_choose * n_words)
        n_log = [math.log(n) for n in ns]
        plt.plot(n_log, avg, linestyle=style, color='tab:orange', marker='.', label=title, alpha=0.7)

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

    plt.tight_layout()
    plt.savefig(f'../images/compare_initial_m_{m}_{n_change}_{rand_key}.pdf')

    print(rand_key)

plt.show()
