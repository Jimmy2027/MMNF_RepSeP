from pathlib import Path

from mmvae_hub.utils.utils import dict2json
from modun.file_io import json2dict

data_dir = Path(__file__).parent.parent.parent / 'data'
exp_uids = json2dict(data_dir / 'thesis/experiment_uids.json')

experiments_dir = data_dir / 'thesis/experiments'

for method in exp_uids:
    for num_mods in exp_uids[method]:
        uids = exp_uids[method][num_mods]
        new_uids = [uid for uid in uids if (experiments_dir / method / uid).exists()]
        exp_uids[method][num_mods] = new_uids

dict2json(d=exp_uids, out_path=data_dir / 'thesis/experiment_uids.json')
