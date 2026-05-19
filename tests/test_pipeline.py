from src.paper_params import PAPER_PARAMS
from src.paper_result_curves import figure2_curves, figure3_curves, figure4_curves


def small_params():
    params = dict(PAPER_PARAMS)
    params['monte_carlo'] = 1
    params['num_users_min'] = 2
    params['num_users_max'] = 6
    params['user_step'] = 2
    return params


def test_figure2_full_simulation_runs():
    df = figure2_curves(small_params())
    assert len(df) > 0
    assert {'users', 'oma', 'conventional_noma', 'swipt_noma_case1'}.issubset(df.columns)
    assert df.notna().all().all()


def test_figure3_full_simulation_runs():
    df = figure3_curves(small_params())
    assert len(df) > 0
    assert {'users', 'oma', 'conventional_noma', 'swipt_noma_case1'}.issubset(df.columns)
    assert df.notna().all().all()


def test_figure4_full_simulation_runs():
    params = small_params()
    params['monte_carlo'] = 1
    df = figure4_curves(params)
    assert len(df) > 0
    assert {'power_splitting_ratio', 'rho_1', 'rho_085'}.issubset(df.columns)
    assert df.notna().all().all()
