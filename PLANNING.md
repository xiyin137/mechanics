# Comprehensive Plan: Notes on Classical Mechanics

## 1. Project Thesis

This repository supports *Notes on Classical Mechanics*, a unified geometric
and computational treatment of mechanics. The notes start from configuration
space and the action principle, pass through Hamiltonian phase space and
symplectic structure, build integrability from concrete examples, study the
breakdown of invariant tori under perturbation, and then carry the same
structural language into elastic bodies, gauge-theoretic descriptions of
deforming bodies, and finally fluids.

The central message is:

> A mechanical system is not just a set of equations. It is a space of possible
> configurations, a variational principle, a phase-space geometry, and a set of
> symmetries and obstructions that organize its motion.

The course should be useful for advanced undergraduates, beginning graduate
students, and self-directed readers who know vector calculus, ordinary
differential equations, and basic linear algebra. Differential geometry is
introduced as needed.

Current snapshot, May 1, 2026:

- The TeX notes compile to a roughly 150-page PDF with the title-page
  architectural abstract requested for the public-facing version.
- The formerly separate Hamilton-Jacobi/adiabatic material has been removed or
  absorbed where it is actually used, so canonical perturbation theory now lives
  with the integrability-and-breakdown arc.
- The notes contain 34 figures; the standard-map island-chain figure is now
  data-backed by actual iterates rather than drawn schematically.
- Worked derivations, exercises, and demo pointers now live at the ends of the
  chapters they support, rather than in standalone concluding chapters.
- The Python laboratory contains 11 scripts; the seven substantial demos have
  Wolfram Language counterparts and a `mathematica-smoke` Makefile target.
- The smoke-test suite currently covers the demos, including the helicopter
  rotor wrappers and the newer CR3BP, torus-breakdown, fluid, and elasticity
  examples.

## 2. Audience And Prerequisites

Expected background:

- Newtonian mechanics at the level of a serious intermediate mechanics course.
- Multivariable calculus and vector calculus.
- Linear algebra, eigenvalues, orthogonal transformations, and quadratic forms.
- Ordinary differential equations and numerical integration.
- Some exposure to Python or Mathematica.

Helpful but not required:

- Manifolds and differential forms.
- Lie groups and Lie algebras.
- Partial differential equations.
- Basic celestial mechanics.
- Continuum mechanics or fluid mechanics.

The course should be written so that a mathematically strong physics student can
learn the geometry while also building numerical intuition.

Primary local source material:

- `/Users/xiyin/Dropbox/2022 216/KAM lecture.pdf`, handwritten Physics 216
  notes. These notes set the central order and emphasis for the mechanics
  sequence: Lagrangian mechanics, Hamiltonian phase space, rigid body on
  `SO(3)`, symplectic and Poisson structure, Liouville tori, action-angle
  variables, perturbation theory, small divisors, KAM, and Poincare-map chaos.
- `/Users/xiyin/Dropbox/Physics 151`, Fall 2014 teaching material. See
  `references/physics_151_extraction.md` for the extracted course spine,
  problem-set inventory, demo inventory, and future integration targets. This
  source is especially useful for classroom examples, Shapere-Wilczek gauge
  kinematics, standard-map resonance calculations, Henon-Heiles, double
  pendulum, and asteroid-belt demos.

## 3. Learning Outcomes

By the end, a student should be able to:

- Derive equations of motion from a variational principle.
- Perform the Legendre transform from Lagrangian to Hamiltonian form.
- Interpret phase space, symplectic forms, Poisson brackets, and canonical maps.
- Use symmetry to derive conserved quantities.
- Distinguish integrable, near-integrable, and chaotic behavior.
- Construct action-angle variables in model problems.
- Analyze the Euler top as an integrable rigid body system.
- Use Poincare sections, Lyapunov indicators, and long-time integration to
  diagnose chaos.
- Explain how resonances in a perturbed Kepler problem lead to asteroid-belt
  structure and ejection.
- Connect continuum mechanics to variational principles and material symmetry.
- Describe fluids in Eulerian and Lagrangian variables.
- Explain the gauge-theoretic view of deforming bodies, including local frames,
  connections, curvature, torsion, and defects.
- Write and interpret numerical simulations without mistaking numerical artifacts
  for physics.

## 4. Repository Architecture

The repository is organized as a course plus a computational laboratory.

```text
mechanics/
  README.md
  PLANNING.md
  requirements.txt
  pyproject.toml
  syllabus/
    course-map.md
  notes/
    tex/
      main.tex
      preamble.tex
      data/
        standard_map_kam_K065.dat
        standard_map_period3_islands_K065.dat
        standard_map_period3_layer_K065.dat
        standard_map_period3_points_K065.dat
      00_notation_assumptions.tex
      01_lagrangian_mechanics.tex
      02_hamiltonian_phase_space.tex
      03_integrability_rigid_body.tex
      04_perturbation_kam_torus_breakdown.tex
      05_three_body_problem.tex
      06_elastic_bodies.tex
      07_deforming_body_gauge.tex
      08_fluid_mechanics.tex
  demos/
    python/
      asteroid_ejection_probability.py
      circular_restricted_three_body.py
      rigid_body_euler_top.py
      standard_map.py
      standard_map_torus_breakdown.py
      hamiltonian_pendulum.py
      fluids_vorticity.py
      navier_stokes_solutions.py
      linear_elasticity.py
      cosserat_rod_demo.py
      deforming_body_gauge.py
    mathematica/
      RigidBodyEulerTop.wl
      CircularRestrictedThreeBody.wl
      AsteroidEjectionProbability.wl
      GaugeDeformingBody.wl
      LinearElasticity.wl
      NavierStokesSolutions.wl
      StandardMapTorusBreakdown.wl
  tests/
    test_demo_smoke.py
  figures/
  data/
  references/
```

The notes are written in TeX so they can become a polished set of lecture notes.
The demos are plain scripts so they are easy to run, inspect, and convert into
notebooks later.

## 5. Course Arcs

### Arc A: Variational Mechanics

The first arc establishes the grammar of mechanics:

- configuration spaces
- tangent bundles and generalized velocities
- action functionals
- Euler-Lagrange equations
- constraints and multipliers
- symmetry and Noether's theorem
- Legendre transform

The guiding principle is that equations of motion should be derived from
structure before being solved.

### Arc B: Hamiltonian Mechanics And Phase Space

The second arc moves to phase space:

- cotangent bundles
- canonical one-form and symplectic two-form
- Hamilton's equations
- Poisson brackets
- canonical transformations
- canonical transformations and generating functions
- geometric meaning of Liouville's theorem

This arc establishes the language needed for integrability and chaos.

### Arc C: Integrability And Rigid Bodies

The third arc asks when mechanics is solvable:

- constants of motion
- involution
- Liouville integrability
- invariant tori
- action-angle variables
- action integrals and angle variables
- Euler top
- heavy top as a bridge to nonintegrability

The 3D rigid body is the recurring example. It is concrete enough for numerical
simulation and geometric enough to motivate Lie-Poisson reduction.

### Arc D: Perturbation, Resonance, And Chaos

The fourth arc studies what happens when integrability is broken:

- near-integrable Hamiltonians
- resonances
- secular perturbation theory
- standard map
- Poincare-Birkhoff island chains
- Chirikov resonance overlap
- cantori and partial transport barriers
- separatrix splitting
- Poincare sections
- KAM intuition
- chaotic transport

The compact model is the standard map, supported by the Sun-Jupiter-asteroid
problem as physical motivation. The Kepler problem is the integrable baseline,
and Jupiter is the perturbation, but the detailed celestial reduction now lives
in its own three-body chapter.

The standard-map figures and demos are the compact model for this arc. They
serve three roles: deriving island chains from resonant tori, visualizing
finite-time transport on the cylinder, and giving a low-cost numerical check on
KAM, cantori, and resonance-overlap language before the reader meets the
three-body problem.

### Arc E: Three-Body Dynamics

The fifth arc develops celestial mechanics as its own subject rather than as a
subsection of perturbation theory:

- full Newtonian three-body equations
- center-of-mass reduction and Jacobi coordinates
- Lagrange-Jacobi identity
- central configurations and special rotating solutions
- circular restricted three-body problem
- rotating-frame Hamiltonian, Jacobi constant, and zero-velocity curves
- Lagrange points and their stability criteria
- heliocentric Sun-Jupiter-asteroid equations and indirect term
- finite-time ejection probability and numerical diagnostics

This arc is the bridge from abstract torus breakdown to a concrete
gravitational system with escape channels, resonances, and observable loss
statistics.

### Arc F: Continua, Elasticity, Gauge Theory, And Fluids

The sixth arc expands mechanics from finitely many degrees of freedom to fields:

- deformation maps
- strain and compatibility
- elastic stress, wave speeds, and boundary-value reductions
- local frames and gauge freedom
- Shapere-Wilczek mechanical connection and holonomy
- Cosserat media
- dislocations, disclinations, torsion, and curvature
- material and spatial descriptions
- Eulerian and Lagrangian variables
- vorticity and circulation
- ideal fluid Hamiltonian structure

This arc shows that rigid body mechanics generalizes in two directions: one
orientation in time becomes an orientation field over a body, and point-particle
phase space becomes an infinite-dimensional space of fields.

## 6. Recurring Case Studies

### 6.1 The Euler Top

The Euler top introduces:

- configuration space SO(3)
- angular velocity in body coordinates
- inertia tensor
- reduced equations on angular momentum space
- energy ellipsoids and angular momentum spheres
- integrability
- stability of principal-axis rotation

Deliverables:

- TeX derivation.
- Python simulation of Euler equations.
- Mathematica symbolic/numerical companion.
- Future interactive visualization of the angular momentum sphere.

### 6.2 Sun-Jupiter-Asteroid Belt

The celestial mechanics case study introduces:

- Kepler motion as an integrable Hamiltonian system.
- Delaunay/action-angle variables as a future extension.
- the circular restricted three-body problem, including the Jacobi integral,
  zero-velocity curves, and Lagrange points.
- Jupiter as a perturbing body.
- mean-motion resonances.
- chaotic layers and transport.
- numerical ejection probability.

Initial numerical model:

- dimensionless circular restricted three-body demo in rotating barycentric
  coordinates, with Lagrange point computation and Jacobi-drift diagnostics.
- planar Sun-centered restricted problem.
- Sun fixed at origin with Jupiter on a circular prescribed orbit.
- massless test particles sampled across an asteroid-belt annulus.
- symplectic-style kick-drift-kick integration for particles.
- ejection declared when a particle reaches a large heliocentric radius or has
  positive heliocentric energy outside the inner system.
- resonance labels attached to semimajor-axis bins for comparison with the
  nominal \(3:1,5:2,7:3,2:1\) resonances.

This model is intentionally teachable. Later versions can upgrade to:

- barycentric coordinates with a live Sun-Jupiter two-body system.
- elliptical Jupiter orbit.
- Saturn and secular forcing.
- adaptive close-encounter handling.
- MEGNO or finite-time Lyapunov indicators.
- resonance-specific ensembles.

### 6.3 Elastic And Deforming Bodies

The elastic and deforming-body thread introduces:

- body manifold and ambient space.
- deformation map.
- finite strain, polar decomposition, and frame indifference.
- stress and stored elastic energy.
- linear isotropic elasticity, elastic moduli, and wave speeds.
- classical elastic reductions: axial bars, circular-shaft torsion, and
  Euler-Bernoulli beams.
- material frames and spatial frames.
- local rotations as gauge freedom.
- connection coefficients as local comparison rules.
- curvature and torsion as incompatibility measures.
- Cosserat rods and media.
- dislocations and disclinations.

The linear-elasticity demo evaluates exact formulas for elastic constants,
bars, shafts, beams, and bar vibration modes. The Cosserat rod demo reconstructs
a planar rod from a curvature field; it is deliberately modest, but it gives a
computational foothold for the idea that a local frame field carries a
connection.
The finite-dimensional deforming-body gauge demo complements it by computing
the nonabelian holonomy of a closed two-rotor shape loop, with explicit helper
functions for the helicopter-rotor laboratory interpretation.

### 6.4 Fluids

The fluids thread introduces:

- flow maps.
- Eulerian velocity fields.
- Cauchy momentum balance and Newtonian stress.
- incompressible Navier-Stokes as a constrained balance law.
- exact laminar and unsteady Navier-Stokes solutions.
- vorticity.
- Kelvin circulation theorem.
- point vortex Hamiltonian systems.
- instability and mixing.
- infinite-dimensional Poisson brackets as an advanced endpoint.

The exact-solution Python demo evaluates Couette-Poiseuille flow,
Hagen-Poiseuille pipe flow, Stokes' first problem, the oscillatory Stokes
layer, and the Taylor-Green vortex. The point-vortex demo complements this by
showing a finite-dimensional Hamiltonian reduction of ideal-fluid motion.

## 7. Pedagogical Pattern For Each Module

Each module should eventually contain:

1. Motivation and geometric picture.
2. Definitions and assumptions.
3. Derivation from a variational or Hamiltonian principle.
4. One worked analytic example.
5. One computational experiment.
6. Conceptual questions.
7. Problems.
8. Extension notes and references.

The course should avoid introducing abstraction without paying it off in a
physical example.

## 8. Simulation Standards

Numerical material should follow these rules:

- State the model and units at the top of the file.
- Make default parameters fast enough for classroom use.
- Provide command-line controls for longer experiments.
- Use fixed seeds when randomness is pedagogically important.
- Print quantitative summaries, not only plots.
- Save figures when requested.
- Mark limitations explicitly in comments or docstrings.
- Use structure-preserving methods when feasible.
- Include smoke tests for syntax and minimal execution.

For long-time Hamiltonian systems, the notes should explicitly discuss why naive
integrators can create or destroy apparent chaos.

## 9. Three-Body Ejection Probability Highlight

The first highlight simulation estimates the probability that massless
asteroids are ejected from an asteroid-belt-like annulus under solar gravity and
Jupiter's perturbation.

The companion circular restricted three-body demo supplies the autonomous
rotating-frame geometry: \(L_1,\ldots,L_5\), the Jacobi constant, and
zero-velocity curves. The ejection experiment then translates this geometry
into a heliocentric ensemble calculation with resonance-labelled bins.

The initial experiment reports:

- number of particles.
- integration time.
- time step.
- global ejection fraction.
- collision/loss fraction.
- survival fraction.
- ejection fraction binned by initial semimajor axis.
- nearest nominal resonance and distance from that resonance for each bin.

Teaching questions:

- Which semimajor axes are most vulnerable?
- How does the result change with integration time?
- How does changing Jupiter's mass change the ejection fraction?
- How does the time step affect the answer?
- Which losses look physical, and which might be numerical artifacts?

Future version:

- refine the current 3:1, 5:2, 7:3, and 2:1 resonance labels into finite-width
  resonant neighborhoods.
- compare ejection probability inside and outside resonant windows.
- compute resonance angles.
- estimate finite-time Lyapunov exponents.
- generate publication-quality figures for lecture.

## 10. Notes Status And Core/Extended Pass

The TeX notes are now an integrated mechanics draft rather than a skeleton.
They are organized so that an instructor can teach a core route without asking
students to read every advanced subsection on the first pass.

Current source files:

- `00_notation_assumptions.tex`: global notation, assumptions, and symbol
  conventions.
- `01_lagrangian_mechanics.tex`: Lagrangian mechanics, variational
  principles, constraints, Noether theorem, Kepler motion, and the rigid body
  as a configuration-space example.
- `02_hamiltonian_phase_space.tex`: Legendre transform, Hamiltonian mechanics,
  symplectic form, Poisson brackets, phase-space action, canonical
  transformations, and structure-preserving numerics.
- `03_integrability_rigid_body.tex`: Liouville integrability, invariant tori,
  action-angle variables, Kepler problem, Euler top, Lie-Poisson reduction, and
  rigid-body stability.
- `04_perturbation_kam_torus_breakdown.tex`: near-integrable systems, resonances,
  KAM proof sketch, invariant-torus breakdown, standard map, cantori, and
  transport barriers.
- `05_three_body_problem.tex`: Newtonian three-body dynamics, Jacobi
  coordinates, central configurations, CR3BP, rotating-frame Hamiltonian,
  Lagrange points, heliocentric asteroid equations, and ejection statistics.
- `06_elastic_bodies.tex`: finite strain, frame indifference, linear
  elasticity, elastic waves, and classical boundary-value formulas.
- `07_deforming_body_gauge.tex`: Shapere-Wilczek gauge theory of deforming
  bodies, shape space, mechanical connection, holonomy, Cosserat media, and
  defect geometry.
- `08_fluid_mechanics.tex`: material and spatial descriptions, balance laws,
  Navier-Stokes derivation, exact laminar and unsteady solutions, stability,
  vorticity, circulation, and point vortices.

Worked derivations, exercises, and demo pointers are placed at the ends of the
chapters they support, rather than in standalone back-matter chapters.

Core classroom pass:

1. Reading rules and standing assumptions.
2. Lagrangian mechanics through constraints, Noether theorem, Kepler motion,
   and the rigid body as a Lagrangian system.
3. Hamiltonian mechanics through Hamilton's equations, Poisson brackets,
   canonical transformations, and symplectic numerics.
4. Integrability through Liouville tori, action-angle variables, and the Euler
   top.
5. Perturbation and chaos through resonant normal forms, KAM survival,
   invariant-torus breakdown, and standard-map diagnostics.
6. Three-body dynamics through Jacobi coordinates, central configurations,
   CR3BP/Jacobi geometry, and asteroid ejection statistics.
7. Elastic bodies through finite strain, linear elasticity, elastic waves, and
   classical bars/shafts/beams.
8. Deforming bodies through Shapere-Wilczek gauge kinematics, holonomy,
   Cosserat rods, and defects.
9. Fluids through the Navier-Stokes derivation and canonical exact laminar
   solutions.
10. Selected worked laboratories.

Extended/project pass:

- detailed KAM iteration and small-divisor estimates.
- Chirikov overlap, cantori, turnstiles, and finite-time transport diagnostics.
- full three-body and asteroid-belt ejection statistics.
- Orr-Sommerfeld stability, Rayleigh inflection criterion, and point-vortex
  Hamiltonian mechanics.
- expanded beam/torsion formula catalog and elastic-mode problems.
- Shapere-Wilczek gauge curvature, two-rotor/helicopter holonomy, Cosserat
  media, and defect geometry.
- the longer derivations in Chapter 8.

Next additions:

- problem sets with solutions keyed to the core route.
- rendered demo figures committed for lecture use.
- an instructor guide with suggested pacing and blackboard plans.
- a compact bibliography with reading paths.

## 11. Assessment Ideas

Problem-set themes:

- derive Euler-Lagrange equations for constrained systems.
- compute Noether charges.
- prove conservation of the symplectic form under Hamiltonian flow.
- analyze Euler top stability.
- construct a Poincare section for the driven pendulum or standard map.
- estimate the resonance-overlap threshold for loss of invariant-curve
  confinement in the standard map.
- estimate ejection probabilities and explain uncertainty.
- derive Kelvin circulation theorem.
- derive Navier-Stokes from mass balance, Cauchy momentum balance, and
  Newtonian stress.
- analyze laminar Couette, Poiseuille, and pipe-flow profiles and their
  stability equations.
- interpret defects using curvature or torsion.

Project themes:

- compare integrators for the asteroid-belt model.
- build a rigid-body attitude visualization.
- study resonance overlap, cantori, and finite-time transport in the standard
  map.
- convert the Physics 151 Henon-Heiles, double-pendulum, and standard-map
  Mathematica demos into reproducible Python demos.
- simulate vortex dynamics.
- reconstruct Cosserat rods from prescribed curvature and twist.
- explore Shapere-Wilczek gauge kinematics for deformable bodies and swimming.

## 12. Implementation Milestones

### Milestone 1: Working Skeleton — complete

- Repo initialized.
- Planning document written.
- TeX notes scaffolded.
- Python demos runnable.
- Mathematica scripts added.
- Smoke tests pass.

### Milestone 2: Core Notes And Laboratories — complete draft

- Lagrangian, Hamiltonian, rigid-body, integrability, perturbation, three-body,
  fluid, elastic-body, and deforming-body chapters are integrated in one PDF.
- Core Python demos and Wolfram Language counterparts are present.
- Smoke tests cover the main computational contracts.
- Remaining work: add problem sets with selected solutions and commit rendered
  lecture figures from the demos.

### Milestone 3: Celestial Mechanics Unit — teaching version complete

- CR3BP rotating-frame geometry, zero-velocity curves, Jacobi diagnostics, and
  asteroid-belt ejection statistics are included.
- Numerical caveats are documented, including the non-symplectic nature of the
  classroom RK4 CR3BP integrator.
- Remaining work: add resonance-angle diagnostics, finite-time Lyapunov or
  MEGNO indicators, and a notebook-style ejection-probability workflow.

### Milestone 4: Continua And Gauge Unit — teaching version complete

- Navier-Stokes, exact laminar and unsteady solutions, stability discussions,
  finite elasticity, linear elasticity, classical bars/shafts/beams, Cosserat
  rods, and Shapere-Wilczek-style deforming-body gauge kinematics are present.
- Python and Wolfram Language demos cover Navier-Stokes solutions, linear
  elasticity, and deforming-body holonomy.
- Remaining work: extend the Cosserat rod and deforming-body demos to richer
  3D shape loops, and deepen the bridge between fluid relabeling symmetry and
  gauge language.

### Milestone 5: Publication Layer — next release work

- Tag a `v0.2.0` release after the current working tree is committed, so the
  149-page PDF, demos, tests, and planning documents are referenced by a stable
  snapshot.
- Convert selected demos to notebooks.
- Add generated figures and an instructor guide.
- Add a course website with Quarto or another static generator.

## 13. Style Guide

- Use ASCII source unless a format requires otherwise.
- Prefer precise equations over prose-only explanation.
- Keep code scripts readable and heavily parameterized.
- Name physical assumptions before deriving results.
- Separate model limitations from implementation limitations.
- Treat numerical outputs as experiments that need interpretation.

## 14. Immediate Next Work

The most valuable next steps are now:

1. Commit the current closure round, then tag `v0.2.0`.
2. Add problem sets and selected solutions for the core route.
3. Commit rendered figures from the Python and Mathematica demos.
4. Add an instructor guide with pacing, lecture goals, and recommended labs.
5. Upgrade the asteroid simulation with resonance-angle diagnostics and
   finite-time Lyapunov indicators.
6. Add a compact bibliography with reading paths.
