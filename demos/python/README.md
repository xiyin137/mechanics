# Python Demonstrations

The Python demos are command-line scripts.  They avoid hidden notebooks so that
the command, output, and test coverage are easy to inspect.

## Recommended Environment

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

The scripts use NumPy for numerical work.  Plotting commands also require
Matplotlib.

## Fast Verification

```sh
python -m compileall -q demos/python
python demos/python/circular_restricted_three_body.py --quick
python demos/python/asteroid_ejection_probability.py --quick --no-plot
```

The repository test suite exercises all core scripts:

```sh
python -m pytest
```

## Machine-Readable Runs

The CR3BP and asteroid-ejection scripts can write JSON summaries:

```sh
python demos/python/circular_restricted_three_body.py \
  --preset sun-jupiter \
  --initial l4 \
  --quick \
  --json-output data/cr3bp_sun_jupiter_quick.json

python demos/python/asteroid_ejection_probability.py \
  --lecture \
  --seed 7 \
  --output-dir data/asteroid_lecture \
  --no-plot
```

The asteroid script also writes binned CSV data:

```sh
python demos/python/asteroid_ejection_probability.py \
  --n 256 \
  --years 200 \
  --dt 0.02 \
  --seed 7 \
  --csv data/ejection_demo.csv \
  --plot figures/ejection_demo.png
```

The JSON summaries are designed for lab records.  They include the model,
configuration, integrator note, diagnostic quantities, output paths, and, for
the asteroid ensemble, binomial standard errors.

## Numerical Diagnostics

- Rigid-body runs monitor energy, angular momentum, attitude orthogonality, and
  determinant drift.
- Hamiltonian pendulum and standard-map runs illustrate structure-preserving
  behavior and area preservation.
- CR3BP runs report Jacobi drift.  RK4 is transparent, but it is not a
  structure-preserving long-time integrator.
- Asteroid ensemble runs report loss counts, ejection probability, loss
  probability, and binned standard errors.
- Fluid and elasticity demos compare formulas, residuals, or boundary values
  against exact expressions.

## Presets

`--quick` is for smoke tests and in-class live runs.  `--lecture` on the
asteroid script is a moderate run for a prepared lecture.  `--long` is reserved
for larger sweeps and should be treated as a computational experiment rather
than a default command.
