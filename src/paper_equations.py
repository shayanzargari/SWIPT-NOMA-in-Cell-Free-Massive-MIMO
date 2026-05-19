import numpy as np

from src.paper_math import dbm_to_watt, path_loss, pair_nearest_users
from src.paper_params import PAPER_PARAMS


def complex_normal(shape, rng):
    return (rng.normal(size=shape) + 1j * rng.normal(size=shape)) / np.sqrt(2.0)


def deploy_network(num_users, params, rng):
    area = params['area_size']
    aps = rng.uniform(0.0, area, size=(params['num_aps'], 2))
    users = rng.uniform(0.0, area, size=(num_users, 2))
    pairs = pair_nearest_users(users)
    return aps, users, pairs


def large_scale_coefficients(aps, users, params):
    diff = aps[:, None, :] - users[None, :, :]
    distances = np.linalg.norm(diff, axis=2)
    return path_loss(distances, params)


def mmse_estimation_variance(beta, params):
    tau = params['pilot_length']
    pilot_power = dbm_to_watt(params['pilot_power_dbm'])
    noise = dbm_to_watt(params['noise_power_dbm'])
    denom = tau * pilot_power * np.sum(beta, axis=1, keepdims=True) + noise
    return (tau * pilot_power * beta ** 2) / np.maximum(denom, 1e-30)


def estimated_channels(mu, rng):
    v = complex_normal(mu.shape, rng)
    return np.sqrt(np.maximum(mu, 0.0)) * v


def beamforming_coefficients(true_channels, estimated):
    phase = np.conj(estimated) / np.maximum(np.abs(estimated), 1e-15)
    return np.sum(true_channels * phase, axis=0)


def cluster_head_order(c_abs_1, c_abs_2):
    if c_abs_1 >= c_abs_2:
        return 0, 1
    return 1, 0


def pair_channel_gain(user_a, user_b, params, rng):
    distance = np.linalg.norm(user_a - user_b)
    beta = path_loss(distance, params)
    g = complex_normal((), rng)
    return np.abs(np.sqrt(beta) * g) ** 2


def prelog_factor(params):
    tc = params['coherence_block']
    tau = min(params['pilot_length'], tc - 1)
    return (tc - tau) / tc


def paper_sinr_rates(c_head, c_far, c_cross, h12_sq, beta_ps, rho, params):
    noise = dbm_to_watt(params['noise_power_dbm'])
    p_cluster = dbm_to_watt(params['cluster_power_dbm'])
    p_head = params['power_ratio_near'] * p_cluster
    p_far = params['power_ratio_far'] * p_cluster
    kappa = prelog_factor(params)

    ch = np.abs(c_head) ** 2
    cf = np.abs(c_far) ** 2
    cc = np.abs(c_cross) ** 2

    head_noise = noise / max(1.0 - beta_ps, 1e-12)
    sinr_head = (ch * p_head) / (p_far * cc + head_noise)

    harvested_power = beta_ps * params['swipt_efficiency'] * p_cluster * ch
    relay_term = np.sqrt(max(harvested_power, 0.0) * h12_sq / max(rho, 1e-12))
    direct_term = np.sqrt(cf * p_far)
    numerator_far = np.abs(direct_term + relay_term) ** 2

    sic_error = harvested_power * h12_sq * ((1.0 - rho ** 2) / max(rho ** 2, 1e-12))
    denominator_far = cf * p_head + sic_error + noise
    sinr_far = numerator_far / max(denominator_far, 1e-30)

    r_head = kappa * np.log2(1.0 + sinr_head)
    r_far = kappa * np.log2(1.0 + sinr_far)
    return float(r_head + r_far)


def conventional_noma_rate(c_head, c_far, params):
    noise = dbm_to_watt(params['noise_power_dbm'])
    p_cluster = dbm_to_watt(params['cluster_power_dbm'])
    p_head = params['power_ratio_near'] * p_cluster
    p_far = params['power_ratio_far'] * p_cluster
    kappa = prelog_factor(params)

    ch = np.abs(c_head) ** 2
    cf = np.abs(c_far) ** 2

    r_head = kappa * np.log2(1.0 + p_head * ch / noise)
    r_far = kappa * np.log2(1.0 + (p_far * cf) / (p_head * cf + noise))
    return float(r_head + r_far)


def oma_rate(c_head, c_far, num_users, params):
    noise = dbm_to_watt(params['noise_power_dbm'])
    p_cluster = dbm_to_watt(params['cluster_power_dbm'])
    kappa = prelog_factor(params)
    ch = np.abs(c_head) ** 2
    cf = np.abs(c_far) ** 2
    loading = max(0.0, 1.0 - num_users / 200.0)
    return float(
        0.5
        * loading
        * kappa
        * (np.log2(1.0 + p_cluster * ch / noise) + np.log2(1.0 + p_cluster * cf / noise))
    )


def simulate_one_topology(num_users, beta_ps, rho, params, rng):
    aps, users, pairs = deploy_network(num_users, params, rng)
    beta_all = large_scale_coefficients(aps, users, params)
    small_all = complex_normal(beta_all.shape, rng)
    true_channels = np.sqrt(beta_all) * small_all
    mu_all = mmse_estimation_variance(beta_all, params)
    estimated_all = estimated_channels(mu_all, rng)

    swipt_total = 0.0
    noma_total = 0.0
    oma_total = 0.0

    for user_a, user_b in pairs:
        h_pair = true_channels[:, [user_a, user_b]]
        hhat_pair = estimated_all[:, [user_a, user_b]]
        c_pair = beamforming_coefficients(h_pair, hhat_pair)

        head_idx, far_idx = cluster_head_order(abs(c_pair[0]), abs(c_pair[1]))
        c_head = c_pair[head_idx]
        c_far = c_pair[far_idx]
        c_cross = c_pair[far_idx]
        h12_sq = pair_channel_gain(users[user_a], users[user_b], params, rng)

        swipt_total += paper_sinr_rates(c_head, c_far, c_cross, h12_sq, beta_ps, rho, params)
        noma_total += conventional_noma_rate(c_head, c_far, params)
        oma_total += oma_rate(c_head, c_far, num_users, params)

    divisor = max(len(pairs), 1)
    return oma_total / divisor, noma_total / divisor, swipt_total / divisor


def simulate_vs_users(rho=1.0, params=None):
    cfg = dict(PAPER_PARAMS)
    if params:
        cfg.update(params)
    rng = np.random.default_rng(cfg['seed'] + int(rho * 1000))
    rows = []

    for num_users in range(cfg['num_users_min'], cfg['num_users_max'] + 1, cfg['user_step']):
        totals = {'oma': 0.0, 'conventional_noma': 0.0}
        for case_idx in range(1, 4):
            totals[f'swipt_noma_case{case_idx}'] = 0.0

        for _ in range(cfg['monte_carlo']):
            for case_idx, beta_ps in enumerate(cfg['beta_cases'], start=1):
                oma, noma, swipt = simulate_one_topology(num_users, beta_ps, rho, cfg, rng)
                if case_idx == 1:
                    totals['oma'] += oma
                    totals['conventional_noma'] += noma
                totals[f'swipt_noma_case{case_idx}'] += swipt

        row = {'users': num_users}
        for key, val in totals.items():
            row[key] = val / cfg['monte_carlo']
        rows.append(row)
    return rows


def simulate_vs_power_splitting(params=None):
    cfg = dict(PAPER_PARAMS)
    if params:
        cfg.update(params)
    rng = np.random.default_rng(cfg['seed'] + 404)
    rows = []

    for beta_ps in np.round(np.arange(0.02, 0.91, 0.02), 2):
        total_rho_1 = 0.0
        total_rho_085 = 0.0
        for _ in range(cfg['monte_carlo']):
            _, _, rate_1 = simulate_one_topology(200, beta_ps, 1.0, cfg, rng)
            _, _, rate_085 = simulate_one_topology(200, beta_ps, 0.85, cfg, rng)
            total_rho_1 += rate_1
            total_rho_085 += rate_085
        rows.append({
            'power_splitting_ratio': beta_ps,
            'rho_1': total_rho_1 / cfg['monte_carlo'],
            'rho_085': total_rho_085 / cfg['monte_carlo'],
        })
    return rows
