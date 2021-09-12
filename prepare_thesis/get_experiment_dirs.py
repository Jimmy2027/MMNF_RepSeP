"""Get the experiment dirs from leomed"""
import os
from pathlib import Path
from modun.zip_utils import unzip_to
from mmvae_hub.utils.utils import json2dict
import os
data_dir = Path('../data/thesis')
data_dir.mkdir(exist_ok=True, parents=True)

conf = json2dict(Path('conf.json'))

# get experiment_uids from leomed
leomed_path = Path(conf['data_dir_leomed']) / 'experiment_uids.json'
experiment_uids_path = data_dir / ('experiment_uids.json')
if experiment_uids_path.exists():
    os.remove(experiment_uids_path)
rsync_command = f'rsync -avP ethsec:{leomed_path} {experiment_uids_path}'
print(rsync_command)
os.system(rsync_command)

exp_uids = json2dict(experiment_uids_path)

for method in ['mopgfm', 'moe']:
# for method in ['mopgfm']:
    for nbr_mods, uid_list in exp_uids[method].items():
        for uid in uid_list:
            try:
                unzip_to(path_to_zip_file=Path(conf['local_leomed_exp_dir']) / (uid + '.zip'), dest_path=data_dir / uid,
                         verbose=True)
            except Exception as e:
                print(e)
