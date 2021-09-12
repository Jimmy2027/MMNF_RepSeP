from pathlib import Path

from matplotlib import pyplot as plt
from mmvae_hub.experiment_vis.utils import save_cond_gen, show_generated_figs
from mmvae_hub.utils.utils import json2dict

d = json2dict(Path('../data/thesis/experiment_uids.json'))
data_dir = Path('../data/thesis')


def save_polymnist_example():
    _id = d['mopoe']['3_mods'][0]
    experiment_dir = data_dir / _id

    save_path = data_dir / f'polymnist_example.png'
    cond_gen_plots = show_generated_figs(_id=_id, experiment_dir=experiment_dir, return_plots=True, nbr_samples_x=10,
                                         nbr_samples_y=0)
    fig = cond_gen_plots['cond_gen_03']['m0_m1_m2__m0']

    plt.figure(figsize=(10, 10))
    plt.imshow(fig)
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()


def save_mnistsvhntext_example():
    _id = d['mopoe']['3_mods'][0]
    experiment_dir = data_dir / _id

    save_path = data_dir / f'mnistsvhntext_example.png'
    cond_gen_plots = show_generated_figs(_id=_id, experiment_dir=experiment_dir, return_plots=True, nbr_samples_x=10,
                                         nbr_samples_y=0)
    fig = cond_gen_plots['cond_gen_03']['m0_m1_m2__m0']

    plt.figure(figsize=(10, 10))
    plt.imshow(fig)
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()


if __name__ == '__main__':

    save_polymnist_example()

    for method in ['mopoe']:
        save_path = data_dir / f'{method}/cond_gen_plots'
        save_path.mkdir(parents=True, exist_ok=True)

        _id = d[method]['3_mods'][0]
        experiment_dir = data_dir / _id

        save_cond_gen(save_path=save_path, with_title=False, experiment_dir=experiment_dir, _id=_id)
