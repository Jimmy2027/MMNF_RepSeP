import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from mmvae_hub.evaluation.eval_metrics.coherence import save_generated_samples
from mmvae_hub.evaluation.eval_metrics.sample_quality import calc_prd_score
from mmvae_hub.experiment_vis.utils import load_experiment
from mmvae_hub.hyperopt.hyperopt_metrics import get_missing_mod_scores_prd, get_reconstr_mod_scores_prd
from mmvae_hub.utils.MongoDB import MongoDatabase
from mmvae_hub.utils.plotting.save_samples import save_generated_samples_singlegroup
from mmvae_hub.utils.utils import at_most_n, dict_to_device
from modun.file_io import json2dict, dict2json
from torch.utils.data import DataLoader
from tqdm import tqdm

from utils import get_experiments_df


def df_maker(epoch: int, data_dir: Path):
    config = json2dict(Path(('conf.json')))
    methods = config['methods']
    data_dir = data_dir / 'thesis'
    experiment_uids_path = data_dir / ('experiment_uids.json')
    exp_uids = json2dict(experiment_uids_path)

    for method in methods:
        method_uids = exp_uids[method]['3_mods']

        d = {'missing_mod_scores': [], 'reconstr_mod_scores': [], 'random_prd_scores': []}
        for method_uid in method_uids:
            epoch_results_dir = data_dir / 'experiments' / method / method_uid / 'epoch_results'

            prd_dict = json2dict(epoch_results_dir / f'{epoch}.json')['test_results']['prd_scores']

            if prd_dict is None:
                tmpdirname = Path('/mnt/data/hendrik/mmnf_data/tempdir')
                tmpdirname.mkdir()
                experiment_dir = data_dir / 'experiments' / method / method_uid
                exp = load_experiment(experiment_dir, _id=method_uid, epoch=epoch,
                                      add_args={'dir_gen_eval_fid': tmpdirname})
                args = exp.flags
                mm_vae = exp.mm_vae
                rand_gen = mm_vae.generate()
                d_loader = DataLoader(exp.dataset_test,
                                      batch_size=args.batch_size,
                                      shuffle=True,
                                      num_workers=exp.flags.dataloader_workers, drop_last=True)
                for iteration, (batch_d, batch_l) in tqdm(enumerate(d_loader), total=len(d_loader)):
                    batch_d = dict_to_device(batch_d, exp.flags.device)
                    save_generated_samples(exp, rand_gen, iteration, batch_d)
                    _, joint_latent = mm_vae.inference(batch_d)
                    cg = mm_vae.cond_generation(joint_latent)
                    for subset, cond_val in cg.items():
                        save_generated_samples_singlegroup(exp, iteration, subset, cond_val)
                prd_dict = calc_prd_score(exp)
                ep_res_dict = json2dict(epoch_results_dir / f'{epoch}.json')

                ep_res_dict['test_results']['prd_scores'] = prd_dict
                dict2json(out_path=epoch_results_dir / f'{epoch}.json', d=ep_res_dict)
                tmpdirname.rmdir()

            d['random_prd_scores'].append(
                np.mean([score for k, score in prd_dict.items() if k.startswith('random')]))

            prd_dict = {k: v for k, v in prd_dict.items() if not k.startswith('random')}

            d['missing_mod_scores'].append(np.mean([score for score in get_missing_mod_scores_prd(
                prd_dict)]))
            d['reconstr_mod_scores'].append(np.mean([score for score in get_reconstr_mod_scores_prd(
                prd_dict)]))

        yield {
            'Method': method,
            'Missing Mod': np.round(np.mean(d['missing_mod_scores']), 3),
            'Reconstruction': np.round(np.mean(d['reconstr_mod_scores']), 3),
            'Random': np.round(np.mean(d['random_prd_scores']), 3),
            'Missing Mod__STDEV': np.round(np.std(d['missing_mod_scores']), 3),
            'Reconstruction__STDEV': np.round(np.std(d['reconstr_mod_scores']), 3),
            'Random__STDEV': np.round(np.std(d['random_prd_scores']), 3),
        }


if __name__ == '__main__':
    config = json2dict(Path('conf.json'))

    prd_eval_df = pd.DataFrame(data=df_maker(epoch=config['max_epoch'], data_dir=Path(config['data_dir'])))

    prd_eval_df.to_csv(Path(__file__).parent.parent / 'data/thesis/prd_eval.csv', index=False)
