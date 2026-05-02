# Lab: Standard Map And Breakdown Of Invariant Tori

## Purpose

The standard map is the smallest numerical laboratory for the transition from
invariant curves to chaotic transport.  It turns the KAM discussion into a
phase-space picture: low-order resonances form islands, surviving irrational
curves act as barriers, and larger perturbations open transport channels.

## Run

```sh
python demos/python/standard_map_torus_breakdown.py \
  --K 1.1 \
  --lecture \
  --plot figures/standard_map_torus_breakdown.png \
  --json-output data/standard_map_torus_breakdown.json
```

For a faster run:

```sh
python demos/python/standard_map_torus_breakdown.py --quick --preset large --json
```

## Questions

1. Where do island chains first become visible as `K` is increased?
2. Which plotted structures behave like barriers, and which behave like partial
   barriers?
3. How does the spread in lifted momentum diagnose transport across broken
   tori?
4. How does this discrete map illustrate the resonance-normal-form discussion
   in the notes?

## Expected Record

Report `K`, number of orbits, number of steps, the printed spread diagnostics,
the diagnostic note about finite-time interpretation, and one figure for at
least two values of `K`.
