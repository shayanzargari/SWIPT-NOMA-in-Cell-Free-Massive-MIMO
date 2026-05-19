import numpy as np


def dbm_to_watt(dbm):
    return 10 ** ((dbm - 30) / 10)


class SchemeEvaluator:
    def __init__(self, cfg):
        self.cfg = cfg
        self.tx_power = dbm_to_watt(cfg.tx_power_dbm)
        self.noise = dbm_to_watt(cfg.noise_power_dbm)

    def shannon(self, sinr):
        return np.log2(1 + sinr)

    def swipt_noma_rate(self, near_gain, far_gain):
        harvested = self.cfg.swipt_efficiency * self.cfg.power_split * near_gain

        far_sinr = (
            self.cfg.noma_alpha_far * self.tx_power * far_gain
        ) / (
            self.cfg.noma_alpha_near * self.tx_power * far_gain + self.noise)

        relay_boost = harvested * near_gain

        near_sinr = (
            self.cfg.noma_alpha_near * self.tx_power * near_gain + relay_boost
        ) / self.noise

        return self.shannon(far_sinr) + self.shannon(near_sinr)

    def conventional_noma_rate(self, near_gain, far_gain):
        far_sinr = (
            self.cfg.noma_alpha_far * self.tx_power * far_gain
        ) / (
            self.cfg.noma_alpha_near * self.tx_power * far_gain + self.noise)

        near_sinr = (
            self.cfg.noma_alpha_near * self.tx_power * near_gain
        ) / self.noise

        return self.shannon(far_sinr) + self.shannon(near_sinr)

    def oma_rate(self, near_gain, far_gain):
        near = 0.5 * self.shannon(self.tx_power * near_gain / self.noise)
        far = 0.5 * self.shannon(self.tx_power * far_gain / self.noise)
        return near + far
