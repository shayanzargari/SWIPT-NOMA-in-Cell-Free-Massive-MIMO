# Methods

This implementation follows the simulation flow of the paper for Figures 2, 3, and 4.

## Implemented workflow

1. Generate AP and user locations uniformly in a 1000 m by 1000 m area.
2. Pair users by global nearest-neighbor distance.
3. Choose the cluster-head according to the effective channel strength.
4. Generate large-scale fading using the paper path-loss model.
5. Generate Rayleigh small-scale fading and true channels.
6. Model same-cluster pilot contamination using a shared pilot variable per cluster.
7. Compute MMSE channel-estimation variance with the pilot length tau.
8. Generate estimated channels using the shared cluster variable.
9. Compute conjugate beamforming phases.
10. Compute the full coefficient tensor C_{n,n',k}.
11. Compute E[C_{n',k}] from the MMSE channel variance.
12. Compute harvested energy at the cluster-head.
13. Evaluate the cluster-head SINR.
14. Evaluate the second-user SINR with the relay term.
15. Compute rates with the prelog factor.
16. Average rates over Monte Carlo realizations.
17. Generate Figures 2, 3, and 4.

## Active files

```text
src/paper_full_simulation.py
src/paper_result_curves.py
src/paper_math.py
src/paper_params.py
src/plotting.py
scripts/rebuild_fig2.py
scripts/rebuild_fig3.py
scripts/rebuild_fig4.py
```

## Output files

```text
figures/figure2_ergodic_capacity.png
figures/figure3_ergodic_capacity_rho085.png
figures/figure4_power_splitting_ratio.png
results/figure2_results.csv
results/figure3_results.csv
results/figure4_results.csv
```
