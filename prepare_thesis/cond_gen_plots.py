from pathlib import Path

from matplotlib import pyplot as plt
from mmvae_hub.experiment_vis.utils import save_cond_gen, show_generated_figs
from mmvae_hub.utils.utils import json2dict

data_dir = Path(__file__).parent.parent / 'data/thesis'
d = json2dict(data_dir / 'experiment_uids.json')
config = json2dict(Path('conf.json'))


def save_polymnist_example():
    method = 'mopoe'
    _id = d[method]['3_mods'][0]
    experiment_dir = data_dir / 'experiments' / method / _id

    save_path = data_dir / 'polymnist_example.png'
    cond_gen_plots = show_generated_figs(_id=_id, experiment_dir=experiment_dir, return_plots=True, nbr_samples_x=10,
                                         nbr_samples_y=0, epoch=config['max_epoch'])
    fig = cond_gen_plots['cond_gen_03']['m0_m1_m2__m0']

    plt.figure(figsize=(10, 10))
    plt.imshow(fig)
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()


def save_mnistsvhntext_example():
    _id = d['mopoe']['3_mods'][0]
    experiment_dir = data_dir / 'experiments' / method / _id

    save_path = data_dir / 'mnistsvhntext_example.png'
    cond_gen_plots = show_generated_figs(_id=_id, experiment_dir=experiment_dir, return_plots=True, nbr_samples_x=10,
                                         nbr_samples_y=0, epoch=config['max_epoch'])
    fig = cond_gen_plots['cond_gen_03']['m0_m1_m2__m0']

    plt.figure(figsize=(10, 10))
    plt.imshow(fig)
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()


def save_iw_comp_cond_gen():
    iw_comp = data_dir / 'iw_comp'
    iw_comp.mkdir(exist_ok=True)
    for method, method_d in d['iw_comparison'].items():
        method_dir = iw_comp / f'{method}/cond_gen_plots'
        method_dir.mkdir(exist_ok=True, parents=True)

        for K, uids in method_d.items():
            K_dir = method_dir / K
            K_dir.mkdir(exist_ok=True)
            for uid in uids:
                experiment_dir = data_dir / 'experiments/iw_comp' / method / uid
                save_cond_gen(save_path=K_dir, with_title=False, experiment_dir=experiment_dir, _id=uid,
                              epoch=config['max_epoch']['polymnist'] - 1)


if __name__ == '__main__':

    # save_polymnist_example()

    # for each method take the first _id and generate cond gen plots
    save_iw_comp_cond_gen()

    for dataset in ['mimic']:
        for method in ['mopgfm', 'mopoe', 'mofop']:
            # for method in config['methods']:
            save_path = data_dir / dataset / f'{method}/cond_gen_plots'
            save_path.mkdir(parents=True, exist_ok=True)

            _id = d[dataset][method]['3_mods'][0]
            experiment_dir = data_dir / 'experiments' / dataset / method / _id

            save_cond_gen(save_path=save_path, with_title=False, experiment_dir=experiment_dir, _id=_id,
                          epoch=config['max_epoch'][dataset] - 1)
