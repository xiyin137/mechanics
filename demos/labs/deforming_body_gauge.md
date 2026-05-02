# Lab: Gauge Holonomy Of A Deforming Body

## Purpose

This lab makes the Shapere-Wilczek gauge viewpoint computational.  A closed
loop in shape space can reconstruct a nonzero group motion when the connection
has curvature.  The demo compares the exact finite product of rotations with
the small-loop curvature prediction obtained from the Baker-Campbell-Hausdorff
expansion.

## Run

```sh
python demos/python/deforming_body_gauge.py \
  --delta-alpha 0.08 \
  --delta-beta 0.06 \
  --plot figures/deforming_body_gauge.png \
  --json-output data/deforming_body_gauge.json
```

For a smoke run:

```sh
python demos/python/deforming_body_gauge.py --quick --json
```

## Questions

1. Which variables are shape coordinates, and which variable is reconstructed
   group motion?
2. What is the small-loop prediction from the curvature?
3. How does reversing the orientation of the shape loop change the phase?
4. Why is the result gauge-invariant even though the connection coefficients
   depend on a choice of frame?
5. How does the `holonomy_scaling` table show the limit in which the
   curvature prediction becomes accurate?

## Expected Record

Save the loop parameters, connection components, curvature vector, net rotation
vector, BCH error, orthogonality and determinant errors, and the scaling plot.
The written interpretation should say which part is a convention-dependent
connection coefficient and which part is the observable holonomy of the loop.
