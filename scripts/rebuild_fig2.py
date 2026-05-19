import argparse

from src.paper_params import PAPER_PARAMS
from src.paper_simulation import PaperSimulation
from src.plotting import plot_capacity


parser = argparse.ArgumentParser(
    description='Rebuild Figure 2 using the paper-level simulation engine.',
)

parser.add_argument('--mc', type=int, default=PAPER_PARAMS['monte_carlo'])
args = parser.parse_args()

params = dict(PAPER_PARAMS)
params['monte_carlo'] = args.mc

simulation = PaperSimulation(params)
df = simulation.run()

df.to_csv('results/figure2_results.csv', index=False)
plot_capacity(df, 'figures/figure2_ergodic_capacity.png')

print('Figure 2 reconstruction completed successfully.')
