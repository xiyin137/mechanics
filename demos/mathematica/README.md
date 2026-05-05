# Wolfram Language Demonstrations

The `.wl` scripts are companion demonstrations for readers who want symbolic
manipulation, exact formula checks, or Wolfram plotting.

## Running All Scripts

From the repository root:

```sh
make mathematica-smoke
```

The `Makefile` defaults to:

```sh
/Applications/Wolfram.app/Contents/MacOS/WolframKernel
```

Override it when needed:

```sh
make mathematica-smoke WOLFRAM=/path/to/WolframKernel
```

## Scripts

| script | purpose |
| --- | --- |
| `RigidBodyEulerTop.wl` | Euler top invariants and reduced dynamics |
| `StandardMapTorusBreakdown.wl` | standard-map phase portraits and torus breakup |
| `CircularRestrictedThreeBody.wl` | CR3BP Lagrange points and Jacobi diagnostics |
| `AsteroidEjectionProbability.wl` | small restricted-asteroid ensemble |
| `AsteroidResonanceNormalForm.wl` | nominal Jovian resonances and pendulum width scaling |
| `LinearElasticity.wl` | elastic constants and formula checks |
| `GaugeDeformingBody.wl` | shape loops, connection, and holonomy |
| `NavierStokesSolutions.wl` | exact laminar-flow and vortex formulas |

Most scripts accept `--plot` to export a figure to `figures/`.  The smoke target
runs without figure export so that it remains fast and noninteractive.
