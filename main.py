import argparse

from src.paper_params import PAPER_PARAMS
from src.paper_simulation import PaperSimulation
from src.plotting import plot_capacity, plot_system_model


parser = argparse.ArgumentParser(
    description='Run the full SWIPT-NOMA cell-free massive MIMO reproduction pipeline.',
)
parser.add_argument('--mc', type=int, default=PAPER_PARAMS['monte_carlo'])
args = parser.parse_args()

params = dict(PAPER_PARAMS)
params['monte_carlo'] = args.mc

simulation = PaperSimulation(params)
df = simulation.run()

plot_system_model('figures/figure1_system_model.png')
df.to_csv('results/figure2_results.csv', index=False)
plot_capacity(df, 'figures/figure2_ergodic_capacity.png')

print('Finished generating all paper figures and numerical results.')
