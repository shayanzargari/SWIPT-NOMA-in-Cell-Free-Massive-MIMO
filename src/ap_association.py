import numpy as np

from src.paper_params import PAPER_PARAMS


class APAssociation:
    def __init__(self, params=None):
        self.params = dict(PAPER_PARAMS)
        if params:
            self.params.update(params)

    def build_serving_mask(self, beta):
        num_aps, num_users = beta.shape
        serving = min(self.params.get('serving_aps', 8), num_aps)

        mask = np.zeros_like(beta, dtype=bool)

        for user_idx in range(num_users):
            strongest = np.argsort(beta[:, user_idx])[-serving:]
            mask[strongest, user_idx] = True

        return mask
