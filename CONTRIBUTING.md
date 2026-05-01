# Contributing

This repository is a teaching codebase: every addition should be readable,
reproducible, and connected to the notes.

## Adding A Demo

Each new demo should state its model, variables, parameters, units, invariants,
and numerical method in the file docstring or header. Hamiltonian demos should
report energy drift and any conserved momentum drift. Probabilistic demos should
report the sampling distribution, random seed, time horizon, and event criteria.

Please add:

- a command-line interface with classroom-sized defaults;
- a focused regression test in `tests/test_demo_smoke.py`;
- a `Makefile` target if the demo generates a standard figure or data file;
- a cross-reference from the relevant note section.

Generated figures and data belong in `figures/` and `data/`; curated reference
figures that should be versioned can go in `figures/canonical/`.

## Keeping Companion Demos In Sync

When a Python demo has a Mathematica/Wolfram counterpart, keep the educational
contract aligned even if the implementations differ. The two files should state
the same physical model, assumptions, variables, parameter units, default
classroom scale, diagnostic invariants, and generated figure path whenever those
notions apply. If the Mathematica version is intentionally more compact, say so
in its header and list what it omits.

The Python regression tests are the executable baseline for this repository.
Mathematica companions should still report the comparable invariants or summary
probabilities at runtime and should export a standard figure when the Python
version does.

## Running Checks

Use the project virtual environment when available:

```sh
make test
make notes
```

`make test` runs the Python test suite. `make notes` rebuilds the TeX notes with
noninteractive failure behavior.

GitHub Actions runs the Python test suite on pushes and pull requests. The TeX
build is intentionally kept as a local check because it depends on a full TeX
installation; run `make notes` before opening a pull request that changes
`notes/tex/`.
