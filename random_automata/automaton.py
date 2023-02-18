from typing import Any, Iterable
import numpy as np

"""
This module describes `Automaton` class and provides two functions to create automaton: permutation and random one.
"""


class Automaton:
    """
    This class describes a simple automaton over {0, 1} alphabet.
    For now we only need two parts of classic DFA description: initial state and transition function.
    List of all states can be deducted from the transition function.
    For given w, we need to decide in which state automaton will finish its work - this is done by `process` method.
    """

    @classmethod
    def f_from_lists(cls, states: list, transitions0: list, transitions1: list):
        """
        On input, we have list of states [q0, q1, ...] and two list of transitions:
        [f(q0, 0), f(q1, 0), ...] and [f(q0, 1), f(q1, 1), ...].
        We output transition function in format needed for `Automaton` creation:
        f[q] = (f(q, 0), f(q, 1))
        """
        return dict(zip(states, zip(transitions0, transitions1)))

    def __init__(self, q0: Any, f: dict[Any, tuple[Any, Any]]):
        """
        :param q0: initial state
        :param f: transition function: for every state it determines two states where one can get by 0/1
        """
        self.q0 = q0
        self.f = f

    def process(self, w: Iterable):

        q = self.q0

        for a in w:
            q = self.f[q][int(a)]

        return q


def random_automaton(n):

    states = list(range(n))
    transitions0 = list(np.random.randint(n, size=n))
    transitions1 = list(np.random.randint(n, size=n))

    f = Automaton.f_from_lists(states, transitions0, transitions1)

    return Automaton(0, f)


def permutation_automaton(n):

    states = list(range(n))
    transitions0 = list(np.random.permutation(n))
    transitions1 = list(np.random.permutation(n))

    f = Automaton.f_from_lists(states, transitions0, transitions1)

    return Automaton(0, f)


def increased_permutation_automaton(n):

    states = list(range(n))
    transitions0 = list(np.random.permutation(n))
    transitions1 = [(t + 1) % n for t in transitions0]

    f = Automaton.f_from_lists(states, transitions0, transitions1)

    return Automaton(0, f)


def shifted_permutation_automaton(n):

    states = list(range(n))
    transitions0 = list(np.random.permutation(n))
    transitions1 = transitions0[1:] + transitions0[:1]

    f = Automaton.f_from_lists(states, transitions0, transitions1)

    return Automaton(0, f)
