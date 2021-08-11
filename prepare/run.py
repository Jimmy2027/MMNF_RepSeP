from cond_gen_plots import *
from make_gen_eval_tab import save_gen_eval_tab
from make_lat_eval_tab import save_lr_eval_tab
from make_llhoods_tab import save_lhood_eval_tab
from make_prd_tab import save_prd_eval_tab
from make_params_tab import save_params_tab
from plot_model_examples import *

df = get_experiments_df()

save_dataset_description(df)

save_params_tab(df)

get_best_mopoe_plot(df)
get_best_mofop_plot(df)
get_best_mopgfm_plot(df)
get_best_mogfm_plot(df)

save_gen_eval_tab(df)

save_lr_eval_tab(df)

save_prd_eval_tab(df)

save_lhood_eval_tab(df)

get_best_mopoe_examples(df)
get_best_mopgfm_examples(df)
get_best_mogfm_examples(df)
get_best_pgfm_examples(df)
get_best_mofop_examples(df)
