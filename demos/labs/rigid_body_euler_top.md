# Lab: Rigid-Body Invariants And Reconstruction

## Purpose

This lab connects Euler's equations to the geometry of the reduced rigid body.
The computation checks energy and angular-momentum invariants and, when
attitude reconstruction is enabled in the code, monitors that the rotation
matrix remains in `SO(3)`.

## Run

```sh
python demos/python/rigid_body_euler_top.py \
  --lecture \
  --plot figures/rigid_body_euler_top.png \
  --json-output data/rigid_body_euler_top.json
```

For a smoke run:

```sh
python demos/python/rigid_body_euler_top.py --quick --json
```

## Questions

1. Which two scalar quantities define the intersection curves in the reduced
   angular-velocity picture?
2. How does the intermediate-axis instability appear in the numerical
   trajectory?
3. Why is attitude reconstruction a separate step after solving the reduced
   Euler equations?
4. Which reported errors test membership in `SO(3)`?

## Expected Record

Save the command, inertia parameters, initial angular velocity, maximum drift
of the invariants, attitude orthogonality and determinant errors, and a short
explanation of the phase portrait.
