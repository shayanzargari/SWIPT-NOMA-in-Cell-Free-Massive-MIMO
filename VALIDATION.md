# Validation Notes

## Current repository status

This repository implements a reproducible Monte Carlo simulation workflow for evaluating SWIPT-NOMA in a cell-free massive MIMO system.

## Reproducibility workflow

Run the complete reproduction pipeline:

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
- publication-style network layout

## Figure 2

The Figure 2 reconstruction reproduces the qualitative trend reported in the paper:

- SWIPT-NOMA achieves the highest ergodic sum rate
- conventional NOMA outperforms OMA
- ergodic rate changes with user count and pairing

The implementation includes:

- random AP/user deployment
- AP-user serving association
- large-scale fading
- Rayleigh fading
- path loss and shadowing
- SWIPT-assisted relaying
- SIC-aware NOMA SINR modeling
- Monte Carlo averaging

## Validation tests

The repository includes:

- unit tests for the simulation pipeline
- CI automation through GitHub Actions
- reproducible seeded topology generation

Run tests locally:

```bash
pytest
```

## Remaining future improvements

Possible future extensions:

- exact analytical derivation matching every equation in the paper
- advanced distributed beamforming optimization
- multi-antenna AP processing
- exact numerical overlap with publication curves under original hidden seeds/settings
