from pathlib import Path

import pandas as pd

from lib.utils import bold_max_column_value
from midterm_presentation.scripts.utils import METHODS, method_footnote_mapping

lr_eval_df = pd.read_csv(Path('data/lr_eval.csv'))
lr_eval_df = lr_eval_df.loc[lr_eval_df.method.isin(METHODS)]

lr_eval_df = lr_eval_df.set_index('method')
lr_eval_df = lr_eval_df[['m0', 'm1', 'm2', 'm0_m1', 'm0_m2', 'm1_m2', 'm0_m1_m2']]
lr_eval_df = lr_eval_df.rename(columns={k: k.replace("_", "\\_") for k in lr_eval_df.columns})

text = bold_max_column_value(lr_eval_df).replace('\\toprule', '').replace('\\midrule', '').replace('\\bottomrule',
                                                                                                   '').replace(
    'lrrrrrrr', 'lccccccc')

for k, v in method_footnote_mapping.items():
    text = text.replace(k, v)
print(text)