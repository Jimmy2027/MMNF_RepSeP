from pathlib import Path

import pandas as pd

from lib.utils import bold_max_column_value
from midterm_presentation.scripts.utils import METHODS, method_footnote_mapping

prd_eval_df = pd.read_csv(Path('data/lhood_eval.csv'))
# prd_eval_df = prd_eval_df.loc[prd_eval_df.method.isin(METHODS)]
prd_eval_df = prd_eval_df.set_index('method')
prd_eval_df = prd_eval_df.rename(columns={k: k.replace("_", "\\_") for k in prd_eval_df.columns})
text = (bold_max_column_value(prd_eval_df, except_cols={'Best score'})
      .replace('\\toprule', '').replace('\\midrule', '').replace('\\bottomrule', '').replace('lrrl', 'lccc'))

for k, v in method_footnote_mapping.items():
    text = text.replace(k, v)
print(text)