from pathlib import Path

import pandas as pd
import torch
from matplotlib import pyplot as plt

data_path = Path('/Users/Hendrik/data/mimic_scratch')
test_df = pd.read_csv(data_path / 'test.csv')
test_pa_imgs = torch.load(data_path / 'files_small_128/test_pa.pt')
lung_opac = test_df.loc[test_df['Support Devices'] == 1]

for idx, row in lung_opac.iterrows():
    print(idx)
    plt.imshow(test_pa_imgs[idx], cmap='gray')
    plt.axis('off')
    plt.show()
    asdf=0

sdfsa = 0
