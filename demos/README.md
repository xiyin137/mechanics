# Demos And Reproducible Laboratories

The demo directory is the computational companion to the notes.  Each script is
intended to be small enough for classroom inspection while still reporting the
diagnostics needed for a meaningful numerical experiment.

## Directory Layout

- `python/`: Python command-line simulations and formula checks.
- `mathematica/`: Wolfram Language companion scripts.
- `labs/`: public lab guides that connect selected scripts to chapters of the
  notes.

Generated figures and data should be written to `figures/` and `data/`; those
outputs are ignored by default unless they are explicitly curated.

## Output Contract

For a script to count as a reproducible lab instrument, it should state:

- the model and units;
- the parameters that define the run;
- the numerical method or analytic formula being evaluated;
- the invariant, residual, or error estimate being monitored;
- the random seed when random sampling is used;
- the output files it wrote.

Every major Python demo supports the same diagnostic convention:

```sh
python demos/python/<demo>.py --quick --json
python demos/python/<demo>.py --lecture --output-dir data/<demo>_lecture
```

Use `--json` when a pure JSON summary on standard output is more useful than
the human-readable report.  Use `--json-output` when the run should leave a lab
record without changing the text report.  For most demos, `--output-dir`
creates a standard JSON file and, when plotting is inexpensive, a standard
figure path.

## Highlighted Labs

| lab | main script | chapter |
| --- | --- | --- |
| rigid-body invariants and reconstruction | `python/rigid_body_euler_top.py` | Integrability and the Rigid Body |
| heavy symmetric top nutation | `python/heavy_symmetric_top.py` | Integrability and the Rigid Body |
| standard-map torus breakdown | `python/standard_map_torus_breakdown.py` | Perturbation, KAM, and Breakdown |
| Henon-Heiles Poincare sections | `python/henon_heiles_poincare.py` | Perturbation, KAM, and Breakdown |
| asteroid resonance normal form | `python/asteroid_resonance_normal_form.py` | Perturbation, KAM, and Breakdown |
| CR3BP and zero-velocity curves | `python/circular_restricted_three_body.py` | The Three-Body Problem |
| Lidov-Kozai secular cycles | `python/lidov_kozai.py` | The Three-Body Problem |
| asteroid ejection probability | `python/asteroid_ejection_probability.py` | The Three-Body Problem |
| binary capture and exchange scattering | `python/binary_capture_scattering.py` | The Three-Body Problem |
| benchmark three-body statistics | `python/three_body_benchmark_studies.py` | The Three-Body Problem |
| elastic constants and boundary formulas | `python/linear_elasticity.py` | Elastic Bodies |
| gauge holonomy of a deforming body | `python/deforming_body_gauge.py` | Gauge Theory of Deforming Bodies |
| exact Navier-Stokes flows | `python/navier_stokes_solutions.py` | Fluid Mechanics |

## Smoke Testing

From the repository root:

```sh
make test
make mathematica-smoke
```

The Python tests compile every Python demo and run short numerical cases.  The
Wolfram target runs each `.wl` script in non-plotting mode.
