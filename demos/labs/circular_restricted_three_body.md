# Lab: Circular Restricted Three-Body Problem

## Purpose

This lab studies the rotating-frame CR3BP, the Lagrange points, zero-velocity
curves, and the Jacobi integral.  It is the bridge between the abstract
Hamiltonian discussion and the asteroid-belt model.

## Run

```sh
python demos/python/circular_restricted_three_body.py \
  --preset sun-jupiter \
  --initial l4 \
  --periods 3 \
  --dt 0.0025 \
  --plot figures/cr3bp_zero_velocity.png \
  --json-output data/cr3bp_zero_velocity.json
```

For a fast reproducibility check:

```sh
python demos/python/circular_restricted_three_body.py --quick --json
```

## Questions

1. What is the physical meaning of the Jacobi constant in the rotating frame?
2. How do the zero-velocity curves change when the initial condition changes?
3. Why is Jacobi drift a numerical diagnostic rather than a new physical
   quantity?
4. How do the `sun-jupiter`, `earth-moon`, and `equal-mass` presets change the
   Lagrange point locations?

## Expected Record

Keep the JSON summary, the figure, and a sentence explaining whether the
reported Jacobi drift is acceptable for the plotted time interval.
