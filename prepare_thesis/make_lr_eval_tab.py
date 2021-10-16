from pathlib import Path

import numpy as np
import pandas as pd
from modun.file_io import json2dict


def df_maker(epoch: int):
    config = json2dict(Path(('conf.json')))
    methods = config['methods']
    data_dir = Path(__file__).parent.parent / 'data/thesis'
    experiment_uids_path = data_dir / ('experiment_uids.json')
    exp_uids = json2dict(experiment_uids_path)['polymnist']

    for method in methods:
        method_uids = exp_uids[method]['3_mods']
        d = {}
        for method_uid in method_uids:
            epoch_results_dir = data_dir / 'experiments' / 'polymnist' / method / method_uid / 'epoch_results'

            lr_eval_results = {k: np.round(v['accuracy'], 3) for k, v in
                               json2dict(epoch_results_dir / f'{epoch}.json')['test_results']['lr_eval_q0'].items()}
            for k, v in lr_eval_results.items():
                if k != 'joint':
                    if k not in d:
                        d[k] = [v]
                    else:
                        d[k].append(v)

        d_ = {}
        for k, v in d.items():
            d_[k] = np.round(np.mean(v), 3)
            d_[k + '__STDEV'] = np.round(np.std(v), 3)

        yield {
            'Method': method,
            **d_,
        }


if __name__ == '__main__':
    config = json2dict(Path('conf.json'))
    lr_eval_df = pd.DataFrame(data=df_maker(epoch=config['max_epoch']['polymnist']))

    lr_eval_df.to_csv(Path(__file__).parent.parent / 'data/thesis/lr_eval.csv', index=False)
