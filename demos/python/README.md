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
python demos/python/asteroid_resonance_normal_form.py --quick
python demos/python/binary_capture_scattering.py --quick
python demos/python/lidov_kozai.py --quick
python demos/python/heavy_symmetric_top.py --quick
python demos/python/three_body_benchmark_studies.py --quick
```

The repository test suite exercises all core scripts:

```sh
python -m pytest
```

## Machine-Readable Runs

Every major Python demo can print JSON summaries:

```sh
python demos/python/hamiltonian_pendulum.py --quick --json
python demos/python/rigid_body_euler_top.py --quick --json
python demos/python/standard_map.py --quick --json
python demos/python/standard_map_homoclinic_tangle.py --quick --json
python demos/python/standard_map_torus_breakdown.py --quick --json
python demos/python/henon_heiles_poincare.py --quick --json
python demos/python/circular_restricted_three_body.py --quick --json
python demos/python/lidov_kozai.py --quick --json
python demos/python/asteroid_ejection_probability.py --quick --no-plot --json
python demos/python/asteroid_resonance_normal_form.py --quick --json
python demos/python/binary_capture_scattering.py --quick --json
python demos/python/three_body_benchmark_studies.py --quick --json
python demos/python/linear_elasticity.py --quick --json
python demos/python/navier_stokes_solutions.py --quick --json
python demos/python/deforming_body_gauge.py --quick --json
python demos/python/cosserat_rod_demo.py --quick --json
python demos/python/fluids_vorticity.py --quick --json
python demos/python/heavy_symmetric_top.py --quick --json
```

Selected runs can write persistent JSON and figures:

```sh
python demos/python/circular_restricted_three_body.py \
  --preset sun-jupiter \
  --initial l4 \
  --quick \
  --output-dir data/cr3bp_sun_jupiter_quick

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

The resonance-normal-form script is the fast analytic companion to the
asteroid ensemble.  It computes nominal resonance locations, illustrative
pendulum width scaling, and a genuine first-order disturbing-function
coefficient for the 2:1 resonance:

```sh
python demos/python/asteroid_resonance_normal_form.py \
  --quick \
  --csv data/asteroid_resonance_normal_form_widths.csv \
  --plot figures/asteroid_resonance_normal_form.png
```

The standard-map homoclinic-tangle script computes finite images of local
stable and unstable manifold segments for the hyperbolic fixed point:

```sh
python demos/python/standard_map_homoclinic_tangle.py \
  --quick \
  --json-output data/standard_map_homoclinic_tangle_quick.json \
  --plot figures/standard_map_homoclinic_tangle.png
```

The binary-scattering script is a parallel planar three-body probability
experiment.  It samples coplanar binary-single encounters and reports
ensemble-dependent finite-time capture, exchange, ionization, flyby, and
collision statistics.  The `--v-inf` parameter is the asymptotic incoming
speed; the script derives the finite launch speed from the initial interaction
energy.  Reported cross sections use the script's axisymmetric area
normalization for planar trajectories, not a full spatial scattering ensemble.

```sh
python demos/python/binary_capture_scattering.py \
  --quick \
  --json-output data/binary_capture_scattering_quick.json \
  --plot figures/binary_capture_scattering.png
```

The Lidov-Kozai and heavy-top scripts are analytic/reduced phase-space labs:

```sh
python demos/python/lidov_kozai.py --quick --plot figures/lidov_kozai.png
python demos/python/heavy_symmetric_top.py --quick --plot figures/heavy_symmetric_top.png
```

The benchmark driver runs a compact pair of statistical three-body studies: a
planar restricted asteroid ensemble and a planar binary-single scattering
sweep:

```sh
python demos/python/three_body_benchmark_studies.py \
  --quick \
  --json-output data/three_body_benchmark_quick.json \
  --plot figures/three_body_benchmark_quick.png \
  --asteroid-plot figures/three_body_asteroid_loss_quick.png \
  --binary-plot figures/three_body_binary_scattering_quick.png
```

For finite-time sensitivity checks in the asteroid lab:

```sh
python demos/python/asteroid_ejection_probability.py \
  --quick \
  --no-plot \
  --sensitivity timestep \
  --json
```

The JSON summaries are designed for lab records.  They include the model,
configuration, integrator note, diagnostic quantities, output paths, and, for
the asteroid ensemble, binomial standard errors, resonance-window diagnostics,
survival checkpoints, per-particle outcome rows, and optional sensitivity rows.
For binary scattering, the JSON records the sampling rule, exclusive outcome
fractions, derived capture-or-exchange count, cross-section estimates,
finite-launch speed diagnostics, and energy-drift diagnostics.
The benchmark JSON records aggregate asteroid loss bins across seeds and a
binary-scattering cross-section sweep over \(v_\infty\).

## Numerical Diagnostics

- Rigid-body runs monitor energy, angular momentum, attitude orthogonality, and
  determinant drift.
- Heavy-top runs monitor the one-dimensional effective-potential reduction and
  energy drift during nutation.
- Hamiltonian pendulum and standard-map runs illustrate structure-preserving
  behavior and area preservation.
- Standard-map homoclinic-tangle runs report the linearized stable and unstable
  eigenvalues at the hyperbolic fixed point and plot finite manifold images.
- Henon-Heiles runs generate genuine Poincare sections on \(y=0,\ p_y>0\) and
  report energy drift for the velocity-Verlet integration.
- CR3BP runs report Jacobi drift for the planar rotating-frame state.  RK4 is
  transparent, but it is not a
  structure-preserving long-time integrator.
- Lidov-Kozai runs report the conserved \(j\cos i\), the critical inclination,
  the tiny regularizing eccentricity used when the requested initial orbit is
  exactly circular, Hamiltonian drift, chart-boundary termination diagnostics,
  and the maximum eccentricity for the initially circular limit.  The demo uses
  classical RK4 for transparency, so the Hamiltonian drift is a diagnostic, not
  a preserved invariant; the quick regression test requires it to stay below
  \(5\times10^{-5}\).
- Asteroid ensemble runs report loss counts, ejection probability, loss
  probability, binned standard errors, nearest-resonance summaries, and
  survival curves for the planar restricted model.
- Resonance-normal-form runs report nominal Jovian resonance locations, the
  generic scaling, and the computed 2:1 disturbing-function width estimate.
- Binary-scattering runs report finite-horizon binding-energy outcome classes,
  launch-speed diagnostics, and area-normalized cross sections for the stated
  planar impact-parameter sampling rule.
- Three-body benchmark runs report aggregate asteroid loss statistics and
  binary capture/exchange cross sections with finite-sample error estimates.
- Fluid and elasticity demos compare formulas, residuals, or boundary values
  against exact expressions.

## Presets

`--quick` is for smoke tests and in-class live runs.  `--lecture` is a moderate
prepared demonstration.  `--long` is reserved for larger sweeps and should be
treated as a computational experiment rather than a default command.
