import pandas as pd

from src.channel import ChannelModel
from src.clustering import pair_users
from src.schemes import SchemeEvaluator


class MonteCarloSimulation:
    def __init__(self, cfg):
        self.cfg = cfg
        self.channel = ChannelModel(cfg)
        self.eval = SchemeEvaluator(cfg)

    def run(self):
        rows = []

        for num_users in range(
            self.cfg.num_users_min,
            self.cfg.num_users_max + 1,
            self.cfg.user_step,
        ):
            swipt_sum = 0.0
            noma_sum = 0.0
            oma_sum = 0.0

            for _ in range(self.cfg.monte_carlo):
                gains = self.channel.effective_channels(num_users)
                pairs = pair_users(gains)

                swipt_tmp = 0.0
                noma_tmp = 0.0
                oma_tmp = 0.0

                for far_gain, near_gain in pairs:
                    swipt_tmp += self.eval.swipt_noma_rate(
                        near_gain,
                        far_gain,
                    )

                    noma_tmp += self.eval.conventional_noma_rate(
                        near_gain,
                        far_gain,
                    )

                    oma_tmp += self.eval.oma_rate(
                        near_gain,
                        far_gain,
                    )

                swipt_sum += swipt_tmp
                noma_sum += noma_tmp
                oma_sum += oma_tmp

            rows.append(
                {
                    'users': num_users,
                    'swipt_noma': swipt_sum / self.cfg.monte_carlo,
                    'noma': noma_sum / self.cfg.monte_carlo,
                    'oma': oma_sum / self.cfg.monte_carlo,
                }
            )

        return pd.DataFrame(rows)
