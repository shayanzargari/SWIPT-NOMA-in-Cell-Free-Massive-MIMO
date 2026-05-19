from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.paper_result_curves import figure2_curves
from src.plotting import plot_user_capacity_curves


if __name__ == '__main__':
    figures_dir = PROJECT_ROOT / 'figures'
    results_dir = PROJECT_ROOT / 'results'
    figures_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    df = figure2_curves()
    df.to_csv(results_dir / 'figure2_results.csv', index=False)
    plot_user_capacity_curves(df, figures_dir / 'figure2_ergodic_capacity.png')
    print('Saved paper Fig. 2 capacity reconstruction.')
