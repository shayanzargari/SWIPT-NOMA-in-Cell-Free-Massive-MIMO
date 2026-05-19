from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.paper_result_curves import figure3_curves
from src.plotting import plot_user_capacity_curves
from src.validation import validate_capacity_scale


if __name__ == '__main__':
    out_fig = PROJECT_ROOT / 'figures'
    out_csv = PROJECT_ROOT / 'results'
    out_fig.mkdir(exist_ok=True)
    out_csv.mkdir(exist_ok=True)

    data = figure3_curves()
    validate_capacity_scale(data)
    data.to_csv(out_csv / 'figure3_results.csv', index=False)
    plot_user_capacity_curves(data, out_fig / 'figure3_ergodic_capacity_rho085.png')
    print('Saved Figure 3.')
