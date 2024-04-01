"""
Stolen shamelessly from:
    https://github.com/berlino/seq_icl/blob/main/src/dataloaders/dfa.py

Then modified to work with this library.
"""


from typing import Tuple, Dict
import numpy as np

from pythomata import SimpleDFA

from babel import Babel, Stage, BabelStageSampler, resolve
from babel import RandomBaseSampler


class DFA:
    """Represents a DFA"""

    def __init__(
        self,
        num_nodes: int,
        alphabet: Tuple[str],
        transitions: Tuple[dict],
        rng: np.random.Generator,
    ):
        assert len(transitions) == num_nodes
        transitions = {i: v for i, v in enumerate(transitions)}
        dfa = SimpleDFA(
            states=set(list(range(num_nodes))),
            alphabet=set(alphabet),
            initial_state=0,
            accepting_states=set(list(range(num_nodes))),
            transition_function=transitions,
        )
        self.dfa = dfa
        self.rng = rng

    def _sorted_transitions(self):
        nodes = sorted(list(self.dfa._transition_function.keys()))
        transitions = []
        for node in nodes:
            node_transitions = self.dfa._transition_function[node]
            # sort node transitions by outgoing state
            transitions.append(
                tuple(sorted(node_transitions.items(), key=lambda item: item[1]))
            )
        return tuple(transitions)

    def _minimize(self):
        # minimize super
        self.dfa = self.dfa.minimize()
        return self

    def _trim(self):
        # trim super
        self.dfa = self.dfa.trim()
        return self

    def __hash__(self):
        # Here I assume the initial state is always the smallest node
        return hash(self._sorted_transitions())

    def __call__(self, word: str):
        current_node = self.dfa._initial_state
        for symbol in word.split():
            if symbol not in self.dfa._transition_function[current_node]:
                return False
            else:
                current_node = self.dfa._transition_function[current_node][symbol]
        return True

    def forward(self, word: str):
        current_node = self.dfa._initial_state
        for symbol in word.split():
            if symbol not in self.dfa._transition_function[current_node]:
                return None
            else:
                current_node = self.dfa._transition_function[current_node][symbol]
        return current_node

    def trace(self, word: str):
        current_node = self.dfa._initial_state
        path = [current_node]
        for symbol in word.split():
            try:
                self.dfa._transition_function[current_node]
            except:
                breakpoint()
            if symbol not in self.dfa._transition_function[current_node]:
                return path
            else:
                current_node = self.dfa._transition_function[current_node][symbol]
                path.append(current_node)
        return path

    def sample(self, length=1):
        """Samples a random word from the DFA"""
        current_node = self.dfa._initial_state
        seq = []
        for _ in range(length):
            outgoing_symbols = list(self.dfa._transition_function[current_node].keys())
            symbol = self.rng.choice(outgoing_symbols)
            seq.append(symbol)
            current_node = self.dfa._transition_function[current_node][symbol]
        return seq




class DFABaseSampler(BabelStageSampler):
    """Samples random DFAs given configs"""

    num_nodes: int
    max_outgoing_edge: int
    rng: np.random.Generator = None

    def __init__(
        self,
        num_nodes: int,
        max_outgoing_edge: int,
        seq_len: int,
        seed: int = 42,
    ):
        self.num_nodes = resolve(num_nodes)
        self.max_outgoing_edge = resolve(max_outgoing_edge)
        self.seq_len = resolve(seq_len)
        self.rng = np.random.default_rng(seed)

    def sample(self, prev:Stage=None):
        num_nodes = np.random.choice(self.num_nodes)
        seq_len = np.random.choice(self.seq_len)
        alphabet = range(0, num_nodes)
        max_outgoing_edge = np.random.choice(self.max_outgoing_edge)

        transitions = [{} for _ in range(num_nodes)]
        for node in range(num_nodes):
            num_transitions = self.rng.integers(1, max_outgoing_edge)
            transition_symbols = self.rng.choice(
                alphabet, size=num_transitions, replace=False
            )
            # exclude self loops
            possible_nodes = [n for n in range(num_nodes) if n != node]
            transition_nodes = self.rng.choice(
                possible_nodes, size=num_transitions, replace=False
            )
            transitions[node] = dict(zip(transition_symbols, transition_nodes))
        dfa_rng = np.random.default_rng(self.rng.integers(0, 2**32))
        dfa = DFA(num_nodes, alphabet, tuple(transitions), dfa_rng)
        dfa._minimize()._trim()

        def convert(seq=None):
            return dfa.sample(length=seq_len)
        return Stage(num_nodes, convert)


if __name__ == "__main__":

    dfa_sampler = DFABaseSampler(4, 4, 20, seed=1234)
    dfa = dfa_sampler.sample()
    print(dfa.convert())

