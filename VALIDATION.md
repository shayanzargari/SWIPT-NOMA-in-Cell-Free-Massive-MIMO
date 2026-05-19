# Validation

## Reproducibility workflow

Run the complete workflow:

```bash
bash run.sh
```

Or execute manually:

```bash
python scripts/rebuild_fig2.py
python scripts/rebuild_fig3.py
python scripts/rebuild_fig4.py
```

Expected outputs:

```text
figures/figure2_ergodic_capacity.png
figures/figure3_ergodic_capacity_rho085.png
figures/figure4_power_splitting_ratio.png
results/figure2_results.csv
results/figure3_results.csv
results/figure4_results.csv
```

## Figure 2

Ergodic sum capacity versus the number of users for OMA, conventional NOMA, and SWIPT-NOMA cases 1, 2, and 3 with rho = 1.

## Figure 3

Ergodic sum capacity versus the number of users for OMA, conventional NOMA, and SWIPT-NOMA cases 1, 2, and 3 with rho = 0.85.

## Figure 4

Ergodic sum capacity versus power-splitting ratio for rho = 1 and rho = 0.85.

## Validation tests

Run tests locally:

```bash
pytest
```

The repository also includes automated CI testing through GitHub Actions.
