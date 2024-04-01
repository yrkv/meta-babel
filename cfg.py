
import numpy as np
#from collections import namedtuple
from typing import Union, Optional

from babel import Babel, Stage, BabelStageSampler, resolve
from babel import RandomBaseSampler



def create_targets(b, beta_count=0.65, beta_len=0.65):
    targets = []
    num_targets = np.random.geometric(beta_count)
    for _ in range(num_targets):
        k = min(np.random.geometric(beta_len) + 1, int(np.floor(b**0.5)))
        targets.append(np.random.choice(b, k).tolist())

    weights = np.random.rand(num_targets)
    weights = (weights / weights.sum()).tolist()
    return targets, weights


def build_tree(a, b, depth_limit=2, recursive_p=0.5):
    mappings = {}
    for i in range(a):
        if depth_limit > 0 and np.random.rand() < recursive_p:
            mappings[i] = build_tree(a=a, b=b, depth_limit=depth_limit-1, recursive_p=recursive_p/2)
        else:
            mappings[i] = create_targets(b=b)
    return mappings


def process_part(seq, tree):
    if type(tree) is dict:
        if len(seq) > 0:
            return process_part(seq[1:], tree[seq[0]])
        else:
            return [], []
    else:
        targets, weights = tree
        i = np.random.choice(len(targets), p=weights)
        return targets[i], seq



class CFGStageSampler(BabelStageSampler):
    def __init__(self, k: Union[int, range],):
        self.k = resolve(k)

    def sample(self, prev:Stage):
        k = np.random.choice(self.k)
        tree = build_tree(a=prev.k, b=k)
        def convert(seq):
            new_seq = []
            while len(seq) > 0:
                processed, seq = process_part(seq, tree)
                new_seq.extend(processed)
            return np.array(new_seq)
        return Stage(k, convert)


if __name__ == '__main__':

    rand_sampler = RandomBaseSampler(k=10, seq_len=20)
    cfg_sampler = CFGStageSampler(k=10)

    rand = rand_sampler.sample()
    print(rand.convert())

    cfg = cfg_sampler.sample(rand)
    print(cfg.convert(rand.convert()))

    babel = Babel([
        RandomBaseSampler(k=10, seq_len=20),
        CFGStageSampler(k=20),
        CFGStageSampler(k=10),
    ])
    generator = babel.sample()
    print(generator())
    print(generator())
    print(generator())


#class CFGStage(BabelStage):
#    def __init__(self, 









