import numpy as np
import pandas as pd

from src.paper_math import dbm_to_watt, pair_nearest_users, path_loss
from src.paper_params import PAPER_PARAMS


def cn(shape, rng):
    return (rng.normal(size=shape) + 1j * rng.normal(size=shape)) / np.sqrt(2.0)


def even_user_counts(params):
    start = int(params['num_users_min'])
    stop = int(params['num_users_max'])
    step = int(params['user_step'])
    values = []

    if start % 2 == 0 and start <= stop:
        values.append(start)

    grid_start = max(step, int(np.ceil(start / step)) * step)
    if grid_start % 2 != 0:
        grid_start += step

    for user_count in range(grid_start, stop + 1, step):
        if user_count % 2 == 0 and user_count not in values:
            values.append(user_count)

    if stop % 2 == 0 and stop not in values:
        values.append(stop)

    return values


def deploy(num_users, params, rng):
    if num_users % 2 != 0:
        raise ValueError('The paper model requires an even number of users, K = 2N.')

    area = params['area_size']
    aps = rng.uniform(0.0, area, size=(params['num_aps'], 2))
    users = rng.uniform(0.0, area, size=(num_users, 2))
    pairs = pair_nearest_users(users)
    return aps, users, pairs


def beta_arrays(aps, users, pairs, params):
    m = params['num_aps']
    n = len(pairs)
    beta = np.zeros((m, n, 2))

    for cluster_idx, (u1, u2) in enumerate(pairs):
        for local_idx, user_idx in enumerate((u1, u2)):
            distances = np.linalg.norm(aps - users[user_idx], axis=1)
            beta[:, cluster_idx, local_idx] = path_loss(distances, params)

    return beta


def build_correlated_channels(beta, mu, v, rng):
    estimation = np.sqrt(np.maximum(mu, 0.0)) * v[:, :, None]
    error_var = np.maximum(beta - mu, 0.0)
    error = np.sqrt(error_var) * cn(beta.shape, rng)
    return estimation + error


def reorder_cluster_heads(beta, mu, h):
    ordered_beta = beta.copy()
    ordered_mu = mu.copy()
    ordered_h = h.copy()
    effective = np.sum(np.abs(h) ** 2, axis=0)

    for cluster_idx in range(beta.shape[1]):
        if effective[cluster_idx, 1] > effective[cluster_idx, 0]:
            ordered_beta[:, cluster_idx, :] = ordered_beta[:, cluster_idx, [1, 0]]
            ordered_mu[:, cluster_idx, :] = ordered_mu[:, cluster_idx, [1, 0]]
            ordered_h[:, cluster_idx, :] = ordered_h[:, cluster_idx, [1, 0]]

    return ordered_beta, ordered_mu, ordered_h


def enforce_ap_power(num_clusters, params):
    cluster_power = dbm_to_watt(params['cluster_power_dbm'])
    ap_limit = dbm_to_watt(params['ap_power_dbm'])
    total_power = num_clusters * cluster_power
    scale = min(1.0, ap_limit / max(total_power, 1e-30))
    return cluster_power * scale


def mmse_mu(beta, params, tau):
    pp = dbm_to_watt(params['pilot_power_dbm'])
    sigma2 = dbm_to_watt(params['noise_power_dbm'])
    same_pilot_sum = np.sum(beta, axis=2, keepdims=True)
    numerator = tau * pp * beta ** 2
    denominator = tau * pp * same_pilot_sum + sigma2
    return numerator / np.maximum(denominator, 1e-30)


def shared_pilot_variable(mu, rng):
    m, n, _ = mu.shape
    return cn((m, n), rng)


def beamforming_phases(v):
    return np.conj(v) / np.maximum(np.abs(v), 1e-15)


def head_channel_phases(h):
    head_channels = h[:, :, 0]
    return np.conj(head_channels) / np.maximum(np.abs(head_channels), 1e-15)


def c_matrix(h, phases):
    return np.einsum('mrk,mt->trk', h, phases)


def expected_c_monte_carlo(mu, samples, rng):
    samples = max(int(samples), 1)
    magnitudes = np.abs(cn((samples, mu.shape[0], mu.shape[1]), rng))
    sqrt_mu = np.sqrt(np.maximum(mu, 0.0))
    return np.einsum('smn,mnk->nk', magnitudes, sqrt_mu) / samples


def inter_user_channel(users, pair, params, rng):
    u1, u2 = pair
    distance = np.linalg.norm(users[u1] - users[u2])
    b12 = path_loss(distance, params)
    return np.sqrt(b12) * cn((), rng)


def prelog_noma(num_clusters, params):
    tc = params['coherence_block']
    tau = min(num_clusters, tc)
    return max((tc - tau) / tc, 0.0)


def prelog_oma(num_clusters, params):
    tc = params['coherence_block']
    tau = min(2 * num_clusters, tc)
    return max((tc - tau) / tc, 0.0)


def inter_cluster_interference(C, cluster_idx, user_idx, p_cluster):
    interference = 0.0
    for other in range(C.shape[0]):
        if other != cluster_idx:
            interference += p_cluster * np.abs(C[other, cluster_idx, user_idx]) ** 2
    return interference


def exact_harvested_power(C, cluster_idx, beta_ps, eta, p_cluster, symbols):
    received_rf = np.sum(np.sqrt(p_cluster) * C[:, cluster_idx, 0] * symbols)
    return beta_ps * eta * np.abs(received_rf) ** 2


def safe_real_power(value):
    return max(float(np.real(value)), 0.0)


def eq17_rates(C, EC, h12, cluster_idx, beta_ps, rho, params, p_cluster, symbols):
    sigma2 = dbm_to_watt(params['noise_power_dbm'])
    p1 = params['power_ratio_near'] * p_cluster
    p2 = params['power_ratio_far'] * p_cluster
    rho_safe = max(rho, 1e-12)

    c11 = C[cluster_idx, cluster_idx, 0]
    c12 = C[cluster_idx, cluster_idx, 1]
    ec11 = EC[cluster_idx, 0]

    inter_head = inter_cluster_interference(C, cluster_idx, 0, p_cluster)
    inter_far = inter_cluster_interference(C, cluster_idx, 1, p_cluster)

    sic_expr = p2 * (
        np.abs(c11) ** 2
        + np.abs(ec11) ** 2
        - 2.0 * rho * np.real(c11 * np.conj(ec11))
    )
    sic_prop = safe_real_power(sic_expr)
    head_den = sic_prop + inter_head + sigma2 / max(1.0 - beta_ps, 1e-12)
    sinr_head = (np.abs(c11) ** 2 * p1) / max(head_den, 1e-30)

    p_eh = exact_harvested_power(C, cluster_idx, beta_ps, params['swipt_efficiency'], p_cluster, symbols)
    relay_signal = np.sqrt(max(p_eh, 0.0)) * np.abs(h12) / rho_safe
    direct_signal = c12 * np.sqrt(p2)
    numerator_far = np.abs(direct_signal + relay_signal) ** 2

    relay_error = p_eh * np.abs(h12) ** 2 * max(1.0 - rho ** 2, 0.0) / (rho_safe ** 2)
    denominator_far = np.abs(c12) ** 2 * p1 + inter_far + relay_error + sigma2
    sinr_far = numerator_far / max(denominator_far, 1e-30)

    return float(max(sinr_head, 0.0)), float(max(sinr_far, 0.0))


def conventional_noma_rate(C, cluster_idx, params, kappa, p_cluster):
    sigma2 = dbm_to_watt(params['noise_power_dbm'])
    p1 = params['power_ratio_near'] * p_cluster
    p2 = params['power_ratio_far'] * p_cluster
    c1 = C[cluster_idx, cluster_idx, 0]
    c2 = C[cluster_idx, cluster_idx, 1]
    inter_head = inter_cluster_interference(C, cluster_idx, 0, p_cluster)
    inter_far = inter_cluster_interference(C, cluster_idx, 1, p_cluster)

    r1 = np.log2(1.0 + p1 * np.abs(c1) ** 2 / (sigma2 + inter_head))
    r2 = np.log2(
        1.0 + (p2 * np.abs(c2) ** 2) / (p1 * np.abs(c2) ** 2 + sigma2 + inter_far)
    )
    return float(kappa * (r1 + r2))


def oma_rate(h, cluster_idx, params, kappa, p_cluster):
    sigma2 = dbm_to_watt(params['noise_power_dbm'])
    c1 = np.sum(np.abs(h[:, cluster_idx, 0]))
    c2 = np.sum(np.abs(h[:, cluster_idx, 1]))
    r1 = np.log2(1.0 + p_cluster * c1 ** 2 / sigma2)
    r2 = np.log2(1.0 + p_cluster * c2 ** 2 / sigma2)
    return float(0.5 * kappa * (r1 + r2))


def one_realization(num_users, beta_ps, rho, params, rng):
    aps, users, pairs = deploy(num_users, params, rng)
    num_clusters = len(pairs)
    beta = beta_arrays(aps, users, pairs, params)

    tau = min(num_clusters, params['coherence_block'])
    mu = mmse_mu(beta, params, tau)
    v = shared_pilot_variable(mu, rng)
    h = build_correlated_channels(beta, mu, v, rng)
    beta, mu, h = reorder_cluster_heads(beta, mu, h)

    estimated_phases = beamforming_phases(v)
    reference_phases = head_channel_phases(h)
    C_estimated = c_matrix(h, estimated_phases)
    C_reference = c_matrix(h, reference_phases)
    EC = expected_c_monte_carlo(mu, params['expectation_samples'], rng)

    p_cluster = enforce_ap_power(num_clusters, params)
    kappa_noma = prelog_noma(num_clusters, params)
    kappa_oma = prelog_oma(num_clusters, params)
    symbols = cn(num_clusters, rng)

    swipt = 0.0
    noma = 0.0
    oma = 0.0

    for cluster_idx, pair in enumerate(pairs):
        h12 = inter_user_channel(users, pair, params, rng)
        sinr1, sinr2 = eq17_rates(C_estimated, EC, h12, cluster_idx, beta_ps, rho, params, p_cluster, symbols)
        swipt += kappa_noma * (np.log2(1.0 + sinr1) + np.log2(1.0 + sinr2))
        noma += conventional_noma_rate(C_reference, cluster_idx, params, kappa_noma, p_cluster)
        oma += oma_rate(h, cluster_idx, params, kappa_oma, p_cluster)

    if params.get('rate_output', 'sum') == 'average':
        divisor = max(num_clusters, 1)
        return oma / divisor, noma / divisor, swipt / divisor

    return oma, noma, swipt


def simulate_users(rho, params=None):
    cfg = dict(PAPER_PARAMS)
    if params:
        cfg.update(params)
    rng = np.random.default_rng(cfg['seed'] + int(1000 * rho))
    rows = []

    for num_users in even_user_counts(cfg):
        totals = {'oma': 0.0, 'conventional_noma': 0.0}
        for case_idx in range(1, 4):
            totals[f'swipt_noma_case{case_idx}'] = 0.0

        for _ in range(cfg['monte_carlo']):
            state = rng.bit_generator.state
            for case_idx, beta_ps in enumerate(cfg['beta_cases'], start=1):
                rng.bit_generator.state = state
                oma, noma, swipt = one_realization(num_users, beta_ps, rho, cfg, rng)
                if case_idx == 1:
                    totals['oma'] += oma
                    totals['conventional_noma'] += noma
                totals[f'swipt_noma_case{case_idx}'] += swipt

        row = {'users': num_users}
        for key, val in totals.items():
            row[key] = val / cfg['monte_carlo']
        rows.append(row)
    return pd.DataFrame(rows)


def simulate_power_splitting(params=None):
    cfg = dict(PAPER_PARAMS)
    if params:
        cfg.update(params)
    rng = np.random.default_rng(cfg['seed'] + 404)
    rows = []
    fig4_users = int(cfg.get('figure4_users', 200))
    if fig4_users % 2 != 0:
        raise ValueError('figure4_users must be even because K = 2N.')

    for beta_ps in np.round(np.arange(0.02, 0.91, 0.02), 2):
        total_1 = 0.0
        total_085 = 0.0
        for _ in range(cfg['monte_carlo']):
            state = rng.bit_generator.state
            _, _, rate_1 = one_realization(fig4_users, beta_ps, 1.0, cfg, rng)
            rng.bit_generator.state = state
            _, _, rate_085 = one_realization(fig4_users, beta_ps, 0.85, cfg, rng)
            total_1 += rate_1
            total_085 += rate_085
        rows.append({
            'power_splitting_ratio': beta_ps,
            'rho_1': total_1 / cfg['monte_carlo'],
            'rho_085': total_085 / cfg['monte_carlo'],
        })
    return pd.DataFrame(rows)
