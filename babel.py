

from collections import namedtuple
from typing import Union, Optional

import numpy as np


def resolve(x: Union[int, range]):
    assert type(x) in (int, range)
    if type(x) is int:
        return range(x, x+1)
    return x


"""
Babel -- procedurally generate languages.

"""

class Babel:
    def __init__(self, stages,):
        self.stages = stages

    def sample(self):
        sampled_stages = []

        last = None
        for stage in self.stages:
            last = stage.sample(last)
            sampled_stages.append(last)


        def generate():
            seq = None
            for sampled in sampled_stages:
                seq = sampled.convert(seq)
            return seq
        return generate


class Stage(namedtuple('Stage', ['k', 'convert'])):
    def __call__(self, seq):
        return self.convert(*args, **kwargs)

class BabelStageSampler:
    def sample(self, last: Optional[Stage]):
        pass



class RandomBaseSampler(BabelStageSampler):
    def __init__(self,
                 k: Union[int, range],
                 seq_len: Union[int, range],):
        self.k = resolve(k)
        self.seq_len = resolve(seq_len)

    def sample(self, prev=None):
        assert prev is None
        k = np.random.choice(self.k)
        seq_len = np.random.choice(self.seq_len)

        def convert(seq=None):
            assert seq is None
            return np.random.randint(0, self.k, self.seq_len)
        return Stage(k, convert)



class ExampleStageSampler(BabelStageSampler):
    def __init__(self,
               k: Union[int, range],
               out_len: Union[int, range]=1,):
        self.k = resolve(k)
        self.out_len = resolve(out_len)

    def sample(self, prev:Stage):
        k = np.random.choice(self.k)
        out_len = np.random.choice(self.out_len)

        mapping = {}
        for i in range(prev.k):
            mapping[i] = np.random.choice(k, out_len).tolist()

        def convert(seq):
            out = []
            for x in seq:
                out += mapping[x]
            return np.array(out)
        return Stage(k, convert)





if __name__ == '__main__':

    rand_sampler = RandomBaseSampler(k=10, seq_len=20)
    ex_sampler = ExampleStageSampler(k=5, out_len=range(2,4))

    rand = rand_sampler.sample()
    print(rand.convert())

    ex = ex_sampler.sample(rand)
    print(ex.convert(rand.convert()))

    babel = Babel([
        RandomBaseSampler(k=10, seq_len=20),
        ExampleStageSampler(k=20, out_len=range(2,4)),
        ExampleStageSampler(k=30, out_len=1),
    ])
    generator = babel.sample()
    print(generator())



