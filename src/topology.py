import numpy as np

from src.paper_params import PAPER_PARAMS


class NetworkTopology:
    def __init__(self, params=None):
        self.params = dict(PAPER_PARAMS)
        if params:
            self.params.update(params)
        self.rng = np.random.default_rng(self.params['seed'])

    def deploy_access_points(self):
        area = self.params['area_size']
        return self.rng.uniform(0.0, area, size=(self.params['num_aps'], 2))

    def deploy_users(self, num_users):
        area = self.params['area_size']
        return self.rng.uniform(0.0, area, size=(num_users, 2))

    def distances(self, aps, users):
        diff = aps[:, None, :] - users[None, :, :]
        d = np.linalg.norm(diff, axis=2)
        return np.maximum(d, self.params['min_distance_m'])
