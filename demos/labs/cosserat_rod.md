# Lab: Cosserat Rod Reconstruction

## Purpose

This lab turns a curvature field into a framed curve.  The planar Cosserat rod
demo integrates the connection equation `theta'(s)=kappa(s)` and then
reconstructs the centerline by integrating the unit tangent.  It is the
one-dimensional continuum analogue of reconstructing group motion from local
frame data.

## Run

```sh
python demos/python/cosserat_rod_demo.py \
  --lecture \
  --plot figures/cosserat_rod.png \
  --json-output data/cosserat_rod.json
```

For a fast JSON check:

```sh
python demos/python/cosserat_rod_demo.py --quick --json
```

## Questions

1. What is the geometric meaning of the reported `frame_holonomy`?
2. Why should the reconstructed tangent have norm one?
3. How do the `base`, `amp`, and `mode` parameters change the endpoint and
   total frame rotation?
4. In what sense is `R^{-1}R'` the rod analogue of a gauge connection?

## Expected Record

Record the curvature parameters, number of sample points, frame holonomy,
endpoint, tangent-norm error, and one centerline figure.
