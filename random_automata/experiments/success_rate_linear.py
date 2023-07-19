import math
import pickle
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from time import time

import numpy as np
import matplotlib.pyplot as plt

from random_automata.automaton import shifted_permutation_automaton, permutation_automaton, random_automaton

"""
In this module we are looking for minimal successful automaton size for a given percentage of changes in the word. 
We start from log(m) going up and looking for a border where for last 5 sizes 
`n_tries` generated automata were successful for all generated `n_words` words. 

We may try different automaton constructions, but for now we stick to "shifted permutation automata".
We compute the results in parallel over words' lengths.
We are trying different word lengths and plot the result.

We store the resulting data in  `data/linear_{key}_{rand_key}.pickle`,
and the resulting graph in `images/linear_{key}_{rand_key}.pdf`,
where key is the name of tried automata type (specified on input).
"""


def random_pair(m, n_changes):

    x = np.random.randint(2, size=m)
    y = x.copy()

    for i in np.random.choice(m, size=n_changes, replace=False):
        y[i] = 1 - y[i]

    return x, y


def run_experiment(automaton, word_len, n_words, n_tries, n_changes):

    print(f'Start experiment (m={word_len})')

    start = int(math.log(word_len))
    n_changes = int(word_len * n_changes)

    success = 0
    first_n = None
    n = start

    history = []
    ns = []

    while True:

        ns.append(n)

        rate = 0
        for i in range(n_words):

            x, y = random_pair(word_len, n_changes)

            for _ in range(n_tries):
                M = automaton(n)
                for s in M.states:
                    q_x = M.process(x, q=s)
                    q_y = M.process(y, q=s)

                    if q_x != q_y:
                        rate += 1
                        break
                else:
                    break

            # early stopping condition - if automaton already failed, this size is not successful
            if rate != n_tries * (i + 1):
                break

        history.append(rate)

        if rate == n_tries * n_words:
            if success == 0:
                first_n = n
            success += 1
        else:
            success = 0

        if success >= 5:
            break

        n += 1

    print(f'Finish m={word_len}, n={first_n}\nhistory: {history}')

    return first_n, history, ns


def main():

    automaton = shifted_permutation_automaton
    key = 'shifted_permutation'

    n_words = 10000
    n_tries = 100

    ms = range(10, 50, 5)

    result = {}

    for n_changes in [0.1, 0.2, 0.5, 0.7, 0.9, 1]:
        task = partial(
            run_experiment,
            automaton,
            n_words=n_words, n_tries=n_tries, n_changes=n_changes
        )

        with Pool() as pool:
            res = pool.map(task, ms)

        res, history, ns = zip(*res)

        result[n_changes] = {'res': res, 'history': history, 'ns': ns}

    rand_key = np.random.randint(10000)
    path = Path(f'../data/linear_{key}_{rand_key}.pickle')
    with open(path, 'wb') as f:
        pickle.dump({'result': result, 'ms': ms}, f)

    plt.figure(figsize=(10, 6.6))

    for n_changes, res in result.items():
        key = int(round(n_changes * 100))
        plt.plot(ms, res['res'], label=f'{key}% of differences')

    plt.legend()
    plt.ylabel('Minimal successful size')
    plt.xlabel('Word length')

    plt.tight_layout()
    plt.savefig(f'../images/linear_{key}_{rand_key}.pdf')


if __name__ == '__main__':

    tt = time()
    main()
    print(f'Completed in {(time() - tt):.2f}s')
    plt.show()
