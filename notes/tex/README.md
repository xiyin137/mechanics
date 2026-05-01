# TeX Notes

Build the notes from this directory:

```sh
latexmk -pdf main.tex
```

The current files form an integrated draft:

- `00_notation_assumptions.tex`
- `01_lagrangian_mechanics.tex`
- `02_hamiltonian_phase_space.tex`
- `03_integrability_rigid_body.tex`
- `04_perturbation_kam_torus_breakdown.tex`
- `05_three_body_problem.tex`
- `06_elastic_bodies.tex`
- `07_deforming_body_gauge.tex`
- `08_fluid_mechanics.tex`

The notes intentionally track the demo scripts. Worked derivations, exercises,
and simulation pointers live at the ends of the chapters they support. Equations
that depend on numerical data should be checked against the corresponding
scripts in `demos/python`.
