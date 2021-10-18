"""Generate a latex file with all the generation comparisons."""
from itertools import chain, combinations
from pathlib import Path


def base_str(which: str, dataset: str):
    if dataset == 'polymnist':
        return r"\begin{figure}\centering\resizebox{0.9\textwidth}{!}{\py{boilerplate.make_cond_gen_fig(which='" \
           + which + \
           r"',methods=['mopoe', 'mopgfm', 'moe', 'poe', 'mofop', 'iwmogfm_amortized', 'iwmogfm'], dataset = '" \
           + dataset + \
           r"')}}\end{figure}" + \
           "\n\n\n\n"

    else:
        return r"\begin{figure}\centering\resizebox{0.9\textwidth}{!}{\py{boilerplate.make_cond_gen_fig_mimic(which='" \
               + which + \
               r"',methods=['mofop', 'mopoe'], dataset = '" \
               + dataset + \
               r"')}}\end{figure}" + \
               "\n\n\n\n"


def make_gen_comp_polymnist():
    text = ""
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
            text += base_str(which=key, dataset='polymnist')

    outfile = Path(__file__).parent.parent / 'thesis/gen_comp_polymnist.tex'
    with open(str(outfile), 'w') as f:
        f.write(text)


def make_gen_comp_mimic():
    text = ""
    mods = ['PA', 'Lateral', 'text']

    subsets_list = chain.from_iterable(combinations(mods, n) for n in range(len(mods) + 1))

    subsets = []
    for mod_names in subsets_list:
        if mod_names:
            subset = '_'.join(sorted(mod_names))
            subsets.append(subset)

    for subset in subsets:
        for out_mod in mods:
            key = f'{subset}__{out_mod}'
            text += base_str(which=key, dataset='mimic')

    outfile = Path(__file__).parent.parent / 'thesis/gen_comp_mimic.tex'
    with open(str(outfile), 'w') as f:
        f.write(text)


if __name__ == '__main__':
    make_gen_comp_polymnist()
    make_gen_comp_mimic()
