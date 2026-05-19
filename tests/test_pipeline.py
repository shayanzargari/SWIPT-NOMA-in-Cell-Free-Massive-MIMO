from src.paper_simulation import PaperSimulation
from src.paper_params import PAPER_PARAMS


def test_simulation_runs():
    params = dict(PAPER_PARAMS)
    params['monte_carlo'] = 2
    params['num_users_max'] = 4

    simulation = PaperSimulation(params)
    df = simulation.run()

    assert len(df) > 0
    assert 'swipt_noma' in df.columns
    assert 'noma' in df.columns
    assert 'oma' in df.columns


def test_swipt_outperforms_oma():
    params = dict(PAPER_PARAMS)
    params['monte_carlo'] = 2
    params['num_users_max'] = 4

    simulation = PaperSimulation(params)
    df = simulation.run()

    assert df['swipt_noma'].mean() >= df['oma'].mean()
