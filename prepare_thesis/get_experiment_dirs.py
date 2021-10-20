"""Get the experiment dirs from leomed"""
import os
from pathlib import Path

from mmvae_hub.experiment_vis.utils import get_exp_dir
from mmvae_hub.utils.MongoDB import MongoDatabase
from mmvae_hub.utils.utils import json2dict

from modun.zip_utils import unzip_to

data_dir = Path(__file__).parent.parent / 'data/thesis'
data_dir.mkdir(exist_ok=True, parents=True)

conf = json2dict(Path('conf.json'))

if conf['use_db']:
    exp_db = MongoDatabase(training=False)
    experiments = exp_db.connect()
    db_uids = {exp['_id'] for exp in experiments.find({})}
else:
    db_uids = []

# get experiment_uids from leomed
leomed_path = Path(conf['data_dir_leomed']) / 'experiment_uids.json'
experiment_uids_path = data_dir / ('experiment_uids.json')

# remove existing experiment_uids
# if experiment_uids_path.exists():
#     os.remove(experiment_uids_path)

rsync_command = f'rsync -avP ethsec:{leomed_path} {experiment_uids_path}'
print(rsync_command)
# os.system(rsync_command)

exp_uids = json2dict(experiment_uids_path)

# get experiments for iw comparison
iw_comp_out_dir = data_dir / 'experiments/iw_comp'
iw_comp_out_dir.mkdir(exist_ok=True)
for method, d in exp_uids['iw_comparison'].items():
    method_dir = iw_comp_out_dir / method
    method_dir.mkdir(exist_ok=True)
    for K_nbr, uids in d.items():
        for uid in uids:
            dest_dir = method_dir / uid
            if not dest_dir.exists() and uid:
                if uid in db_uids:
                    get_exp_dir(_id=uid, dest_dir=dest_dir)
                else:
                    try:
                        unzip_to(path_to_zip_file=Path(conf['local_leomed_exp_dir']) / (uid + '.zip'),
                                 dest_path=dest_dir,
                                 verbose=True)
                    except Exception as e:
                        print(e)

# for dataset in exp_uids:
# for dataset in ['mimic']:
for dataset in ['mimic']:
    dataset_data_dir = data_dir / 'experiments' / dataset
    dataset_data_dir.mkdir(exist_ok=True)

    for method in ['mopgfm']:
        method_data_dir = dataset_data_dir / method
        method_data_dir.mkdir(exist_ok=True)
        # for method in ['mopgfm']:
        for nbr_mods, uid_list in exp_uids[dataset][method].items():
            for uid in uid_list:
                dest_dir = method_data_dir / uid

                if not dest_dir.exists() and uid:

                    if uid in db_uids:
                        get_exp_dir(_id=uid, dest_dir=dest_dir)
                    else:
                        try:
                            unzip_to(path_to_zip_file=Path(conf['local_leomed_exp_dir']) / (uid + '.zip'),
                                     dest_path=dest_dir,
                                     verbose=True)
                        except Exception as e:
                            print(e)
