PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
WOLFRAM ?= /Applications/Wolfram.app/Contents/MacOS/WolframKernel
PYCACHE ?= .pycache-build
MPLCACHE ?= .matplotlib-cache

.PHONY: smoke test mathematica-smoke asteroid-demo asteroid-accelerated-demo asteroid-normal-form-demo binary-capture-demo three-body-benchmark-demo lidov-kozai-demo cr3bp-demo cr3bp-zerovel-demo rigid-body-demo heavy-top-demo standard-map-demo homoclinic-tangle-demo torus-breakdown-demo standard-map-breakdown-demo henon-heiles-demo pendulum-demo fluids-demo navier-stokes-demo elasticity-demo rod-demo notes clean

smoke:
	env PYTHONPYCACHEPREFIX=$(PYCACHE) $(PYTHON) -m compileall -q demos/python
	env PYTHONPYCACHEPREFIX=$(PYCACHE) $(PYTHON) demos/python/asteroid_ejection_probability.py --n 24 --years 2 --dt 0.05 --bins 6 --no-plot

test:
	env PYTHONPYCACHEPREFIX=$(PYCACHE) $(PYTHON) -m pytest

mathematica-smoke:
	$(WOLFRAM) -script demos/mathematica/AsteroidEjectionProbability.wl
	$(WOLFRAM) -script demos/mathematica/AsteroidResonanceNormalForm.wl
	$(WOLFRAM) -script demos/mathematica/CircularRestrictedThreeBody.wl
	$(WOLFRAM) -script demos/mathematica/GaugeDeformingBody.wl
	$(WOLFRAM) -script demos/mathematica/LinearElasticity.wl
	$(WOLFRAM) -script demos/mathematica/NavierStokesSolutions.wl
	$(WOLFRAM) -script demos/mathematica/RigidBodyEulerTop.wl
	$(WOLFRAM) -script demos/mathematica/StandardMapTorusBreakdown.wl

figures data:
	mkdir -p $@

asteroid-demo: figures/ejection_demo.png

figures/ejection_demo.png: demos/python/asteroid_ejection_probability.py | figures data
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/asteroid_ejection_probability.py --n 256 --years 200 --dt 0.02 --seed 7 --plot figures/ejection_demo.png --csv data/ejection_demo.csv

asteroid-accelerated-demo: figures/ejection_accelerated_demo.png

figures/ejection_accelerated_demo.png: demos/python/asteroid_ejection_probability.py | figures data
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/asteroid_ejection_probability.py --n 128 --years 50 --dt 0.02 --bins 12 --jupiter-mass-scale 25 --seed 4 --plot figures/ejection_accelerated_demo.png --csv data/ejection_accelerated_demo.csv

asteroid-normal-form-demo: figures/asteroid_resonance_normal_form.png

figures/asteroid_resonance_normal_form.png: demos/python/asteroid_resonance_normal_form.py | figures data
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/asteroid_resonance_normal_form.py --quick --plot figures/asteroid_resonance_normal_form.png --csv data/asteroid_resonance_normal_form_widths.csv

binary-capture-demo: figures/binary_capture_scattering.png

figures/binary_capture_scattering.png: demos/python/binary_capture_scattering.py | figures data
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/binary_capture_scattering.py --quick --plot figures/binary_capture_scattering.png --json-output data/binary_capture_scattering_quick.json

three-body-benchmark-demo: figures/three_body_asteroid_loss_quick.png figures/three_body_binary_scattering_quick.png

figures/three_body_asteroid_loss_quick.png figures/three_body_binary_scattering_quick.png figures/three_body_benchmark_quick.png: demos/python/three_body_benchmark_studies.py demos/python/asteroid_ejection_probability.py demos/python/binary_capture_scattering.py | figures data
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/three_body_benchmark_studies.py --quick --plot figures/three_body_benchmark_quick.png --asteroid-plot figures/three_body_asteroid_loss_quick.png --binary-plot figures/three_body_binary_scattering_quick.png --json-output data/three_body_benchmark_quick.json

lidov-kozai-demo: figures/lidov_kozai.png

figures/lidov_kozai.png: demos/python/lidov_kozai.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/lidov_kozai.py --quick --plot figures/lidov_kozai.png

cr3bp-demo: figures/cr3bp_zero_velocity.png

cr3bp-zerovel-demo: cr3bp-demo

figures/cr3bp_zero_velocity.png: demos/python/circular_restricted_three_body.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/circular_restricted_three_body.py --periods 3 --dt 0.0025 --plot figures/cr3bp_zero_velocity.png

rigid-body-demo: figures/rigid_body_euler_top.png

figures/rigid_body_euler_top.png: demos/python/rigid_body_euler_top.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/rigid_body_euler_top.py --plot figures/rigid_body_euler_top.png

heavy-top-demo: figures/heavy_symmetric_top.png

figures/heavy_symmetric_top.png: demos/python/heavy_symmetric_top.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/heavy_symmetric_top.py --quick --plot figures/heavy_symmetric_top.png

standard-map-demo: figures/standard_map.png

figures/standard_map.png: demos/python/standard_map.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/standard_map.py --K 0.95 --plot figures/standard_map.png

homoclinic-tangle-demo: figures/standard_map_homoclinic_tangle.png

figures/standard_map_homoclinic_tangle.png: demos/python/standard_map_homoclinic_tangle.py | figures data
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) MPLBACKEND=Agg $(PYTHON) demos/python/standard_map_homoclinic_tangle.py --quick --plot figures/standard_map_homoclinic_tangle.png --json-output data/standard_map_homoclinic_tangle_quick.json

torus-breakdown-demo: figures/standard_map_torus_breakdown.png

standard-map-breakdown-demo: torus-breakdown-demo

figures/standard_map_torus_breakdown.png: demos/python/standard_map_torus_breakdown.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) MPLBACKEND=Agg $(PYTHON) demos/python/standard_map_torus_breakdown.py --K 1.1 --steps 1500 --orbits 128 --plot figures/standard_map_torus_breakdown.png

henon-heiles-demo: figures/henon_heiles_poincare.png

figures/henon_heiles_poincare.png: demos/python/henon_heiles_poincare.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) MPLBACKEND=Agg $(PYTHON) demos/python/henon_heiles_poincare.py --lecture --plot figures/henon_heiles_poincare.png

pendulum-demo: figures/hamiltonian_pendulum.png

figures/hamiltonian_pendulum.png: demos/python/hamiltonian_pendulum.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/hamiltonian_pendulum.py --plot figures/hamiltonian_pendulum.png

fluids-demo: figures/point_vortices.png

figures/point_vortices.png: demos/python/fluids_vorticity.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/fluids_vorticity.py --plot figures/point_vortices.png

navier-stokes-demo: figures/navier_stokes_solutions.png

figures/navier_stokes_solutions.png: demos/python/navier_stokes_solutions.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) MPLBACKEND=Agg $(PYTHON) demos/python/navier_stokes_solutions.py --plot figures/navier_stokes_solutions.png

elasticity-demo: figures/linear_elasticity.png

figures/linear_elasticity.png: demos/python/linear_elasticity.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) MPLBACKEND=Agg $(PYTHON) demos/python/linear_elasticity.py --plot figures/linear_elasticity.png

rod-demo: figures/cosserat_rod.png

figures/cosserat_rod.png: demos/python/cosserat_rod_demo.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/cosserat_rod_demo.py --plot figures/cosserat_rod.png

notes:
	cd notes/tex && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	rm -rf $(PYCACHE) $(MPLCACHE) figures/*.png data/*.csv
	cd notes/tex && latexmk -C main.tex
