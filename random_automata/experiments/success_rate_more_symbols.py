import math
import pickle
from pathlib import Path
from time import time

import numpy as np
import matplotlib.pyplot as plt

from random_automata.automaton import (
    permutation_automaton, random_automaton,
    shifted_permutation_automaton
)

"""
In this module we compare success rate of different automata on word pairs with more than one symbol difference.
We are given the list of number of changes to be made in the word and we process them one by one.
For a fixed word length `m` we create `n_words` random pairs of words which differs in given number of symbols.
We try `n_ns` automaton sizes spaced evenly or logarithmically over interval [1, m].
For each pair and automaton size, we create `n_tries` random and permutation automata and 
count successful tries - when words from the pair finish in different states.

For each `n` (automaton size) we compute overall success ratio and plot it for different number of changes. 
Results of different automata are plotted in separate figures.

We store the results together with settings of the experiment in `data/res_multiple_{m}_{random_suffix}.pickle` 
for reproducibility. We save the resulting graphs as 
`images/experiment_m_{m}_{automata_type}_{random_suffix}.pdf` with the same suffix as corresponding data.
"""


def random_pair(m, n_changes):

    x = np.random.randint(2, size=m)
    y = x.copy()

    for i in np.random.choice(m, size=n_changes, replace=False):
        y[i] = 1 - y[i]

    return x, y


def run_experiment(automaton, word_len, ns, n_words, n_tries, n_changes):

    results = np.zeros((len(ns), n_words))

    for i in range(n_words):
        ttt = time()

        x, y = random_pair(word_len, n_changes)

        for j, n in enumerate(ns):
            for _ in range(n_tries):
                M = automaton(n)
                q_x = M.process(x)
                q_y = M.process(y)

                results[j, i] += int(q_x != q_y)

        print(f'{i}th word completed in {(time() - ttt):.2f}s')

    return results


def plot_results(results, ns, n_words, n_tries, n_changes, style):

    for n_change, res in zip(n_changes, results):
        avg = res.sum(axis=1) / (n_tries * n_words)
        n_log = [math.log(n) for n in ns]

        legend = 'differences' if n_change > 1 else 'difference'
        plt.plot(n_log, avg, linestyle=style, marker='.', label=f'{n_change} {legend}')


def main():

    m = 1000
    n_words = 100
    n_tries = 1000
    n_ns = 50
    n_changes = [1, 2, 3, 5, 10, 50, 100, 500, 1000]

    ns = np.geomspace(1, m, num=n_ns, dtype=int)
    ns = sorted(set(ns))

    tries = {
        'log(n)': int(math.log(m)),
        r'$\sqrt{n}$': int(m ** (1 / 2)),
        r'$\frac{n}{2}$': m // 2,
        'n': m,
    }

    res = {
        'settings': {
            'm': m,
            'n_words': n_words,
            'n_tries': n_tries,
            'n_ns': n_ns,
            'n_changes': n_changes,
        },
        'permutation': [],
        'random': [],
        'shifted_permutation': [],
    }

    for n_change in n_changes:
        print(f'Start `Permutation automaton` experiment ({n_change} changes)')
        res['permutation'].append(run_experiment(permutation_automaton, m, ns, n_words, n_tries, n_change))

        print(f'Start `Random automaton` experiment ({n_change} changes)')
        res['random'].append(run_experiment(random_automaton, m, ns, n_words, n_tries, n_change))

        print(f'Start `Shifted permutation automaton` experiment ({n_change} changes)')
        res['shifted_permutation'].append(
            run_experiment(shifted_permutation_automaton, m, ns, n_words, n_tries, n_change)
        )

    rand_key = np.random.randint(10000)
    path = Path(f'../data/res_multiple_{m}_{rand_key}.pickle')
    with open(path, 'wb') as f:
        pickle.dump(res, f)

    keys = ['permutation', 'random', 'shifted_permutation']
    styles = ['-', '--', 'dotted']

    for key, style in zip(keys, styles):
        plt.figure(figsize=(8, 5.3))

        plot_results(res[key], ns, n_words, n_tries, n_changes, style)

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
        plt.savefig(f'../images/experiment_m_{m}_{key}_{rand_key}.pdf')

    plt.show()


if __name__ == '__main__':

    tt = time()
    main()
    print(f'Completed in {(time() - tt):.2f}s')
