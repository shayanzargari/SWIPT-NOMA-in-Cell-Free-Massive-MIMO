from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

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

results_dir = PROJECT_ROOT / 'results'
figures_dir = PROJECT_ROOT / 'figures'

results_dir.mkdir(exist_ok=True)
figures_dir.mkdir(exist_ok=True)

csv_path = results_dir / 'figure2_results.csv'
fig_path = figures_dir / 'figure2_ergodic_capacity.png'

df.to_csv(csv_path, index=False)
plot_capacity(df, fig_path)

print('Figure 2 reconstruction completed successfully.')
