import numpy as np

from src.paper_math import dbm_to_watt


def cluster_sum_rates(
    g_a,
    g_b,
    h_12,
    beta_ps,
    rho,
    params,
    num_clusters=1,
    interference_gain=0.0,
):
    noise = dbm_to_watt(params['noise_power_dbm'])
    power = dbm_to_watt(params['cluster_power_dbm'])
    p_near = params['power_ratio_near'] * power
    p_far = params['power_ratio_far'] * power
    kappa = (params['coherence_block'] - 1.0) / params['coherence_block']

    g_near = max(g_a, g_b)
    g_far = min(g_a, g_b)

    inter_cluster = max(num_clusters - 1, 0) * power * interference_gain

    oma = 0.5 * kappa * (
        np.log2(1.0 + power * g_near / (noise + inter_cluster))
        + np.log2(1.0 + power * g_far / (noise + inter_cluster))
    )

    noma_near = kappa * np.log2(
        1.0 + p_near * g_near / (noise + inter_cluster)
    )
    noma_far = kappa * np.log2(
        1.0 + (p_far * g_far) / (p_near * g_far + noise + inter_cluster)
    )
    noma = noma_near + noma_far

    id_factor = max(1.0 - beta_ps, 1e-12)
    harvested_power = params['swipt_efficiency'] * beta_ps * power * g_near
    relay_sinr = harvested_power * h_12 / (noise + inter_cluster)
    sic_error = (1.0 - rho ** 2) * p_far * g_near

    swipt_near = kappa * np.log2(
        1.0
        + (id_factor * p_near * g_near)
        / (id_factor * noise + inter_cluster + sic_error)
    )
    swipt_far_direct = (id_factor * p_far * g_far) / (
        id_factor * p_near * g_far + id_factor * noise + inter_cluster
    )
    swipt_far = kappa * np.log2(1.0 + swipt_far_direct + relay_sinr)

    return oma, noma, swipt_near + swipt_far
