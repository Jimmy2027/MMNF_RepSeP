import typing
from pathlib import Path

import numpy as np
import pandas as pd
from modun.file_io import json2dict

from lib.utils import bold_max_column_value
from thesis.scripts.utils import METHODS, method_footnote_mapping


def get_stats_and_bold_max_column_value(df, except_cols: typing.Iterable[str] = None):
    """
    Detect numeric values in a pandas dataframe LaTeX string (as produced by df.to_latex()), and highlight the largest
    value of each column by wrapping it with a LaTeX bold tag (\textbf{}).

    Parameters
    ----------
    df :  pandas.DataFrame
            Pandas DataFrame object containing at least one column with only numerical values.
    """
    stdev_cols = [col for col in df.columns if col.endswith('__STDEV')]

    if except_cols is None:
        except_cols = {*stdev_cols}
    else:
        except_cols = {*except_cols, *stdev_cols}

    for col in df.columns:
        if col not in except_cols:
            df[col].loc[df[col] == df[col].max()] = rf'\textbf{{{np.round(df[col].max(), 3)}}}'

            for idx in range(len(df)):
                df[col].iloc[idx] = f"${df[col].iloc[idx]} \\pm  {df[col + '__STDEV'].iloc[idx]}$"

    return df[[*[col for col in df.columns if col not in except_cols]]].to_latex(escape=False)


gen_eval_df = pd.read_csv(Path('data/thesis/gen_eval.csv'))
gen_eval_df = gen_eval_df.loc[gen_eval_df.Method.isin(METHODS)]
gen_eval_df = gen_eval_df.set_index('Method')

text = (get_stats_and_bold_max_column_value(gen_eval_df, except_cols={'Best score'})
        .replace('\\toprule', '').replace('\\midrule', '').replace('\\bottomrule', '').replace('lrrl', 'lccc'))

for k, v in method_footnote_mapping.items():
    text = text.replace(k, v)
print(text)
