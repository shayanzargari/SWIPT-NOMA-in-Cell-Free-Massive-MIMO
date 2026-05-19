import numpy as np


def dbm_to_watt(dbm):
    return 10 ** ((dbm - 30.0) / 10.0)


def path_loss(distance, params):
    d = np.maximum(distance, params['min_distance_m'])
    d0 = params['reference_distance_m']
    return (d / d0) ** (-params['path_loss_exp'])


def rayleigh_gain(beta, rng):
    g = (rng.normal() + 1j * rng.normal()) / np.sqrt(2.0)
    return np.abs(np.sqrt(beta) * g) ** 2


def pair_nearest_users(users):
    remaining = list(range(len(users)))
    pairs = []
    while len(remaining) >= 2:
        first = remaining.pop(0)
        distances = np.linalg.norm(users[remaining] - users[first], axis=1)
        second_pos = int(np.argmin(distances))
        second = remaining.pop(second_pos)
        pairs.append((first, second))
    return pairs
