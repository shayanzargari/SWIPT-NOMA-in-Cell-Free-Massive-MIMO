from src.paper_params import PAPER_PARAMS
from src.paper_simulation import PaperSimulation


def small_params():
    params = dict(PAPER_PARAMS)
    params['monte_carlo'] = 2
    params['num_users_max'] = 4
    return params


def test_simulation_runs():
    simulation = PaperSimulation(small_params())
    df = simulation.run()

    assert len(df) > 0
    assert {'users', 'swipt_noma', 'noma', 'oma'}.issubset(df.columns)
    assert df.notna().all().all()


def test_expected_rate_ordering():
    simulation = PaperSimulation(small_params())
    df = simulation.run()

    assert df['swipt_noma'].mean() >= df['oma'].mean()
    assert df['noma'].mean() >= df['oma'].mean()
