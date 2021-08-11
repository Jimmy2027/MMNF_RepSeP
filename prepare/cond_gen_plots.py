from utils import *
from mmvae_hub.utils.utils import json2dict

config = json2dict(Path(__file__).parent / 'config.json')


def get_best_mopoe_plot(df):
    method = 'mopoe'

    if config[method] == 'best':
        df = df.loc[(df['method'].str.startswith(f'joint_elbo')) & (df['num_mods'] == 3)]
        _id = df[df.score == df.score.max()]._id.item()

    else:
        _id = config[method]

    save_path = Path(__file__).parent.parent / f'data/{method}/cond_gen_plots'
    save_path.mkdir(parents=True, exist_ok=True)

    save_plots(_id, save_path, method)


def get_best_pgfm_plot(df):
    method = 'pgfm'

    if config[method] == 'best':
        df = df.loc[(df['method'].str.startswith(f'joint_elbo')) & (df['num_mods'] == 3)]
        _id = df[df.score == df.score.max()]._id.item()
    else:
        _id = config[method]
    save_path = Path(__file__).parent.parent / f'data/{method}/cond_gen_plots'
    save_path.mkdir(parents=True, exist_ok=True)

    save_plots(_id, save_path, method)


def get_best_mopgfm_plot(df):
    method = 'mopgfm'

    if config[method] == 'best':
        df = df.loc[(df['method'].str.startswith(f'joint_elbo')) & (df['num_mods'] == 3)]
        _id = df[df.score == df.score.max()]._id.item()

    else:
        _id = config[method]
    save_path = Path(__file__).parent.parent / f'data/{method}/cond_gen_plots'
    save_path.mkdir(parents=True, exist_ok=True)

    save_plots(_id, save_path, method)


def get_best_mofop_plot(df):
    method = 'mofop'
    df = df.loc[(df['method'].str.startswith(f'{method}_')) & (df['num_mods'] == 3)]
    best_score_id = df[df.score == df.score.max()]._id.item()
    save_path = Path(__file__).parent.parent / f'data/{method}/cond_gen_plots'
    save_path.mkdir(parents=True, exist_ok=True)

    save_plots(best_score_id, save_path, method)


def get_best_mogfm_plot(df):
    method = 'mogfm'
    if config[method] == 'best':
        df = df.loc[(df['method'].str.startswith(f'joint_elbo')) & (df['num_mods'] == 3)]
        _id = df[df.score == df.score.max()]._id.item()

    else:
        _id = config[method]
    save_path = Path(__file__).parent.parent / f'data/{method}/cond_gen_plots'
    save_path.mkdir(parents=True, exist_ok=True)

    save_plots(_id, save_path, method)


def save_plots_(_id, save_path, method: str):
    cond_gen_plots = show_generated_figs(_id=_id, return_plots=True, nbr_samples_x=10, nbr_samples_y=1)

    for p_key, ps in cond_gen_plots.items():
        for name, fig in ps.items():
            plt.figure(figsize=(10, 10))
            plt.imshow(fig)
            title = fr'\textbf{{{method.replace("joint_elbo", "mopoe")}}}: ' + name.replace('__', r'$\rightarrow$')
            plt.title(title)
            plt.axis('off')
            plt.savefig(save_path / name, bbox_inches='tight', pad_inches=0)
            plt.close()


def save_plots__(_id, save_path, method: str):
    cond_gen_plots = show_generated_figs(_id=_id, return_plots=True, nbr_samples_x=10, nbr_samples_y=1)

    for nbr_input_modalities, plots in cond_gen_plots.items():
        for plot_name, plot in plots.items():
            split = plot_name.split('__')
            in_mods = split[0]
            out_mod = split[-1]
            out_folder = save_path / plot_name
            out_folder.mkdir(exist_ok=True)
            # there are nbr in_mods + 1 modalities in total in the plot.
            row_height = int(plot.shape[0] / (len(in_mods.split('_')) + 1))
            inmods_plot = plot[:row_height * len(in_mods.split('_'))]
            outmods_plot = plot[row_height * len(in_mods.split('_')):]

            for k, fig in {'inmods_plot': inmods_plot, 'outmods_plot': outmods_plot}.items():
                plt.figure(figsize=(10, 10))
                plt.imshow(fig)
                # title = fr'\textbf{{{method.replace("joint_elbo", "mopoe")}}}: ' + name.replace('__', r'$\rightarrow$')
                # plt.title(title)
                plt.axis('off')
                plt.savefig(out_folder / k, bbox_inches='tight', pad_inches=0)
                plt.close()


def save_plots(_id, save_path, method: str):
    save_cond_gen(_id=_id, save_path=save_path, with_title=False)


def save_dataset_description(df):
    df = df.loc[(df['method'].str.startswith(f'mogfm')) & (df['num_mods'] == 3)]
    best_score_id = df[df.score == df.score.max()]._id.item()
    save_path = Path(__file__).parent.parent / f'data/polymnist_example.png'
    cond_gen_plots = show_generated_figs(_id=best_score_id, return_plots=True, nbr_samples_x=10, nbr_samples_y=0)
    fig = cond_gen_plots['cond_gen_03']['m0_m1_m2__m0']

    plt.figure(figsize=(10, 10))
    plt.imshow(fig)
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()


if __name__ == '__main__':
    df = get_experiments_df()
    # save_dataset_description(df)
    # get_best_mogfm_plot(df)
    # get_best_mogfm_plot(df)
    # get_best_mopgfm_plot(df)
    get_best_mopoe_plot(df)
    # get_best_mofop_plot(df)
