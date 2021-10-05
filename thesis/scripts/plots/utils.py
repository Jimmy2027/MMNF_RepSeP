import numpy as np
from pathlib import Path

from matplotlib import pyplot as plt
from mmvae_hub.utils.utils import json2dict
from modun.iter_utils import _cycle


def plot_comparisons(which: str, metric: str):
    title_mapping = {
        'coherence_eval': 'Evaluation of the generation coherence',
        'lat_eval': 'Evaluation of the separability of the latent representation',

    }

    if which == 'nbr_mods_comp':
        d = dict_elements_to_array(json2dict(Path('data/thesis/nbr_mods_comp.json')), exclude='nbr_mods')
        x_steps = d['nbr_mods']
    elif which == 'epoch_comp':
        d = dict_elements_to_array(json2dict(Path('data/thesis/epoch_comp.json')), exclude='epochs')
        x_steps = d['epochs']
    else:
        raise ValueError(f'{which} not implemented for plot_comparisons.')

    markers = _cycle(['o', 's', 'v', 'p', '*', 'h'])
    config = json2dict(Path('prepare_thesis/conf.json'))
    methods = config['methods']

    # adapt to the experiment that was trained for the least epochs
    x_steps = x_steps[:min(len(e) for _, e in d.items())]

    for method in methods:
        plt.plot(x_steps, d[method][metric][:len(x_steps)], marker=next(markers))
        plt.fill_between(x_steps, d[method][metric][:len(x_steps)] - d[method][f'{metric}_std'][:len(x_steps)],
                         d[method][metric][:len(x_steps)] + d[method][f'{metric}_std'][:len(x_steps)],
                         alpha=0.5, linewidth=1)
    plt.title(title_mapping[metric])
    plt.legend(methods)


def dict_elements_to_array(d: dict, exclude: str = None):
    """Changes lists in dict to arrays."""
    for mod, value in d.items():
        if mod != exclude:
            for nbr_mod in value:
                d[mod][nbr_mod] = np.array(d[mod][nbr_mod])
    return d
