from pathlib import Path

import pandas as pd

from lib.utils import bold_max_column_value, get_stats_and_bold_max_column_value
from midterm_presentation.scripts.utils import METHODS, method_footnote_mapping

lr_eval_df = pd.read_csv(Path('data/thesis/lr_eval.csv'))
lr_eval_df = lr_eval_df.loc[lr_eval_df.Method.isin(METHODS)]
lr_eval_df = lr_eval_df.set_index('Method')

text = get_stats_and_bold_max_column_value(lr_eval_df, escape_colnames=True,
                                           column_order=['m0', 'm1', 'm2', 'm0_m1', 'm0_m2', 'm1_m2', 'm0_m1_m2']) \
    .replace('\\toprule', '') \
    .replace('\\midrule', '') \
    .replace('\\bottomrule', '') \
    .replace('lrrrrrrr', 'lccccccc')

for k, v in method_footnote_mapping.items():
    text = text.replace(k, v)
print(text)
