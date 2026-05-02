# Lab: Elasticity Formulas And Exact Navier-Stokes Flows

## Purpose

This lab pairs two continuum checks.  The elasticity script evaluates material
constants and classical boundary formulas.  The Navier-Stokes script evaluates
exact laminar and unsteady solutions and checks residuals.

## Run

```sh
python demos/python/linear_elasticity.py --plot figures/linear_elasticity.png
python demos/python/navier_stokes_solutions.py --plot figures/navier_stokes_solutions.png
```

For smoke runs:

```sh
python demos/python/linear_elasticity.py --points 12
python demos/python/navier_stokes_solutions.py --points 12
```

## Questions

1. Which elastic moduli are independent for an isotropic linear solid?
2. What happens to the Lamé parameter as the Poisson ratio approaches the
   incompressible limit?
3. Which assumptions reduce Navier-Stokes to the Couette-Poiseuille ordinary
   differential equation?
4. Why does the Taylor-Green vortex give an exact residual check?

## Expected Record

Record the input parameters, boundary values or residuals checked by the
scripts, and one comparison between an elastic boundary-value formula and a
fluid exact solution.
