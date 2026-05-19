# SWIPT-NOMA in Cell-Free Massive MIMO

Simulation code for the paper **SWIPT-NOMA in Cell-Free Massive MIMO**.

This repository reconstructs the system model and ergodic capacity comparison presented in the paper using a reproducible Monte Carlo simulation framework.

## Overview

This project provides a modular implementation for evaluating simultaneous wireless information and power transfer (SWIPT) with non-orthogonal multiple access (NOMA) in a cell-free massive MIMO network.

The repository includes:

- distributed access point deployment
- AP-user serving association
- path loss and log-normal shadowing
- Rayleigh fading channels
- SWIPT-assisted relaying
- SIC-aware NOMA SINR modeling
- SWIPT-NOMA, conventional NOMA, and OMA baselines
- publication-style Figure 1 reconstruction
- upgraded Figure 2 ergodic capacity reconstruction
- validation tests and CI

## Repository structure

```text
src/
  config.py
  paper_params.py
  topology.py
  fading.py
  ap_association.py
  channel_realization.py
  paper_simulation.py
  link_budget.py
  channel.py
  clustering.py
  schemes.py
  simulation.py
  plotting.py

scripts/
  rebuild_fig1.py
  rebuild_fig2.py

tests/
  test_pipeline.py

.github/workflows/
  python-tests.yml

figures/
results/

main.py
run.sh
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
python scripts/rebuild_fig2.py --mc 500
```

## Run everything

```bash
python main.py --mc 500
```

Or:

```bash
bash run.sh
```

## Outputs

```text
figures/figure1_system_model.png
figures/figure2_ergodic_capacity.png
results/figure2_results.csv
```

## Validation

See `VALIDATION.md` for implementation details, validation workflow, current limitations, and future extensions.

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
