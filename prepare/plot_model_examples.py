from mmvae_hub.experiment_vis.utils import *
from mmvae_hub.utils.MongoDB import MongoDatabase


def get_best_mopoe_examples(df):
    df = df.loc[df['method'] == 'joint_elbo']
    best_score_id = df[df.score == df.score.max()]._id.item()
    save_path = Path(__file__).parent.parent / 'data/mopoe/cond_gen_examples'
    save_path.mkdir(parents=True, exist_ok=True)
    save_cond_gen(_id=best_score_id, save_path=save_path)


if __name__ == '__main__':
    exp_db = MongoDatabase(training=False)
    experiments = exp_db.connect()

    df = make_experiments_dataframe(experiments)

    get_best_mopoe_examples(df)
