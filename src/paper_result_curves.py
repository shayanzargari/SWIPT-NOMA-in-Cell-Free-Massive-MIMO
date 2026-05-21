from src.paper_full_simulation import simulate_power_splitting, simulate_users


def _figure_params(params=None):
    return {} if params is None else dict(params)


def figure2_curves(params=None):
    return simulate_users(rho=1.0, params=_figure_params(params))


def figure3_curves(params=None):
    return simulate_users(rho=0.85, params=_figure_params(params))


def figure4_curves(params=None):
    return simulate_power_splitting(params=_figure_params(params))
