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
        best_pair = None
        best_distance = np.inf

        for i, first in enumerate(remaining[:-1]):
            rest = remaining[i + 1:]
            distances = np.linalg.norm(users[rest] - users[first], axis=1)
            j = int(np.argmin(distances))
            if distances[j] < best_distance:
                best_distance = float(distances[j])
                best_pair = (first, rest[j])

        first, second = best_pair
        pairs.append((first, second))
        remaining.remove(first)
        remaining.remove(second)

    return pairs
