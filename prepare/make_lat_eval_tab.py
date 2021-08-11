from pathlib import Path

import numpy as np
import pandas as pd
from mmvae_hub.utils.MongoDB import MongoDatabase

from utils import get_experiments_df


def df_maker(exp_df):
    methods = ['joint_elbo', 'mopgfm', 'mogfm', 'mofop']

    for method in methods:
        if method == 'mopgfm':
            best_score_id = 'polymnist_mopgfm_2021_07_31_12_04_29_783810'
        else:
            sub_df = exp_df.loc[(exp_df['method'].str.startswith(f'{method}')) & (exp_df['num_mods'] == 3)]
            best_score_id = sub_df[sub_df.score == sub_df.score.max()]._id.item()
        experiments_database = MongoDatabase(training=False, _id=best_score_id)
        experiment_dict = experiments_database.get_experiment_dict()
        max_epoch = max(int(epoch) for epoch in experiment_dict['epoch_results'] if (
                experiment_dict['epoch_results'][epoch]['test_results'] and
                experiment_dict['epoch_results'][epoch]['test_results']['lr_eval_q0']))

        lr_eval_results = {k: np.round(v['accuracy'], 3) for k, v in
                           experiment_dict['epoch_results'][str(max_epoch)]['test_results']['lr_eval_q0'].items()}
        yield {'method': method.replace("joint_elbo", "mopoe"), **{k: v for k, v in lr_eval_results.items() if k != 'joint'}}


def save_lr_eval_tab(exp_df):
    lr_eval_df = pd.DataFrame(data=df_maker(exp_df))

    lr_eval_df.to_csv(Path(__file__).parent.parent / 'data/lr_eval.csv', index=False)


if __name__ == '__main__':
    exp_df = get_experiments_df()
    lr_eval_df = pd.DataFrame(data=df_maker(exp_df))

    lr_eval_df.to_csv(Path(__file__).parent.parent / 'data/lr_eval.csv', index=False)
