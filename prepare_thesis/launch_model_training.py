from pathlib import Path

from mmvae_hub.leomed_utils.launch_jobs import launch_leomed_jobs
from mmvae_hub.utils.setup.filehandling import get_experiment_uid
from mmvae_hub.utils.utils import json2dict, dict2json

end_epoch = 500
eval_freq = 500
nbr_repeats = 2

poe_args = {
    'method': 'poe',
    "initial_learning_rate": 0.0005,
    'class_dim': 512,
    "min_beta": 0,
    "max_beta": 2.5,
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
    "initial_learning_rate": 0.001,
    'class_dim': 512,
    "min_beta": 0,
    "max_beta": 2.5,
    "beta_warmup": 0,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
}

mopgfm_args = {
    'method': 'mopgfm',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 1.4,
    "beta_warmup": 50,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 64,
    "num_gfm_flows": 1,
    "nbr_coupling_block_layers": 5
}

mofop_args = {
    'method': 'mofop',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 1.,
    "beta_warmup": 50,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 128,
    "num_gfm_flows": 3,
    "nbr_coupling_block_layers": 8
}

iwmogfm_amortized_args = {
    'method': 'iwmogfm_amortized',
    "initial_learning_rate": 0.0005,
    'class_dim': 1280,
    "min_beta": 0,
    "max_beta": 0,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 512,
    "num_gfm_flows": 4,
    "nbr_coupling_block_layers": 2
}

# mogfm_args = {
#     'method': 'iwmogfm',
#     "initial_learning_rate": 0.0005,
#     'class_dim': 640,
#     "min_beta": 0,
#     "max_beta": 2.0,
#     "beta_warmup": 50,
#     "num_mods": 3,
#     "end_epoch": end_epoch,
#     "eval_freq": eval_freq,
#     "coupling_dim": 32,
#     "num_gfm_flows": 3,
#
# }

if __name__ == '__main__':
    experiment_uids_path = Path(__file__).parent.parent / 'data/thesis/experiment_uids.json'
    if experiment_uids_path.exists():
        exp_uids = json2dict(experiment_uids_path)
    else:
        experiment_uids_path.parent.mkdir(exist_ok=True, parents=True)
        exp_uids = {}

    for params in [poe_args, mopgfm_args, moe_args, mopoe_args, mofop_args]:
        # for params in [mofop_args]:
        method = params['method']

        if method not in exp_uids:
            exp_uids[method] = {}

        for num_mods in range(1, 6):
            params['num_mods'] = num_mods
            # more evaluation steps are needed for 3 mods
            if num_mods == 3:
                params['eval_freq'] = 100
            exp_uids[method][f'{num_mods}_mods'] = []

            for _ in range(nbr_repeats):
                experiment_uid = get_experiment_uid('polymnist', method=method)
                params["experiment_uid"] = experiment_uid
                params['dir_experiment'] = str(Path('~/klugh/mmvae_hub_data/experiments/mmnf_repsep').expanduser())

                exp_uids[method][f'{num_mods}_mods'].append(experiment_uid)

                launch_leomed_jobs(which_dataset='polymnist', params=params)

    dict2json(experiment_uids_path, d=exp_uids)
