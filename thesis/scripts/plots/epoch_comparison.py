"""Plot comparison over epochs for latent space eval and coherence eval."""

from pathlib import Path

import numpy as np
import pandas as pd
from mmvae_hub.utils.utils import json2dict


def df_maker(exp_uids: dict):
    df = pd.DataFrame()

    for id in exp_uids[method]:
        epoch_results_dir = data_dir / id / 'epoch_results'
        if 'epoch' not in df.columns:
            df['epoch'] = [int(i.stem) for i in epoch_results_dir.iterdir()]
        for i in epoch_results_dir.iterdir():
            epoch = int(i.stem)
            res_dict = json2dict(i)
            if res_dict['test_results'] and 'lr_eval_q0' in res_dict['test_results']:
                lr_eval_score = np.mean([v['accuracy'] for _, v in res_dict['test_results']['lr_eval_q0'].items()])
                coherence_score = np.mean([v for _, v in res_dict['test_results']['gen_eval'].items()])
                df.loc[df['epoch'] == epoch, f'lr_eval_score_{id}'] = lr_eval_score
                df.loc[df['epoch'] == epoch, f'coherence_score_{id}'] = coherence_score

    return df.dropna()


data_dir = Path('data/thesis')
experiment_uids_path = data_dir / ('experiment_uids.json')
exp_uids = json2dict(experiment_uids_path)

d = {}

for method in ['mopoe']:
    df = df_maker(exp_uids)

    d[method] = {
        'lat_eval': df[[col for col in df.columns if col.startswith('lr_eval_score_')]].astype(float).mean(
            axis=1).tolist(),
        'lat_eval_std': df[[col for col in df.columns if col.startswith('lr_eval_score_')]].astype(float).std(
            axis=1).tolist(),
        'coherence_eval': df[[col for col in df.columns if col.startswith('coherence_score_')]].astype(float).mean(
            axis=1).tolist(),
        'coherence_eval_std': df[[col for col in df.columns if col.startswith('coherence_score_')]].astype(float).std(
            axis=1).tolist()
    }
