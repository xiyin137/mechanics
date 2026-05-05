# Canonical Figure Manifest

These figures are deterministic quick-run visual baselines.  They are not the
largest or most polished lecture figures; they are small reference artifacts
used to check that plotting commands still work and that each demo has a stable
visual output.

Regenerate from the repository root with the local Python environment active:

```sh
env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/hamiltonian_pendulum.py --quick \
  --plot figures/canonical/hamiltonian_pendulum_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/rigid_body_euler_top.py --quick \
  --plot figures/canonical/rigid_body_euler_top_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/heavy_symmetric_top.py --quick \
  --plot figures/canonical/heavy_symmetric_top_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/standard_map.py --quick \
  --plot figures/canonical/standard_map_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/standard_map_homoclinic_tangle.py --quick \
  --plot figures/canonical/standard_map_homoclinic_tangle_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache MPLBACKEND=Agg \
  python demos/python/standard_map_torus_breakdown.py --quick \
  --plot figures/canonical/standard_map_torus_breakdown_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/circular_restricted_three_body.py --quick \
  --plot figures/canonical/cr3bp_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/lidov_kozai.py --quick \
  --plot figures/canonical/lidov_kozai_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/asteroid_ejection_probability.py --quick \
  --plot figures/canonical/asteroid_ejection_probability_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/asteroid_resonance_normal_form.py --quick \
  --plot figures/canonical/asteroid_resonance_normal_form_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/three_body_benchmark_studies.py --quick \
  --plot figures/canonical/three_body_benchmark_quick.png \
  --asteroid-plot figures/canonical/three_body_asteroid_loss_quick.png \
  --binary-plot figures/canonical/three_body_binary_scattering_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/linear_elasticity.py --quick \
  --plot figures/canonical/linear_elasticity_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache MPLBACKEND=Agg \
  python demos/python/navier_stokes_solutions.py --quick \
  --plot figures/canonical/navier_stokes_solutions_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/deforming_body_gauge.py --quick \
  --plot figures/canonical/deforming_body_gauge_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/cosserat_rod_demo.py --quick \
  --plot figures/canonical/cosserat_rod_quick.png

env PYTHONPYCACHEPREFIX=.pycache-build MPLCONFIGDIR=.matplotlib-cache \
  python demos/python/fluids_vorticity.py --quick \
  --plot figures/canonical/fluids_vorticity_quick.png
```
