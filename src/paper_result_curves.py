from src.paper_full_simulation import simulate_power_splitting, simulate_users


def figure2_curves(params=None):
    return simulate_users(rho=1.0, params=params)


def figure3_curves(params=None):
    return simulate_users(rho=0.85, params=params)


def figure4_curves(params=None):
    return simulate_power_splitting(params=params)
