# Lab: Gauge Holonomy Of A Deforming Body

## Purpose

This lab makes the Shapere-Wilczek gauge viewpoint computational.  A closed
loop in shape space can reconstruct a nonzero group motion when the connection
has curvature.

## Run

```sh
python demos/python/deforming_body_gauge.py \
  --delta-alpha 0.08 \
  --delta-beta 0.06 \
  --plot figures/deforming_body_gauge.png
```

For a smoke run:

```sh
python demos/python/deforming_body_gauge.py --delta-alpha 0.05 --delta-beta 0.04
```

## Questions

1. Which variables are shape coordinates, and which variable is reconstructed
   group motion?
2. What is the small-loop prediction from the curvature?
3. How does reversing the orientation of the shape loop change the phase?
4. Why is the result gauge-invariant even though the connection coefficients
   depend on a choice of frame?

## Expected Record

Save the loop parameters, printed phase or holonomy estimate, and a short
comparison between the numerical result and the curvature approximation.
