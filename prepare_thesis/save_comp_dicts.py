"""Save the dicts containing data for the epoch comparison and nbr_mods comparison."""

from pathlib import Path
from typing import Mapping, Union

import numpy as np
import pandas as pd
import torch
from mmvae_hub.evaluation.eval_metrics.coherence import flatten_cond_gen_values
from mmvae_hub.utils.utils import json2dict, dict2json

# data_dir = Path('../data/thesis')
from modun.dict_utils import flatten_dict, dict2pyobject

data_dir = Path(__file__).parent.parent / 'data/thesis'
experiment_uids_path = data_dir / ('experiment_uids.json')
exp_uids = json2dict(experiment_uids_path)
methods = ['mopoe', 'moe', 'mopgfm']


def load_flags(dir_path: Path):
    if (dir_path / 'flags.rar').exists():
        return torch.load(dir_path / 'flags.rar')
    elif (dir_path / 'flags.json').exists():
        return dict2pyobject(json2dict(dir_path / 'flags.json'), 'flags')


def df_maker_epoch_comp(exp_uids: dict, method: str, data_dir: Path):
    df = pd.DataFrame()
    for _id in exp_uids[method]['3_mods']:

        epoch_results_dir = data_dir / _id / 'epoch_results'

        # get the epochs where the model was evaluated
        flags = load_flags(dir_path=data_dir / _id)
        eval_epochs = [i - 1 for i in range(1, flags.end_epoch) if i % flags.eval_freq == 0]

        if epoch_results_dir.exists():
            if 'epoch' not in df.columns:
                df['epoch'] = [int(i.stem) for i in epoch_results_dir.iterdir()]
            for epoch in eval_epochs:

                res_dict = json2dict(epoch_results_dir / f'{epoch}.json')
                if res_dict['test_results'] and 'lr_eval_q0' in res_dict['test_results']:
                    lr_eval_score = np.mean([v['accuracy'] for _, v in res_dict['test_results']['lr_eval_q0'].items()])
                    coherence_score = np.mean(
                        [v for _, v in flatten_dict(res_dict['test_results']['gen_eval']).items()])
                    df.loc[df['epoch'] == epoch, f'lr_eval_score_{_id}'] = lr_eval_score
                    df.loc[df['epoch'] == epoch, f'coherence_score_{_id}'] = coherence_score

    return df.dropna()


d = {}

for method in methods:
    df = df_maker_epoch_comp(exp_uids, method, data_dir).sort_values('epoch')

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

d['epochs'] = df['epoch'].tolist()
dict2json(data_dir / 'epoch_comp.json', d)


def df_maker_nbr_mods_comp(exp_uids: dict, method: str, data_dir: Path):
    df = pd.DataFrame()
    df['nbr_mods'] = list(exp_uids[method])
    for nbr_mods in exp_uids[method]:
        for id in exp_uids[method][nbr_mods]:
            epoch_results_dir = data_dir / id / 'epoch_results'
            if epoch_results_dir.exists():
                last_epoch = max(int(i.stem) for i in epoch_results_dir.iterdir())
                res_dict = json2dict(epoch_results_dir / f'{last_epoch}.json')

                lr_eval_score = np.mean([v['accuracy'] for _, v in res_dict['test_results']['lr_eval_q0'].items()])
                coherence_score = np.mean([v for _, v in flatten_dict(res_dict['test_results']['gen_eval']).items()])
                df.loc[df['nbr_mods'] == nbr_mods, f'lr_eval_score_{id}'] = lr_eval_score
                df.loc[df['nbr_mods'] == nbr_mods, f'coherence_score_{id}'] = coherence_score

    return df


d = {}

for method in methods:
    df = df_maker_nbr_mods_comp(exp_uids, method, data_dir).sort_values('nbr_mods')

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

d['nbr_mods'] = df['nbr_mods'].tolist()
dict2json(data_dir / 'nbr_mods_comp.json', d)
