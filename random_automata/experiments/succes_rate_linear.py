import math
import pickle
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from time import time

import numpy as np
import matplotlib.pyplot as plt

from random_automata.automaton import shifted_permutation_automaton

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

    while True:

        rate = 0
        succ = True
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
                    succ = False
                    break

            if not succ:
                break

        # print(f'm = {word_len}, {n = }: success rate = {rate / (n_tries * n_words)}' )
        if rate == n_tries * n_words:
            if success == 0:
                first_n = n
            success += 1
        else:
            success = 0

        if success >= 5:
            break

        n += 1

    return first_n


def plot_results(results, ns, n_words, n_tries, n_changes, style):

    for n_change, res in zip(n_changes, results):
        avg = res.sum(axis=1) / (n_tries * n_words)
        n_log = [math.log(n) for n in ns]

        plt.plot(n_log, avg, linestyle=style, marker='.', label=f'{n_change} changes')


def main():

    n_words = 100
    n_tries = 1000

    ms = list(range(50, 4000, 50))

    for n_changes in [0.2,  0.5, 0.7, 0.9, 1.0]:
        task = partial(
            run_experiment,
            shifted_permutation_automaton,
            n_words=n_words, n_tries=n_tries, n_changes=n_changes
        )

        with Pool() as pool:
            res = pool.map(task, ms)

        rand_key = np.random.randint(10000)
        path = Path(f'../data/linear_{n_changes}_{rand_key}.pickle')
        with open(path, 'wb') as f:
            pickle.dump({'ms': ms, 'res': res}, f)

        plt.figure()
        plt.plot(ms, res)

        plt.ylabel('n = minimal successful size')
        plt.xlabel('m = word length')

        plt.title(f'Shifted permutation automaton, {int(n_changes * 100)}% of changes in the word')

        plt.tight_layout()
        plt.savefig(f'../images/linear_size_changes_{n_changes}_{rand_key}.pdf')


if __name__ == '__main__':

    tt = time()
    main()
    print(f'Completed in {(time() - tt):.2f}s')
    plt.show()
