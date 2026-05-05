# Canonical Data

This directory contains versioned reference outputs for short or lecture-scale
demo runs.  Files here should be small, deterministic, and useful for checking
that a public command still produces the same kind of diagnostic record.

Before adding a canonical data file, record:

- the exact command;
- the random seed, if any;
- whether the file is intended as a smoke-test reference or a lecture reference;
- which chapter or lab uses it.

Large exploratory outputs belong in `data/`, which is ignored by default.

## Current Quick-Run Set

Regenerate the current JSON baselines from the repository root with the local
Python environment active:

```sh
env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/hamiltonian_pendulum.py --quick \
  --json-output data/canonical/hamiltonian_pendulum_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/rigid_body_euler_top.py --quick \
  --json-output data/canonical/rigid_body_euler_top_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/standard_map.py --quick \
  --json-output data/canonical/standard_map_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/standard_map_homoclinic_tangle.py --quick \
  --json-output data/canonical/standard_map_homoclinic_tangle_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/standard_map_torus_breakdown.py --quick \
  --json-output data/canonical/standard_map_torus_breakdown_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/circular_restricted_three_body.py --quick \
  --json-output data/canonical/circular_restricted_three_body_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/lidov_kozai.py --quick \
  --json-output data/canonical/lidov_kozai_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/asteroid_resonance_normal_form.py --quick \
  --json-output data/canonical/asteroid_resonance_normal_form_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/asteroid_ejection_probability.py --quick --no-plot \
  --json-output data/canonical/asteroid_ejection_probability_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/three_body_benchmark_studies.py --quick \
  --json-output data/canonical/three_body_benchmark_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/heavy_symmetric_top.py --quick \
  --json-output data/canonical/heavy_symmetric_top_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/linear_elasticity.py --quick \
  --json-output data/canonical/linear_elasticity_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/navier_stokes_solutions.py --quick \
  --json-output data/canonical/navier_stokes_solutions_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/deforming_body_gauge.py --quick \
  --json-output data/canonical/deforming_body_gauge_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/cosserat_rod_demo.py --quick \
  --json-output data/canonical/cosserat_rod_quick.json

env PYTHONPYCACHEPREFIX=.pycache-build \
  python demos/python/fluids_vorticity.py --quick \
  --json-output data/canonical/fluids_vorticity_quick.json
```
