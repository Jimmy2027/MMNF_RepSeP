from pathlib import Path
# tikz_mod_path = Path('scripts')
# import sys
# sys.path.append(tikz_mod_path)

from scripts_ import tikz
from dataclasses import dataclass


@dataclass
class Nodes:
    input_m0: str = '$M_0$'
    input_mK: str = '$M_K$'
    encoder: str = 'Encoder'
    lr: str = 'Latent Representation'
    decoder: str = 'Decoder'
    out_m0: str = '$M_0$'
    out_mK: str = '$M_K$'
    points: str = r'\ldots'


nodes = Nodes()
pic = tikz.Picture('modalities/.style={rectangle, draw=green!60, fill=green!5, very thick, minimum size=10mm},'
                   'model/.style={rectangle, draw=red!60, fill=red!5, very thick, minimum size=20mm},'
                   'lr/.style={ellipse, draw=blue!60, fill=blue!5, very thick, minimum size=15mm}')

pic.set_node(text=nodes.input_m0, options='modalities', name='input_m0')
pic.set_node(text=nodes.points, options=' below of=input_m0', name='input_points')
pic.set_node(text=nodes.input_mK, options='modalities, below of=input_points', name='input_mK')
pic.set_node(text=nodes.encoder, options='model, right of=input_points, xshift=2cm', name='encoder')
pic.set_node(text=nodes.lr, options='lr, right of=encoder, xshift=3cm', name='lr')
pic.set_node(text=nodes.decoder, options='model, right of=lr, xshift=3cm', name='decoder')
pic.set_node(text=nodes.points, options=' right of=decoder, xshift=2cm', name='out_points')
pic.set_node(text=nodes.out_m0, options='modalities, above of=out_points', name='out_m0')
pic.set_node(text=nodes.out_mK, options='modalities, below of=out_points', name='out_mK')

pic.set_line('input_m0', 'encoder')
pic.set_line('input_points', 'encoder')
pic.set_line('input_mK', 'encoder')
pic.set_line('encoder', 'lr')
pic.set_line('lr', 'decoder')
pic.set_line('decoder', 'out_m0')
pic.set_line('decoder', 'out_points')
pic.set_line('decoder', 'out_mK')

output = r'\resizebox{\textwidth}{!}{% ' + '\n' + pic.make() + '}'
print(output)
