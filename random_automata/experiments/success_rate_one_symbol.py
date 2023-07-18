import math
import pickle
from pathlib import Path
from time import time

import numpy as np
import matplotlib.pyplot as plt

from random_automata.automaton import permutation_automaton, random_automaton, shifted_permutation_automaton

"""
In this module we compare success rate of different automata types automata (random, permutation, shifted permutation). 
For a fixed word length `m`, we create `n_words` random pairs of words which differs in one symbol only.
We try `n_ns` automaton sizes spaced evenly or logarithmically over interval [1, m].
For each pair and automaton size, we create `n_tries` random and permutation automata and 
count successful tries - when words from the pair finish in different states.

For each `n` (automaton size) we compute 
- overall success ratio (ratio of successful tries over all `n_words` * `n_tries` tries)
- min success ratio (minimal ratio of successful tries over all tried word pairs)
- max success ratio (maximal ratio of successful tries over all tried word pairs)

We store the results together with settings of the experiment in `data/res_{m}_{random_suffix}.pickle` 
for reproducibility. We plot computed statistics and save the resulting graph as 
`images/experiment_m_{m}_{random_suffix}.pdf` with the same suffix as corresponding data.
"""


def random_pair(m):

    x = np.random.randint(2, size=m)
    y = x.copy()

    i = np.random.randint(m)
    y[i] = 1 - y[i]

    return x, y


def run_experiment(automaton, word_len, ns, n_words, n_tries):

    results = np.zeros((len(ns), n_words))

    for i in range(n_words):
        ttt = time()

        x, y = random_pair(word_len)

        for j, n in enumerate(ns):
            for _ in range(n_tries):
                M = automaton(n)
                q_x = M.process(x)
                q_y = M.process(y)

                results[j, i] += int(q_x != q_y)

        print(f'{i}th word completed in {(time() - ttt):.2f}s')

    return results


def plot_results(results, ns, n_words, n_tries, title, style):

    avg = results.sum(axis=1) / (n_tries * n_words)
    min_ = results.min(axis=1) / n_tries
    max_ = results.max(axis=1) / n_tries

    n_log = [math.log(n) for n in ns]

    plt.plot(n_log, avg, linestyle=style, marker='.', label=f'{title} (avg)')
    plt.plot(n_log, min_, linestyle=style, marker='.', label=f'{title} (min)')
    plt.plot(n_log, max_, linestyle=style, marker='.', label=f'{title} (max)')


def main():

    m = 4000
    n_words = 100
    n_tries = 1000
    n_ns = 100

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
        }
    }

    print('Start `Shifted permutation automaton` experiment')
    res['shifted_permutation'] = run_experiment(shifted_permutation_automaton, m, ns, n_words, n_tries)

    print('Start `Permutation automaton` experiment')
    res['permutation'] = run_experiment(permutation_automaton, m, ns, n_words, n_tries)

    print('Start `Random automaton` experiment')
    res['random'] = run_experiment(random_automaton, m, ns, n_words, n_tries)

    suffix = np.random.randint(10000)
    path = Path(f'../data/res_{m}_{suffix}.pickle')
    with open(path, 'wb') as f:
        pickle.dump(res, f)

    plt.figure(figsize=(10, 6.6))

    plot_results(res['shifted_permutation'], ns, n_words, n_tries, 'Shifted permutation', 'dotted')
    plot_results(res['permutation'], ns, n_words, n_tries, 'Permutation', '-')
    plot_results(res['random'], ns, n_words, n_tries, 'Random', '--')

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
    plt.savefig(f'../images/experiment_m_{m}_{suffix}.pdf')
    plt.show()


if __name__ == '__main__':

    tt = time()
    main()
    print(f'Completed in {(time() - tt):.2f}s')
