"""Generate a latex file with all the generation comparisons."""
from itertools import chain, combinations
from pathlib import Path

text = ""
base_str = r"\begin{figure}\centering\resizebox{0.9\textwidth}{!}{\py{boilerplate.make_cond_gen_fig(which='m1_m2__m2'," \
           r" methods=['mopoe','mopgfm', 'moe'])}}\end{figure}"

mods = ['m0', 'm1', 'm2']

subsets_list = chain.from_iterable(combinations(mods, n) for n in range(len(mods) + 1))
# print(list(subsets_list))
subsets = []
for mod_names in subsets_list:
    if mod_names:
        subset = '_'.join(sorted(mod_names))
        subsets.append(subset)

for subset in subsets:
    for out_mod in mods:
        key = f'{subset}__{out_mod}'
        text += r"\begin{figure}\centering\resizebox{0.9\textwidth}{!}{\py{boilerplate.make_cond_gen_fig(which='" \
                + key + \
                r"',methods=['mopoe','mopgfm', 'moe'])}}\end{figure}" + \
                "\n\n\n\n"

outfile = Path(__file__).parent.parent / 'thesis/gen_comp.tex'
with open(str(outfile), 'w') as f:
    f.write(text)

# rand generation comparison
