from pathlib import Path

import numpy as np
import pandas as pd
from mmvae_hub.hyperopt.hyperopt_metrics import get_missing_mod_scores_prd, get_reconstr_mod_scores_prd
from mmvae_hub.utils.MongoDB import MongoDatabase
from modun.file_io import json2dict

from utils import get_experiments_df


def df_maker():
    methods = ['mopoe', 'mopgfm', 'moe']
    data_dir = Path(__file__).parent.parent / 'data/thesis'
    experiment_uids_path = data_dir / ('experiment_uids.json')
    exp_uids = json2dict(experiment_uids_path)

    for method in methods:
        method_uids = exp_uids[method]['3_mods']

        d = {'missing_mod_scores': [], 'reconstr_mod_scores': [], 'random_prd_scores': []}
        for method_uid in method_uids:
            epoch_results_dir = data_dir / 'experiments' / method / method_uid / 'epoch_results'
            end_epoch = max(int(item.stem) for item in epoch_results_dir.iterdir())
            prd_dict = json2dict(epoch_results_dir / f'{end_epoch}.json')['test_results']['prd_scores']

            d['random_prd_scores'].append(
                np.mean([score for k, score in prd_dict.items() if k.startswith('random')]))

            prd_dict = {k: v for k, v in prd_dict.items() if not k.startswith('random')}

            d['missing_mod_scores'].append(np.mean([score for score in get_missing_mod_scores_prd(
                prd_dict)]))
            d['reconstr_mod_scores'].append(np.mean([score for score in get_reconstr_mod_scores_prd(
                prd_dict)]))

        yield {
            'Method': method,
            'Missing Mod': np.round(np.mean(d['missing_mod_scores']), 3),
            'Reconstruction': np.round(np.mean(d['reconstr_mod_scores']), 3),
            'Random': np.round(np.mean(d['random_prd_scores']), 3),
            'Missing Mod__STDEV': np.round(np.std(d['missing_mod_scores']), 3),
            'Reconstruction__STDEV': np.round(np.std(d['reconstr_mod_scores']), 3),
            'Random__STDEV': np.round(np.std(d['random_prd_scores']), 3),
        }


if __name__ == '__main__':
    prd_eval_df = pd.DataFrame(data=df_maker())

    prd_eval_df.to_csv(Path(__file__).parent.parent / 'data/thesis/prd_eval.csv', index=False)
