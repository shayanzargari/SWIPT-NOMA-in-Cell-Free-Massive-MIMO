# SWIPT-NOMA in Cell-Free Massive MIMO

Simulation code for the paper **SWIPT-NOMA in Cell-Free Massive MIMO**.

This repository contains the simulation framework used to evaluate simultaneous wireless information and power transfer (SWIPT) with non-orthogonal multiple access (NOMA) in a cell-free massive MIMO network.

## Overview

The implementation includes:

- distributed access point deployment
- AP-user serving association
- path loss and log-normal shadowing
- Rayleigh fading channels
- SWIPT-assisted relaying
- SIC-aware NOMA SINR modeling
- SWIPT-NOMA, conventional NOMA, and OMA baselines
- Figure 1 system model generation
- Figure 2 ergodic capacity generation
- validation tests and CI

## Repository structure

```text
src/
  paper_params.py
  topology.py
  fading.py
  ap_association.py
  channel_realization.py
  paper_simulation.py
  link_budget.py
  clustering.py
  schemes.py
  plotting.py

scripts/
  rebuild_fig1.py
  rebuild_fig2.py

tests/
  test_pipeline.py

main.py
run.sh
VALIDATION.md
requirements.txt
```

## Installation

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

## Generate figures

```bash
python scripts/rebuild_fig1.py
python scripts/rebuild_fig2.py --mc 500
```

To run the complete workflow:

```bash
python main.py --mc 500
```

or

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

```bash
pytest
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
