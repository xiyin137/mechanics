# Lab: Standard Map Phase Portraits

## Purpose

This lab studies the area-preserving standard map before focusing on torus
breakdown.  The map is a discrete symplectic system on the two-torus.  Small
kick strength shows deformed invariant curves, intermediate kick strength
shows island chains around resonances, and larger kick strength shows broad
chaotic regions.

## Run

```sh
python demos/python/standard_map.py \
  --preset near-critical \
  --lecture \
  --plot figures/standard_map.png \
  --json-output data/standard_map.json
```

For a fast JSON check:

```sh
python demos/python/standard_map.py --quick --preset small --json
```

## Questions

1. Why does the map preserve area even though nearby points may separate?
2. How do fixed and periodic points organize the island chains?
3. What information is contained in a finite-time rotation-number estimate,
   and what information is not?
4. Compare the `small`, `near-critical`, and `large` presets.  Which visual
   changes correspond to resonances, and which correspond to global transport?

## Expected Record

Record `K`, the number of initial orbits, the number of map iterations, the
finite rotation-number mean and standard deviation, and one figure for at least
two kick strengths.
