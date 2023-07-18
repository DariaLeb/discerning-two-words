from time import time

import numpy as np

from random_automata.automaton import shifted_permutation_automaton

"""
In this module we compute the success of the automaton of given constant size.
Given number of tries, for each we generate a word pair of length `word_len` 
with `n_changes` differences and an automaton of size `automaton_size`. We increase the number of success tries
if there is at least one state starting in which the automaton will distinguish the words.

The output of the script is one number, printed on the standard output.
"""


def random_pair(m, n_changes):

    x = np.random.randint(2, size=m)
    y = x.copy()

    for i in np.random.choice(m, size=n_changes, replace=False):
        y[i] = 1 - y[i]

    return x, y


def run_experiment(automaton, size, word_len, n_tries, n_changes):

    success = 0

    for _ in range(n_tries):
        x, y = random_pair(word_len, n_changes)
        M = automaton(size)

        for s in M.states:
            q_x = M.process(x, q=s)
            q_y = M.process(y, q=s)

            if q_x != q_y:
                success += 1
                break

    return success


def main():

    automaton_size = 10

    n_tries = 1_000_000
    word_len = 1_000
    n_changes = word_len // 10

    success = run_experiment(
        shifted_permutation_automaton,
        size=automaton_size, word_len=word_len, n_tries=n_tries, n_changes=n_changes
    )

    print(f'Shifted permutation automaton of size {automaton_size} '
          f'was successful {success} of {n_tries} tries ({success * 100 / n_tries:.2f}%) '
          f'on words of length {word_len} with {n_changes} differences.')


if __name__ == '__main__':

    tt = time()
    main()
    print(f'Completed in {(time() - tt):.2f}s')
