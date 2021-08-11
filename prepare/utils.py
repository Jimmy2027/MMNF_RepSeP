from mmvae_hub.experiment_vis.utils import *
from mmvae_hub.utils.MongoDB import MongoDatabase


def get_experiments_df():
    exp_db = MongoDatabase(training=False)
    experiments = exp_db.connect()

    return make_experiments_dataframe(experiments)
