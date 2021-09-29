from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from scripts_ import tikz


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


def make_cond_gen_fig(which: str, methods: List[str]):
    split = which.split('__')
    in_mods = split[0]
    out_mod = split[-1]

    input_samples_dir = Path(f'data/thesis/{methods[0]}/cond_gen_plots/input_samples')
    cond_samples_path = {method: Path(f'data/thesis/{method}/cond_gen_plots/{in_mods}') for method in methods}

    pic = tikz.Picture()
    plot_xshift_base = 3

    yshift = 0
    for in_mod in in_mods.split('_'):
        xshift = plot_xshift_base
        for class_idx in range(10):
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
        pic.set_node(text=fr'\Large{{\textbf{{{method}}}}}', options=f'yshift=-{yshift}cm')
        xshift = plot_xshift_base
        for class_idx in range(10):
            img_name = f"{out_mod}_{class_idx}"

            pic.set_node(
                text=f'\\includegraphics[width=2cm]{{{cond_samples_path[method] / img_name}}}',
                options=f'xshift={xshift}cm, yshift=-{yshift}cm',
                name=f'outmod_{img_name}',
            )

            xshift += 2.1
        yshift += 2.1

    return pic.make()


if __name__ == '__main__':
    # get_cond_gen_plot(method=r'joint\_elbo', which='m0__m0')
    make_cond_gen_fig(which='m0_m1__m0', methods=['mogfm'])
