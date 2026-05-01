# Comprehensive Extraction: Physics 151 Teaching Material

Local source folder:

`/Users/xiyin/Dropbox/Physics 151`

This is the source ledger for the Physics 151 teaching folder. It records the
instructional content that should be mined for the mechanics repository. The
folder contains authored TeX course material, Mathematica notebooks, generated
PDFs and build files, a small number of administrative files, and a reference
shelf of papers/books used for the course.

This extraction has three levels:

1. Fully extracted authored TeX material: syllabus, lecture outline, problem
   sets, exam, and exam solution.
2. Notebook extraction: equations, parameters, numerical workflows, and
   pedagogical purpose extracted from the Mathematica `.nb` files, ignoring
   cached graphics/output except where the output reveals the intended demo.
3. Reference shelf catalog: local PDFs/DJVU/PPT are cataloged by filename and
   topic. Some are scanned or compressed external references rather than
   authored course notes, so their existence and intended use are recorded, but
   they are not represented as fully text-transcribed source.

The course material is directly aligned with the repo goals: Lagrangian
mechanics, Hamiltonian mechanics and phase space, rigid body mechanics,
Shapere-Wilczek gauge theory of deforming bodies, action-angle variables,
integrability, perturbation theory, KAM, resonances, asteroid-belt dynamics,
Poincare sections, standard maps, dissipative chaos, and numerical demos.

## Source Coverage

### Authored TeX Files Fully Extracted

- `151 syllabus.tex`
- `151_Lectures.tex`
- `Problem Set 1.tex`
- `Problem Set 2.tex`
- `Problem Set 4.tex`
- `Problem Set 5.tex`
- `Problem Set 6.tex`
- `Exam.tex`
- `Exam solution.tex`

No `Problem Set 3.tex` was present in the folder. This absence should be kept
explicit in future course reconstruction.

Generated PDFs corresponding to the TeX files were present:

- `151 syllabus.pdf`
- `151_Lectures.pdf`
- `Problem Set 1.pdf`
- `Problem Set 2.pdf`
- `Problem Set 4.pdf`
- `Problem Set 5.pdf`
- `Problem Set 6.pdf`
- `Exam.pdf`
- `Exam solution.pdf`

The generated PDFs duplicate the authored TeX content above. Auxiliary build
artifacts such as `.aux`, `.log`, `.synctex.gz`, and `.toc` were cataloged as
non-content build products.

### Mathematica Notebooks Inspected And Extracted

- `3 body homework.nb`
- `Demo 1 - Newtonian.nb`
- `Demo 2 - double pendulum.nb`
- `double pendulum.nb`
- `Demo 3 - Euler angles and rotation of rigid body.nb`
- `Demo 3 -new - Euler angles and rotation of rigid body.nb`
- `Demo 4 - two spherical shells.nb`
- `Demo 5 - phase space plot of 2D harmonic oscillator.nb`
- `Demo 6 - Liouville theorem.nb`
- `Demo 7 - coupled harmonic oscillator.nb`
- `Demo 8 - asteroid belt.nb`
- `Demo 8 - asteroid Jupiter coupling.nb`
- `Demo 9 - Henon-Heiles potential.nb`
- `test 9 - Henon-Heiles potential.nb`
- `Demo 10 - standard map.nb`
- `new Demo 10 - standard map.nb`
- `Demo 11 - homoclinic tangle of the standard map.nb`
- `Demo 12 - limit cycles and attractors.nb`
- `Demo 12 - van der Pol.nb`
- `Demo 13 - logistic map.nb`
- `Euler.nb`
- `Schw.nb`
- `kepler.nb`
- `phase space 1.nb`
- `ps6stuff.nb`
- `recur.nb`
- `rigid body Hamiltonian.nb`
- `Untitled-1-XY.nb`
- `Untitled-2.nb`
- `Untitled-3.nb`

The notebooks are Mathematica source files with substantial cached output and
graphics. The extraction below records the equations, parameters, numerical
procedures, and visual objectives rather than the cached image payloads.

### External Reference Shelf Cataloged

- `shapere-wilczek.pdf`
- `128_Gauge_Kinematics_of_Deformable_Bodies.pdf`
- `Wilczek.pdf`
- `cat_gauge_theory.PDF`
- `berry115.pdf`
- `kam theorem.pdf`
- `kirkwood.pdf`
- `asteroid belt.pdf`
- `asteroid belt II.pdf`
- `Hill Lunar Theory.pdf`
- `Moon-Earth-Sin RMP.70.589.pdf`
- `thoriedumouvem03plan.pdf`
- `0210068.pdf`
- `02-440.pdf`
- `03-ApteW05.pdf`
- `1303.0181v1.pdf`
- `200_COURSE_UCSD.pdf`
- `97PHD_morrison.pdf`
- `ASME-Liapunov.pdf`
- `Harding.pdf`
- `dvp-6.946-pset9.pdf`
- `AlgTrans_Chap5.pdf`
- `RG logistic.pdf`
- `Logistic Map.pdf`
- `king2010.pdf`
- `Mathematical Methods of Classical Mechanics, 2nd ed.  - V.I. Arnold.djvu`
- `Mechanics 3rd ed. - L. Landau, E. Lifshitz.djvu`
- `p600_04r.ppt`

`PHYS151 Mechanics grades.numbers` is an administrative gradebook, not teaching
content for this repo. It is cataloged but not extracted.

## Course Spine From The Syllabus

The syllabus identifies the course as Fall 2014 Physics 151 at Harvard, taught
by Xi Yin. Mathematica was used throughout. The declared course arc is:

1. Lagrangian formalism.
2. Rigid rotating bodies.
3. Shapere-Wilczek gauge theory for deformations and rotations.
4. Canonical formalism.
5. Phase space.
6. Action-angle variables.
7. Chaotic dynamics.

The textbook backbone was Goldstein, with additional material from specialized
references. Evaluation consisted of problem sets and a 48-hour take-home exam.
For repo purposes the important pedagogical fact is that the course was built
around deriving mechanics from variational and symplectic principles and then
using computation to visualize rigid bodies, invariant tori, resonance,
transport, and chaos.

## Lecture Outline Extraction

The lecture outline is concise but gives the intended order of exposition.

### 1. Variational Principles And Lagrangian Mechanics

Core topics:

- Generalized coordinates.
- Principle of least action.
- Euler-Lagrange equations.
- Constrained systems.
- Holonomic constraints.
- Nonholonomic constraints.
- Lagrange multipliers.
- d'Alembert principle.
- Example: rolling ball on rotating disc.
- Symmetry and conservation laws.
- Noether theorem.
- Central-force problem.
- Scattering.
- Lenz vector.
- Orbital precession.
- Special three-body solutions.

Repo implication: the notes should introduce generalized coordinates and
constraints before Hamiltonian mechanics, and the examples should include both
elementary constrained motion and the central force/Kepler problem. The Lenz
vector and orbital precession should appear as nontrivial conserved-quantity
and perturbation examples.

### 2. Rigid Body

Core topics:

- Angular velocity in space and body frames.
- Angular momentum.
- Inertia tensor.
- Euler angles.
- Rotation matrices.
- The group `SO(3)`.
- Spinning tops.
- Euler equations.
- Free symmetric top.
- Heavy symmetric top.
- Free asymmetric top.

Repo implication: rigid-body mechanics should not be merely an example at the
end. It should be a central bridge from Lagrangian mechanics on configuration
manifolds to Hamiltonian mechanics on `T^*SO(3)`, momentum maps, and
integrability.

### 3. Nonholonomic Systems And Gauge Theory

Core topics:

- Rotation of a deforming body.
- `SO(3)` gauge theory.
- Gauge field/connection.
- Field strength.
- Holonomy.
- Two rotating shells.
- Falling cat.

Repo implication: the advanced deforming-body chapter should follow the
Shapere-Wilczek approach. Internal shape variables define a base manifold,
overall rotation is an `SO(3)` fiber, and zero-angular-momentum reconstruction
is governed by a mechanical connection. Holonomy then explains net rotation
after a closed shape cycle.

### 4. Canonical Formalism And Hamiltonian Mechanics

Core topics:

- Hamiltonian and equivalence to Euler-Lagrange equations.
- Phase-space orbits.
- Pendulum as a phase-space example.
- Poisson bracket.
- Canonical transformations.
- Liouville theorem.
- Hamilton-Jacobi theory.
- Analogy between Hamilton-Jacobi and wave/Schrodinger equations.

Repo implication: Hamiltonian mechanics should be derived from the Legendre
transform with all regularity assumptions stated. The Hamilton-Jacobi section
is currently a high-value gap and should be added as a bridge from canonical
transformations to action-angle variables.

### 5. Integrable Systems And Perturbations

Core topics:

- Action-angle variables.
- Invariant tori.
- KAM theorem.
- Resonant tori.
- Nonresonant tori.
- Strongly nonresonant tori.
- Probability of stable orbits.

Repo implication: the integrability chapter should prove the local origin of
invariant tori, explain cycles and action integrals, and then show how
perturbations destroy resonant tori first while Diophantine tori persist under
KAM hypotheses.

### 6. Chaotic Dynamics

Core topics:

- Attractors.
- Poincare maps.
- Henon-Heiles system.
- Lyapunov exponents.
- Bifurcation.
- Fractals.
- Noninteger dimensions.

Repo implication: the chaos chapter should include Hamiltonian chaos through
Poincare sections and homoclinic tangles, plus a separate comparison section
for dissipative attractors such as the van der Pol oscillator and logistic map.

## Problem Set 1 Extraction

Date: September 9, 2014. Due: September 23, 2014.

Pedagogical role: establish coordinate invariance of the Euler-Lagrange
equations, introduce nonstandard Lagrangians, constrained rolling motion,
time-dependent Lagrangians, equilibrium bifurcation, Euler-angle matrices, and
basic numerical three-body dynamics.

### PS1 Problem 1: Point Transformations

Reference: Goldstein 1.10.

Given a point transformation

`q_l = q_l(s_1, ..., s_n, t)`,

prove that the Euler-Lagrange equations preserve their form when expressed in
the generalized coordinates `s_j`. The intended derivation is the chain-rule
proof:

- velocities transform as
  `qdot_l = sum_j (partial q_l/partial s_j) sdot_j + partial q_l/partial t`;
- the transformed Lagrangian is
  `L'(s,sdot,t)=L(q(s,t),qdot(s,sdot,t),t)`;
- the identities
  `partial qdot_l/partial sdot_j = partial q_l/partial s_j` and
  `d/dt(partial q_l/partial s_j) = partial qdot_l/partial s_j`
  give
  `d/dt(partial L'/partial sdot_j)-partial L'/partial s_j
   = sum_l [d/dt(partial L/partial qdot_l)-partial L/partial q_l]
     partial q_l/partial s_j`.

If the Jacobian has full rank, the vanishing of the original Euler-Lagrange
expressions implies the vanishing of the transformed ones.

Repo use: early theorem that Euler-Lagrange equations are intrinsic under
regular point transformations.

### PS1 Problem 2: Nonstandard One-Dimensional Lagrangian

Reference: Goldstein 1.20.

Lagrangian:

`L = m^2 xdot^4/12 + m xdot^2 V(x) - V(x)^2`.

The exercise asks for the motion and the physical nature of the system. The
important point is that inequivalent-looking Lagrangians can produce familiar
equations of motion or singular sectors. One computes

`partial L/partial xdot = (m^2/3) xdot^3 + 2m V xdot`,

`partial L/partial x = m xdot^2 V'(x) - 2 V V'(x)`.

The Euler-Lagrange equation factors after differentiation:

`(m xdot^2 + 2V)(m xddot + V') = 0`.

Thus one branch is the ordinary Newton equation

`m xddot = -V'(x)`,

while the other branch is the singular/non-Newtonian branch

`m xdot^2 + 2V(x) = 0`.

This is a useful example for explaining that a Lagrangian is not unique and
that regularity of the velocity Hessian matters.

Repo use: in the Lagrangian foundations chapter under "non-unique and
non-regular Lagrangians."

### PS1 Problem 3: Hoop Rolling On A Fixed Cylinder

System:

- Uniform hoop of mass `m` and radius `r`.
- Fixed cylinder of radius `R`.
- Hoop rolls without slipping on the outside of the cylinder.
- Gravity acts downward.
- Hoop starts from rest at the top.
- Find where the hoop loses contact.

Coordinates: take `theta` as the angular position of the hoop center relative
to the upward vertical. The center of mass has radius `R+r`. Rolling without
slipping relates the hoop spin angle to the orbital angle by

`r phi_dot = (R+r) theta_dot`

up to sign convention. For a hoop, the spin inertia about its center is
`I = m r^2`. Hence

`T = (1/2)m(R+r)^2 theta_dot^2 + (1/2)I phi_dot^2
   = m(R+r)^2 theta_dot^2`,

using the rolling constraint. With gravitational potential

`V = m g (R+r) cos theta`,

energy from rest at the top gives

`m(R+r)^2 theta_dot^2 = m g (R+r)(1 - cos theta)`.

The radial equation, with outward radial direction from the fixed cylinder
center, gives the normal-force condition. Loss of contact occurs when the
normal force becomes zero:

`m g cos theta - N = m(R+r) theta_dot^2`.

Using the energy relation gives

`N = m g[cos theta - (1-cos theta)]`.

For the hoop, loss of contact therefore occurs at

`cos theta = 1/2`.

This exercise is a clean place to compare eliminating constraints with using
Lagrange multipliers.

Repo use: constrained Lagrangian mechanics and rolling constraints.

### PS1 Problem 4: Damped Oscillator From A Time-Dependent Lagrangian

Reference: Goldstein 2.16.

Lagrangian:

`L = exp(gamma t) [ (m/2) qdot^2 - (k/2) q^2 ]`.

The Euler-Lagrange equation is

`m qddot + m gamma qdot + k q = 0`.

The problem asks for constants of motion and the transformation

`s = exp(gamma t/2) q`.

With this transformation, the damped oscillator is mapped into an effective
undamped oscillator with shifted frequency. The transformed equation has the
form

`sddot + (k/m - gamma^2/4) s = 0`

after discarding a total derivative in the Lagrangian. This is an excellent
example for explaining time-dependent Lagrangians, nonconservation of the
ordinary energy, and the role of total time derivatives.

Repo use: time-dependent Lagrangians and Noether theorem caveats.

### PS1 Problem 5: Bead On A Rotating Vertical Hoop

Reference: Goldstein 2.18.

System:

- Bead of mass `m`.
- Hoop of radius `a`.
- Hoop lies in a vertical plane and rotates about a vertical diameter with
  angular speed `omega`.
- Coordinate `theta` measures bead angle on the hoop.

The effective one-degree-of-freedom Lagrangian has the standard form

`L = (1/2)m a^2 theta_dot^2
     + (1/2)m a^2 omega^2 sin^2 theta
     + m g a cos theta`

up to the convention for `theta=0`. The effective potential is

`V_eff(theta) = - (1/2)m a^2 omega^2 sin^2 theta - m g a cos theta`.

Stationary points solve

`sin theta (g - a omega^2 cos theta) = 0`

or the equivalent sign-convention variant. A critical angular velocity

`omega_0 = sqrt(g/a)`

marks the bifurcation where the bottom equilibrium loses stability and two
off-bottom equilibria appear.

Repo use: symmetry-reduced effective potential and pitchfork-style
equilibrium bifurcation.

### PS1 Problem 6: Euler-Angle Rotation Matrix

Reference: Goldstein 4.5.

The problem asks for the rotation matrix built from component Euler rotations
and the verification of orthogonality. This should be used in the rigid-body
chapter to establish conventions before angular velocity is computed.

Repo use: define the Euler-angle convention once, state whether rotations are
active/passive and body/space ordered, then use the same convention for the
rigid-body notebooks.

### PS1 Problem 7: Numerical Three-Body Problem

System:

- Three identical masses.
- Pairwise Newtonian attraction `V = -k/r`.
- Units `m=k=l=1`.
- Initial equilateral positions:
  - `r_1(0) = (1,0)`.
  - `r_2(0) = (-1/2, sqrt(3)/2)`.
  - `r_3(0) = (-1/2, -sqrt(3)/2)`.
- Symmetric rotating state with speed parameter `v=0.8`.
- Perturbation `epsilon=0.05` in the `xdot_1` and `xdot_2` components.
- Integrate on `t in [0,50]`.

The associated notebook `3 body homework.nb` implements this problem. It uses
the potential

`V = -k/r12 - k/r23 - k/r13`,

with `m=k=1`, `v=.8`, `epsilon=.05`, and velocity perturbations

`xdot_1(0)=epsilon`,

`xdot_2(0)=-v sqrt(3)/2 - epsilon`,

`xdot_3(0)= v sqrt(3)/2`.

Repo use: bridge from Lagrangian mechanics to numerical sensitivity and the
later three-body ejection-probability demo.

## Problem Set 2 Extraction

Date: September 23, 2014. Due: October 7, 2014.

Pedagogical role: deepen Lagrangian modeling, transition to Hamiltonian
systems, introduce relativistic/effective radial dynamics, and make
deforming-body gauge theory computationally concrete.

### PS2 Problem 1: Compound Pendulum With Freely Rotating Disk

Reference: Goldstein 5.20.

System:

- Plane compound pendulum.
- Rod of length `ell` and mass `m`.
- Disk of radius `a` and mass `M`.
- Disk can rotate freely in its own vertical plane.

The problem asks to set up the Lagrange equations. The main modeling point is
to distinguish the rod swing angle from the disk spin angle and to compute the
kinetic energy from center-of-mass translation plus rotational kinetic energy.

Repo use: modeling composite rigid systems with independent generalized
coordinates.

### PS2 Problem 2: Tilted Door Hinge

Reference: Goldstein 5.30.

System:

- Door height `2 m`.
- Door width `0.9 m`.
- Door is opened by `90 deg` and released.
- Door closes in `3 s`.
- Hinges are frictionless.
- Find the hinge angle with the vertical.

The problem is a rigid-body pendulum about a tilted axis. The gravitational
torque is produced by the component of the center-of-mass displacement along
the tilted hinge geometry. The period/closing time determines the tilt angle
through the small-angle or finite-angle equation depending on the intended
approximation.

Repo use: nonstandard rigid-body axis and physical interpretation of moments
of inertia about a constrained axis.

### PS2 Problem 3: Pendulum With Suspension Point On A Parabola

Reference: Goldstein 8.19.

System:

- Pendulum length `ell`, mass `m`.
- Suspension point constrained to a parabola
  `z = a x^2`.
- Derive Hamiltonian and Hamilton equations.

This problem is useful because the kinetic metric depends on the coordinate
used to describe the support point. It forces a careful Legendre transform:
define coordinates, compute `T(q,qdot)`, construct momenta, invert the
velocity-momentum relation, and derive Hamilton equations.

Repo use: first Hamiltonian example with a nontrivial coordinate metric.

### PS2 Problem 4: Schwarzschild-Type Radial Lagrangian

Lagrangian in polar coordinates:

`L = -m sqrt( (1 - R/r) - rdot^2/(1 - R/r) - r^2 thetadot^2 )`,

with assumption `r > R`.

Tasks:

1. Find relation between angular momentum `p_theta` and circular-orbit radius.
2. Perturb `r = r_0 + x(t)` at fixed `p_theta` and derive
   `xddot + omega^2 x = 0`.
3. Show circular orbits are stable for `r > 3R` and unstable for `r < 3R`.
4. Numerically explore `m=R=1`, `r_0=3R`, varying angular momentum.

This problem is a natural advanced example after Kepler. It teaches effective
radial potentials, conserved angular momentum, circular-orbit conditions, and
stability from the second variation of the effective potential. The associated
`Schw.nb` notebook contains the numerical/visual version.

Repo use: advanced central-force section and orbital stability demo.

### PS2 Problem 5: Deforming-Body Gauge Equation

This is one of the most important Physics 151 inputs for the repo.

Definitions:

- `Q` is a symmetric shape tensor built from the body's instantaneous internal
  coordinates.
- `A` is an antisymmetric angular-velocity matrix representing the gauge
  potential/mechanical connection.
- `tilde I` is the inertia tensor in the body/shape frame:

  `tilde I_ij = delta_ij sum_k Q_kk - Q_ij`.

- `tilde J` is an internal angular momentum-like vector.
- `hat J` is the antisymmetric matrix associated to `tilde J`:

  `hat J_ij = (1/2) sum_k epsilon_ijk tilde J_k`.

The central equation is

`A Q + Q A = 2 hat J`.

The problem asks one to show

`A_ij = sum_{k,l} epsilon_ijk (tilde I^{-1})_{kl} tilde J_l`.

Derivation sketch to preserve in repo notes:

1. Identify antisymmetric matrices with vectors:
   `A_ij = epsilon_ijk Omega_k` up to convention.
2. Multiply out `AQ+QA` and use symmetry of `Q`.
3. Repackage the resulting linear map from `Omega` to `tilde J` as the inertia
   tensor `tilde I`.
4. Invert the inertia tensor on the nondegenerate shape sector.

Assumptions to state:

- The shape tensor is such that `tilde I` is invertible.
- The body is considered in a zero-total-angular-momentum or prescribed
  angular-momentum reconstruction setting.
- Sign conventions depend on whether `A_ij=epsilon_ijk Omega_k` or
  `A_ij=-epsilon_ijk Omega_k`.

Repo use: this formula is already folded into
`notes/tex/07_deforming_body_gauge.tex`, and should remain a central
computational result in the Shapere-Wilczek section.

### PS2 Problem 6: Helicopter Model As An SO(3) Gauge System

System:

- Rigid body with principal inertias all equal to `I_0`.
- Two internal rotary wings.
- First rotor is horizontal about the `z` axis with inertia `I_1`.
- Second rotor is vertical about the `y` axis with inertia `I_2`.

Tasks:

1. Identify the internal configuration space.
2. Derive the Shapere-Wilczek `SO(3)` gauge field `A_mu`.
3. Determine possible overall rotations after a closed internal cycle when air
   resistance and gravity are neglected.

Pedagogical point: this is a finite-dimensional rotor model for gauge
reconstruction. The internal rotor angles are base coordinates; the orientation
of the whole object is an `SO(3)` fiber. With zero total angular momentum, the
overall angular velocity is a connection applied to the internal angular
velocities.

Repo use: example immediately after the abstract deforming-body gauge
derivation, before the two-shell/falling-cat notebook visualization.

## Problem Set 4 Extraction

Date: October 21, 2014. Due: November 4, 2014.

Pedagogical role: action-angle variables, invariant tori, integrability of the
harmonic oscillator and rigid body, and the explicit computation of actions as
Poincare integral invariants.

### PS4 Problem 1: One-Dimensional Inverse-Absolute Potential

Reference: Goldstein 10.14.

Potential:

`V(x) = -k/|x|`.

For negative bounded oscillatory motion, use action-angle variables to find the
period as a function of energy. Since the motion is one-dimensional, the action
is

`I(E) = (1/2pi)oint p dx`,

where

`p = sqrt(2m(E + k/|x|))`

over the allowed interval. The frequency follows from

`omega(E) = dH/dI`,

and the period is

`T(E) = 2pi dI/dE`.

Repo use: one-dimensional action-angle derivation before tori.

### PS4 Problem 2: Two-Dimensional Harmonic Oscillator In Polar Coordinates

Hamiltonian:

`H = p_r^2/(2m) + p_theta^2/(2m r^2) + (1/2) k r^2`.

Tasks:

1. Show `P_1=H` and `P_2=p_theta` Poisson commute.
2. Find a canonical transformation from
   `(r,theta,p_r,p_theta)` to `(Q_1,Q_2,P_1,P_2)`.
3. At fixed `(P_1,P_2)`, identify the invariant torus.
4. Use cycles:
   - `gamma_1`: fixed `r`, `theta` from `0` to `2pi`.
   - `gamma_2`: fixed `theta`, `r` from `r_min` to `r_max` with positive
     `p_r`, then back with negative `p_r`.
5. Find actions as Poincare integral invariants and construct angle variables.

Important formulas:

- Angular action:

  `I_theta = (1/2pi)oint p_theta dtheta = p_theta`.

- Radial action:

  `I_r = (1/pi) integral_{r_min}^{r_max}
          sqrt(2mE - p_theta^2/r^2 - m k r^2) dr`.

For the isotropic oscillator, the energy depends on actions in the form

`H = omega(2 I_r + |I_theta|)`,

with `omega=sqrt(k/m)`.

Repo use: canonical route to invariant tori with explicit cycles.

### PS4 Problem 3: Free Rigid Body In Euler Angles

System:

- Free rigid body.
- Euler angles `(phi,theta,psi)`.
- Principal moments `I_1,I_2,I_3`.

Tasks:

1. Express `H`, `J_x`, `J_y`, and `J_z` in Euler angles and conjugate momenta.
2. Compute phase-space vector fields from conserved quantities.
3. Use notation:
   - `eta` for Euler-angle coordinates.
   - `n = grad_eta F`.
   - `t = J dot grad_eta F`.
4. Compute commutators of the vector fields.

Pedagogical point: the rigid body supplies a concrete nontrivial Hamiltonian
system whose constants of motion reflect rotational symmetry. This bridges
Euler equations, Poisson brackets, and the geometry of `T^*SO(3)`.

Repo use: include as an advanced exercise after deriving rigid-body
Hamiltonian mechanics.

### PS4 Problem 4: Symmetric Free Rigid Body And A Three-Torus

System:

- Symmetric free rigid body.
- `I_1=I_2>I_3`, described as a football-like body.
- Conserved quantities: `H`, `J^2`, `J_z`.
- These Poisson commute and label invariant three-tori.

Tasks and results:

1. Determine the allowed range of `theta` in terms of `H`, `J^2`, and `J_z`.
2. Use cycles:
   - `gamma_1`: `phi` from `0` to `2pi`.
   - `gamma_2`: `psi` from `0` to `2pi`.
   - `gamma_3`: `theta` libration with positive and negative `p_theta`.
3. Show the actions:

   `I_phi = J_z`,

   `I_psi = sqrt( (2 I_1 I_3/(I_1-I_3)) (H - J^2/(2 I_1)) )`,

   `I_theta = J - I_psi`.

4. Useful integral:

   `integral_a^b sqrt((b-x)(x-a))/(1-x^2) dx`

   `= (pi/2)[2 - sqrt((1+a)(1+b)) - sqrt((1-a)(1-b))]`.

5. Derive the equations of motion for conjugate angles
   `(alpha_phi, alpha_psi, alpha_theta)`.
6. Ask whether a generic trajectory is dense on the invariant three-torus.

Repo use: this should become a flagship example in the integrability chapter:
the free symmetric top is a fully worked Liouville integrable system with
explicit actions and torus flow.

## Problem Set 5 Extraction

Date: November 4, 2014. Due: November 18, 2014.

Pedagogical role: perturbation theory, resonance, small divisors, failure of
canonical perturbation at resonance, and the Henon-Heiles system as a concrete
Hamiltonian chaos bridge.

### PS5 Problem 1: Driven One-Angle Hamiltonian

Hamiltonian:

`H = I^2/2 + epsilon cos(n theta - nu t)`.

Interpretation: toy model for a planet orbiting a star under the influence of
another massive planet.

Tasks:

1. Find resonant values of `I`.
2. Numerically solve for `nu=1`, `epsilon=0.01`,
   `theta(0)=0`, `I(0)=a`, with `a` close to `1`, and describe `theta(t)`.
3. Perform the perturbation expansion

   `theta = theta_0 + epsilon theta_1 + epsilon^2 theta_2 + ...`,

   `I = I_0 + epsilon I_1 + epsilon^2 I_2 + ...`,

   through order `epsilon`.

Core equations:

`theta_dot = partial H/partial I = I`,

`I_dot = -partial H/partial theta = n epsilon sin(n theta - nu t)`.

The unperturbed motion is `theta_0 = I_0 t + theta_0(0)`. Resonance occurs
when

`n I_0 - nu = 0`,

or

`I_res = nu/n`.

Away from resonance, perturbation theory gives bounded oscillatory corrections
with denominators involving `n I_0 - nu`. Near resonance, those denominators
become small and one must replace naive perturbation theory by resonant normal
forms.

Repo use: introductory small-divisor example before KAM.

### PS5 Problem 2: Henon-Heiles In Cartesian Oscillator Actions

Hamiltonian:

`H = H_0 + lambda H_1`,

`H_0 = (1/2)p_x^2 + (1/2)p_y^2 + (1/2)x^2 + (1/2)y^2`,

`H_1 = x^2 y - y^3/3`.

Tasks:

1. Express the Hamiltonian in Cartesian oscillator action-angle variables
   `(I_1,theta_1),(I_2,theta_2)`.
2. Seek a canonical transformation generated by

   `S(I',theta) = I'_1 theta_1 + I'_2 theta_2
                  + lambda S_1 + lambda^2 S_2 + ...`

   that makes the transformed Hamiltonian integrable:

   `H' = H'(I')`.

3. Calculate `S_1`.
4. Show that `S_2` does not exist because resonance creates a small-divisor
   obstruction.

For the isotropic oscillator,

`x = sqrt(2I_1) sin theta_1`,

`p_x = sqrt(2I_1) cos theta_1`,

and similarly for `y`. Since the unperturbed frequencies are equal, Fourier
modes with zero divisor `k dot omega = 0` obstruct the removal of all angle
dependence at higher order.

Repo use: clear derivation of why nonresonance matters in canonical
perturbation theory.

### PS5 Problem 3: Henon-Heiles In Polar Action-Angle Variables

Hamiltonian:

`H_0 = p_r^2/2 + p_phi^2/(2r^2) + r^2/2`,

`H_1 = (1/3) r^3 sin(3 phi)`.

Use the PS4 oscillator actions:

`J_1 = p_phi`,

`psi_1 = phi`,

`J_2 = H_0 - p_phi`,

`psi_2 = integral dr/sqrt(2(J_1+J_2)-J_1^2/r^2-r^2)`.

The problem gives, up to a constant shift,

`r = [ J_1 + J_2 + cos(2 psi_2) sqrt(J_2^2+2J_1J_2) ]^(1/2)`.

Tasks:

1. Express the full Hamiltonian in the action-angle variables.
2. Use the generating function

   `S(J',psi)=J'_1 psi_1 + J'_2 psi_2 + lambda S_1 + O(lambda^2)`

   and calculate `S_1`.

Repo use: parallel derivation to the Cartesian action-angle obstruction,
showing how the same physical system can be treated in coordinates adapted to
rotational structure.

### PS5 Extra Material After End Of Document

The file contains draft/abandoned material after `\end{document}`. It should be
treated as useful source but not as a polished assigned problem.

Draft double pendulum:

- Identical masses and lengths.
- Intended task: derive Lagrangian, small-angle linearization, and general
  solution.
- Raw text appears to contain a typo or missing square in the first kinetic
  term. It should not be copied verbatim without correction.

Coupled particles on concentric circles:

Hamiltonian:

`H = p_1^2/(2mR_1^2) + p_2^2/(2mR_2^2)`

`    + (k/2)(R_1^2 + R_2^2 - 2R_1R_2 cos(theta_1-theta_2))`.

Conserved total angular momentum:

`J = p_1 + p_2`.

The system is integrable by reduction to center and relative angles.

Repo use: good exercise for symmetry reduction and integrability.

## Problem Set 6 Extraction

Date: November 18, 2014. Due: December 2, 2014.

Pedagogical role: standard map, resonant-torus breakup, elliptic islands,
hyperbolic points, Lyapunov exponents, and numerical verification of
perturbative resonance theory.

Map:

`T_K(theta,p) = (theta+p, p+K sin(theta+p))`,

with `theta` modulo `2pi`. This is the kicked-rotor standard map in a
convention where the kick is evaluated at the advanced angle.

At `K=0`, invariant circles are `p=constant`. Resonant tori occur when

`p/(2pi)` is rational.

The assigned resonance is

`C: p = 2pi/3`,

which is fixed by `T_0^3`.

### PS6 Part A: Nearby Resonant Curve

For small `K`, find a nearby curve `C'` such that `T_K^3` fixes the angle
`theta`, not necessarily the momentum `p`.

This is a first-order resonant normal-form calculation. In the repo notes this
has already been folded in as the period-three standard-map example. The key
result is that one writes

`p = 2pi/3 + K rho(theta) + O(K^2)`

and solves the angle-fixing condition for `rho(theta)`.

### PS6 Part B: Six Period-Three Points

Find six points on `C'` fixed by `T_K^3`, classify them as elliptic or
hyperbolic, and determine the Lyapunov exponents at the hyperbolic points to
order `K^(3/2)`.

Pedagogical point: a resonant invariant circle breaks into alternating elliptic
and hyperbolic periodic points. The elliptic points are centers of island
chains, while the hyperbolic points generate stable and unstable manifolds.

### PS6 Part C: Elliptic Rotation Phase

Near each elliptic fixed point, the linearized `T_K^3` has eigenvalues

`exp(+- i alpha)`.

Determine `alpha` through order `K^(3/2)`.

Repo use: connect local linear stability to the visible angular step around an
island in the Poincare map.

### PS6 Part D: Numerical Verification

For `K=0.1`, start at

`(theta,p) = (pi/3, 2pi/3 + K/(2 sqrt(3)))`.

Numerically observe the surviving island torus and determine how many
applications of `T_K^3` are needed to move around once. Compare with the
perturbative expansion for `alpha`.

Associated notebooks:

- `Demo 10 - standard map.nb`
- `new Demo 10 - standard map.nb`
- `Demo 11 - homoclinic tangle of the standard map.nb`
- `ps6stuff.nb`
- `recur.nb`

Repo use: flagship bridge from KAM theory to visible resonant island chains.

## Exam Extraction

The exam contains four main problems. It also contains an extra unfinished rods
problem after the document end; that material is cataloged separately.

### Exam Problem 1: Solid Cylinder Rolling Inside A Hollow Cylinder

System:

- Solid cylinder of radius `R`.
- Fixed hollow cylinder of radius `2R`.
- Rolling without slipping inside the hollow cylinder.
- Find small oscillation frequency.

Solution content:

`L = (1/2) M R^2 theta_dot^2 + (1/4) M R^2 theta_dot^2
     + M g R cos theta`.

The translational kinetic energy is the center-of-mass motion on a circle of
radius `R`. For a solid cylinder, `I = (1/2)MR^2`, giving the rotational term
`(1/4)MR^2 theta_dot^2` under the rolling constraint.

Euler-Lagrange equation:

`(3/2) theta_ddot + (g/R) sin theta = 0`.

Small oscillation frequency:

`omega = sqrt(2g/(3R))`.

Repo use: exam-level constrained rolling example.

### Exam Problem 2: Mass Driven Along A Rod

System:

- A mass constrained on a rod.
- Prescribed radial motion:

  `r(t) = (ell/2)(1 + cos Omega t)`.

- Generalized coordinate: angular displacement `theta`.

Solution Lagrangian:

`L = (1/2)m( r'(t)^2 + r(t)^2 theta_dot^2 ) + m g r(t) cos theta`.

Equation of motion:

`(1 + cos Omega t) theta_ddot`

`- 2 Omega sin Omega t theta_dot`

`+ (2g/ell) sin theta = 0`.

Repo use: time-dependent constraint and parametric driving.

### Exam Problem 3: Particle Between Fixed Wall And Slowly Moving Wall

System:

- Particle bouncing elastically between one fixed wall and one slowly moving
  wall.
- Wall separation changes slowly from `L` to `x(t)`.

Solution idea:

For wall speed `u` treated as approximately constant over one bounce period,
the time between collisions is

`Delta t = 2L/v`.

The speed/momentum increases by `2u` while the wall displacement is

`Delta L = -2Lu/v`.

Therefore

`Delta p = -(p/L) Delta L`,

which integrates to the adiabatic invariant

`p L = constant`.

If the wall position is `x(t)`, then

`p(t) = p(0) L/x(t)`,

and

`E(t) = p(t)^2/(2m) = m v^2 L^2/(2 x(t)^2)`.

Repo use: adiabatic invariant example before action-angle variables.

### Exam Problem 4: Logarithmic Hamiltonian

Hamiltonian:

`H = -1/2 log[(x_1-x_2)^2 + (p_1-p_2)^2]`.

Solution change of variables:

`x = (x_1-x_2)/2`,

`p = p_1-p_2`,

`tilde x = (x_1+x_2)/2`,

`tilde p = p_1+p_2`.

The center variables are constant. The reduced equations are

`xdot = -p/(4x^2+p^2)`,

`pdot = 4x/(4x^2+p^2)`.

Write

`x = (R/2) cos theta`,

`p = R sin theta`.

Then

`Rdot = 0`,

`theta_dot = 2/R^2`.

Solution:

`x = (R/2) cos(2(t-t_0)/R^2)`,

`p = R sin(2(t-t_0)/R^2)`.

Repo use: solvable two-degree-of-freedom Hamiltonian and canonical reduction.

### Exam Extra Material After End Of Document

The exam source contains an unfinished rods problem after `\end{document}`.

System:

- Two particles joined by three rods of length `ell`.
- Fixed endpoints at `(-ell,0)` and `(ell,0)`.
- No gravity.
- Coordinates `theta_1, theta_2`.

Constraint:

`(2 - cos theta_1 - cos theta_2)^2`

`+ (sin theta_1 - sin theta_2)^2 = 1`.

Equivalent form:

`5 - 4 cos theta_1 - 4 cos theta_2 + 2 cos(theta_1+theta_2) = 0`.

Lagrangian with multiplier:

`L = (1/2)m ell^2(theta_dot_1^2 + theta_dot_2^2)`

`    + lambda [constraint]`.

Energy relation:

`theta_dot_1^2 + theta_dot_2^2 = C`.

Allowed range:

`|theta_1|, |theta_2| < theta_0`,

where

`theta_0 = arctan(1/2)`.

Turning-point condition for `theta_dot_2=0`:

`2 sin theta_1 = sin(theta_1+theta_2)`.

The source ends with an incomplete line beginning with `If theta_2=theta_0`.

Repo use: catalog only, or repair into a constrained-configuration exercise
after deriving the constraint geometry.

## Mathematica Notebook Extraction

This section records the equations, parameters, and intended visual outputs of
the Mathematica notebooks.

### `kepler.nb`

Purpose: Kepler motion with a small central perturbation.

Coordinates and energies:

`T = (1/2)m(rdot^2 + r^2 theta_dot^2)`,

`V = -k/r - epsilon/r^3`,

`L = T - V`.

Parameter values:

- `m=1`
- `k=1`
- `epsilon=.02`
- `r(0)=1`
- `theta(0)=0`
- `rdot(0)=0`
- `theta_dot(0)=1.2`
- `maxtime=100`

Euler-Lagrange equations extracted from the notebook:

Radial:

`3 epsilon/r^4 + k/r^2 - m r theta_dot^2 + m rddot = 0`.

Angular:

`m r(2 rdot theta_dot + r theta_ddot) = 0`.

Visual workflow:

- Solve with `NDSolve`.
- Animate the trajectory in the plane.
- Plot phase data.

Repo use: follow the Kepler problem with precession from a perturbing
`epsilon/r^3` potential.

### `Demo 2 - double pendulum.nb` And `double pendulum.nb`

Purpose: derive and simulate the double pendulum from a Lagrangian.

Kinetic energy:

`T = (1/2)m_1 l_1^2 theta_dot_1^2`

`  + (1/2)m_2[(l_1 theta_dot_1 cos theta_1`

`                  + l_2 theta_dot_2 cos theta_2)^2`

`              + (l_1 theta_dot_1 sin theta_1`

`                  + l_2 theta_dot_2 sin theta_2)^2]`.

Potential energy:

`V = -m_1 g l_1 cos theta_1`

`    -m_2 g(l_2 cos theta_2 + l_1 cos theta_1)`.

Parameters:

- `g=1`
- `m_1=m_2=1`
- `l_1=l_2=1`
- `theta_1(0)=0`
- `theta_2(0)=0`
- `theta_dot_1(0)=1`
- `theta_dot_2(0)=0`
- `maxtime=100`

Workflow:

- Derive Euler-Lagrange equations.
- Use `NDSolve`.
- Animate rods and masses.
- Show trajectory traces.

Repo use: advanced Lagrangian example and later optional chaos demo.

### `3 body homework.nb`

Purpose: numerical three-body dynamics for PS1 Problem 7.

Potential:

`V = -k/r_12 - k/r_23 - k/r_13`.

Parameters:

- `m=1`
- `k=1`
- `v=.8`
- `epsilon=.05`
- `maxtime=50`
- plotting range approximately `[-4,4]^2`

Initial positions:

`r_1(0)=(1,0)`,

`r_2(0)=(-1/2,sqrt(3)/2)`,

`r_3(0)=(-1/2,-sqrt(3)/2)`.

Initial velocity perturbation:

`xdot_1(0)=epsilon`,

`xdot_2(0)=-v sqrt(3)/2 - epsilon`,

`xdot_3(0)=v sqrt(3)/2`.

Workflow:

- Define pair distances.
- Build Lagrange/Newton equations.
- Integrate with `NDSolve`.
- Animate three particle trajectories.

Repo use: seed for a reproducible three-body simulator and for later
ejection-probability Monte Carlo.

### `Demo 3 - Euler angles and rotation of rigid body.nb`

Purpose: derive Euler-angle kinematics and rigid-body equations, then animate
the body-frame axes.

Notebook constructs frame vectors `e_1,e_2,e_3` and rotation matrix

`R = Transpose[{e_1,e_2,e_3}]`.

It builds a skew angular-velocity matrix

`dd = -(dR/dphi dphi + dR/dtheta dtheta + dR/dpsi dpsi) R^T`.

Angular velocity in the space frame:

`omega = { theta_dot cos phi + psi_dot sin theta sin phi,`

`          -psi_dot cos phi sin theta + theta_dot sin phi,`

`          phi_dot + psi_dot cos theta }`.

It computes the invariant `SO(3)` metric:

`(1/2) Tr(dd dd^T)`.

It then computes body angular velocity

`Omega = omega R`

and the rigid-body Lagrangian

`L = sum_i (1/2) I_i Omega_i^2`.

Workflow:

- Derive Euler-Lagrange equations.
- Solve with `NDSolve`.
- Animate body-frame axes in space.

Related files:

- `Demo 3 -new - Euler angles and rotation of rigid body.nb`
- `Euler.nb`
- `rigid body Hamiltonian.nb`

These contain expanded or cached variants of the same rigid-body material,
including Hamiltonian/phase-space versions.

Repo use: rigid-body chapter, with exactly stated Euler-angle convention.

### `Demo 4 - two spherical shells.nb`

Purpose: visual Shapere-Wilczek gauge/holonomy demo.

Model:

- Two concentric or nearly concentric spherical shells.
- Outer sphere radius `R=2`.
- Inner sphere radius `r=1.85`.
- Transparency/visual spacing parameter `int=.3`.
- Colored rods attached to shells for orientation.

Workflow:

- Define rotation steps `Step1` through `Step5`.
- Compose `RotationTransform`s about `x`, `y`, and `z` axes.
- Counter-rotate inner and outer shells through a closed internal cycle.
- Animate the final orientation change.

Pedagogical point: a closed loop in internal configuration space can produce a
nontrivial overall orientation. This is holonomy of the mechanical connection,
the same idea behind the falling cat.

Repo use: deforming-body gauge theory chapter and possible Python/Three.js
visual demo.

### `Demo 5 - phase space plot of 2D harmonic oscillator.nb`

Purpose: visualize invariant tori for the two-dimensional harmonic oscillator.

Parameters:

- `omega_1=0.17`
- `omega_2=1`
- `tmax=200`

The notebook notes that the torus is artificially deformed for visualization
because the actual phase space is four-dimensional.

Embedded trajectory:

`{ cos(omega_1 t)(3 + sin(omega_2 t)),`

`  sin(omega_1 t)(3 + sin(omega_2 t)),`

`  cos(omega_2 t) }`.

Torus surface:

`{ (3+cos v) cos u, (3+cos v) sin u, sin v }`.

Repo use: explanatory figure for quasi-periodic torus winding.

### `Demo 6 - Liouville theorem.nb`

Purpose: demonstrate phase-area preservation under Hamiltonian flow.

Hamiltonian:

`H = p^2/2 + 1/(2r^3) - 1/(2r)`.

Initial family:

`r(0,s) = 1 + R cos s`,

`p(0,s) = R sin s`,

with

`R=.3`,

`maxtime=15`.

Workflow:

- Solve the Hamiltonian equations for a one-parameter family of initial
  conditions.
- Plot the evolving closed curve in the phase plane.

Repo use: Liouville theorem demo. In a Python port, compute area enclosed by
the curve numerically to show preservation.

### `Demo 7 - coupled harmonic oscillator.nb`

Purpose: coupled oscillator dynamics with a weak nonlinear coupling.

Coordinates: `x_1,x_2`.

Kinetic energy:

`T = (xdot_1^2 + xdot_2^2)/2`.

Potential:

`V = (1/2)omega_1^2 x_1^2 + (1/2)omega_2^2 x_2^2`

`    + (1/2)k(x_1-x_2)^3`.

Parameters:

- `omega_1=1`
- `omega_2=2`
- `k=.1`
- `x_1(0)=x_2(0)=0`
- `xdot_1(0)=1`
- `xdot_2(0)=0`
- `maxtime=100`

Workflow:

- Integrate equations.
- Animate phase portraits `(x_i,xdot_i)`.

Repo use: perturbation/near-integrable oscillator demo.

### `Demo 8 - asteroid belt.nb`

Purpose: asteroid-belt resonance visualization with a fixed Sun and circular
Jupiter.

Model:

- Sun fixed at origin.
- Jupiter has prescribed unit circular orbit:

  `(x_J(t),y_J(t)) = (cos t, sin t)`.

- Asteroid coordinates `(x_1,y_1)`.
- Potential:

  `V = -1/r_1 - k/r_12`,

  where `r_1` is asteroid-Sun distance and `r_12` is asteroid-Jupiter
  distance.

- Jupiter coupling strength:

  `k=.001`.

Equations:

`x_1'' + partial V/partial x_1 = 0`,

`y_1'' + partial V/partial y_1 = 0`,

after substituting Jupiter's circular motion.

Initialization:

- Kepler relation:

  `R = T^(2/3)`.

- Circular speed:

  `v = R^(-1/2)`.

- Random initial angle:

  `theta_0 = RandomReal[{0,2pi}]`.

- Period scan:

  `T = .1 + .0005 i`,

  `i=0,...,1000`.

- `maxtime=1000`.

Output:

- Solves 1001 asteroid orbits.
- Plots/animates the belt.
- Shows resonance/gap structure associated with Jupiter coupling.

Repo use: central source for the requested Sun-Jupiter-asteroid-belt
simulation. A Python port should replace cached notebook output with a
reproducible integrator, random seed control, resonance labeling, survival
metrics, and ejection probability.

### `Demo 8 - asteroid Jupiter coupling.nb`

Purpose: deterministic variant of the asteroid-Jupiter resonance demo.

Model: same potential and circular Jupiter as `Demo 8 - asteroid belt.nb`.

Parameters:

- `k=.001`
- deterministic initial angle `theta_0=0`
- period scan:

  `T = .1 + .0025 i`,

  `i=0,...,280`

- `maxtime=200`

Output:

- Coupling/resonance visualizations.

Repo use: faster deterministic comparison demo for resonance gaps.

### `Demo 9 - Henon-Heiles potential.nb`

Purpose: Hamiltonian chaos and Poincare sections.

Hamiltonian used in the notebook, with `x/y` exchanged relative to one common
textbook convention:

`H = p_x^2/2 + p_y^2/2 + x^2/2 + y^2/2 + y^2 x - x^3/3`.

Poincare section:

- section at `y=0`,
- choose the positive branch

  `p_y = +sqrt(...)`.

Notebook definitions:

- `pys[x,px,h]` computes the positive `p_y` branch at energy `h`.
- `T[{X,PX,PY}]` maps a section point to the next section crossing using
  `NDSolve` and `FindRoot[y[t]==0]`.
- `Generate` iterates the map.
- `Gra` and `GraSam` generate point clouds for Poincare plots.
- `bound[h]` computes the accessible domain from

  `p_x^2/2 + x^2/2 - x^3/3 < h`.

Related file:

- `test 9 - Henon-Heiles potential.nb`.

Repo use: Hamiltonian Poincare-section demo. This should be ported to Python
with event detection and energy checks.

### `Demo 10 - standard map.nb`

Purpose: standard map and resonance islands.

Map:

`T[{x,p}] := { Mod[x+p,2 Pi], Mod[p+K Sin[x+p],2 Pi] }`.

Notebook utilities:

- `Generate(seed,NN)` iterates the map.
- `Gra` plots an orbit.
- `GraSam` plots samples from many seeds.
- `grid[m]` generates an initial-condition grid.
- plotting range `[0,2pi]^2`.

Example:

- `K=0.1`
- `GraSam[grid[10],1000]`

Output:

- invariant curves,
- resonance islands,
- regular and chaotic regions depending on `K`.

Related file:

- `new Demo 10 - standard map.nb`.

Repo use: standard-map Python demo and figures for KAM/chaos.

### `Demo 11 - homoclinic tangle of the standard map.nb`

Purpose: stable and unstable manifolds of the standard map.

Map on `[-pi,pi]^2`:

`T[{x,p}] = { Mod[x+p,2pi,-pi],`

`             Mod[p+K Sin[x+p],2pi,-pi] }`.

Inverse map:

`TI[{x,p}] = { Mod[x-p+K Sin[x],2pi,-pi],`

`              Mod[p-K Sin[x],2pi,-pi] }`.

The inverse comes from solving

`y = x+p`,

`q = p + K sin(x+p)`.

Demo value:

- `K=1`.

Workflow:

- Generate forward iterates for unstable manifolds.
- Generate backward iterates for stable manifolds.
- Plot interleaving/tangling manifolds.

Repo use: visual explanation of homoclinic tangles and transverse
intersections.

### `Demo 12 - van der Pol.nb`

Purpose: dissipative limit cycle as contrast with Hamiltonian phase-volume
preservation.

Equation:

`x'' + (x^2 - lambda) x' + x = 0`.

Function:

`VDP[lambda, lis, maxtime, r]`.

Example parameter sets:

- `lambda=.2`, initial conditions `(-2,0)` and `(-.5,0)`, `maxtime=30`.
- `lambda=1`, initial conditions `(-4,0)` and `(0.1,0)`.

Output:

- phase-plane curves converging to a limit cycle.

Repo use: dissipative-dynamics appendix or chaos chapter comparison.

### `Demo 12 - limit cycles and attractors.nb`

Purpose: attractors and forced dissipative dynamics.

Includes the van der Pol oscillator and a forced damped pendulum:

`x'' + k x' + sin x = A sin(2t/3)`.

Helper:

`FDPP[A] = FDP[.5,A,{-2,0},1500]`.

The notebook varies

`A = .8, .9, ..., 1.6`

and samples the driven pendulum dynamics for attractor-like plots.

Repo use: optional dissipative chaos module; keep separate from the
Hamiltonian/KAM spine.

### `Demo 13 - logistic map.nb`

Purpose: discrete dissipative chaos and bifurcation diagram.

Map:

`T[{r,x}] = {r, r x(1-x)}`.

Workflow:

- `Generate(seed,MM,NN)` discards early iterates `MM`.
- Plot final iterates against `r`.
- Parameter range:

  `0 <= r <= 4`,

  `0 <= x <= 1`.

- Initial condition:

  `x_0=.2`.

- Grid spacing:

  `gap=.002`.

Repo use: optional chaos comparison and fractal/bifurcation figure.

### `Schw.nb`

Purpose: numerical visualization for PS2 Problem 4.

Content:

- Schwarzschild-type radial Lagrangian/orbit model.
- `NDSolve` integration.
- `Animate`, `ParametricPlot`, and `ListPlot` outputs.
- Circular orbit and stability visualization.

Repo use: convert to Python after central-force/Kepler section.

### `Euler.nb`

Purpose: rigid-body rotation visualization, related to Demo 3.

Content:

- Euler-angle equations.
- `NDSolve` integration.
- `ParametricPlot3D` and animation of body axes.

Repo use: rigid-body demo support.

### `phase space 1.nb`

Purpose: simple phase-space or invariant-torus visualization.

Content:

- 3D visual representation of phase-space motion.
- Companion to harmonic oscillator torus visualization.

Repo use: simple figure/demo source.

### `ps6stuff.nb`

Purpose: standard-map and Problem Set 6 scratch calculations.

Content:

- Likely period-three standard-map computations.
- Resonance/island visualization support.

Repo use: consult when refining the PS6 derivation or numerical standard-map
demo.

### `recur.nb`

Purpose: recurrence or standard-map-like large cached plot notebook.

Content:

- Large cached outputs.
- Iterated-map/recurrence visual material.

Repo use: low priority unless needed for additional recurrence figures.

### `rigid body Hamiltonian.nb`

Purpose: Hamiltonian rigid-body calculations.

Content:

- Rigid-body variables, momenta, and Hamiltonian expressions.
- Large cached output.

Repo use: source support for the rigid-body Hamiltonian and integrability
chapter.

### `Demo 1 - Newtonian.nb`

Purpose: introductory Newtonian numerical mechanics.

Content found:

- repeated `NDSolve`, `Animate`, `ParametricPlot`, and `ListPlot` workflows,
- comments and templates overlapping with later mechanics demos,
- likely early orbital/projectile and phase-curve demonstrations.

Repo use: low priority after extracting the more specific Kepler, three-body,
and Henon-Heiles notebooks.

### Miscellaneous Scratch Notebooks

`Untitled-1-XY.nb`:

- contains `NDSolve`/animation style exploratory calculations.

`Untitled-2.nb`:

- contains symbolic material involving gamma/EulerGamma expressions.

`Untitled-3.nb`:

- miscellaneous scratch content.

Repo use: catalog only unless a later search reveals a missing derivation.

## Reference Shelf Extraction And Use Map

The folder contains a substantial reference shelf. The repo should cite and
consult these as background, but the authored lecture notes should remain
self-contained.

### Gauge Theory, Deforming Bodies, And Geometric Phase

- `shapere-wilczek.pdf`
- `128_Gauge_Kinematics_of_Deformable_Bodies.pdf`
- `Wilczek.pdf`
- `cat_gauge_theory.PDF`
- `berry115.pdf`

Use:

- Shapere-Wilczek gauge kinematics of deformable bodies.
- Falling-cat problem as `SO(3)` holonomy.
- Berry/geometric phase analogy.
- Mechanical connection, curvature, and holonomy.

Important caution:

- Some files are scanned PDFs with image streams. They were cataloged as
  references, not fully transcribed text.

### Celestial Mechanics, Asteroid Belt, And Resonances

- `kirkwood.pdf`
- `asteroid belt.pdf`
- `asteroid belt II.pdf`
- `Hill Lunar Theory.pdf`
- `Moon-Earth-Sin RMP.70.589.pdf`
- `thoriedumouvem03plan.pdf`
- `0210068.pdf`
- `02-440.pdf`
- `03-ApteW05.pdf`
- `1303.0181v1.pdf`
- `200_COURSE_UCSD.pdf`
- `king2010.pdf`

Use:

- Kirkwood gaps and asteroid-belt resonances.
- Restricted three-body problem.
- Lunar theory/Hill problem.
- Resonance overlap and long-time instability.
- Context for the Sun-Jupiter-asteroid Python simulations.

### KAM, Hamiltonian Chaos, And Stability

- `kam theorem.pdf`
- `ASME-Liapunov.pdf`
- `Harding.pdf`
- `dvp-6.946-pset9.pdf`
- `AlgTrans_Chap5.pdf`

Use:

- KAM theorem reference.
- Lyapunov stability.
- Perturbative and algebraic transformations.
- Supporting material for action-angle and small-divisor sections.

The handwritten `KAM lecture.pdf` in `/Users/xiyin/Dropbox/2022 216` remains
the primary extracted KAM source for this repo; see
`references/kam_lecture_extraction.md`.

### Logistic Map, Renormalization, And Dissipative Chaos

- `RG logistic.pdf`
- `Logistic Map.pdf`

Use:

- Logistic-map bifurcation and period doubling.
- Renormalization-group viewpoint.
- Supplemental material for optional dissipative chaos section.

### Fluids And Hamiltonian Field Theory

- `97PHD_morrison.pdf`

Use:

- Morrison's Hamiltonian/noncanonical bracket viewpoint for fluids.
- Background for the repo's fluid mechanics chapter after Navier-Stokes.

### Core Mechanics Texts

- `Mathematical Methods of Classical Mechanics, 2nd ed.  - V.I. Arnold.djvu`
- `Mechanics 3rd ed. - L. Landau, E. Lifshitz.djvu`

Use:

- Arnold for symplectic/geometric mechanics and KAM context.
- Landau-Lifshitz for concise classical-mechanics derivations.

### Presentation File

- `p600_04r.ppt`

Use:

- Cataloged as a presentation source. Content not yet integrated because the
  present extraction priority is authored TeX and notebooks.

## Material Already Folded Into The Current Repo

Physics 151 material already integrated into the repo:

- `notes/tex/04_perturbation_kam_torus_breakdown.tex` includes the period-three
  standard-map calculation near `p=2pi/3`, following Problem Set 6.
- `notes/tex/07_deforming_body_gauge.tex` includes the deforming-body
  gauge equation `A Q + Q A = 2 Jhat` and the inertia-tensor solution from
  Problem Set 2.
- `PLANNING.md` references Physics 151 as a source for exercises, demos, and
  course architecture.

## Required Integrations Into Notes

These are not optional if the mechanics repo is meant to inherit the Physics
151 course quality.

1. Add a Hamilton-Jacobi chapter.

   The Physics 151 lecture outline explicitly includes Hamilton-Jacobi theory
   and the wave/Schrodinger analogy. The repo notes should derive Hamilton's
   principal function, the time-independent characteristic function, separation
   of variables, and the action-angle connection.

2. Expand the Kepler/central-force sequence.

   Integrate:

   - Kepler solution and Lenz vector.
   - Scattering.
   - Orbital precession from the `epsilon/r^3` perturbation in `kepler.nb`.
   - Schwarzschild-type circular-orbit stability from PS2 and `Schw.nb`.

3. Build a polished rigid-body module.

   Include:

   - Euler-angle convention.
   - Rotation matrices and `SO(3)`.
   - Angular velocities in body and space frames.
   - Inertia tensor.
   - Free top Euler equations.
   - Symmetric-top actions from PS4.
   - Hamiltonian on `T^*SO(3)`.

4. Build a Shapere-Wilczek deforming-body module.

   Include:

   - Shape space and `SO(3)` fiber.
   - Mechanical connection.
   - Gauge equation `AQ+QA=2Jhat`.
   - Helicopter rotor model.
   - Two-shell holonomy demo.
   - Falling cat interpretation.

5. Convert problem sets into repo exercises.

   Suggested sequence:

   - Set A: coordinate invariance, constraints, rolling, damped oscillator.
   - Set B: Hamiltonian construction and central-force stability.
   - Set C: rigid body and deforming-body gauge theory.
   - Set D: action-angle variables and invariant tori.
   - Set E: perturbation theory, Henon-Heiles, standard map.
   - Set F: numerical three-body and asteroid-belt resonance.

6. Port Mathematica demos to Python.

   Priority order:

   - Kepler perturbation.
   - Rigid-body Euler angles.
   - Two-shell holonomy.
   - Harmonic oscillator torus.
   - Liouville theorem.
   - Henon-Heiles Poincare section.
   - Standard map and homoclinic tangle.
   - Sun-Jupiter-asteroid belt.
   - Three-body ejection probability.
   - Logistic map and van der Pol oscillator as optional dissipative contrast.

7. Implement the highlighted three-body ejection-probability simulation.

   The Physics 151 sources provide two relevant seeds:

   - `3 body homework.nb`: direct Newtonian three-body integration from
     equilateral initial data.
   - `Demo 8 - asteroid belt.nb`: restricted Sun-Jupiter-asteroid dynamics
     with random initial asteroid phase and period scan.

   A repo-quality implementation should:

   - define a reproducible random seed;
   - choose mass parameters and nondimensional units explicitly;
   - sample asteroid initial semimajor axis or period and phase;
   - integrate with event detection;
   - define ejection by positive two-body energy, large radius threshold, or
     escape beyond a prescribed domain;
   - report confidence intervals for estimated ejection probability;
   - produce survival/ejection plots versus period ratio and resonance.

8. Add Henon-Heiles as the finite-dimensional Hamiltonian chaos bridge.

   It should sit between KAM theory and the asteroid problem because it gives
   a clean Poincare section and a standard transition from invariant curves to
   chaos.

9. Keep dissipative chaos separate.

   The van der Pol, forced pendulum, and logistic-map notebooks are valuable,
   but they should be marked as dissipative/non-Hamiltonian contrast rather
   than blended into the Hamiltonian KAM spine.

## Symbol And Assumption Checklist Captured From Physics 151

The final notes should define every one of these before use:

- `q_i`: generalized coordinates.
- `s_i`: transformed generalized coordinates.
- `L(q,qdot,t)`: Lagrangian.
- `p_i`: canonical momenta.
- `H(q,p,t)`: Hamiltonian.
- `theta,phi,psi`: Euler angles, with convention stated.
- `I_i`: principal moments of inertia.
- `J_i`: angular momentum components.
- `R`: rotation matrix or radius depending on context; avoid reusing without
  local definition.
- `Q`: shape tensor for deforming body.
- `A`: antisymmetric gauge/connection matrix.
- `tilde I`: inertia tensor in the shape/body frame.
- `tilde J`: internal angular-momentum-like vector.
- `hat J`: antisymmetric matrix associated with `tilde J`.
- `I`: action variable, not to be confused with moment of inertia.
- `theta`: angle variable in action-angle contexts.
- `omega(I)`: unperturbed frequency vector.
- `epsilon` or `lambda`: perturbation parameter.
- `K`: standard-map kick strength.
- `T_K`: standard map.
- `r_ij`: pair distance in the three-body problem.
- `k`: coupling constant or spring constant; define locally.

Assumptions to state explicitly in notes derived from this source:

- Coordinate transformations must be regular for Euler-Lagrange form invariance.
- Legendre transforms require a nondegenerate velocity Hessian.
- Rolling constraints may be holonomic or nonholonomic depending on geometry.
- Deforming-body reconstruction formulas assume an invertible inertia map on
  the shape under consideration.
- Action-angle coordinates are local and require regular compact invariant
  tori.
- KAM persistence requires nondegeneracy and Diophantine nonresonance
  hypotheses.
- Numerical demos require units, tolerances, integration time, and event
  definitions to be stated.

## Extraction Status

Authored Physics 151 TeX content has been extracted into this file at the level
needed to reconstruct polished lecture notes, exercises, and demos. Mathematica
notebook source has been mined for equations, parameters, and workflows. The
external reference shelf has been cataloged and source-mapped, with scanned or
compressed external papers treated as references rather than complete
transcriptions.
