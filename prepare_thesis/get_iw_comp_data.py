from pathlib import Path

import numpy as np
import pandas as pd
from modun.dict_utils import flatten_dict
from modun.file_io import json2dict

conf = json2dict(Path('conf.json'))
data_dir = Path(__file__).parent.parent / 'data/thesis'
exp_uids = json2dict(data_dir / 'experiment_uids.json')


def df_maker():
    for method in exp_uids['iw_comparison']:
        d = {}
        for K in [1, 3, 5]:
            if K == 1:
                method_ = method.replace('iw', '')
                uid = exp_uids['polymnist'][method_]['3_mods'][0]
                exp_dir = data_dir / f'experiments/polymnist/{method_}/{uid}'
            else:
                uid = exp_uids['iw_comparison'][method][f"K{K}"][0]
                exp_dir = data_dir / f"experiments/iw_comp/{method}/{uid}"

            res_dict = json2dict(exp_dir / f"epoch_results/{conf['max_epoch']['polymnist'] - 1}.json")
            d[f'lr_{K}'] = np.mean([v['accuracy'] for _, v in res_dict['test_results']['lr_eval_q0'].items()])
            d[f'coherence_{K}'] = np.mean([v for _, v in flatten_dict(res_dict['test_results']['gen_eval']).items()])
            d[f'prd_{K}'] = np.mean([v for _, v in flatten_dict(res_dict['test_results']['prd_scores']).items()])
        d['method'] = method
        yield d


iw_comp_df = pd.DataFrame(data=df_maker())

iw_comp_df.to_csv(Path(__file__).parent.parent / 'data/thesis/iw_comp.csv', index=False)
