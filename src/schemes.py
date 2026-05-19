import numpy as np


def dbm_to_watt(dbm):
    return 10 ** ((dbm - 30) / 10)


class SchemeEvaluator:
    def __init__(self, cfg):
        self.cfg = cfg
        self.tx_power = dbm_to_watt(getattr(cfg, 'ap_tx_power_dbm', 30.0))
        self.relay_power_limit = dbm_to_watt(
            getattr(cfg, 'relay_tx_power_dbm', 20.0)
        )
        self.noise = dbm_to_watt(cfg.noise_power_dbm)

    def shannon(self, sinr):
        return np.log2(1.0 + np.maximum(sinr, 1e-12))

    def swipt_noma_rate(self, near_gain, far_gain):
        alpha_far = self.cfg.noma_alpha_far
        alpha_near = self.cfg.noma_alpha_near

        direct_far_signal = alpha_far * self.tx_power * far_gain
        direct_far_interference = alpha_near * self.tx_power * far_gain

        direct_far_sinr = direct_far_signal / (
            direct_far_interference + self.noise
        )

        harvested_power = (
            self.cfg.swipt_efficiency
            * self.cfg.power_split
            * self.tx_power
            * near_gain
        )

        relay_power = min(harvested_power, self.relay_power_limit)

        relay_sinr = (relay_power * far_gain) / self.noise

        combined_far_sinr = direct_far_sinr + relay_sinr

        sic_noise = self.cfg.sic_residual * self.tx_power * near_gain

        near_sinr = (
            alpha_near * self.tx_power * near_gain
        ) / (
            self.noise + sic_noise)

        return (
            self.shannon(combined_far_sinr)
            + self.shannon(near_sinr)
        )

    def conventional_noma_rate(self, near_gain, far_gain):
        alpha_far = self.cfg.noma_alpha_far
        alpha_near = self.cfg.noma_alpha_near

        far_sinr = (
            alpha_far * self.tx_power * far_gain
        ) / (
            alpha_near * self.tx_power * far_gain + self.noise)

        near_sinr = (
            alpha_near * self.tx_power * near_gain
        ) / self.noise

        return self.shannon(far_sinr) + self.shannon(near_sinr)

    def oma_rate(self, near_gain, far_gain):
        near_rate = 0.5 * self.shannon(
            self.tx_power * near_gain / self.noise
        )

        far_rate = 0.5 * self.shannon(
            self.tx_power * far_gain / self.noise
        )

        return near_rate + far_rate
