import pandas as pd

from src.paper_equations import simulate_vs_users
from src.paper_monte_carlo import simulate_power_splitting


def figure2_curves(params=None):
    return pd.DataFrame(simulate_vs_users(rho=1.0, params=params))


def figure3_curves(params=None):
    return pd.DataFrame(simulate_vs_users(rho=0.85, params=params))


def figure4_curves(params=None):
    return simulate_power_splitting(params=params)
