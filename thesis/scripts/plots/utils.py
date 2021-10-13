import numpy as np
from pathlib import Path

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
        methods = [m for m in config['methods'] if m not in ['iwmogfm_amortized']]
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
