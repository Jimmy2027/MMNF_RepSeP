from pathlib import Path

import pandas as pd

from lib.utils import get_stats_and_bold_max_column_value
from thesis.scripts.utils import METHODS, method_footnote_mapping

gen_eval_df = pd.read_csv(Path('data/thesis/prd_eval.csv'))
gen_eval_df = gen_eval_df.loc[gen_eval_df.Method.isin(METHODS)]
gen_eval_df = gen_eval_df.set_index('Method')

text = (get_stats_and_bold_max_column_value(gen_eval_df, except_cols={'Best score'})
        .replace('\\toprule', '').replace('\\midrule', '').replace('\\bottomrule', '').replace('lrrl', 'lccc'))

for k, v in method_footnote_mapping.items():
    text = text.replace(k, v)
print(text)




