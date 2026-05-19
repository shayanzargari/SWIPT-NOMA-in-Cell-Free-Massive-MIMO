# Reproduction Checklist

Use this checklist to verify that the repository is complete and runnable.

## Environment

- [ ] Python 3.10 or newer is installed
- [ ] Dependencies are installed with `pip install -r requirements.txt`
- [ ] Optional test dependency is installed with `pip install pytest`

## Figure generation

- [ ] Figure 1 runs with `python scripts/rebuild_fig1.py`
- [ ] Figure 2 runs with `python scripts/rebuild_fig2.py --mc 500`
- [ ] Full pipeline runs with `python main.py --mc 500`
- [ ] Shell helper runs with `bash run.sh`

## Expected outputs

- [ ] `figures/figure1_system_model.png` is generated
- [ ] `figures/figure2_ergodic_capacity.png` is generated
- [ ] `results/figure2_results.csv` is generated

## Model components

- [ ] AP/user topology generation is active
- [ ] AP-user association is active
- [ ] Large-scale fading is active
- [ ] Rayleigh fading is active
- [ ] Effective channel realization is active
- [ ] SWIPT-NOMA relay contribution is active
- [ ] Conventional NOMA baseline is active
- [ ] OMA baseline is active

## Validation

- [ ] `pytest` passes locally
- [ ] GitHub Actions workflow passes
- [ ] SWIPT-NOMA curve is above OMA in the smoke test
- [ ] Output CSV contains `users`, `swipt_noma`, `noma`, and `oma`

## Notes

The implementation is designed for research-grade reproduction and extension. Exact point-by-point numerical overlap with the original publication requires the original random seeds, plotting choices, and any unpublished experimental details used at the time of manuscript preparation.
