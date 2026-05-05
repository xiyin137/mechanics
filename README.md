# Notes on Classical Mechanics

This repository is a teaching project for advanced mechanics centered on
Lagrangian mechanics, Hamiltonian mechanics, phase space, integrability, chaos,
rigid bodies, celestial mechanics, elastic and deforming bodies, and fluids.

The organizing idea is that mechanics is geometry made computational: motion is
described by variational principles, conserved quantities come from symmetry,
phase space carries structure, and both finite-dimensional bodies and continua
can be studied through the same geometric language.

## Current Contents

- `notes/tex`: TeX source for the integrated course notes.
- `main.pdf`: current rendered PDF at the repository root.
- `demos/python`: runnable Python simulations and numerical experiments.
- `demos/mathematica`: Wolfram Language scripts for symbolic and numerical demos.
- `demos/labs`: public laboratory guides attached to selected chapters.
- `references`: public reference shelf and bibliography notes.
- `syllabus`: course map and module sequence.
- `tests`: smoke and numerical-behavior tests for the demo code.

## First Case Studies

1. **Euler top and 3D rigid body mechanics**
   - Euler equations
   - energy and angular momentum invariants
   - integrability and reduced phase portraits

2. **Sun-Jupiter-asteroid restricted problem**
   - Kepler problem as an integrable baseline
   - Jupiter as a perturbation
   - circular restricted three-body problem, Lagrange points, and Jacobi integral
   - full three-body reduction, central configurations, and Jacobi coordinates
   - resonances, chaotic transport, resonance-labelled finite-time ejection
     probabilities
   - binary-star and binary-single scattering examples as broader
     astrophysical three-body applications
   - Lidov-Kozai secular cycles and benchmark statistical studies

3. **Elastic and deforming bodies**
   - finite strain, linear elasticity, elastic waves, bars, shafts, and beams
   - gauge theory of deforming bodies in the Shapere-Wilczek style
   - shape space, mechanical connection, curvature, holonomy, and local frames
   - Cosserat media and defect fields as bridges from rigid bodies to continua

4. **Fluid mechanics**
   - Navier-Stokes derivation from balance laws and Newtonian stress
   - exact Couette, Poiseuille, Stokes-layer, and Taylor-Green solutions
   - vorticity, circulation, and Hamiltonian point vortices

## Reading Path

The notes are written as a full reference, but they can be taught in two
passes. The core pass covers notation, variational mechanics, Hamiltonian phase
space, Liouville tori, Kepler motion, the Euler top, resonant perturbation
theory, KAM survival and torus breakdown, CR3BP/Jacobi geometry, finite strain,
linear elasticity, the first gauge-theory examples, Navier-Stokes derivation,
and exact laminar solutions. The extended pass adds the longer KAM discussion,
cantori and turnstiles, the full three-body reduction, asteroid ejection
statistics, detailed elastic boundary-value formulas, Shapere-Wilczek holonomy,
Cosserat media, defect geometry, Orr-Sommerfeld stability, and point vortices.

## Quick Start

Create a Python 3.9 or newer environment and install the Python dependencies:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the highlighted planar asteroid ejection probability demo:

```sh
python demos/python/asteroid_ejection_probability.py --lecture --seed 7 --output-dir data/asteroid_lecture --plot figures/ejection_demo.png
```

Run the planar circular restricted three-body demo with Jacobi-drift
diagnostics and zero-velocity curves:

```sh
python demos/python/circular_restricted_three_body.py --preset sun-jupiter --periods 3 --dt 0.0025 --plot figures/cr3bp_zero_velocity.png --json-output data/cr3bp_zero_velocity.json
```

The Makefile alias for this figure is:

```sh
make cr3bp-zerovel-demo
```

Run the invariant-torus breakdown diagnostic for the standard map:

```sh
python demos/python/standard_map_torus_breakdown.py --K 1.1 --steps 1500 --orbits 128 --plot figures/standard_map_torus_breakdown.png
```

The Makefile alias for this figure is:

```sh
make standard-map-breakdown-demo
```

Run the stable/unstable manifold and homoclinic-tangle figure for the standard
map:

```sh
python demos/python/standard_map_homoclinic_tangle.py --quick --plot figures/standard_map_homoclinic_tangle.png
```

The Makefile alias for this figure is:

```sh
make homoclinic-tangle-demo
```

Run the Henon-Heiles Poincare-section demo used for the numerical section
figure in the perturbation chapter:

```sh
python demos/python/henon_heiles_poincare.py --lecture --plot figures/henon_heiles_poincare.png
```

The Makefile alias for this figure is:

```sh
make henon-heiles-demo
```

Run the exact Navier-Stokes solution demo:

```sh
python demos/python/navier_stokes_solutions.py --plot figures/navier_stokes_solutions.png
```

Run the linear elasticity formula demo:

```sh
python demos/python/linear_elasticity.py --plot figures/linear_elasticity.png
```

For a short classroom run that visibly ejects particles, use a scaled Jupiter
mass as an accelerated perturbation experiment:

```sh
python demos/python/asteroid_ejection_probability.py --n 128 --years 50 --dt 0.02 --jupiter-mass-scale 25 --seed 4 --no-plot
```

Run a faster smoke version:

```sh
python demos/python/asteroid_ejection_probability.py --quick --no-plot
```

Run the analytic resonance-normal-form companion:

```sh
python demos/python/asteroid_resonance_normal_form.py --quick --plot figures/asteroid_resonance_normal_form.png
```

Run the Lidov-Kozai and heavy symmetric top reduced phase-space labs:

```sh
python demos/python/lidov_kozai.py --quick --plot figures/lidov_kozai.png
python demos/python/heavy_symmetric_top.py --quick --plot figures/heavy_symmetric_top.png
```

Run the planar binary-single capture/exchange scattering demo:

```sh
python demos/python/binary_capture_scattering.py --quick --json
```

Here `--v-inf` is the asymptotic incoming speed; reported capture classes are
finite-time binding-energy outcomes for the stated planar scattering ensemble.
The reported cross sections use the script's area-weighted convention and are
not a full spatial binary-single scattering survey.

Run the compact benchmark statistical studies, combining the planar asteroid
ensemble and planar binary-single scattering sweep:

```sh
python demos/python/three_body_benchmark_studies.py --quick --json-output data/three_body_benchmark_quick.json --plot figures/three_body_benchmark_quick.png --asteroid-plot figures/three_body_asteroid_loss_quick.png --binary-plot figures/three_body_binary_scattering_quick.png
```

Run all smoke tests:

```sh
python -m pytest
```

Run the Wolfram Language companion diagnostics without figure export:

```sh
make mathematica-smoke
```

To request a figure from an individual Wolfram script, pass `--plot` to
`WolframKernel -script`, for example:

```sh
/Applications/Wolfram.app/Contents/MacOS/WolframKernel -script demos/mathematica/LinearElasticity.wl --plot
```

Build the TeX notes from `notes/tex` with a local TeX installation:

```sh
cd notes/tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Or use the Makefile, which prefers `.venv/bin/python` when the local virtual
environment exists:

```sh
make test
make notes
```

## License

Code is licensed under MIT. Notes, syllabi, prose, and pedagogical figures are
licensed under CC BY-SA 4.0. See `LICENSE` for the split-license details.

## Design Commitments

- Notes and demos should be teachable in the classroom.
- Every major abstraction should have at least one numerical or visual example.
- Simulations should preserve geometric structure when the model calls for it.
- The repository should remain readable as source, not only as rendered output.
- Advanced topics should be connected to concrete systems throughout.
- Reproducible numerical labs should state their model, units, parameters,
  diagnostics, and output files.
