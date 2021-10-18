from pathlib import Path

import numpy as np
import pandas as pd
from mmvae_hub.hyperopt.hyperopt_metrics import get_missing_mod_scores_gen_eval, get_reconstr_mod_scores_gen_eval
from modun.dict_utils import flatten_dict
from modun.file_io import json2dict


def df_maker(epoch: int, methods):
    data_dir = Path(__file__).parent.parent / 'data/thesis'
    experiment_uids_path = data_dir / ('experiment_uids.json')
    exp_uids = json2dict(experiment_uids_path)['polymnist']

    for method in methods:
        method_uids = exp_uids[method]['3_mods']
        d = {'missing_mod_scores': [], 'reconstr_mod_scores': [], 'random_gen_scores': []}
        for method_uid in method_uids:
            epoch_results_dir = data_dir / 'experiments' / 'polymnist' / method / method_uid / 'epoch_results'

            gen_eval_dict = flatten_dict(json2dict(epoch_results_dir / f'{epoch}.json')['test_results']['gen_eval'])

            d['random_gen_scores'].append(
                np.mean([score for k, score in gen_eval_dict.items() if k.startswith('random')]))

            gen_eval_dict = {k: v for k, v in gen_eval_dict.items() if not k.startswith('random')}

            d['missing_mod_scores'].append(np.mean([score for score in get_missing_mod_scores_gen_eval(
                gen_eval_dict)]))
            d['reconstr_mod_scores'].append(np.mean([score for score in get_reconstr_mod_scores_gen_eval(
                gen_eval_dict)]))

        yield {
            'Method': method,
            'Missing Mod': np.round(np.mean(d['missing_mod_scores']), 3),
            'Reconstruction': np.round(np.mean(d['reconstr_mod_scores']), 3),
            'Random': np.round(np.mean(d['random_gen_scores']), 3),
            'Missing Mod__STDEV': np.round(np.std(d['missing_mod_scores']), 3),
            'Reconstruction__STDEV': np.round(np.std(d['reconstr_mod_scores']), 3),
            'Random__STDEV': np.round(np.std(d['random_gen_scores']), 3),
        }


if __name__ == '__main__':
    config = json2dict(Path(__file__).parent / 'conf.json')

    gen_eval_df = pd.DataFrame(data=df_maker(epoch=config['max_epoch']['polymnist'] - 1, methods=config['methods']))

    gen_eval_df.to_csv(Path(__file__).parent.parent / 'data/thesis/gen_eval.csv', index=False)
