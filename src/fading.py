import numpy as np

from src.link_budget import db_to_linear


def large_scale_fading(distances, params, rng):
    path_loss_db = -10.0 * params['path_loss_exp'] * np.log10(distances)
    shadow_db = rng.normal(0.0, params['shadow_std_db'], distances.shape)
    return db_to_linear(path_loss_db + shadow_db)


def small_scale_fading(shape, rng):
    real = rng.normal(0.0, 1.0, shape)
    imag = rng.normal(0.0, 1.0, shape)
    return (real + 1j * imag) / np.sqrt(2.0)
