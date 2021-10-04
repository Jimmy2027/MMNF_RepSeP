from pathlib import Path

import pandas as pd
from modun.file_io import json2dict

from prepare_thesis.launch_model_training import poe_args, mopoe_args, moe_args, mopgfm_args

config = json2dict(Path('prepare_thesis/conf.json'))

method_args_mapping = {
    'mopoe': mopoe_args,
    'poe': poe_args,
    'moe': moe_args,
    'mopgfm': mopgfm_args
}


def df_maker():
    for method in config['methods']:
        args = method_args_mapping[method]
        yield {
            k: v
            for k, v in args.items()
            if k not in ['eval_freq', 'beta_warmup', 'min_beta', 'num_mods']
        }


df = pd.DataFrame(data=df_maker()).astype({'coupling_dim': pd.Int16Dtype(), 'num_gfm_flows': pd.Int8Dtype(),
                                           'nbr_coupling_block_layers': pd.Int8Dtype()}).rename(
    columns={'method': 'Method',
             'initial_learning_rate': 'Learning Rate',
             'class_dim': 'Class Dim',
             'max_beta': 'beta',
             'coupling_dim': 'Coupling Dim',
             'num_gfm_flows': 'Nbr GfM Flows',
             'nbr_coupling_block_layers': 'Nbr Coupling Block layers',
             'end_epoch': 'End Epoch'})
df = df.set_index('Method')

print(df.to_latex(escape=True).replace('<NA>', r'').replace('\\toprule', '').replace('\\midrule', '').replace(
    '\\bottomrule', '').replace('lrrrrrrr', 'cccccccc'))
