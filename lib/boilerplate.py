from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from lib.utils import tex_escape, float_to_tex
from scripts_ import tikz
from mmvae_hub.utils.utils import json2dict


def get_cond_gen_plot(method: str, which: str):
    if which == 'best_prd_score':
        gen_eval_df = pd.read_csv(Path('data/prd_eval.csv'))
        method_df = gen_eval_df.loc[gen_eval_df['method'] == method]
        img_name = method_df['Max score'].item().split(':')[0].replace('$\\rightarrow$', '__').replace(r'\_', '_')
    else:
        img_name = which

    if method == r'joint\_elbo':
        method = 'mopoe'

    return f'\\includegraphics{{data/{method}/cond_gen_plots/{img_name}.png}}'


def make_cond_gen_fig(which: str, methods: List[str], dataset: str):
    nbr_examples = {
        "polymnist": 10,
        "mimic": 5
    }
    split = which.split('__')
    in_mods = split[0]
    out_mod = split[-1]

    input_samples_dir = Path(f'data/thesis/{dataset}/{methods[0]}/cond_gen_plots/input_samples')
    cond_samples_path = {method: Path(f'data/thesis/{dataset}/{method}/cond_gen_plots/{in_mods}') for method in methods}

    pic = tikz.Picture()
    plot_xshift_base = 3

    yshift = 0
    for in_mod in in_mods.split('_'):
        xshift = plot_xshift_base
        for class_idx in range(nbr_examples[dataset]):
            img_name = f"{in_mod}_{class_idx}"
            pic.set_node(
                text=f'\\includegraphics[width=2cm]{{{input_samples_dir / img_name}}}',
                options=f'xshift={xshift}cm, yshift=-{yshift}cm',
                name=f'inmod_{img_name}',
            )

            xshift += 2.1
        yshift += 2

    pic.set_node(text=r'\Large{\textbf{Input}}', options=f'yshift=-{np.floor(yshift / (2 * 2))}cm')

    yshift += 1.5

    for method in methods:
        if method == 'iwmogfm_amortized':
            pic.set_node(text=fr'\Large{{\textbf{{iwmogfm}}}}\\\Large{{\textbf{{amortized}}}}',
                         options=f'yshift=-{yshift}cm, align=center')
        else:
            pic.set_node(text=fr'\Large{{\textbf{{{tex_escape(method)}}}}}', options=f'yshift=-{yshift}cm')

        xshift = plot_xshift_base
        for class_idx in range(nbr_examples[dataset]):
            img_name = f"{out_mod}_{class_idx}"

            pic.set_node(
                text=f'\\includegraphics[width=2cm]{{{cond_samples_path[method] / img_name}}}',
                options=f'xshift={xshift}cm, yshift=-{yshift}cm',
                name=f'outmod_{img_name}',
            )

            xshift += 2.1
        yshift += 2.1

    return pic.make()

def make_cond_gen_fig_mimic(which: str, methods: List[str], dataset: str):
    nbr_examples = {
        "polymnist": 10,
        "mimic": 5
    }
    split = which.split('__')
    in_mods = split[0]
    out_mod = split[-1]

    input_samples_dir = Path(f'data/thesis/{dataset}/{methods[0]}/cond_gen_plots/input_samples')
    cond_samples_path = {method: Path(f'data/thesis/{dataset}/{method}/cond_gen_plots/{in_mods}') for method in methods}

    pic = tikz.Picture()
    plot_xshift_base = 3

    yshift = 0
    for in_mod in in_mods.split('_'):
        xshift = plot_xshift_base
        if in_mod == 'text':
            width= 3
        else:
            width = 2
        for class_idx in range(nbr_examples[dataset]):
            img_name = f"{in_mod}_{class_idx}"
            pic.set_node(
                text=f'\\includegraphics[width={width}cm]{{{input_samples_dir / img_name}}}',
                options=f'xshift={xshift}cm, yshift=-{yshift}cm',
                name=f'inmod_{img_name}',
            )

            xshift += 4
        yshift += 2

    pic.set_node(text=r'\Large{\textbf{Input}}', options=f'yshift=-{np.floor(yshift / (2 * 2))}cm')

    yshift += 1.5

    for method in methods:
        if method == 'iwmogfm_amortized':
            pic.set_node(text=fr'\Large{{\textbf{{iwmogfm}}}}\\\Large{{\textbf{{amortized}}}}',
                         options=f'yshift=-{yshift}cm, align=center')
        else:
            pic.set_node(text=fr'\Large{{\textbf{{{tex_escape(method)}}}}}', options=f'yshift=-{yshift}cm')

        xshift = plot_xshift_base
        if out_mod == 'text':
            width= 3
        else:
            width = 2
        for class_idx in range(nbr_examples[dataset]):
            img_name = f"{out_mod}_{class_idx}"

            pic.set_node(
                text=f'\\includegraphics[width={width}cm]{{{cond_samples_path[method] / img_name}}}',
                options=f'xshift={xshift}cm, yshift=-{yshift}cm',
                name=f'outmod_{img_name}',
            )

            xshift += 4
        yshift += 2.1

    return pic.make()


def get_lr_score(method: str):
    epoch_comp_dict = json2dict(Path('data/thesis/epoch_comp.json'))
    return float_to_tex(epoch_comp_dict[method]['lat_eval'][-1])


def get_unimodal_lr_score(method: str):
    lr_eval_df = pd.read_csv(Path('data/thesis/lr_eval.csv'))
    return np.round(
        lr_eval_df[[k for k in lr_eval_df.columns if len(k.split('_')) == 1]].loc[lr_eval_df['Method'] == method].mean(
            axis=1).item(), decimals=3)


if __name__ == '__main__':
    # get_cond_gen_plot(method=r'joint\_elbo', which='m0__m0')
    # print(make_cond_gen_fig(which='m0_m1__m0', methods=['mopoe','mopgfm', 'moe', 'poe','mofop', 'iwmogfm_amortized', 'iwmogfm2'], dataset = 'polymnist'))
    # get_lr_score('mopoe')
    # get_lr_score('mofop')
    # get_lr_score('mopgfm')
    print(get_unimodal_lr_score(method='mopoe'))
    print(get_unimodal_lr_score(method='mopgfm'))
    print(get_unimodal_lr_score(method='mofop'))
