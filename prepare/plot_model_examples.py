from utils import *


def get_best_mopoe_examples(df):
    df = df.loc[df['method'] == 'joint_elbo']
    best_score_id = df[df.score == df.score.max()]._id.item()
    save_path = Path(__file__).parent.parent / 'data/mopoe/cond_gen_examples'
    save_path.mkdir(parents=True, exist_ok=True)
    save_cond_gen(_id=best_score_id, save_path=save_path)


def get_best_pgfm_examples(df):
    df = df.loc[(df['method'].str.startswith('pgfm_')) & (df['num_mods'] == 3)]
    best_score_id = df[df.score == df.score.max()]._id.item()
    save_path = Path(__file__).parent.parent / 'data/pgfm/cond_gen_examples'
    save_path.mkdir(parents=True, exist_ok=True)
    save_cond_gen(_id=best_score_id, save_path=save_path)


def get_best_mopgfm_examples(df):
    df = df.loc[(df['method'].str.startswith('mopgfm_')) & (df['num_mods'] == 3)]
    best_score_id = df[df.score == df.score.max()]._id.item()
    save_path = Path(__file__).parent.parent / 'data/mopgfm/cond_gen_examples'
    save_path.mkdir(parents=True, exist_ok=True)
    save_cond_gen(_id=best_score_id, save_path=save_path)


def get_best_mofop_examples(df):
    df = df.loc[(df['method'].str.startswith('mofop_')) & (df['num_mods'] == 3)]
    best_score_id = df[df.score == df.score.max()]._id.item()
    save_path = Path(__file__).parent.parent / 'data/mofop/cond_gen_examples'
    save_path.mkdir(parents=True, exist_ok=True)
    save_cond_gen(_id=best_score_id, save_path=save_path)


def get_best_mogfm_examples(df):
    df = df.loc[(df['method'].str.startswith('mogfm_')) & (df['num_mods'] == 3)]
    best_score_id = df[df.score == df.score.max()]._id.item()
    save_path = Path(__file__).parent.parent / 'data/mogfm/cond_gen_examples'
    save_path.mkdir(parents=True, exist_ok=True)
    save_cond_gen(_id=best_score_id, save_path=save_path)


if __name__ == '__main__':
    df = get_experiments_df()

    # get_best_mopoe_examples(df)
    get_best_mofop_examples(df)
    # get_best_mopgfm_examples(df)
    # get_best_mogfm_examples(df)
