# Validation

## Reproducibility workflow

Run the complete workflow:

```bash
bash run.sh
```

Or execute manually:

```bash
python scripts/rebuild_fig1.py
python scripts/rebuild_fig2.py --mc 500
```

Expected outputs:

```text
figures/figure1_system_model.png
figures/figure2_ergodic_capacity.png
results/figure2_results.csv
```

## Figure 1

The Figure 1 reconstruction includes:

- distributed access points
- CPU/controller
- near and far NOMA users
- SWIPT-assisted relaying
- decode-forward relay links
- energy-transfer annotations

## Figure 2

The Figure 2 workflow includes:

- random AP/user deployment
- AP-user serving association
- large-scale fading
- Rayleigh fading
- path loss and shadowing
- SWIPT-assisted relaying
- SIC-aware NOMA SINR modeling
- Monte Carlo averaging

## Validation tests

Run tests locally:

```bash
pytest
```

The repository also includes automated CI testing through GitHub Actions.
