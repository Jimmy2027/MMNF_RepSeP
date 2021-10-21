from pathlib import Path
from shutil import rmtree

from modun.file_io import json2dict

data_dir = Path(__file__).parent.parent.parent / 'data'
exp_uids = json2dict(data_dir / 'thesis/experiment_uids.json')

experiments_dir = data_dir / 'thesis/experiments'

for dataset in ['polymnist', 'mimic']:
    for method in exp_uids[dataset]:
        for num_mods in exp_uids[dataset][method]:
            uids = exp_uids[dataset][method][num_mods]
            # for uid in uids:
            #     if not (experiments_dir / dataset / method / uid).exists():
            #         print(num_mods)
            #         print(uid)
            new_uids = [uid for uid in uids if (experiments_dir / dataset / method / uid).exists()]
            if not new_uids:
                new_uids = [""]
            exp_uids[dataset][method][num_mods] = new_uids

# dict2json(d=exp_uids, out_path=data_dir / 'thesis/experiment_uids.json')

# clean experiment_dirs
for dataset in ['polymnist', 'mimic']:
    for method_dir in (experiments_dir / dataset).iterdir():
        method = method_dir.name
        method_uids = [_id for _id in exp_uids[dataset][method][num_mods] for num_mods in exp_uids[dataset][method]]
        for exp_dir in method_dir.iterdir():
            exp_uid = exp_dir.name
            if not exp_uid in method_uids:
                print(f'deleting {exp_uid}')
                rmtree(exp_dir)
