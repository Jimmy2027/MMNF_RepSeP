from pathlib import Path

from mmvae_hub.leomed_utils.launch_jobs import launch_leomed_jobs
from mmvae_hub.utils.setup.filehandling import get_experiment_uid
from mmvae_hub.utils.utils import json2dict, dict2json

conf = json2dict(Path(__file__).parent / 'conf.json')
end_epoch = conf['max_epoch']['polymnist']
eval_freq = 500
nbr_repeats = 5

poe_args = {
    'method': 'poe',
    "initial_learning_rate": 0.0005,
    'class_dim': 512,
    "min_beta": 0,
    "max_beta": 2.,
    "beta_warmup": 0,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
}

moe_args = {
    'method': 'moe',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 2.0,
    "beta_warmup": 0,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
}

mopoe_args = {
    'method': 'mopoe',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 2.,
    "beta_warmup": 0,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
}

iwmopoe_args = {
    'method': 'iwmopoe',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 2.,
    "beta_warmup": 0,
    "num_mods": 3,
    "K": [3, 5],
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
}

mopgfm_args = {
    'method': 'mopgfm',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 2.,
    "beta_warmup": 50,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 64,
    "num_gfm_flows": 1,
    "nbr_coupling_block_layers": 8
}

iwmopgfm_args = {
    'method': 'iwmopgfm',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 2.,
    "beta_warmup": 50,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 64,
    "num_gfm_flows": 1,
    "nbr_coupling_block_layers": 8,
    "K": [3, 5],
}

mofop_args = {
    'method': 'mofop',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 2.,
    "beta_warmup": 50,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 64,
    "num_flows": 1,
    "nbr_coupling_block_layers": 8
}

mogfm_amortized_args = {
    'method': 'mogfm_amortized',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 0,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 512,
    "num_gfm_flows": 4,
    "nbr_coupling_block_layers": 2,
    "K": 1
}

iwmogfm2_args = {
    'method': 'iwmogfm2',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 0,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 512,
    "num_gfm_flows": 4,
    "nbr_coupling_block_layers": 2,
    "K": 2,
}

mopoe_mimic_args = {
    'method': 'mopoe',
    "initial_learning_rate": 0.0005,
    'class_dim': 512,
    "min_beta": 0,
    "max_beta": 1.,
    "beta_warmup": 50,
    "end_epoch": conf['max_epoch']['mimic'],
    "eval_freq": 50,
}

mofop_mimic_args = {
    'method': 'mofop',
    "initial_learning_rate": 0.0005,
    'class_dim': 512,
    "min_beta": 0,
    "max_beta": 1.,
    "beta_warmup": 50,
    "end_epoch": conf['max_epoch']['mimic'],
    "eval_freq": 50,
    "coupling_dim": 64,
    "num_flows": 3,
    "nbr_coupling_block_layers": 8
}

mopgfm_mimic_args = {
    'method': 'mopgfm',
    "initial_learning_rate": 0.0005,
    'class_dim': 512,
    "min_beta": 0,
    "max_beta": 1.,
    "beta_warmup": 50,
    "end_epoch": conf['max_epoch']['mimic'],
    "eval_freq": 50,
    "coupling_dim": 64,
    "num_gfm_flows": 3,
    "nbr_coupling_block_layers": 8
}


def launch_polymnist_training():
    experiment_uids_path = Path(__file__).parent.parent / 'data/thesis/experiment_uids.json'
    dataset = 'polymnist'
    if experiment_uids_path.exists():
        exp_uids = json2dict(experiment_uids_path)
    else:
        experiment_uids_path.parent.mkdir(exist_ok=True, parents=True)
        exp_uids = {dataset: {}}

    for params in [mopoe_args, poe_args, moe_args, mopgfm_args, mofop_args, iwmogfm2_args, mogfm_amortized_args]:
        # for params in [mofop_args]:
        method = params['method']

        if method not in exp_uids[dataset]:
            exp_uids[dataset][method] = {}

        for num_mods in range(1, 5):
            params['num_mods'] = num_mods
            # more evaluation steps are needed for 3 mods
            if num_mods == 3:
                params['eval_freq'] = 100
            exp_uids[dataset][method][f'{num_mods}_mods'] = []

            for _ in range(nbr_repeats):
                experiment_uid = get_experiment_uid('polymnist', method=method)
                params["experiment_uid"] = experiment_uid

                exp_uids[dataset][method][f'{num_mods}_mods'].append(experiment_uid)

                launch_leomed_jobs(which_dataset='polymnist', params=params)

    dict2json(experiment_uids_path, d=exp_uids)


def launch_mimic_training():
    experiment_uids_path = Path(__file__).parent.parent / 'data/thesis/experiment_uids.json'
    dataset = 'mimic'
    if experiment_uids_path.exists():
        exp_uids = json2dict(experiment_uids_path)
    else:
        experiment_uids_path.parent.mkdir(exist_ok=True, parents=True)
        exp_uids = {dataset: {}}

    for params in [mopoe_mimic_args, mofop_mimic_args, mopgfm_mimic_args]:
        method = params['method']

        if method not in exp_uids[dataset]:
            exp_uids[dataset][method] = {}

        num_mods = 3
        exp_uids[dataset][method][f'{num_mods}_mods'] = []

        experiment_uid = get_experiment_uid('mimic', method=method)
        params["experiment_uid"] = experiment_uid

        exp_uids[dataset][method][f'{num_mods}_mods'].append(experiment_uid)

        launch_leomed_jobs(which_dataset='mimic', params=params)

    dict2json(experiment_uids_path, d=exp_uids)


if __name__ == '__main__':
    launch_polymnist_training()
    launch_mimic_training()
