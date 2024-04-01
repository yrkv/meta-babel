
from babel import Babel, RandomBaseSampler
from dfa import DFABaseSampler
from cfg import CFGStageSampler


if __name__ == "__main__":
    babel = Babel([
        DFABaseSampler(num_nodes=10, max_outgoing_edge=4, seq_len=10, seed=42),
        CFGStageSampler(k=50),
        CFGStageSampler(k=26),
    ])

    language = babel.sample()

    def display():
        seq = language()
        seq = [chr(ord('A') + x) for x in seq]
        print(' '.join(seq))

    display()
    display()
    display()

