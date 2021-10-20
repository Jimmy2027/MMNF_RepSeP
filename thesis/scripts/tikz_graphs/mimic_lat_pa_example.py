from pathlib import Path
from scripts_ import tikz

data_path = Path('data/thesis/mimic')

mofop_dir = data_path / 'mofop/cond_gen_plots/Lateral_PA'
mopoe_dir = data_path / 'mopoe/cond_gen_plots/Lateral_PA'
mopgfm_dir = data_path / 'mopgfm/cond_gen_plots/Lateral_PA'
input_samples_dir = data_path / 'mopoe/cond_gen_plots/input_samples'

pic = tikz.Picture()

imgsize = 3

pic.set_node(
    text=f'\\includegraphics[width={imgsize}cm]{{{input_samples_dir / "PA_1.png"}}}',
    name='inmod_PA',
)
pic.set_node(
    text=r"Input PA",
    options="above of=inmod_PA, yshift=0.8cm"
)


pic.set_node(
    text=f'\\includegraphics[width={imgsize}cm]{{{input_samples_dir / "Lateral_1.png"}}}',
    options='right of=inmod_PA, xshift=2.5cm',
    name='inmod_lat',
)
pic.set_node(
    text=r"Input Lateral",
    options="above of=inmod_lat, yshift=0.8cm"
)

pic.set_node(
    text=f'\\includegraphics[width={imgsize}cm]{{{mopoe_dir / "PA_1.png"}}}',
    options='below of=inmod_PA, yshift=-3.5cm, xshift=-2.7cm',
    name='out_mopoe',
)
pic.set_node(
    text=r"MoPoE output",
    options="above of=out_mopoe, yshift=0.8cm"
)

pic.set_node(
    text=f'\\includegraphics[width={imgsize}cm]{{{mofop_dir / "PA_1.png"}}}',
    options='right of=out_mopoe, xshift=3.5cm',
    name='out_mofop',
)
pic.set_node(
    text=r"MofoP output",
    options="above of=out_mofop, yshift=0.8cm"
)

pic.set_node(
    text=f'\\includegraphics[width={imgsize}cm]{{{mopgfm_dir / "PA_1.png"}}}',
    options='right of=out_mofop, xshift=3.5cm',
    name='out_mopgfm',
)
pic.set_node(
    text=r"MopgfM output",
    options="above of=out_mopgfm, yshift=0.8cm"
)

print(pic.make())
