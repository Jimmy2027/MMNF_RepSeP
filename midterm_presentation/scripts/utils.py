from dataclasses import dataclass
from pathlib import Path

from scripts_ import tikz
METHODS = ['mopoe', 'mopgfm', 'mogfm']

method_footnote_mapping = {'mopoe': r'mopoe \footnote{mixture-of-product-of-expert}',
                           'mopgfm': r'mopgfm \footnote{mixture-of-parameter-generalized-$f$-mean}',
                           'mogfm': r'mogfm \footnote{mixture-of-generalized-$f$-mean}'
                           }

def make_graph(with_red_circle: bool = False):
    cond_samples_path = Path('data/pgfm/cond_gen_examples')
    input_samples_dir = cond_samples_path / 'input_samples'

    @dataclass
    class Nodes:
        input_m1: str = f'\\includegraphics[width=2cm]{{{str(input_samples_dir / "m2.png")}}}'
        input_m0: str = f'\\includegraphics[width=2cm]{{{str(input_samples_dir / "m1.png")}}}'
        output__m1m2_m2: str = f'\\includegraphics[width=2cm]{{{str(cond_samples_path / "m1_m2" / "m2.png")}}}'
        output__m1m2_m1: str = f'\\includegraphics[width=2cm]{{{str(cond_samples_path / "m1_m2" / "m1.png")}}}'
        output__m2_m1: str = f'\\includegraphics[width=2cm]{{{str(cond_samples_path / "m2" / "m1.png")}}}'
        output__m1_m2: str = f'\\includegraphics[width=2cm]{{{str(cond_samples_path / "m1" / "m2.png")}}}'
        q1: str = r'$q_{\phi_1}$'
        q2: str = r'$q_{\phi_2}$'
        q1_tilde: str = r'$\tilde{q}_{\phi_1}$'
        q2_tilde: str = r'$\tilde{q}_{\phi_2}$'
        q12_tilde: str = r'$\tilde{q}_{\phi_{12}}$'
        gfm: str = r'$f$-Mean'
        points: str = r'\ldots'

    nodes = Nodes()
    pic = tikz.Picture(
        'gfm/.style={rectangle, draw=red!60, fill=red!5, very thick, minimum size=10mm},'
        # 'lr/.style={ellipse, draw=blue!60, fill=blue!5, very thick, minimum size=15mm},'
        'm0/.style={regular polygon,regular polygon sides=4, draw=green!60, fill=green!5, very thick, minimum size=28mm},'
        'm0_dis/.style={circle, draw=green!60, fill=green!5, very thick, minimum size=10mm},'
        'm1/.style={regular polygon,regular polygon sides=4, draw=orange!60, fill=orange!5, very thick, minimum size=28mm},'
        'm1_distr/.style={circle, draw=orange!60, fill=orange!5, very thick, minimum size=10mm},'
        'lr/.style={circle, draw=gray!60, fill=gray!5, very thick, minimum size=15mm},'
        'subset/.style={circle, draw=gray!60, fill=gray!5, very thick, minimum size=5mm},'
    )

    pic.set_node(text=nodes.input_m0, name='input_m0')
    pic.set_node(text=nodes.q1, options='m0_dis, right of=input_m0, xshift=1.5cm', name='q1')
    pic.set_node(text=nodes.input_m1, options='below of=input_m0, yshift=-2cm', name='input_m1')
    pic.set_node(text=nodes.q2, options='m1_distr, right of=input_m1, xshift=1.5cm', name='q2')

    pic.set_node(text=nodes.gfm, options='gfm, right of=q1, xshift=1cm,yshift=-1.5cm, align=center', name='gfm')

    pic.set_node(text=nodes.q12_tilde, options='lr, right of=gfm, xshift=1.5cm', name='q12_tilde')



    pic.set_node(text=nodes.output__m1m2_m2, options='right of=q12_tilde, xshift=2cm,yshift=-1.5cm', name='output__m1m2_m2')
    pic.set_node(text=nodes.output__m1_m2, options='right of=output__m1m2_m2, xshift=1.5cm', name='output__m1_m2')

    pic.set_node(text=nodes.output__m1m2_m1, options='above of=output__m1m2_m2, yshift=2cm', name='output__m1m2_m1')
    pic.set_node(text=nodes.output__m2_m1, options='right of=output__m1m2_m1, xshift=1.5cm', name='output__m2_m1')

    if with_red_circle:
        pic.set_node(
            options='right of=output__m1m2_m2, xshift=1.5cm, yshift=1.5cm, ellipse, draw=red!100, line width=2pt, minimum height=70mm, minimum width=30mm')

    pic.set_line('input_m0', 'q1', label=r'$enc_1$', label_pos='south')
    pic.set_line('input_m1', 'q2', label=r'$enc_2$', label_pos='south')

    pic.set_line('q1', 'gfm', label=r'\textcolor{green}{$\mu_1$}', edge_options='bend right=-10', label_pos='south')
    pic.set_line('q1', 'gfm', label=r'\textcolor{green}{$\sigma_1$}', edge_options='bend right=10', label_pos='north')

    pic.set_line('q2', 'gfm', label=r'\textcolor{orange}{$\mu_2$}', edge_options='bend right=10', label_pos='north')
    pic.set_line('q2', 'gfm', label=r'\textcolor{orange}{$\sigma_2$}', edge_options='bend right=-10', label_pos='south')

    pic.set_line('gfm', 'q12_tilde')

    pic.set_line('q12_tilde', 'output__m1m2_m2', label=r'$dec_2$', label_pos='north', edge_options='bend right=30')
    # pic.set_line('z', 'output__m1_m2', label=r'$dec_2$', label_pos='north, rotate=-45', edge_options='bend right=50')

    pic.set_line('q12_tilde', 'output__m1m2_m1', label=r'$dec_1$\ ', label_pos='south, rotate=10', edge_options='bend left=30')
    # pic.set_line('z', 'output__m2_m1', label=r'$dec_1$\ ', label_pos='south, rotate=45', edge_options='bend left=50')

    output = pic.make()
    print(output)