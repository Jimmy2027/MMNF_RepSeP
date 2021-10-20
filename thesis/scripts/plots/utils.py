import numpy as np
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
from mmvae_hub.utils.utils import json2dict
from modun.iter_utils import _cycle, chunks


def plot_comparisons(which: str, metric: str):
    title_mapping = {
        'coherence_eval': 'Evaluation of the generation coherence',
        'lat_eval': 'Evaluation of the separability of the latent representation',
    }

    config = json2dict(Path('prepare_thesis/conf.json'))

    if metric == 'coherence_eval':
        y_label = 'Generation Coherence Accuracy'
    elif metric == 'lat_eval':
        y_label = 'Linear Classification Accuracy'
    else:
        y_label = None

    if which == 'nbr_mods_comp':
        d = dict_elements_to_array(json2dict(Path('data/thesis/nbr_mods_comp.json')), exclude='nbr_mods')
        x_steps = [e.replace('_mods', '') for e in d['nbr_mods']]
        methods = [m for m in config['methods']]
        x_label = 'Number of modalities'
    elif which == 'epoch_comp':
        d = dict_elements_to_array(json2dict(Path('data/thesis/epoch_comp.json')), exclude='epochs')
        x_steps = d['epochs']
        methods = config['methods']
        x_label = 'Epochs'
    else:
        raise ValueError(f'{which} not implemented for plot_comparisons.')

    markers = _cycle(['o', 's', 'v', 'p', '*', 'h'])

    for method in methods:
        plt.plot(x_steps, d[method][metric], marker=next(markers))
        plt.fill_between(x_steps, d[method][metric] - d[method][f'{metric}_std'],
                         d[method][metric] + d[method][f'{metric}_std'],
                         alpha=0.2, linewidth=1)
    plt.title(title_mapping[metric])
    plt.xlabel(x_label)
    plt.ylabel(ylabel=y_label)

    plt.legend(methods, ncol=2)


def dict_elements_to_array(d: dict, exclude: str = None):
    """Changes lists in dict to arrays."""
    for mod, value in d.items():
        if mod != exclude:
            for nbr_mod in value:
                d[mod][nbr_mod] = np.array(d[mod][nbr_mod])
    return d


def plot_iw_comp(metric: str):
    if metric == 'coherence_eval':
        title = 'Evaluation of the generation coherence'
        kw = 'coherence_'
        y_label = 'Generation Coherence Accuracy'

    elif metric == 'lat_eval':
        title = 'Evaluation of the separability of the latent representation'
        kw = 'lr_'
        y_label = 'Linear Classification Accuracy'

    elif metric == 'prd':
        title = 'Evaluation of the generation quality'
        kw = 'prd_'
        y_label = 'Area under the Precision and Recall curve'

    iw_comp_df = pd.read_csv('data/thesis/iw_comp.csv')
    lr_columns = [col for col in iw_comp_df.columns if col.startswith(kw)]

    x_label = "K"
    x_steps = ["1", "3", "5"]

    methods = iw_comp_df.method.tolist()

    d = {}
    for method in methods:
        d[method] = iw_comp_df.loc[iw_comp_df['method'] == method][lr_columns].values[0].tolist()

    markers = _cycle(['o', 's', 'v', 'p', '*', 'h'])

    for method in iw_comp_df.method:
        plt.plot(x_steps, d[method], marker=next(markers))

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(ylabel=y_label)

    plt.legend(methods)
