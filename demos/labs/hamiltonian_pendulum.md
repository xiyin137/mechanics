# Lab: Hamiltonian Pendulum And The Separatrix

## Purpose

This lab is the first phase-space experiment.  The pendulum has one degree of
freedom, so the Hamiltonian itself draws the qualitative dynamics: closed
libration curves below the separatrix energy, open rotation curves above it,
and a singular separatrix through the unstable upright equilibrium.

## Run

```sh
python demos/python/hamiltonian_pendulum.py \
  --q0 1.0 \
  --p0 0.0 \
  --lecture \
  --plot figures/hamiltonian_pendulum.png \
  --json-output data/hamiltonian_pendulum.json
```

For a fast JSON check:

```sh
python demos/python/hamiltonian_pendulum.py --quick --json
```

## Questions

1. Which equilibrium points are elliptic and which are hyperbolic?
2. How does the value `separatrix_energy` divide libration from rotation?
3. Why is energy drift a diagnostic of the numerical method rather than a new
   mechanical effect?
4. What happens to the period as the initial energy approaches the separatrix
   from below?

## Expected Record

Record the initial condition, time step, total integration time, initial
energy, maximum energy drift, and the reported phase region.  Include one
phase portrait and mark where the separatrix energy lies in the Hamiltonian
level sets.
