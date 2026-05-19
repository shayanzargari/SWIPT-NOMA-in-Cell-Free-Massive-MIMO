# SWIPT-NOMA in Cell-Free Massive MIMO

Simulation code for the paper **SWIPT-NOMA in Cell-Free Massive MIMO**.

This repository reconstructs the system model and ergodic capacity comparison presented in the paper using a reproducible Monte Carlo simulation framework.

## Overview

This project provides a modular implementation for evaluating simultaneous wireless information and power transfer (SWIPT) with non-orthogonal multiple access (NOMA) in a cell-free massive MIMO network.

The repository includes:

- distributed access point deployment
- random user topology generation
- path loss and log-normal shadowing
- Rayleigh fading channels
- SWIPT-assisted relaying
- SIC-aware NOMA SINR modeling
- SWIPT-NOMA, conventional NOMA, and OMA baselines
- Figure 1 reconstruction
- Figure 2 ergodic capacity reconstruction

## Repository structure

```text
src/
  config.py
  paper_params.py
  channel.py
  clustering.py
  schemes.py
  simulation.py
  plotting.py

scripts/
  rebuild_fig1.py
  rebuild_fig2.py

main.py
VALIDATION.md
requirements.txt
```

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

## Validation

See `VALIDATION.md` for implementation details, current limitations, and future extensions.

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
