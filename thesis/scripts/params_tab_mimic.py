from pathlib import Path

import pandas as pd
from modun.file_io import json2dict

from prepare_thesis.launch_model_training import mopoe_mimic_args, mofop_mimic_args, mopgfm_mimic_args

config = json2dict(Path('prepare_thesis/conf.json'))

method_args_mapping = {
    'mopoe': mopoe_mimic_args,
    'mofop': mofop_mimic_args,
    'mopgfm': mopgfm_mimic_args,

}


def df_maker():
    for method in method_args_mapping:
        args = method_args_mapping[method]
        if method == 'mofop':
            args['num_gfm_flows'] = args['num_flows']
        yield {
            k: v
            for k, v in args.items()
            if k not in ['eval_freq', 'beta_warmup', 'min_beta', 'num_mods', 'num_flows', 'K']
        }


df = pd.DataFrame(data=df_maker()).astype({'coupling_dim': pd.Int16Dtype(), 'num_gfm_flows': pd.Int8Dtype(),
                                           'nbr_coupling_block_layers': pd.Int8Dtype()}).rename(
    columns={'method': 'Method',
             'class_dim': 'Class Dim',
             'max_beta': 'beta',
             'coupling_dim': 'Coupling Dim',
             'initial_learning_rate': 'Learning Rate',
             'num_gfm_flows': 'Nbr Flows',
             'nbr_coupling_block_layers': 'Nbr Coupling Block layers',
             'end_epoch': 'End Epoch'})
df = df.set_index('Method')

print(df[sorted(df.columns)].to_latex(escape=True).replace('<NA>', r'').replace('\\toprule', '').replace('\\midrule', '').replace(
    '\\bottomrule', '').replace('lrrrrrr', 'ccccccc'))
