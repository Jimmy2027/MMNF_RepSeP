from mmvae_hub.leomed_utils.launch_jobs import launch_leomed_jobs

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
    "end_epoch": 150,
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
    "end_epoch": 150,
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
    "end_epoch": 150,
    "eval_freq": eval_freq,
    "coupling_dim": 32,
    "num_gfm_flows": 3,

}

if __name__ == '__main__':

    for params in [mopoe_args]:
        for _ in range(nbr_repeats):
            launch_leomed_jobs(which_dataset='polymnist', params=params)
