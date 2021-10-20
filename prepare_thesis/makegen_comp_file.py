"""Generate a latex file with all the generation comparisons."""
from itertools import chain, combinations
from pathlib import Path


def base_str(which: str, dataset: str):
    inp_mods, out_mod = which.split('__')

    inp_mods = inp_mods.replace('_', ', ')
    out_mod = out_mod.replace('_', ', ')

    if len(inp_mods.split(',')) == 1:
        inp_mods_str = f"modality is {inp_mods}"
    else:
        inp_mods_str = f"modalities are {inp_mods}"

    if dataset == 'polymnist':
        resize = 0.9
        py_scriptname = "make_cond_gen_fig_polymnist"
        caption = f"Generated examples, conditioned on samples from the PolyMNIST Test set. The input {inp_mods_str} and the generated modality is {out_mod}."
        methods = "['mopoe', 'mopgfm', 'moe', 'poe', 'mofop', 'mogfm_amortized', 'iwmogfm']"

    elif dataset == 'iw_comp':
        resize = 0.9
        py_scriptname = "make_cond_gen_fig_iw_comp"
        caption = f"Generated examples with different number of important samples (K), conditioned on samples from the PolyMNIST Test set. The input {inp_mods_str} and the generated modality is {out_mod}."
        methods = "['iwmopoe', 'iwmopgfm', 'iwmoe']"
        dataset = 'polymnist'

    else:
        resize = 1
        py_scriptname = "make_cond_gen_fig_mimic"
        caption = f"Generated examples, conditioned on samples from the MIMIC-CXR Test set. The input {inp_mods_str} and the generated modality is {out_mod}."
        methods = "['mofop', 'mopoe', 'mopgfm']"

    label = f"fig: {which}"

    return r"\begin{figure}\centering\resizebox{" + str(resize) + r"\textwidth}{!}{\py{boilerplate." \
           + py_scriptname + "(which='" \
           + which + \
           r"',methods=" + methods + ", dataset = '" \
           + dataset + \
           r"')}}" \
           r"\caption{" + caption + \
           r"}\label{" + label + "}\end{figure}" + \
           "\n\n\n\n"


def make_gen_comp_polymnist(iw_comp: bool = False):
    text = ""
    mods = ['m0', 'm1', 'm2']

    if iw_comp == True:
        dataset = 'iw_comp'
    else:
        dataset = 'polymnist'
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
            text += base_str(which=key, dataset=dataset)

    outfile = Path(__file__).parent.parent / f'thesis/gen_comp_{dataset}.tex'
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
    make_gen_comp_polymnist(iw_comp=True)
