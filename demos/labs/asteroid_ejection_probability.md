# Lab: Asteroid Ejection Probability

## Purpose

This lab treats the restricted Sun-Jupiter-asteroid model as a statistical
experiment.  The goal is not a precision ephemeris; it is to understand how
resonances, chaotic transport, finite time horizons, and sampling error enter
an ejection estimate.

## Run

```sh
python demos/python/asteroid_ejection_probability.py \
  --lecture \
  --seed 7 \
  --output-dir data/asteroid_lecture \
  --plot figures/ejection_demo.png
```

For a fast smoke run:

```sh
python demos/python/asteroid_ejection_probability.py --quick --no-plot --json
```

For an accelerated classroom perturbation:

```sh
python demos/python/asteroid_ejection_probability.py \
  --n 128 \
  --years 50 \
  --dt 0.02 \
  --jupiter-mass-scale 25 \
  --seed 4 \
  --no-plot
```

## Questions

1. Which semimajor-axis bins are nearest the `3:1`, `5:2`, and `2:1`
   resonances?
2. Where are the binomial standard errors large enough that a visible
   difference may be sampling noise?
3. How do the conclusions change when the horizon is doubled but the seed is
   held fixed?
4. What changes when the indirect heliocentric term is omitted?
5. Why is the scaled-Jupiter run an accelerated perturbation experiment rather
   than a faithful Solar System prediction?

## Expected Record

Keep the command, JSON summary, CSV bin table, and any figure.  The writeup
should distinguish sampling error, time-step error, and model idealization.
