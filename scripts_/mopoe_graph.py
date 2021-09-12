from dataclasses import dataclass
from pathlib import Path

from scripts_ import tikz

cond_samples_path = Path('data/thesis/mopoe/cond_gen_single_imgs')
input_samples_dir = cond_samples_path / 'input_samples'


@dataclass
class Nodes:
    input_m1: str = f'\\includegraphics[width=2cm]{{{str(input_samples_dir / "m2_0.png")}}}'
    input_m0: str = f'\\includegraphics[width=2cm]{{{str(input_samples_dir / "m1_0.png")}}}'
    output__m1m2_m2: str = f'\\includegraphics[width=2cm]{{{str(cond_samples_path / "m1_m2" / "m2_0.png")}}}'
    output__m1m2_m1: str = f'\\includegraphics[width=2cm]{{{str(cond_samples_path / "m1_m2" / "m1_0.png")}}}'
    output__m2_m1: str = f'\\includegraphics[width=2cm]{{{str(cond_samples_path / "m2" / "m1_0.png")}}}'
    output__m1_m2: str = f'\\includegraphics[width=2cm]{{{str(cond_samples_path / "m1" / "m2_0.png")}}}'
    q1: str = r'$q_{\phi_1}$'
    q2: str = r'$q_{\phi_2}$'
    q1_tilde: str = r'$\tilde{q}_{\phi_1}$'
    q2_tilde: str = r'$\tilde{q}_{\phi_2}$'
    q12_tilde: str = r'$\tilde{q}_{\phi_{12}}$'
    poe: str = r'\textbf{PoE}'
    moe: str = r'\textbf{MoE}'
    z: str = r'joint\\ posterior'
    points: str = r'\ldots'


nodes = Nodes()
pic = tikz.Picture(
    'PoE/.style={rectangle, draw=red!60, fill=red!5, very thick, minimum size=10mm},'
    'MoE/.style={rectangle, draw=red!60, fill=red!5, very thick, , minimum height=20mm, minimum width=10mm},'
    # 'lr/.style={ellipse, draw=blue!60, fill=blue!5, very thick, minimum size=15mm},'
    'm0/.style={regular polygon,regular polygon sides=4, draw=green!60, fill=green!5, very thick, minimum size=28mm},'
    'm0_dis/.style={circle, draw=green!60, fill=green!5, very thick, minimum size=10mm},'
    'm1/.style={regular polygon,regular polygon sides=4, draw=orange!60, fill=orange!5, very thick, minimum size=28mm},'
    'm1_distr/.style={circle, draw=orange!60, fill=orange!5, very thick, minimum size=10mm},'
    'lr/.style={circle, draw=gray!60, fill=gray!5, very thick, minimum size=5mm},'
    'subset/.style={circle, draw=gray!60, fill=gray!5, very thick, minimum size=5mm},'
)

pic.set_node(text=nodes.input_m0, name='input_m0')
pic.set_node(text=nodes.q1, options='m0_dis, right of=input_m0, xshift=1.5cm', name='q1')
pic.set_node(text=nodes.input_m1, options='below of=input_m0, yshift=-2cm', name='input_m1')
pic.set_node(text=nodes.q2, options='m1_distr, right of=input_m1, xshift=1.5cm', name='q2')

pic.set_node(text=nodes.poe, options='PoE, right of=q1, xshift=1cm, align=center', name='poe1')
pic.set_node(text=nodes.poe, options='PoE, right of=q2, xshift=1cm, align=center', name='poe2')
pic.set_node(text=nodes.poe, options='PoE, below of=poe1, yshift=-0.5cm, align=center', name='poe3')

pic.set_node(text=nodes.q1_tilde, options='m0_dis, right of=poe1, xshift=0.5cm', name='q1_tilde')
pic.set_node(text=nodes.q2_tilde, options='m1_distr, right of=poe2, xshift=0.5cm', name='q2_tilde')
pic.set_node(text=nodes.q12_tilde, options='subset, right of=poe3, xshift=0.5cm', name='q12_tilde')

pic.set_node(text=nodes.moe, options='MoE, right of=q12_tilde, xshift=1cm, align=center', name='moe')
pic.set_node(text=nodes.z, options='lr,right of=moe, xshift=1cm, align=center', name='z')

pic.set_node(text=nodes.output__m1m2_m2, options='right of=z, xshift=2cm,yshift=-1.5cm', name='output__m1m2_m2')
pic.set_node(text=nodes.output__m1_m2, options='right of=output__m1m2_m2, xshift=1.5cm', name='output__m1_m2')

pic.set_node(text=nodes.output__m1m2_m1, options='above of=output__m1m2_m2, yshift=2cm', name='output__m1m2_m1')
pic.set_node(text=nodes.output__m2_m1, options='right of=output__m1m2_m1, xshift=1.5cm', name='output__m2_m1')

pic.set_line('input_m0', 'q1', label=r'$enc_1$', label_pos='south')
pic.set_line('input_m1', 'q2', label=r'$enc_2$', label_pos='south')

pic.set_line('q1', 'poe1')
pic.set_line('q2', 'poe2')
pic.set_line('q1', 'poe3')
pic.set_line('q2', 'poe3')

pic.set_line('poe1', 'q1_tilde')
pic.set_line('poe2', 'q2_tilde')
pic.set_line('poe3', 'q12_tilde')

pic.set_line('q1_tilde', 'moe')
pic.set_line('q12_tilde', 'moe')
pic.set_line('q2_tilde', 'moe')

pic.set_line('moe', 'z')

pic.set_line('z', 'output__m1m2_m2', label=r'$dec_2$', label_pos='north', edge_options='bend right=30')
# pic.set_line('z', 'output__m1_m2', label=r'$dec_2$', label_pos='north, rotate=-45', edge_options='bend right=50')

pic.set_line('z', 'output__m1m2_m1', label=r'$dec_1$\ ', label_pos='south, rotate=10', edge_options='bend left=30')
# pic.set_line('z', 'output__m2_m1', label=r'$dec_1$\ ', label_pos='south, rotate=45', edge_options='bend left=50')

output = pic.make()
print(output)
