import numpy as np
import pandas as pd

from src.paper_math import pair_nearest_users, path_loss, rayleigh_gain
from src.paper_rates import cluster_sum_rates
from src.paper_params import PAPER_PARAMS


def ap_user_gain(aps, user, params, rng):
    distances = np.linalg.norm(aps - user, axis=1)
    beta = path_loss(distances, params)
    gains = [rayleigh_gain(b, rng) for b in beta]
    return float(np.mean(gains))


def user_user_gain(user_a, user_b, params, rng):
    distance = np.linalg.norm(user_a - user_b)
    beta = path_loss(distance, params)
    return float(rayleigh_gain(beta, rng))


def simulate_users(rho=1.0, params=None):
    cfg = dict(PAPER_PARAMS)
    if params:
        cfg.update(params)

    rng = np.random.default_rng(cfg['seed'] + int(1000 * rho))
    user_values = np.arange(cfg['num_users_min'], cfg['num_users_max'] + 1, cfg['user_step'])
    rows = []

    for user_count in user_values:
        total = dict(oma=0.0, conventional_noma=0.0)
        for case in range(1, 4):
            total[f'swipt_noma_case{case}'] = 0.0

        sample_count = 0

        for _ in range(cfg['monte_carlo']):
            aps = rng.uniform(0.0, cfg['area_size'], size=(cfg['num_aps'], 2))
            users = rng.uniform(0.0, cfg['area_size'], size=(user_count, 2))
            pairs = pair_nearest_users(users)
            num_clusters = max(len(pairs), 1)

            for u1, u2 in pairs:
                g1 = ap_user_gain(aps, users[u1], cfg, rng)
                g2 = ap_user_gain(aps, users[u2], cfg, rng)
                h12 = user_user_gain(users[u1], users[u2], cfg, rng)
                interference_gain = 0.5 * (g1 + g2)

                for idx, beta_ps in enumerate(cfg['beta_cases'], start=1):
                    oma, noma, swipt = cluster_sum_rates(
                        g1,
                        g2,
                        h12,
                        beta_ps,
                        rho,
                        cfg,
                        num_clusters=num_clusters,
                        interference_gain=interference_gain,
                    )
                    if idx == 1:
                        total['oma'] += oma
                        total['conventional_noma'] += noma
                    total[f'swipt_noma_case{idx}'] += swipt

                sample_count += 1

        row = {'users': int(user_count)}
        for key, value in total.items():
            row[key] = value / max(sample_count, 1)
        rows.append(row)

    return pd.DataFrame(rows)


def simulate_power_splitting(params=None):
    cfg = dict(PAPER_PARAMS)
    if params:
        cfg.update(params)

    rng = np.random.default_rng(cfg['seed'] + 404)
    beta_values = np.round(np.arange(0.02, 0.91, 0.02), 2)
    rows = []

    for beta_ps in beta_values:
        total_rho_1 = 0.0
        total_rho_085 = 0.0
        sample_count = 0

        for _ in range(cfg['monte_carlo']):
            aps = rng.uniform(0.0, cfg['area_size'], size=(cfg['num_aps'], 2))
            users = rng.uniform(0.0, cfg['area_size'], size=(200, 2))
            pairs = pair_nearest_users(users)
            num_clusters = max(len(pairs), 1)

            for u1, u2 in pairs:
                g1 = ap_user_gain(aps, users[u1], cfg, rng)
                g2 = ap_user_gain(aps, users[u2], cfg, rng)
                h12 = user_user_gain(users[u1], users[u2], cfg, rng)
                interference_gain = 0.5 * (g1 + g2)

                _, _, r1 = cluster_sum_rates(
                    g1,
                    g2,
                    h12,
                    beta_ps,
                    1.0,
                    cfg,
                    num_clusters=num_clusters,
                    interference_gain=interference_gain,
                )
                _, _, r085 = cluster_sum_rates(
                    g1,
                    g2,
                    h12,
                    beta_ps,
                    0.85,
                    cfg,
                    num_clusters=num_clusters,
                    interference_gain=interference_gain,
                )
                total_rho_1 += r1
                total_rho_085 += r085
                sample_count += 1

        rows.append({
            'power_splitting_ratio': beta_ps,
            'rho_1': total_rho_1 / max(sample_count, 1),
            'rho_085': total_rho_085 / max(sample_count, 1),
        })

    return pd.DataFrame(rows)
