from pathlib import Path

import numpy as np
import pandas as pd
from mmvae_hub.utils.MongoDB import MongoDatabase
from mmvae_hub.utils.utils import json2dict

from utils import get_experiments_df

PARAMS = {
    'end_epoch', 'class_dim', 'initial_learning_rate', 'max_beta', 'beta_warmup'
}

PARAMS_GFM = PARAMS | {'num_gfm_flows'}
PARAMS_FLOW = PARAMS | {'num_flows'}
PARAMS_MAPPING = {'mopoe': PARAMS, 'mopgfm': PARAMS_GFM, 'mogfm': PARAMS_GFM, 'mofop': PARAMS_FLOW}

config = json2dict(Path(__file__).parent / 'config.json')


def df_maker(exp_df):
    # methods = ['mopoe', 'mopgfm', 'mogfm', 'mofop']
    methods = ['mopoe', 'mopgfm', 'mogfm']

    for method in methods:
        if config[method] == 'best':
            sub_df = exp_df.loc[(exp_df['method'].str.startswith(f'{method}')) & (exp_df['num_mods'] == 3)]
            _id = sub_df[sub_df.score == sub_df.score.max()]._id.item()
        else:
            _id = config[method]

        experiments_database = MongoDatabase(training=False, _id=_id)
        experiment_dict = experiments_database.get_experiment_dict()
        yield {k: np.round(experiment_dict['flags'][k], 3) for k in PARAMS_MAPPING[method]} | {
            'method': method.replace("joint_elbo", "mopoe")}


def save_params_tab(exp_df):
    prd_eval_df = pd.DataFrame(data=df_maker(exp_df))

    prd_eval_df.to_csv(Path(__file__).parent.parent / 'data/params_tab.csv', index=False)


if __name__ == '__main__':
    exp_df = get_experiments_df()
    save_params_tab(exp_df)
