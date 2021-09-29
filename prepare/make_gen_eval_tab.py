from pathlib import Path

import numpy as np
import pandas as pd
from mmvae_hub.hyperopt.hyperopt_metrics import get_missing_mod_scores_gen_eval, get_reconstr_mod_scores_gen_eval
from mmvae_hub.utils.MongoDB import MongoDatabase

from utils import get_experiments_df


def df_maker(exp_df):
    methods = ['joint_elbo', 'mopgfm', 'mogfm', 'mofop']

    for method in methods:
        sub_df = exp_df.loc[(exp_df['method'].str.startswith(f'{method}')) & (exp_df['num_mods'] == 3)]
        best_score_id = sub_df[sub_df.score == sub_df.score.max()]._id.item()
        experiments_database = MongoDatabase(training=False, _id=best_score_id)
        experiment_dict = experiments_database.get_experiment_dict()
        max_epoch = max(int(epoch) for epoch in experiment_dict['epoch_results'] if (
                experiment_dict['epoch_results'][epoch]['test_results'] and
                experiment_dict['epoch_results'][epoch]['test_results']['gen_eval']))
        max_epoch_results = experiment_dict['epoch_results'][str(max_epoch)]['test_results']['gen_eval']
        missing_mod_score = np.mean([score for score in get_missing_mod_scores_gen_eval(
            max_epoch_results)])
        reconstr_mod_score = np.mean([score for score in get_reconstr_mod_scores_gen_eval(
            max_epoch_results)])
        max_score = str({k: np.round(v, 3) for k, v in max_epoch_results.items() if
                         v == max(val for _, val in max_epoch_results.items())}).replace('{', '').replace('}',
                                                                                                          '').replace(
            'digit_', '').replace('__', r'$\rightarrow$').replace('_', '\\_').replace("'", "")

        yield {'method': method.replace("joint_elbo", "mopoe"),
               'Missing Mod': np.round(missing_mod_score, 3), 'Reconstruction': np.round(reconstr_mod_score, 3),
               'Best score': max_score}


def save_gen_eval_tab(exp_df):
    gen_eval_df = pd.DataFrame(data=df_maker(exp_df))

    gen_eval_df.to_csv(Path(__file__).parent.parent / 'data/gen_eval.csv', index=False)


if __name__ == '__main__':
    exp_df = get_experiments_df()
    gen_eval_df = pd.DataFrame(data=df_maker(exp_df))

    gen_eval_df.to_csv(Path(__file__).parent.parent / 'data/gen_eval.csv', index=False)
