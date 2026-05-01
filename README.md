# Mechanics Through Phase Space

This repository is a teaching project for advanced mechanics centered on
Lagrangian mechanics, Hamiltonian mechanics, phase space, integrability, chaos,
rigid bodies, celestial mechanics, fluids, and the gauge theory of deforming
bodies.

The organizing idea is that mechanics is geometry made computational: motion is
described by variational principles, conserved quantities come from symmetry,
phase space carries structure, and both finite-dimensional bodies and continua
can be studied through the same geometric language.

## Current Contents

- `PLANNING.md`: comprehensive course and repository plan.
- `notes/tex`: TeX source for the first course notes.
- `demos/python`: runnable Python simulations and numerical experiments.
- `demos/mathematica`: Wolfram Language scripts for symbolic and numerical demos.
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
   - resonances, chaotic transport, and numerical ejection probabilities

3. **Fluids and deforming bodies**
   - vorticity, circulation, and Hamiltonian point vortices
   - deformation maps, local frames, connections, and defect fields
   - Cosserat media as a bridge from rigid bodies to continua

## Quick Start

Create a Python 3.9 or newer environment and install the Python dependencies:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the highlighted asteroid ejection probability demo:

```sh
python demos/python/asteroid_ejection_probability.py --n 256 --years 200 --dt 0.02 --seed 7 --plot figures/ejection_demo.png
```

For a short classroom run that visibly ejects particles, use a scaled Jupiter
mass as an accelerated perturbation experiment:

```sh
python demos/python/asteroid_ejection_probability.py --n 128 --years 50 --dt 0.02 --jupiter-mass-scale 25 --seed 4 --no-plot
```

Run a faster smoke version:

```sh
python demos/python/asteroid_ejection_probability.py --n 24 --years 2 --dt 0.05 --no-plot
```

Run all smoke tests:

```sh
python -m pytest
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
