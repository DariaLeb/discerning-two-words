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

We also store the results in  `data/linear_{n_changes}_{rand_key}.pickle`.
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

        if success >= 10:
            break

        n += 5

    bool_history = map(lambda x: int(x == n_tries * n_words), history)
    bool_history = ', '.join(map(str, bool_history))
    print(f'Finish m={word_len}, n={first_n}\nstart={start}\nsuccess rates: {bool_history}\nhistory: {history}')

    return first_n, history[:-9], ns[:-9]


def main():

    n_words = 1000
    n_tries = 100

    ms = range(50, 1050, 50)

    for n_changes in [0.5, 1]:
        task = partial(
            run_experiment,
            random_automaton,
            n_words=n_words, n_tries=n_tries, n_changes=n_changes
        )

        with Pool() as pool:
            res = pool.map(task, ms)

        res, history, ns = zip(*res)
        rand_key = np.random.randint(10000)
        path = Path(f'../data/linear_usual_{n_changes}_{rand_key}.pickle')
        with open(path, 'wb') as f:
            pickle.dump({'ms': ms, 'res': res, 'history': history, 'ns': ns}, f)

        plt.figure()
        plt.plot(ms, res)

        plt.ylabel('n = minimal successful size')
        plt.xlabel('m = word length')

        plt.title(f'Random automaton, {int(n_changes * 100)}% of changes in the word')

        plt.tight_layout()
        plt.savefig(f'../images/linear_random_size_changes_{n_changes}_{rand_key}.pdf')

        for i in list(range(0, len(ms), 4)) + [len(ms) - 1]:
            h = history[i]
            h = [j * 100 / (n_tries * n_words) for j in h]
            n = ns[i]
            m = ms[i]

            plt.figure()
            plt.plot(n, h)

            plt.ylabel('Percentage before first fail [%]')
            plt.xlabel('n = automaton size')

            plt.title(f'Random automaton, {int(n_changes * 100)}% of changes in the word, m = {m}')

            plt.tight_layout()
            plt.savefig(f'../images/linear_random_size_history_{n_changes}_{m}_{rand_key}.pdf')


if __name__ == '__main__':

    tt = time()
    main()
    print(f'Completed in {(time() - tt):.2f}s')
    plt.show()
