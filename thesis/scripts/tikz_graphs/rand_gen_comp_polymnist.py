from pathlib import Path

from modun.file_io import json2dict

from lib.utils import tex_escape
from scripts_ import tikz

conf = json2dict(Path('prepare_thesis/conf.json'))

methods = conf['methods']

pic = tikz.Picture()

yshift = 0
for method in methods:
    img_path = Path(f'data/thesis/polymnist/{method}/rand_gen_plot.png')
    pic.set_node(text=fr'\Large{{\textbf{{{tex_escape(method)}}}}}', options=f'yshift=-{yshift}cm', name=method)
    pic.set_node(text=f'\\includegraphics[scale=0.8]{{{img_path}}}', options=f'right of={method}, xshift=8.5cm')

    yshift += 6

print(pic.make())
