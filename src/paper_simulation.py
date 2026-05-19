import pandas as pd

from src.channel_realization import ChannelRealization
from src.clustering import pair_users
from src.paper_params import PAPER_PARAMS
from src.schemes import SchemeEvaluator


class PaperSimulation:
    def __init__(self, params=None):
        self.params = dict(PAPER_PARAMS)
        if params:
            self.params.update(params)
        self.channel = ChannelRealization(self.params)
        self.scheme = self._build_scheme()

    def _build_scheme(self):
        class Config:
            pass
        cfg = Config()
        for key, value in self.params.items():
            setattr(cfg, key, value)
        cfg.tx_power_dbm = self.params['ap_tx_power_dbm']
        return SchemeEvaluator(cfg)

    def run(self):
        rows = []
        start = self.params['num_users_min']
        stop = self.params['num_users_max'] + 1
        step = self.params['user_step']

        for num_users in range(start, stop, step):
            totals = {'swipt_noma': 0.0, 'noma': 0.0, 'oma': 0.0}

            for _ in range(self.params['monte_carlo']):
                realization = self.channel.generate(num_users)
                pairs = pair_users(realization['effective_channels'])

                for far_gain, near_gain in pairs:
                    totals['swipt_noma'] += self.scheme.swipt_noma_rate(near_gain, far_gain)
                    totals['noma'] += self.scheme.conventional_noma_rate(near_gain, far_gain)
                    totals['oma'] += self.scheme.oma_rate(near_gain, far_gain)

            rows.append({
                'users': num_users,
                'swipt_noma': totals['swipt_noma'] / self.params['monte_carlo'],
                'noma': totals['noma'] / self.params['monte_carlo'],
                'oma': totals['oma'] / self.params['monte_carlo'],
            })

        return pd.DataFrame(rows)
