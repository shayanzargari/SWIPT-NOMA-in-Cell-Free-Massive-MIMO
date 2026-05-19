import numpy as np
import pandas as pd

from src.paper_math import dbm_to_watt, pair_nearest_users, path_loss
from src.paper_params import PAPER_PARAMS


def cn(shape, rng):
    return (rng.normal(size=shape) + 1j * rng.normal(size=shape)) / np.sqrt(2.0)


def deploy(num_users, params, rng):
    area = params['area_size']
    aps = rng.uniform(0.0, area, size=(params['num_aps'], 2))
    users = rng.uniform(0.0, area, size=(num_users, 2))
    pairs = pair_nearest_users(users)
    return aps, users, pairs


def pair_arrays(aps, users, pairs, params, rng):
    m = params['num_aps']
    n = len(pairs)
    beta = np.zeros((m, n, 2))
    h = np.zeros((m, n, 2), dtype=complex)

    for cluster_idx, (u1, u2) in enumerate(pairs):
        for local_idx, user_idx in enumerate((u1, u2)):
            distances = np.linalg.norm(aps - users[user_idx], axis=1)
            beta[:, cluster_idx, local_idx] = path_loss(distances, params)
            h[:, cluster_idx, local_idx] = np.sqrt(beta[:, cluster_idx, local_idx]) * cn(m, rng)

    return beta, h


def reorder_cluster_heads(beta, h):
    ordered_beta = beta.copy()
    ordered_h = h.copy()
    effective = np.sum(np.abs(h) ** 2, axis=0)

    for cluster_idx in range(beta.shape[1]):
        if effective[cluster_idx, 1] > effective[cluster_idx, 0]:
            ordered_beta[:, cluster_idx, :] = ordered_beta[:, cluster_idx, [1, 0]]
            ordered_h[:, cluster_idx, :] = ordered_h[:, cluster_idx, [1, 0]]

    return ordered_beta, ordered_h


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


def c_matrix(h, phases):
    return np.einsum('mrk,mt->trk', h, phases)


def expected_c_monte_carlo(mu, samples, rng):
    m, n, k = mu.shape
    acc = np.zeros((n, k), dtype=complex)

    for _ in range(samples):
        v = cn((m, n), rng)
        h_hat = np.sqrt(np.maximum(mu, 0.0)) * v[:, :, None]
        phase = beamforming_phases(v)
        acc += np.einsum('mnk,mn->nk', h_hat, phase)

    return acc / max(samples, 1)


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


def exact_harvested_power(C, cluster_idx, beta_ps, eta, p_cluster):
    symbols = np.ones(C.shape[0], dtype=complex)
    received_rf = np.sum(np.sqrt(p_cluster) * C[:, cluster_idx, 0] * symbols)
    return beta_ps * eta * np.abs(received_rf) ** 2


def eq17_rates(C, EC, h12, cluster_idx, beta_ps, rho, params, p_cluster):
    sigma2 = dbm_to_watt(params['noise_power_dbm'])
    p1 = params['power_ratio_near'] * p_cluster
    p2 = params['power_ratio_far'] * p_cluster

    n = C.shape[0]
    c11 = C[cluster_idx, cluster_idx, 0]
    c12 = C[cluster_idx, cluster_idx, 1]
    ec11 = EC[cluster_idx, 0]

    inter_head = 0.0
    inter_far = 0.0
    for other in range(n):
        if other == cluster_idx:
            continue
        inter_head += p_cluster * np.abs(C[other, cluster_idx, 0]) ** 2
        inter_far += p_cluster * np.abs(C[other, cluster_idx, 1]) ** 2

    sic_prop = p2 * (
        np.abs(c11) ** 2
        + np.abs(ec11) ** 2
        - 2.0 * rho * np.real(c11 * np.conj(ec11))
    )
    sinr_head = (np.abs(ec11) ** 2 * p1) / (
        sic_prop + inter_head + sigma2 / max(1.0 - beta_ps, 1e-12)
    )

    p_eh = exact_harvested_power(C, cluster_idx, beta_ps, params['swipt_efficiency'], p_cluster)
    relay_signal = np.sqrt(max(p_eh, 0.0)) * h12 / max(rho, 1e-12)
    direct_signal = c12 * np.sqrt(p2)
    numerator_far = np.abs(direct_signal + relay_signal) ** 2

    relay_error = p_eh * np.abs(h12) ** 2 * ((1.0 - rho ** 2) / max(rho ** 2, 1e-12))
    denominator_far = np.abs(c12) ** 2 * p1 + inter_far + relay_error + sigma2
    sinr_far = numerator_far / max(denominator_far, 1e-30)

    return sinr_head, sinr_far


def conventional_noma_rate(C, cluster_idx, params, kappa, p_cluster):
    sigma2 = dbm_to_watt(params['noise_power_dbm'])
    p1 = params['power_ratio_near'] * p_cluster
    p2 = params['power_ratio_far'] * p_cluster
    c1 = C[cluster_idx, cluster_idx, 0]
    c2 = C[cluster_idx, cluster_idx, 1]
    r1 = np.log2(1.0 + p1 * np.abs(c1) ** 2 / sigma2)
    r2 = np.log2(1.0 + (p2 * np.abs(c2) ** 2) / (p1 * np.abs(c2) ** 2 + sigma2))
    return float(kappa * (r1 + r2))


def oma_rate(C, cluster_idx, params, kappa, p_cluster):
    sigma2 = dbm_to_watt(params['noise_power_dbm'])
    c1 = C[cluster_idx, cluster_idx, 0]
    c2 = C[cluster_idx, cluster_idx, 1]
    r1 = np.log2(1.0 + p_cluster * np.abs(c1) ** 2 / sigma2)
    r2 = np.log2(1.0 + p_cluster * np.abs(c2) ** 2 / sigma2)
    return float(0.5 * kappa * (r1 + r2))


def one_realization(num_users, beta_ps, rho, params, rng):
    aps, users, pairs = deploy(num_users, params, rng)
    num_clusters = len(pairs)
    beta, h = pair_arrays(aps, users, pairs, params, rng)
    beta, h = reorder_cluster_heads(beta, h)

    tau = min(num_clusters, params['coherence_block'])
    mu = mmse_mu(beta, params, tau)
    v = shared_pilot_variable(mu, rng)
    phases = beamforming_phases(v)
    C = c_matrix(h, phases)
    EC = expected_c_monte_carlo(mu, params['expectation_samples'], rng)

    p_cluster = enforce_ap_power(num_clusters, params)
    kappa_noma = prelog_noma(num_clusters, params)
    kappa_oma = prelog_oma(num_clusters, params)

    swipt = 0.0
    noma = 0.0
    oma = 0.0

    for cluster_idx, pair in enumerate(pairs):
        h12 = inter_user_channel(users, pair, params, rng)
        sinr1, sinr2 = eq17_rates(C, EC, h12, cluster_idx, beta_ps, rho, params, p_cluster)
        swipt += kappa_noma * (np.log2(1.0 + sinr1) + np.log2(1.0 + sinr2))
        noma += conventional_noma_rate(C, cluster_idx, params, kappa_noma, p_cluster)
        oma += oma_rate(C, cluster_idx, params, kappa_oma, p_cluster)

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

    for num_users in range(cfg['num_users_min'], cfg['num_users_max'] + 1, cfg['user_step']):
        totals = {'oma': 0.0, 'conventional_noma': 0.0}
        for case_idx in range(1, 4):
            totals[f'swipt_noma_case{case_idx}'] = 0.0

        for _ in range(cfg['monte_carlo']):
            for case_idx, beta_ps in enumerate(cfg['beta_cases'], start=1):
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
    fig4_users = cfg.get('figure4_users', 200)

    for beta_ps in np.round(np.arange(0.02, 0.91, 0.02), 2):
        total_1 = 0.0
        total_085 = 0.0
        for _ in range(cfg['monte_carlo']):
            _, _, rate_1 = one_realization(fig4_users, beta_ps, 1.0, cfg, rng)
            _, _, rate_085 = one_realization(fig4_users, beta_ps, 0.85, cfg, rng)
            total_1 += rate_1
            total_085 += rate_085
        rows.append({
            'power_splitting_ratio': beta_ps,
            'rho_1': total_1 / cfg['monte_carlo'],
            'rho_085': total_085 / cfg['monte_carlo'],
        })
    return pd.DataFrame(rows)
