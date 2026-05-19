import argparse

from src.config import SimulationConfig
from src.plotting import plot_capacity
from src.simulation import MonteCarloSimulation


parser = argparse.ArgumentParser()
parser.add_argument('--mc', type=int, default=200)
args = parser.parse_args()

cfg = SimulationConfig(monte_carlo=args.mc)

sim = MonteCarloSimulation(cfg)
df = sim.run()

df.to_csv('results/figure2_results.csv', index=False)
plot_capacity(df, 'figures/figure2_ergodic_capacity.png')

print('Saved Figure 2 reconstruction.')
