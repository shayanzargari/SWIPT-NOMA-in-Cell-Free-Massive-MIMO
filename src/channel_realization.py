import numpy as np

from src.paper_params import PAPER_PARAMS
from src.topology import NetworkTopology
from src.fading import large_scale_fading, small_scale_fading
from src.ap_association import APAssociation


class ChannelRealization:
    def __init__(self, params=None):
        self.params = dict(PAPER_PARAMS)
        if params:
            self.params.update(params)

        self.rng = np.random.default_rng(self.params['seed'])
        self.topology = NetworkTopology(self.params, rng=self.rng)
        self.association = APAssociation(self.params)

    def generate(self, num_users):
        aps = self.topology.deploy_access_points()
        users = self.topology.deploy_users(num_users)

        distances = self.topology.distances(aps, users)

        beta = large_scale_fading(
            distances,
            self.params,
            self.rng,
        )

        fading = small_scale_fading(beta.shape, self.rng)

        channels = np.sqrt(beta) * fading

        serving_mask = self.association.build_serving_mask(beta)

        effective_channels = np.sum(
            np.abs(channels * serving_mask) ** 2,
            axis=0,
        )

        return {
            'aps': aps,
            'users': users,
            'distances': distances,
            'beta': beta,
            'channels': channels,
            'serving_mask': serving_mask,
            'effective_channels': np.sort(effective_channels),
        }
