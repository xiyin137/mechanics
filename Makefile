PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
PYCACHE ?= .pycache-build
MPLCACHE ?= .matplotlib-cache

.PHONY: smoke test asteroid-demo asteroid-accelerated-demo rigid-body-demo standard-map-demo pendulum-demo fluids-demo rod-demo notes clean

smoke:
	env PYTHONPYCACHEPREFIX=$(PYCACHE) $(PYTHON) -m compileall -q demos/python
	env PYTHONPYCACHEPREFIX=$(PYCACHE) $(PYTHON) demos/python/asteroid_ejection_probability.py --n 24 --years 2 --dt 0.05 --bins 6 --no-plot

test:
	env PYTHONPYCACHEPREFIX=$(PYCACHE) $(PYTHON) -m pytest

figures data:
	mkdir -p $@

asteroid-demo: figures/ejection_demo.png

figures/ejection_demo.png: demos/python/asteroid_ejection_probability.py | figures data
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/asteroid_ejection_probability.py --n 256 --years 200 --dt 0.02 --seed 7 --plot figures/ejection_demo.png --csv data/ejection_demo.csv

asteroid-accelerated-demo: figures/ejection_accelerated_demo.png

figures/ejection_accelerated_demo.png: demos/python/asteroid_ejection_probability.py | figures data
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/asteroid_ejection_probability.py --n 128 --years 50 --dt 0.02 --bins 12 --jupiter-mass-scale 25 --seed 4 --plot figures/ejection_accelerated_demo.png --csv data/ejection_accelerated_demo.csv

rigid-body-demo: figures/rigid_body_euler_top.png

figures/rigid_body_euler_top.png: demos/python/rigid_body_euler_top.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/rigid_body_euler_top.py --plot figures/rigid_body_euler_top.png

standard-map-demo: figures/standard_map.png

figures/standard_map.png: demos/python/standard_map.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/standard_map.py --K 0.95 --plot figures/standard_map.png

pendulum-demo: figures/hamiltonian_pendulum.png

figures/hamiltonian_pendulum.png: demos/python/hamiltonian_pendulum.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/hamiltonian_pendulum.py --plot figures/hamiltonian_pendulum.png

fluids-demo: figures/point_vortices.png

figures/point_vortices.png: demos/python/fluids_vorticity.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/fluids_vorticity.py --plot figures/point_vortices.png

rod-demo: figures/cosserat_rod.png

figures/cosserat_rod.png: demos/python/cosserat_rod_demo.py | figures
	env PYTHONPYCACHEPREFIX=$(PYCACHE) MPLCONFIGDIR=$(MPLCACHE) $(PYTHON) demos/python/cosserat_rod_demo.py --plot figures/cosserat_rod.png

notes:
	cd notes/tex && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	rm -rf $(PYCACHE) $(MPLCACHE) figures/*.png data/*.csv
	cd notes/tex && latexmk -C main.tex
