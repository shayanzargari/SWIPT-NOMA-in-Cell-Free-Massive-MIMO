import numpy as np


def dbm_to_watt(dbm):
    return 10.0 ** ((dbm - 30.0) / 10.0)


def watt_to_dbm(watt):
    return 10.0 * np.log10(np.maximum(watt, 1e-30)) + 30.0


def db_to_linear(value_db):
    return 10.0 ** (value_db / 10.0)


def spectral_efficiency(sinr):
    return np.log2(1.0 + np.maximum(sinr, 1e-15))
