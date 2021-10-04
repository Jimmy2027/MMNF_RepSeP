#!/usr/bin/env bash

python prepare.py || exit 1;
python get_experiment_dirs.py || exit 1;
python cond_gen_plots.py || exit 1;
python cond_gen_single_img.py || exit 1;
python make_rand_gen_plots.py || exit 1;
python save_comp_dicts.py || exit 1;

python makegen_comp_file.py || exit 1;

python make_lr_eval_tab.py || exit 1;
python make_prd_tab.py || exit 1;
python make_gen_eval_tab.py || exit 1;

