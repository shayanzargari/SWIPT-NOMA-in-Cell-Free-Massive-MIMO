import numpy as np


class ChannelModel:
    def __init__(self, cfg):
        self.cfg = cfg
        self.rng = np.random.default_rng(cfg.seed)

    def deploy_nodes(self, num_users):
        aps = self.rng.uniform(0, self.cfg.area_size, (self.cfg.num_aps, 2))
        users = self.rng.uniform(0, self.cfg.area_size, (num_users, 2))
        return aps, users

    def compute_distances(self, aps, users):
        diff = aps[:, None, :] - users[None, :, :]
        return np.linalg.norm(diff, axis=2) + 1.0

    def path_loss(self, distances):
        shadow = self.rng.normal(0, self.cfg.shadow_std_db, distances.shape)
        pl_db = -10 * self.cfg.path_loss_exp * np.log10(distances)
        return 10 ** ((pl_db + shadow) / 10)

    def fading(self, shape):
        real = self.rng.normal(size=shape)
        imag = self.rng.normal(size=shape)
        return (real + 1j * imag) / np.sqrt(2)

    def effective_channels(self, num_users):
        aps, users = self.deploy_nodes(num_users)
        d = self.compute_distances(aps, users)
        beta = self.path_loss(d)
        h = self.fading(beta.shape)
        g = np.sqrt(beta) * h
        eff = np.sum(np.abs(g), axis=0)
        return np.sort(eff)
