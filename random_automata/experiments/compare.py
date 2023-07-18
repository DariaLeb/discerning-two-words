import pickle
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

"""
This script is used to compare different automata from multiple symbols experiments in one figure.
It loads experiments' data and create a figure for each number of changes there with all tried automata.
We store the figures in `images/compare_m_{m}_{n_changes}_{rand_suffix}.pdf`, 
where suffix correspond to a suffix of input data.
"""


rand_key = 8386
path = Path('../data') / f'res_multiple_1000_{rand_key}.pickle'

with path.open('rb') as f:
    result = pickle.load(f)

settings = result['settings']
m = settings['m']
n_words = settings['n_words']
n_tries = settings['n_tries']
n_ns = settings['n_ns']
n_changes = settings['n_changes']

ns = np.geomspace(1, m, num=n_ns, dtype=int)
ns = sorted(set(ns))

tries = {
    'log(n)': int(math.log(m)),
    r'$\sqrt{n}$': int(m ** (1 / 2)),
    r'$\frac{n}{2}$': m // 2,
    'n': m,
}

keys = ['shifted_permutation', 'permutation', 'random']
titles = ['Shifted permutation', 'Permutation', 'Random']
styles = ['dotted', '-', '--']

for i, n_change in enumerate(n_changes):
    plt.figure(figsize=(8, 5.3))

    for key, title, style in zip(keys, titles, styles):

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

    plt.tight_layout()

    plt.savefig(f'../images/compare_m_{m}_{n_change}_{rand_key}.pdf')

plt.show()
