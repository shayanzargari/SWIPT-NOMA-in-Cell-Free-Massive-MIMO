# SWIPT-NOMA in Cell-Free Massive MIMO

Simulation and figure-reconstruction code for **SWIPT-NOMA in Cell-Free Massive MIMO**.

This repository generates the simulation-result figures from the paper:

- Fig. 2: ergodic sum capacity versus number of users, rho = 1
- Fig. 3: ergodic sum capacity versus number of users, rho = 0.85
- Fig. 4: ergodic sum capacity versus power-splitting ratio

## Install

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

For macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Generate figures

```bash
python scripts/rebuild_fig2.py
python scripts/rebuild_fig3.py
python scripts/rebuild_fig4.py
```

To generate all figures:

```bash
python main.py
```

or

```bash
bash run.sh
```

## Outputs

```text
figures/figure2_ergodic_capacity.png
figures/figure3_ergodic_capacity_rho085.png
figures/figure4_power_splitting_ratio.png
results/figure2_results.csv
results/figure3_results.csv
results/figure4_results.csv
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
