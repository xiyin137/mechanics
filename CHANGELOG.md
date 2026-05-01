# Changelog

## Unreleased

- Split the former combined chapters into separate Lagrangian, Hamiltonian
  phase-space, perturbation/KAM, three-body, elastic-body, and deforming-body
  chapters; updated the source tree, notation ledger, and public documentation
  to match the new architecture.
- Developed the new three-body chapter with Jacobi coordinates,
  center-of-mass reduction, the Lagrange-Jacobi identity, the CR3BP rotating
  Hamiltonian, and three-body-specific reader questions and demos.
- Developed the new deforming-body chapter with the principal-bundle
  formulation of shape space, explicit gauge transformations, regularity
  assumptions, and a clearer kinetic-energy derivation of the mechanical
  connection.
- Reorganized the notes after removing the standalone Hamilton-Jacobi and
  adiabatic-invariance material; cleaned the remaining stale adiabatic notation.
- Expanded celestial mechanics with the Newtonian three-body problem, central
  configurations, the circular restricted three-body problem, Lagrange points,
  the Jacobi integral, zero-velocity curves, and resonance-labelled asteroid
  statistics.
- Expanded deforming-body mechanics with Shapere-Wilczek gauge kinematics,
  a two-rotor nonabelian holonomy model, and cross-references to the helicopter
  rotor laboratory.
- Expanded fluid mechanics with detailed Navier-Stokes derivations, exact
  laminar solutions, stability discussion, and the `navier_stokes_solutions.py`
  demo.
- Expanded elastic-body mechanics with moduli, positivity, static
  Navier-Cauchy boundary-value problems, bars, circular-shaft torsion,
  Euler-Bernoulli beams, elastic waves, and the `linear_elasticity.py` demo.
- Added and synchronized companion computational demos for CR3BP,
  deforming-body gauge holonomy, standard-map torus breakdown, Navier-Stokes
  exact solutions, and linear elasticity.
- Strengthened the exposition pass with chapter-opening motivation, clearer
  derivation checkpoints, a CR3BP zero-velocity schematic, and a polar
  decomposition figure for elasticity.
- Polished the notes' TikZ figures end-to-end, reducing label overlaps,
  clarifying panel structure, and improving visual callouts in the course map,
  Legendre transform, rigid-body, KAM, fluid, elasticity, and laboratory
  figures.
- Addressed review cleanup: added Mathematica companions for the new standard
  map, Navier-Stokes, and linear-elasticity demos; added CR3BP and standard-map
  Makefile aliases; documented the CR3BP RK4/Jacobi-drift limitation; and
  refreshed the public reading path with core versus extended routes.
- Improved note exposition end-to-end with additional reader checkpoints,
  modelling-stage warnings, conceptual bridges around Legendre transforms,
  Liouville tori, KAM, three-body reduction, continuum balance laws,
  objectivity, gauge holonomy, and worked-problem laboratories.
- Audited all Wolfram Language demos, fixed Mathematica-specific issues in
  anomaly conversion, CR3BP figure output, rigid-body integration, and gauge
  plotting, and added a `mathematica-smoke` target using `WolframKernel`.
- Addressed review findings: corrected the Liouville-torus Poisson-bracket
  sign display, replaced the symmetric-top action shortcut by the chamber-wise
  formula, and upgraded pendulum, Stokes-layer, Taylor-Green, and Legendre
  transform figures.
- Re-audited all 34 TeX figures from rendered PDF pages; corrected the
  Stokes-layer axis scaling and the rotating-hoop potential's \(\theta\)-axis
  geometry.
- Addressed the latest review pass by replacing the remaining
  schematic standard-map island-chain figure with actual \(K=0.65\) iterates
  read from TeX data tables, then completed a publication-readiness pass over
  public documentation, ignore rules, derivation gaps, and figure polish.

## v0.1.0 - 2026-05-01

- Expanded the TeX notes into a self-contained mechanics sequence with notation
  tables, derivations, worked laboratories, and improved TikZ figures.
- Added Python and Mathematica demos for rigid-body dynamics, pendulum phase
  flow, the standard map, point vortices, Cosserat rods, gauge deformation, and
  restricted Sun-Jupiter asteroid ejection.
- Added numerical regression tests for invariant drift, area preservation,
  Kepler initial conditions, point-vortex motion, Cosserat reconstruction, and
  asteroid probability bookkeeping.
- Added project housekeeping: split teaching/code licensing, contributor
  guidance, clean build targets, and dependency notes.
