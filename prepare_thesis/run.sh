#!/usr/bin/env bash

python prepare.py || exit 1;
python get_experiment_dirs.py || exit 1;
python cond_gen_plots.py || exit 1;
python cond_gen_single_img.py || exit 1;
python save_comp_dicts.py || exit 1;

