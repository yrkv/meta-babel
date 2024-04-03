
from babel import Babel, RandomBaseSampler
from dfa import DFABaseSampler
from cfg import CFGStageSampler

import argparse
from tqdm.auto import tqdm
import pickle
import numpy as np


CONFIGS = {
    'icll_dfa': Babel([
        DFABaseSampler(num_nodes=range(4, 13),
                       alphabet=range(4, 19),
                       max_outgoing_edge=4,
                       seq_len=100),
    ]),
    'dfa_cfg_base': Babel([
        DFABaseSampler(num_nodes=range(4, 13),
                       alphabet=range(4, 19),
                       max_outgoing_edge=4,
                       seq_len=100),
        CFGStageSampler(k=26),
    ]),
    'dfa_cfg_large': Babel([
        DFABaseSampler(num_nodes=range(10, 20),
                       alphabet=range(40, 60),
                       max_outgoing_edge=4,
                       seq_len=100),
        CFGStageSampler(k=range(25, 75)),
        CFGStageSampler(k=26),
    ]),
}


def parse():
    parser = argparse.ArgumentParser(
            prog='meta-babel',
            description='Data generator library for meta-learning language learning algorithms',)

    parser.add_argument('--config', required=True, type=str,
                        help='Select configuration defined in main.py')
    parser.add_argument('--languages', required=True, type=int,
                        help='number of languages to generate')
    parser.add_argument('--tokens', required=True, type=int,
                        help='minimum number of tokens to generate per language (approximately)')
    parser.add_argument('--output', required=False, type=str,
                        help='(optional) specify output path/file. default: [CONFIG].pickle')

    args = parser.parse_args()
    if args.output is None:
        args.output = f'{args.config}.pickle'
    return args


if __name__ == "__main__":
    args = parse()
    print(args)

    babel = CONFIGS[args.config]

    data = []
    for _ in tqdm(range(args.languages)):
        lang = babel.sample()

        total_tokens = 0
        rows = []

        while total_tokens < args.tokens:
            row = np.array(lang(), dtype=np.int32)
            rows.append(row)
            total_tokens += len(row)

        data.append(rows)

    with open(args.output, 'wb') as f:
        pickle.dump(data, f)


