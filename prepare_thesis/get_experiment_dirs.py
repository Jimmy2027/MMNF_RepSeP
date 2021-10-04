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
if experiment_uids_path.exists():
    os.remove(experiment_uids_path)
rsync_command = f'rsync -avP ethsec:{leomed_path} {experiment_uids_path}'
print(rsync_command)
os.system(rsync_command)

exp_uids = json2dict(experiment_uids_path)

for method in ['mopoe', 'mopgfm', 'moe', 'poe']:
    method_data_dir = data_dir / 'experiments' / method
    method_data_dir.mkdir(exist_ok=True)
    # for method in ['mopgfm']:
    for nbr_mods, uid_list in exp_uids[method].items():
        for uid in uid_list:
            dest_dir = method_data_dir / uid

            if dest_dir.exists() and not list((dest_dir / 'epoch_results').iterdir()):
                print(dest_dir)

            if not dest_dir.exists():

                if uid in db_uids:
                    get_exp_dir(_id=uid, dest_dir=dest_dir)
                else:
                    try:
                        unzip_to(path_to_zip_file=Path(conf['local_leomed_exp_dir']) / (uid + '.zip'),
                                 dest_path=dest_dir,
                                 verbose=True)
                    except Exception as e:
                        print(e)
