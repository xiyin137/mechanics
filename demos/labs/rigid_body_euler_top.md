# Lab: Rigid-Body Invariants And Reconstruction

## Purpose

This lab connects Euler's equations to the geometry of the reduced rigid body.
The computation checks energy and angular-momentum invariants and, when
attitude reconstruction is enabled in the code, monitors that the rotation
matrix remains in `SO(3)`.

## Run

```sh
python demos/python/rigid_body_euler_top.py --plot figures/rigid_body_euler_top.png
```

For a smoke run:

```sh
python demos/python/rigid_body_euler_top.py --steps 50
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
of the invariants, and a short explanation of the phase portrait.
