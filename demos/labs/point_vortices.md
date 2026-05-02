# Lab: Vorticity And Point Vortices

## Purpose

This lab connects the fluid chapter's vorticity equation to a finite-dimensional
Hamiltonian model.  Point vortices replace a continuous vorticity field by
singular circulation carriers.  The resulting equations conserve a Hamiltonian,
linear impulse, and angular impulse under the idealized assumptions of the
model.

## Run

```sh
python demos/python/fluids_vorticity.py \
  --ic four-vortex \
  --lecture \
  --plot figures/point_vortices.png \
  --json-output data/point_vortices.json
```

For fast checks:

```sh
python demos/python/fluids_vorticity.py --quick --ic dipole --json
python demos/python/fluids_vorticity.py --quick --ic like-signed-pair --json
```

## Questions

1. How does a vortex dipole translate, and how does a like-signed pair rotate?
2. Which reported conserved quantities are tied to translation and rotation
   symmetries?
3. Why is point-vortex motion Hamiltonian even though it is not Newtonian
   particle mechanics with ordinary mass?
4. What physical effects are lost when a smooth vortex patch is replaced by
   point vortices?

## Expected Record

Record the initial condition, circulations, time step, Hamiltonian drift,
impulse drift, angular-impulse drift, and one trajectory figure.
