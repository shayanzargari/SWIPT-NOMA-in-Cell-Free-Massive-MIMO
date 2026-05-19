from pathlib import Path

from src.paper_result_curves import figure2_curves, figure3_curves, figure4_curves
from src.plotting import plot_power_splitting_curves, plot_user_capacity_curves


PROJECT_ROOT = Path(__file__).resolve().parent
FIGURES_DIR = PROJECT_ROOT / 'figures'
RESULTS_DIR = PROJECT_ROOT / 'results'

FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

fig2 = figure2_curves()
fig2.to_csv(RESULTS_DIR / 'figure2_results.csv', index=False)
plot_user_capacity_curves(fig2, FIGURES_DIR / 'figure2_ergodic_capacity.png')

fig3 = figure3_curves()
fig3.to_csv(RESULTS_DIR / 'figure3_results.csv', index=False)
plot_user_capacity_curves(fig3, FIGURES_DIR / 'figure3_ergodic_capacity_rho085.png')

fig4 = figure4_curves()
fig4.to_csv(RESULTS_DIR / 'figure4_results.csv', index=False)
plot_power_splitting_curves(fig4, FIGURES_DIR / 'figure4_power_splitting_ratio.png')

print('Generated paper Figures 2, 3, and 4.')
