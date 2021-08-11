from pathlib import Path

import numpy as np
import pandas as pd
from mmvae_hub.hyperopt.hyperopt_metrics import get_missing_mod_scores_prd, get_reconstr_mod_scores_prd
from mmvae_hub.utils.MongoDB import MongoDatabase

from utils import get_experiments_df

ids = {
    'joint_elbo': 'polymnist_joint_elbo_2021_08_01_17_43_20_301599',
    'mopgfm': 'polymnist_mopgfm_2021_08_02_14_40_15_988947'
}


def df_maker(exp_df):
    methods = ['joint_elbo', 'mopgfm']

    for method in methods:
        # sub_df = exp_df.loc[(exp_df['method'].str.startswith(f'{method}')) & (exp_df['num_mods'] == 3)]
        # best_score_id = sub_df[sub_df.score == sub_df.score.max()]._id.item()
        # experiments_database = MongoDatabase(training=False, _id=best_score_id)
        experiments_database = MongoDatabase(training=False, _id=ids[method])
        experiment_dict = experiments_database.get_experiment_dict()
        max_epoch = max(int(epoch) for epoch in experiment_dict['epoch_results'] if (
                experiment_dict['epoch_results'][epoch]['test_results'] and
                experiment_dict['epoch_results'][epoch]['test_results']['lhoods']))
        max_epoch_results = experiment_dict['epoch_results'][str(max_epoch)]['test_results']['lhoods']

        # remove random gen scores
        max_epoch_results = {k: v for k, v in max_epoch_results.items() if 'random' not in k}

        results = {}
        for in_mods, values in max_epoch_results.items():
            for out_mod in values:
                if out_mod != 'joint':
                    results[f'{in_mods}__{out_mod}'] = max_epoch_results[in_mods][out_mod]

        missing_mod_score = np.mean([score for score in get_missing_mod_scores_prd(results)])
        reconstr_mod_score = np.mean([score for score in get_reconstr_mod_scores_prd(results)])

        lhood_results = {}
        for k, v in results.items():
            split = k.split('_')
            out_mod = split[-1]
            in_mods = split[:-1]
            key = '__'.join(['_'.join(in_mods), out_mod])
            lhood_results[key] = v

        min_score = str({k: np.round(v, 3) for k, v in lhood_results.items() if
                         v == max(val for _, val in lhood_results.items())}).replace('{', '').replace('}',
                                                                                                      '').replace(
            'digit_', '').replace('__', r'$\rightarrow$').replace('_', '\\_').replace("'", "")

        yield {'method': method.replace("joint_elbo", "mopoe"),
               'Missing Mod': np.round(missing_mod_score, 3), 'Reconstruction': np.round(reconstr_mod_score, 3),
               'Best score': min_score}


def save_lhood_eval_tab(exp_df):
    prd_eval_df = pd.DataFrame(data=df_maker(exp_df))

    prd_eval_df.to_csv(Path(__file__).parent.parent / 'data/lhood_eval.csv', index=False)


if __name__ == '__main__':
    exp_df = get_experiments_df()
    prd_eval_df = pd.DataFrame(data=df_maker(exp_df))

    prd_eval_df.to_csv(Path(__file__).parent.parent / 'data/lhood_eval.csv', index=False)
