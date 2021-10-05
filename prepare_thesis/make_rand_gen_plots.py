import random
from pathlib import Path

import torch
from matplotlib import pyplot as plt
from mmvae_hub.experiment_vis.utils import load_experiment
from mmvae_hub.utils.plotting import plot
from modun.file_io import json2dict

data_dir = Path(__file__).parent.parent / 'data/thesis'
exp_uids = json2dict(data_dir / 'experiment_uids.json')

num_samples = 30

# for method in ['mopoe', 'mopgfm', 'moe']:
for method in ['mofop', 'iwmogfm_amortized', 'poe']:
    save_path = data_dir / f'{method}/rand_gen_plot.png'

    _id = exp_uids[method]['3_mods'][0]
    experiment_dir = data_dir / _id

    exp = load_experiment(experiment_dir=experiment_dir, _id=_id)

    model = exp.mm_vae
    mods = exp.modalities
    random_samples = model.generate(num_samples)
    m_keys = list(mods.keys())

    rec = torch.zeros(mods['m0'].plot_img_size,
                      dtype=torch.float32).repeat(num_samples, 1, 1, 1)
    for l in range(num_samples):
        m_key_in = random.choice(m_keys)
        mod = mods[m_key_in]
        samples_mod = random_samples[m_key_in]
        rand_plot = mod.plot_data(samples_mod[l])
        rec[l, :, :, :] = rand_plot

    fig = plot.create_fig('', rec, 10, save_figure=False)

    plt.figure(figsize=(10, 10))
    plt.imshow(fig)
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()
