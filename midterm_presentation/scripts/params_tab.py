from pathlib import Path

import pandas as pd

from midterm_presentation.scripts.utils import METHODS

df = pd.read_csv(Path('data/params_tab.csv'))
df = df.loc[df.method.isin(METHODS)]
df = df.dropna(how='all', axis=1)
df = df.set_index('method').fillna(r'$\sim$')
df = df.rename(columns={k: k.replace("_", "\\_") for k in df.columns})
print(
    df.to_latex(escape=False).replace('\\toprule', '').replace('\\midrule', '').replace('\\bottomrule', '').replace('lrrrrrl', 'lcccccc'))
