from pathlib import Path

from mmvae_hub.leomed_utils.launch_jobs import launch_leomed_jobs
from mmvae_hub.utils.setup.filehandling import get_experiment_uid
from mmvae_hub.utils.utils import json2dict, dict2json

end_epoch = 150
eval_freq = 1000
nbr_repeats = 5

mopoe_args = {
    'method': 'mopoe',
    "initial_learning_rate": 0.0005,
    'class_dim': 640,
    "min_beta": 0,
    "max_beta": 2.0,
    "beta_warmup": 50,
    "num_gfm_flows": 3,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
}

mopgfm_args = {
    'method': 'mopgfm',
    "initial_learning_rate": 0.0005,
    'class_dim': 640,
    "min_beta": 0,
    "max_beta": 2.0,
    "beta_warmup": 50,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 32,
    "num_gfm_flows": 3,

}

mogfm_args = {
    'method': 'iwmogfm',
    "initial_learning_rate": 0.0005,
    'class_dim': 640,
    "min_beta": 0,
    "max_beta": 2.0,
    "beta_warmup": 50,
    "num_mods": 3,
    "end_epoch": end_epoch,
    "eval_freq": eval_freq,
    "coupling_dim": 32,
    "num_gfm_flows": 3,

}

if __name__ == '__main__':
    experiment_uids_path = Path('../data/experiment_uids.json')
    if experiment_uids_path.exists():
        exp_uids = json2dict(experiment_uids_path)
    else:
        exp_uids = {}

    for params in [mopoe_args]:
        for _ in range(nbr_repeats):
            experiment_uid = get_experiment_uid('polymnist', method=params['method'])
            params["experiment_uid"] = experiment_uid
            if 'method' not in exp_uids:
                params["method"] = []
            exp_uids['method'].append(experiment_uid)
            launch_leomed_jobs(which_dataset='polymnist', params=params)

    dict2json(experiment_uids_path, d=exp_uids)
