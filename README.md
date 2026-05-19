# SWIPT-NOMA in Cell-Free Massive MIMO

Simulation code for the paper **SWIPT-NOMA in Cell-Free Massive MIMO**.

This repository rebuilds the system model and ergodic capacity comparison presented in the paper using a Monte Carlo simulation framework.

## Overview

This project provides a clean and reproducible implementation of the main simulation workflow for evaluating simultaneous wireless information and power transfer (SWIPT) with non-orthogonal multiple access (NOMA) in a cell-free massive MIMO network.

## Implemented features

- Cell-free massive MIMO deployment
- Random AP and user locations
- Distance-based path loss and log-normal shadowing
- Rayleigh fading
- Distributed conjugate beamforming style effective channels
- SWIPT-NOMA rate model
- Conventional NOMA baseline
- OMA baseline
- Figure 1 system model reconstruction
- Figure 2 ergodic capacity reconstruction

## Install

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Rebuild figures

```bash
python scripts/rebuild_fig1.py
python scripts/rebuild_fig2.py --mc 200
```

For a faster smoke test:

```bash
python scripts/rebuild_fig2.py --mc 20
```

## Run everything

```bash
python main.py --mc 200
```

## Outputs

```text
figures/figure1_system_model.png
figures/figure2_ergodic_capacity.png
results/figure2_results.csv
```

## Citation

```bibtex
@inproceedings{zargari2020swipt,
  title={SWIPT-NOMA in Cell-Free Massive MIMO},
  author={Zargari, Shayan and Khalili, Ata and Zhang, Rui},
  booktitle={2020 28th Iranian Conference on Electrical Engineering (ICEE)},
  year={2020},
  organization={IEEE}
}
```
