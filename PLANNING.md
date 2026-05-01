# Comprehensive Plan: Mechanics Through Phase Space

## 1. Project Thesis

This repository teaches mechanics as a unified geometric and computational
subject. The course starts with Lagrangian and Hamiltonian mechanics, develops
phase-space geometry, moves through integrability and chaos, and then extends
the same language to continua, fluids, and gauge-theoretic descriptions of
deforming bodies.

The central message is:

> A mechanical system is not just a set of equations. It is a space of possible
> configurations, a variational principle, a phase-space geometry, and a set of
> symmetries and obstructions that organize its motion.

The course should be useful for advanced undergraduates, beginning graduate
students, and self-directed readers who know vector calculus, ordinary
differential equations, and basic linear algebra. Differential geometry is
introduced as needed.

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
      01_geometric_lagrangian_hamiltonian.tex
      02_integrability_rigid_body.tex
      03_perturbation_chaos_celestial.tex
      04_fluid_mechanics.tex
      05_elastic_deforming_bodies.tex
  demos/
    python/
      asteroid_ejection_probability.py
      rigid_body_euler_top.py
      standard_map.py
      hamiltonian_pendulum.py
      fluids_vorticity.py
      cosserat_rod_demo.py
    mathematica/
      RigidBodyEulerTop.wl
      AsteroidEjectionProbability.wl
      GaugeDeformingBody.wl
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
- Hamilton-Jacobi theory
- geometric meaning of Liouville's theorem

This arc establishes the language needed for integrability and chaos.

### Arc C: Integrability And Rigid Bodies

The third arc asks when mechanics is solvable:

- constants of motion
- involution
- Liouville integrability
- invariant tori
- action-angle variables
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
- separatrix splitting
- Poincare sections
- KAM intuition
- chaotic transport

The flagship example is the Sun-Jupiter-asteroid restricted problem. The Kepler
problem is the integrable baseline. Jupiter is the perturbation. The asteroid
belt gives a natural laboratory for resonance, long-time instability, and
ejection probabilities.

### Arc E: Continua, Fluids, And Gauge Theory

The fifth arc expands mechanics from finitely many degrees of freedom to fields:

- deformation maps
- material and spatial descriptions
- Eulerian and Lagrangian variables
- strain and compatibility
- vorticity and circulation
- ideal fluid Hamiltonian structure
- local frames and gauge freedom
- Cosserat media
- dislocations, disclinations, torsion, and curvature

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
- Jupiter as a perturbing body.
- mean-motion resonances.
- chaotic layers and transport.
- numerical ejection probability.

Initial numerical model:

- planar Sun-centered restricted problem.
- Sun fixed at origin with Jupiter on a circular prescribed orbit.
- massless test particles sampled across an asteroid-belt annulus.
- symplectic-style kick-drift-kick integration for particles.
- ejection declared when a particle reaches a large heliocentric radius or has
  positive heliocentric energy outside the inner system.

This model is intentionally teachable. Later versions can upgrade to:

- barycentric coordinates with a live Sun-Jupiter two-body system.
- elliptical Jupiter orbit.
- Saturn and secular forcing.
- adaptive close-encounter handling.
- MEGNO or finite-time Lyapunov indicators.
- resonance-specific ensembles.

### 6.3 Fluids

The fluids thread introduces:

- flow maps.
- Eulerian velocity fields.
- vorticity.
- Kelvin circulation theorem.
- point vortex Hamiltonian systems.
- instability and mixing.
- infinite-dimensional Poisson brackets as an advanced endpoint.

The initial Python demo uses point vortices because they are simple, visual, and
Hamiltonian.

### 6.4 Gauge Theory Of Deforming Bodies

The deforming-body thread introduces:

- body manifold and ambient space.
- deformation map.
- material frames and spatial frames.
- local rotations as gauge freedom.
- connection coefficients as local comparison rules.
- curvature and torsion as incompatibility measures.
- Cosserat rods and media.
- dislocations and disclinations.

The initial demo reconstructs a planar Cosserat rod from a curvature field. It
is deliberately modest, but it gives a computational foothold for the idea that
a local frame field carries a connection.

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

The initial experiment reports:

- number of particles.
- integration time.
- time step.
- global ejection fraction.
- collision/loss fraction.
- survival fraction.
- ejection fraction binned by initial semimajor axis.

Teaching questions:

- Which semimajor axes are most vulnerable?
- How does the result change with integration time?
- How does changing Jupiter's mass change the ejection fraction?
- How does the time step affect the answer?
- Which losses look physical, and which might be numerical artifacts?

Future version:

- identify 3:1, 5:2, 7:3, and 2:1 resonant neighborhoods.
- compare ejection probability inside and outside resonant windows.
- compute resonance angles.
- estimate finite-time Lyapunov exponents.
- generate publication-quality figures for lecture.

## 10. Notes Roadmap

Current TeX notes are a first integrated draft:

- `01_geometric_lagrangian_hamiltonian.tex`
- `02_integrability_rigid_body.tex`
- `03_perturbation_chaos_celestial.tex`
- `04_fluid_mechanics.tex`
- `05_elastic_deforming_bodies.tex`

Next additions:

- dedicated chapter on constraints and reduction.
- dedicated chapter on symplectic geometry.
- dedicated chapter on Hamilton-Jacobi and action-angle variables.
- problem sets with solutions.
- lecture slides or short blackboard plans.
- rendered figures from the demos.

## 11. Assessment Ideas

Problem-set themes:

- derive Euler-Lagrange equations for constrained systems.
- compute Noether charges.
- prove conservation of the symplectic form under Hamiltonian flow.
- analyze Euler top stability.
- construct a Poincare section for the driven pendulum or standard map.
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
- study resonance overlap in the standard map.
- convert the Physics 151 Henon-Heiles, double-pendulum, and standard-map
  Mathematica demos into reproducible Python demos.
- simulate vortex dynamics.
- reconstruct Cosserat rods from prescribed curvature and twist.
- explore Shapere-Wilczek gauge kinematics for deformable bodies and swimming.

## 12. Implementation Milestones

### Milestone 1: Working Skeleton

- Repo initialized.
- Planning document written.
- TeX notes scaffolded.
- Python demos runnable.
- Mathematica scripts added.
- Smoke tests pass.

### Milestone 2: First Teaching Unit

- Complete polished rigid-body chapter.
- Add problem set and solutions.
- Add rendered figures from rigid-body demo.
- Add Mathematica notebook export.

### Milestone 3: Celestial Mechanics Unit

- Improve restricted three-body model.
- Add resonance diagnostics.
- Add Poincare section tooling.
- Add ejection-probability notebook.
- Add discussion of numerical reliability.

### Milestone 4: Continua And Gauge Unit

- Expand notes on deformation maps and compatibility.
- Add Cosserat rod simulation in 2D and 3D.
- Add dislocation/disclination examples.
- Connect fluid relabeling symmetry to gauge language.

### Milestone 5: Publication Layer

- Render notes to PDF.
- Convert selected demos to notebooks.
- Add a course website with Quarto or another static generator.
- Add generated figures and instructor guide.

## 13. Style Guide

- Use ASCII source unless a format requires otherwise.
- Prefer precise equations over prose-only explanation.
- Keep code scripts readable and heavily parameterized.
- Name physical assumptions before deriving results.
- Separate model limitations from implementation limitations.
- Treat numerical outputs as experiments that need interpretation.

## 14. Immediate Next Work

After this first implementation, the most valuable next steps are:

1. Add problem sets for the first four TeX chapters.
2. Render the first set of figures from the Python demos.
3. Upgrade the asteroid simulation with resonance labels.
4. Add a polished lecture on symplectic maps using the standard map.
5. Add a compact bibliography with reading paths.
