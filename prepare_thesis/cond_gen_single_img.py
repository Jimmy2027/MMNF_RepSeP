from pathlib import Path

from matplotlib import pyplot as plt
from mmvae_hub.experiment_vis.utils import save_cond_gen, show_generated_figs
from mmvae_hub.utils.utils import json2dict

data_dir = Path(__file__).parent.parent / 'data/thesis'
d = json2dict(data_dir / 'experiment_uids.json')
config = json2dict(Path('conf.json'))


def save_plots(_id, experiment_dir: Path, save_path, method: str):
    cond_gen_plots = show_generated_figs(_id=_id, experiment_dir=experiment_dir, return_plots=True, nbr_samples_x=10,
                                         nbr_samples_y=1)

    for p_key, ps in cond_gen_plots.items():
        for name, fig in ps.items():
            plt.figure(figsize=(10, 10))
            plt.imshow(fig)
            title = fr'\textbf{{{method}}}: ' + name.replace('__', r'$\rightarrow$')
            plt.title(title)
            plt.axis('off')
            plt.savefig(save_path / name, bbox_inches='tight', pad_inches=0)
            plt.close()


if __name__ == '__main__':
    config = json2dict(Path('conf.json'))
    for dataset in ['mimic']:
        for method in ['mopoe', 'mofop']:
            # for method in config['methods']:
            save_path = data_dir / dataset / f'{method}/cond_gen_single_imgs'
            save_path.mkdir(parents=True, exist_ok=True)

            _id = d[dataset][method]['3_mods'][0]
            experiment_dir = data_dir / 'experiments' / dataset / method / _id

            save_cond_gen(_id=_id, save_path=save_path, experiment_dir=experiment_dir,
                          epoch=config['max_epoch'][dataset])

            # save_plots(save_path=save_path, experiment_dir=experiment_dir, _id=_id, method=method)
