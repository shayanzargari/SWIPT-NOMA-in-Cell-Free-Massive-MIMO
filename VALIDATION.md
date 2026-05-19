# Validation Notes

## Current repository status

This repository implements a reproducible Monte Carlo simulation workflow for evaluating SWIPT-NOMA in a cell-free massive MIMO system.

## Figure 1

The current Figure 1 reconstruction is a clean conceptual redraw of the system architecture presented in the paper. It illustrates:

- distributed access points
- near and far NOMA users
- SWIPT-assisted relaying
- energy transfer links

The current figure is not an exact pixel-level recreation of the published figure.

## Figure 2

The current Figure 2 reconstruction reproduces the qualitative trend reported in the paper:

- SWIPT-NOMA achieves the highest ergodic sum rate
- conventional NOMA outperforms OMA
- ergodic rate changes with user count and pairing

The implementation includes:

- random AP/user deployment
- Rayleigh fading
- path loss and shadowing
- SWIPT-assisted relaying
- SIC-aware NOMA SINR modeling
- Monte Carlo averaging

## Remaining future improvements

Possible future extensions:

- exact analytical derivation matching every equation in the paper
- AP clustering / user-centric association
- explicit distributed beamforming coefficients
- multi-antenna AP processing
- exact reproduction of publication figure styling
