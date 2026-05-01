# Page-Indexed Extraction: `KAM lecture.pdf`

Local source:

`/Users/xiyin/Dropbox/2022 216/KAM lecture.pdf`

This file is a page-by-page extraction of the handwritten Physics 216 KAM
lecture. It is intended as an audit map for the TeX notes. The goal is to
preserve every conceptual step, formula, example, warning, and figure idea from
the handwritten source, while leaving the polished exposition to the main notes.

## Page 1

- Opens "Phys 216: Part I, some classical physics" and "Classical mechanics".
- Sets up the contrast:
  - Lagrangian side: coordinates `q_i(t)`, `i=1,...,N`; `L=L(q_i,\dot q_i)`.
  - Euler-Lagrange equations:
    `d/dt (partial L / partial \dot q_i) - partial L / partial q_i = 0`.
  - Equivalence with stationary action: `delta S=0`, `S=int L dt`.
  - Hamiltonian side: phase-space coordinates `(q_i,p_i)`, `H=H(q_i,p_i)`.
  - Hamilton equations: `\dot q_i=partial H/partial p_i`,
    `\dot p_i=-partial H/partial q_i`.
  - Legendre transform relation:
    `H=p_i \dot q_i - L`, with `p_i=partial L/partial \dot q_i`.
- Important slogan: phase space is the same as the space of solutions.

## Page 2

- Main example: three-dimensional rigid body with fixed center of mass.
- Number of degrees of freedom: `N=3`.
- Attach three orthonormal body axes `\hat e_1,\hat e_2,\hat e_3` to the body.
- The `3 x 3` matrix
  `R=(\hat e_1 \ \hat e_2 \ \hat e_3)` lies in `SO(3)`.
- Matrix entries: `R_{ia}=(\hat e_a)_i`.
- Configuration space is `SO(3)`; it can be parametrized locally by three
  independent coordinates, for example Euler angles.
- Angular velocity `\omega` is defined by
  `d\hat e_a/dt = \omega x \hat e_a`.
- Equivalent component form:
  `d R_{ia}/dt = epsilon_{ijk} omega_j R_{ka}`.
- Notes that one can choose the frame in which the inertia tensor is diagonal.

## Page 3

- With principal axes, the Lagrangian is
  `L = 1/2 sum_{a=1}^3 I_a (\hat e_a . \omega)^2`.
- Angular momentum:
  `J_i = partial L / partial omega_i
       = sum_a I_a (\hat e_a)_i (\hat e_a . \omega)`.
- Hamiltonian in body components:
  `H=sum_a \tilde J_a^2/(2 I_a)`,
  where `\tilde J_a=\hat e_a . J` and `\tilde\omega_a=\hat e_a . \omega`.
- Warning: angular momenta `\tilde J_a` or `J_i` are not canonical momenta.
- In particular, `\tilde\omega_a` are not time derivatives of coordinates on
  configuration space.
- Begins a concrete Euler-angle coordinate system on `SO(3)`:
  `(phi,theta,psi)`.
- Gives explicit formulas for `\hat e_1` and `\hat e_2`:
  - `\hat e_1=(cos phi cos psi - sin phi cos theta sin psi,
               sin phi cos psi + cos phi cos theta sin psi,
               sin theta sin psi)`.
  - `\hat e_2=(-cos phi sin psi - sin phi cos theta cos psi,
               -sin phi sin psi + cos phi cos theta cos psi,
               sin theta cos psi)`.

## Page 4

- Completes the Euler-angle basis with
  `\hat e_3=(sin phi sin theta, -cos phi sin theta, cos theta)`.
- Angle ranges:
  `phi in [0,2pi]`, `theta in [0,pi]`, `psi in [0,2pi]`.
- Aside: a natural line element on configuration space:
  `ds^2=-1/2 tr(R^{-1} dR)^2`.
- In Euler angles:
  `ds^2=dphi^2+dtheta^2+dpsi^2+2 dphi dpsi cos theta`.
- Change variables:
  `phi=(xi_1+xi_2)/2`, `psi=(xi_1-xi_2)/2`.
- Then:
  `ds^2=dtheta^2+cos^2(theta/2) dxi_1^2
       +sin^2(theta/2) dxi_2^2`.
- Figure idea: as `theta` runs from `0` to `pi`, one circle shrinks at one end
  and the other circle shrinks at the other end; solid tori are glued.
- Conclusion: this gives `S^3`, with an identification leading to
  `SO(3) ~= S^3/Z_2`.

## Page 5

- The remaining identification is
  `(xi_1,xi_2) ~ (xi_1+2pi, xi_2+2pi)`.
- Therefore `SO(3) ~= S^3/Z_2`.
- Summary for the rigid body:
  - fixed center of mass;
  - configuration space `M=SO(3)`;
  - one may use local coordinates `q_i`, `i=1,2,3`, for example Euler angles
    `(phi,theta,psi)`;
  - such coordinates are valid only in nondegenerate patches.
- Warning: Euler-angle coordinates are singular at `theta=0,pi`, even though
  `SO(3)` is a homogeneous smooth space.
- Introduces the question: what is phase space?
- Canonical momenta are related to coordinates and velocities by
  `p_i=partial L/partial \dot q_i`.

## Page 6

- Under a coordinate change `q_i -> \tilde q_i(q)`, momenta transform by
  `\tilde p_i = partial L/partial \dot{\tilde q}_i`.
- Chain-rule derivation:
  `\tilde p_i=(partial q_j/partial \tilde q_i) p_j`.
- Recalls tangent vectors on `M`:
  `v=v_i partial/partial q_i`.
- Under a coordinate change:
  `\tilde v_i=(partial \tilde q_i/partial q_j) v_j`.
- Hence `p_i` transforms as a cotangent vector, or one-form.
- The one-form `p_i dq_i` is invariant under coordinate redefinition.
- Phase space is the cotangent bundle `T^*M`.
- For the fixed-COM rigid body, phase space is `T^*SO(3)`.

## Page 7

- Key "obvious but curious fact":
  for any nondegenerate coordinate choice `q_i` on the rigid-body configuration
  space, there is a nondegenerate linear relation between canonical momenta
  `p_i` and body angular momenta `\tilde J_a`.
- Relation:
  `p_i = sum_{a=1}^3 f_{ia}(q) \tilde J_a`,
  where `(f_{ia})` is a nondegenerate `3 x 3` matrix.
- The body angular momenta `\tilde J_a` can be viewed as linear coordinates on
  the fiber of `T^*SO(3)`.
- They are not canonical coordinates; for example `f_{ia}` cannot be constant.
- This is the statement that `T^*SO(3)` admits a global trivialization and is
  in this sense a trivial vector bundle.

## Page 8

- Begins Poisson structure on phase space.
- For functions `f,g` on phase space, canonical Poisson bracket:
  `{f,g}=sum_i (partial f/partial p_i partial g/partial q_i
               - partial f/partial q_i partial g/partial p_i)`.
- Equations of motion:
  `df/dt={H,f}`, assuming no explicit time dependence in `f`.
- Poisson structure captures the whole content of splitting phase-space
  coordinates into positions and momenta, but treats them on equal footing.
- Introduces symplectic structure:
  `omega = sum_i dq_i wedge dp_i`.
- This can be passed to an arbitrary coordinate system.

## Page 9

- Let arbitrary phase-space coordinates be `x_m`, `m=1,...,2N`.
- Write a general symplectic form
  `omega = 1/2 omega_{mn} dx_m wedge dx_n`.
- Conditions:
  - `d omega=0`;
  - `omega_{mn}` is a nondegenerate antisymmetric matrix.
- General Poisson bracket:
  `{f,g}=(omega^{-1})^{mn} partial f/partial x^m partial g/partial x^n`.
- Canonical example with `x_m=(p_i,q_i)`:
  `omega_{mn} = [[0,-I_N],[I_N,0]]`,
  `omega^{-1}_{mn} = [[0,I_N],[-I_N,0]]`.
- Under coordinate change `x^m -> \tilde x^m`, one verifies tensor
  transformation of `omega`.

## Page 10

- Completes the coordinate-transformation statement:
  the same Poisson bracket formula holds in any coordinate system.
- Begins canonical transformations.
- A canonical transformation `(p_i,q_i) -> (P_i,Q_i)` preserves the canonical
  Poisson structure:
  `{f,g}_{p,q} = {f,g}_{P,Q}`.
- Equivalently, it preserves the canonical symplectic form:
  `omega=sum_i dp_i wedge dq_i = sum_i dP_i wedge dQ_i`.
- A useful way to construct canonical transformations is a generating function
  `F(P,q)`, with `P` new and `q` old.

## Page 11

- Imposes:
  `Q_i = partial F/partial P_i |_{q}`,
  `p_i = partial F/partial q_i |_{P}`.
- One then solves `(P,Q)` in terms of `(p,q)`.
- Checks the symplectic form:
  `dP_i wedge dQ_i =
    dP_i wedge (partial^2 F/partial P_i partial q_j dq_j)
    + dP_i wedge (partial^2 F/partial P_i partial P_j dP_j)`.
- The second term vanishes by symmetry of second derivatives and antisymmetry
  of wedge product.
- Similarly:
  `dp_j wedge dq_j =
    (partial^2 F/partial P_i partial q_j dP_i) wedge dq_j
    + (partial^2 F/partial q_i partial q_j dq_i) wedge dq_j`,
  and the last term vanishes.
- Therefore the canonical form is preserved.

## Page 12

- Begins integrable systems.
- Hamiltonian system with `N` degrees of freedom.
- Suppose there are `N` independent mutually Poisson-commuting functions on
  phase space:
  `F_i(p,q)`, `i=1,...,N`, with `{F_i,F_j}=0`.
- One of these functions is `H` itself.
- Then the Hamiltonian system is called integrable.
- Examples:
  - any Hamiltonian system with one degree of freedom is integrable;
  - 3D rigid body with fixed COM.
- For the rigid body, `H,J_i` do not all Poisson commute, but
  `H,J_3,J^2` are mutually Poisson commuting, hence the system is integrable.

## Page 13

- Consequence of integrability:
  a solution to the equations of motion lies on
  `M_N(f_1,...,f_N) = {(p,q) | F_i(p,q)=f_i, i=1,...,N}`.
- This is an `N`-dimensional submanifold.
- Normal vectors to `M_N`:
  `(n_i)_a = partial F_i/partial x_a`, `a=1,...,2N`.
- Tangent vectors to `M_N` are constructed using the symplectic inverse:
  `(t_i)^a = (omega^{-1})^{ab}(n_i)_b`.
- To see tangency, for `t_i=t_i^a partial/partial x^a`,
  `t_i . f = t_i^a partial f/partial x^a
             = (omega^{-1})^{ab} partial f/partial x^a partial F_i/partial x^b
             = {f,F_i}`.
- In particular, `t_i . F_j = 0` for all `j`, so `t_i` are tangent to `M_N`.

## Page 14

- Shows the tangent fields commute.
- Computes:
  `t_i . n_j = (omega^{-1})^{ab}(n_i)_b(n_j)_a
             = {F_j,F_i}=0`,
  so `n_j` are normal to `M_N`.
- As vector fields on `M_N`,
  `[t_i,t_j].f = t_i(t_j.f)-t_j(t_i.f)
               = {{f,F_j},F_i}-(i<->j)`.
- Jacobi identity plus integrability gives zero:
  `{{F_i,F_j},f}=0`.
- Therefore `t_1,...,t_N` are independent commuting vector fields on `M_N`.
- For a general vector field `v^a(x)`, define trajectories by
  `dx^a(s)/ds=v^a(x(s))`.
- This is "transport by vector field".

## Page 15

- Flow of a vector field maps `x^a(0)` to `x^a(s)`, determined uniquely by the
  initial point, vector field, and flow parameter.
- Commuting vector fields give commuting transports.
- Assuming `t_1,...,t_N` are also linearly independent at every point on
  `M_N`, the "grid" defines local coordinates `(s^1,...,s^N)` on `M_N` such
  that
  `t_i^a(x)=partial x^a/partial s^i`, i.e. `t_i=partial/partial s^i`.
- Hence `M_N ~= R^N/Lambda`, where `Lambda` is a discrete group of
  translations.

## Page 16

- If `M_N` is compact, for example if the fixed-energy region `H=E_0` is
  bounded, then
  `M_N ~= T^N`, an `N`-dimensional torus.
- Rigid-body example:
  `H=sum_a \tilde J_a^2/(2I_a)`.
  `J^2=sum_a \tilde J_a^2`.
  `J_3=sum_a (\hat e_a)_3 \tilde J_a = R_{3a}\tilde J_a`.
- `\tilde J_a` are noncanonical coordinates on the fiber of `T^*SO(3)`.
- The torus `M_3` can be visualized geometrically.

## Page 17

- Values of `H` and `J^2` restrict the cotangent-space coordinates
  `\tilde J_a` to the intersection of a sphere and an ellipsoid.
- Figure: sphere `J^2=const`; ellipsoid slice `H=const`; their intersection is
  a closed curve.
- Given `\tilde J_a` on this curve, the relation
  `J_3=R_{3a}\tilde J_a=const`
  restricts `R_{3a}` to lie on the intersection of the unit sphere `S^2` with a
  plane.
- Figure: for fixed `R_{3a}` there is a circle worth of `R_{1a},R_{2a}`.

## Page 18

- Completes the rigid-body torus visualization.
- `M_3` consists of a circle fibered over a circle, and also over the other
  closed curves drawn in the momentum-space picture.
- The page is mainly a diagrammatic summary of the fibration structure.

## Page 19

- Introduces invariant torus and action variables.
- `M_N`: `F_i(p,q)=f_i` constant, `{F_i,F_j}=0`.
- Symplectic form on the torus:
  `omega=dq_i wedge dp_i`.
- Substitute `p_i=p_i(q,F)` on fixed `F`:
  `omega=dq_i wedge ((partial p_i/partial q_j)|_F dq_j
                    +(partial p_i/partial F_j)|_q dF_j)`.
- Claim:
  `(partial p_i/partial q_j)|_F = (partial p_j/partial q_i)|_F`.
- Therefore `omega=(partial p_i/partial F_j)|_q dq_i wedge dF_j`.
- In particular, `omega|_{M_N}=0` because `dF=0` on `M_N`.

## Page 20

- Proof of the claim in page 19.
- Differentiate the constraint relation:
  `0 = partial/partial q_i F_k(p(F,q),q)|_F`.
- This gives
  `A_{kj} M_{ji} + B_{ki}=0`,
  where
  `A_{kj}=partial F_k/partial p_j|_q`,
  `M_{ji}=partial p_j/partial q_i|_F`,
  `B_{ki}=partial F_k/partial q_i|_p`.
- Hence `A M + B=0`, so `M=-A^{-1}B`.
- Since `{F_i,F_j}=0`, one obtains
  `A B^T - B A^T=0`.
- Therefore `A^{-1}B = B^T(A^T)^{-1} = (A^{-1}B)^T`, so `M=M^T`.
- Claim proved.

## Page 21

- Defines action variables:
  `I_j = (1/2pi) integral_{gamma_j} p . dq`.
- Figure: cycles `gamma_1,gamma_2` on `M_N`.
- Action variables are invariant under deformation of `gamma_j` along `M_N`.
- If two cycles bound a region on the torus, then
  `integral_C p dq = integral_D dp wedge dq = 0`
  because `omega|_{M_N}=0`.
- The action variables `(I_1,...,I_N)` are functions on phase space; they label
  `M_N` and can replace `(F_1,...,F_N)`.
- Begins: the `I_j` may also be viewed as a new set of canonical momenta.

## Page 22

- To find conjugate coordinates `(theta_1,...,theta_N)`, construct locally a
  generating function `S(I_i,q_i)`, with `I` new and `q` old.
- Equations:
  `p_i = partial S/partial q_i |_{I}`,
  `theta_i = partial S/partial I_i |_{q}`.
- The `p_i` equation is a set of PDEs to be solved.
- Since `I_i=I_i(p,q)`, invert to get known functions `p_i(I,q)`.
- Solve:
  `partial S(I,q)/partial q_i = p_i(I,q)`.
- This is integrable if the compatibility condition holds:
  `partial p_i/partial q_j|_I = partial p_j/partial q_i|_I`.

## Page 23

- Notes the compatibility condition has already been checked.
- `(theta_i,I_i)` are "angle-action" variables.
- Around a cycle `gamma_j`:
  `integral_{gamma_j} p . dq = 2pi I_j`.
- Since `p_i=partial S/partial q_i`, this is
  `integral_{gamma_j} dS`.
- `S` is locally defined; going around `M_N` along `gamma_j`, `S` jumps by
  `2pi I_j`.
- Thus `theta_i` jumps by
  `Delta_{gamma_j} theta_i
    = Delta_{gamma_j}(partial S/partial I_i|_q)
    = partial/partial I_i (Delta_{gamma_j} S)`.

## Page 24

- Completes the jump calculation:
  `Delta_{gamma_j} theta_i=2pi delta_{ij}`.
- Therefore `theta_i ~ theta_i+2pi` are angle coordinates on `M_N`.
- In action-angle variables, equations of motion are:
  `I_i=const`,
  `\dot theta_i = partial H/partial I_i = omega_i(I)`, a constant on each torus.
- Figure: straight-line flow on a square torus.

## Page 25

- Begins perturbation of integrable systems.
- Hamiltonian:
  `H=H_0 + epsilon H_1`,
  where `H_0` is integrable, `H_1` is generic, and `0<epsilon<<1`.
- Question: what happens to invariant tori?
- Landau expectation: system remains integrable; phase space filled by
  invariant tori; one only needs to find new integrals of motion.
- Fermi expectation: generic `H_1` breaks integrability completely; a typical
  orbit wanders through all of phase space; "ergodic".
- Both expectations were wrong.

## Page 26

- Fermi, Pasta, Ulam, Tsingou (1953): numerical simulation disproves the
  ergodic hypothesis.
- Kolmogorov, Arnold, Moser (1954--1963):
  - for small `epsilon`, "most" orbits remain confined to tori;
  - a small amount of orbits not confined to tori wander chaotically.
- Why might one expect the perturbed system to remain integrable?
- Begin with angle-action variables `(theta_i,I_i)` for `H_0`; then
  `H_0=H_0(I)`.
- Perturbed Hamiltonian is `H(I,theta)=H_0(I)+epsilon H_1(I,theta)`.

## Page 27

- Asks whether there is a new action-only Hamiltonian `H'(I')` for some new
  action variables `I_i'`.
- To find a canonical transformation `(I,theta) -> (I',theta')`, seek a
  generating function `S(I',theta)`:
  `I_i=partial S(I',theta)/partial theta_i`,
  `theta_i'=partial S(I',theta)/partial I_i'`.
- Require
  `H'(I')=H(I,theta)
          =H(partial S/partial theta |_{I'}, theta)`
  for some `H'`.
- This is canonical perturbation theory.

## Page 28

- Assume an expansion:
  `S=S_0+epsilon S_1+epsilon^2 S_2+...`.
- `S_0` generates the identity transformation:
  `S_0=I_i' theta_i`.
- Then
  `I=partial S/partial theta
    =I' + epsilon partial S_1/partial theta + ...`.
- Expanding:
  `H'(I')=H(I,theta)
    =H(I' + epsilon partial S_1/partial theta + ..., theta)`
  `=H_0(I') + epsilon (partial S_1/partial theta . partial H_0(I')/partial I')
    + epsilon H_1(I',theta)+O(epsilon^2)`.
- To satisfy the relation at order `epsilon`, need
  `(partial H_0/partial I') . (partial S_1/partial theta)
   = -H_1(I',theta)+f_1(I')`.

## Page 29

- Let `omega_0(I')=partial H_0/partial I'`; it is independent of `theta`.
- Since `theta_i~theta_i+2pi`, `S_1(I',theta)` is periodic in every `theta_i`.
- Therefore
  `<partial S/partial theta>_theta=0`.
- Hence
  `f_1(I')=<H_1(I',theta)>_theta`.
- Solve `S_1` using Fourier expansion:
  `H_1(I',theta)=sum_{k in Z^N} H_{1k}(I') e^{i k.theta}`.
  `S_1(I',theta)=sum_{k in Z^N} S_{1k}(I') e^{i k.theta}`.
- For `k != 0`:
  `S_{1k}(I')= i H_{1k}(I')/(k . omega_0(I'))`.

## Page 30

- One may set the zero mode `S_{10}=0`.
- Then:
  `S_1(I',theta)
    = i sum_{k != 0} H_{1k}(I') e^{i k.theta}/(k . omega_0(I'))`.
- Asks: is this well-defined?
- Problem if `k . omega_0(I')=0` for some nonzero `k`.
- Equivalent to `k . theta(t)=const`: orbit lies on an `(N-1)`-dimensional
  subtorus.
- These are "resonance tori".
- Assuming `omega_0(I')` depends nontrivially on `I'`, resonance tori are dense
  in phase space.
- Worse: even if `k . omega_0(I') != 0` for every integer `k`, the sum over
  `k` may diverge.
- Question: how do the Fourier coefficients `H_{1k}(I')` behave at large `|k|`?

## Page 31

- To estimate Fourier coefficients, start with one angle variable:
  `f(theta)=sum_{k in Z} f_k e^{ik theta}`.
- Assume `f(theta)` is real analytic and can be analytically continued to a
  neighborhood of the real line.
- Fourier coefficient:
  `f_k=(1/2pi) int_0^{2pi} f(theta)e^{-ik theta} dtheta`.
- Deform contour to `eta=theta-i epsilon`:
  `f_k=(1/2pi) int_{0-i epsilon}^{2pi-i epsilon}
        f(eta)e^{-ik eta} d eta`.
- For `k>0`, `epsilon>0`,
  `|f_k| <= |f(theta-i epsilon)|_max e^{-k epsilon}`.
- Thus Fourier coefficients are exponentially suppressed for large positive
  `k`; same conclusion for `k<0` with `eta=theta+i epsilon`.

## Page 32

- Examples:
  - `sum_{k=1}^\infty sin(k theta)/k`: Fourier coefficients are not
    exponentially suppressed; graph has a jump discontinuity, not real
    analytic.
  - `sum_{k=1}^\infty cos(k theta)/k^2 = 1/4(theta-pi)^2 - pi^2/12` for
    `|theta|<2pi`: also not analytic at periodic endpoints; coefficients decay
    only polynomially.
  - Real-analytic example:
    `sum_{k=-infty}^{infty} cos(k theta) e^{-k^2/2}`; related to an elliptic
    theta function; coefficients rapidly suppressed.

## Page 33

- Therefore, for `H_1(I,theta)` real analytic in `theta`, the coefficients
  `H_{1k}` are exponentially suppressed at large `k`.
- Asks about convergence of
  `S_1 = i sum_{k != 0} H_{1k} e^{ik.theta}/(k . omega_0)`.
- Given `omega_0(I')=(omega_1,...,omega_N)`, if
  `|k . omega_0|=|k_1 omega_1+...+k_N omega_N|
    >= alpha/(|k_1|+...+|k_N|)^tau`
  for some `alpha>0`, fixed `tau`, and all nonzero `k`, then the series
  converges.
- This gives a well-defined solution for `S_1`.

## Page 34

- This first-order construction does not work for resonant tori:
  if `k . omega_0=0` for some nonzero integer vector `k`.
- With generic `I'` dependence in `omega_0(I')`, resonant tori form a
  zero-measure subset of phase space, but they are dense.
- Therefore a randomly chosen torus has zero probability of exact resonance.
- What about generic irrational `omega_0`?
- For simplicity, take `N=2`.
- Ask whether there exist `alpha>0`, `tau` such that
  `|k_1 omega_1+k_2 omega_2|
    >= alpha/(|k_1|+|k_2|)^tau`.
- Equivalently for `x=omega_1/omega_2`, with positive integers `p,q`, one is
  led to a rational-approximation condition.

## Page 35

- The rational-approximation condition is written as
  `|x-p/q| >= \tilde A/(p+q)^{tau+1}`,
  or more simply
  `|x-p/q| >= A/q^{tau+1}` for `p~x q`.
- Failure occurs only if a rational `p/q` closely approximates `x`.
- Question: how close to rational is the irrational number `x`?
- Example: `x=sqrt(2)`, solving `f(x)=x^2-2=0`.
- Approximate `x` by `p/q=x-epsilon`.
- Evaluate:
  `f(p/q)=p^2/q^2 - 2 = (p^2-2q^2)/q^2`.

## Page 36

- Since `p^2-2q^2=N` for some nonzero integer `N`,
  `|N|>=1`.
- Linearizing:
  `f(x)-epsilon f'(x)+O(epsilon^2)`,
  with `f(x)=0`, `f'(x)=2x=2sqrt(2)`.
- Therefore
  `epsilon ~= -(1/(2sqrt(2))) N/q^2`.
- Hence `|epsilon| > A/q^2` for some `A>0`.
- This works for `tau=1`.
- More generally, if `x` solves an irreducible polynomial
  `x^N+c_1 x^{N-1}+...+c_N=0`, with rational coefficients, then a similar
  algebraic-number estimate holds.

## Page 37

- Conclusion for algebraic numbers:
  `|x-p/q| > A/q^N` for some `A>0`.
- Gives a counterexample to any fixed Diophantine-type lower bound:
  `x=sum_{n=0}^\infty 1/2^{n!}`.
- For every `n`, there exists `m` such that
  `|x - m/2^{n!}| <= 2/2^{(n+1)!}`.
- This is too well approximated by rationals.
- However, one does not need to exclude much:
  for some `tau` and `A>0`,
  `|x-p/q| > A/q^{tau+1}` holds for "most" real numbers `x`.
- Reformulates in the general frequency setting:
  ask whether there exist `alpha>0`, `tau` such that the Diophantine bound
  holds.

## Page 38

- States the general Diophantine condition:
  `|k . omega| >= alpha/(|k_1|+...+|k_N|)^tau`
  in the space of possible values of `omega`.
- Let `R_k` be the bad set where this condition fails:
  `|k . omega| < alpha/(|k_1|+...+|k_N|)^tau`.
- Figure: `R_k` is a thin slab around a resonant hyperplane in a bounded domain
  `Omega` in frequency space.
- The slab thickness scales like
  `alpha const/(|k_1|+...+|k_N|)^{tau+1}`.
- Therefore the total excluded volume satisfies
  `sum_{k != 0} vol(R_k cap Omega) ~ O(alpha)`,
  and the sum converges if `tau+1>N`.

## Page 39

- Let `R = union_{k != 0} R_k`.
- The volume `vol(R cap Omega)` can be made small if `alpha` is sufficiently
  small.
- `Omega \ R` is the set of frequencies satisfying the small-divisor condition
  for all nonzero integer vectors.
- It is almost all of `Omega` in measure, provided `alpha` is small and
  `tau>N-1`.
- For `omega_0(I') in Omega \ R`, the first-order expression for `S_1` is
  well-defined.
- Assuming `omega_0(I')` is nondegenerate as a function of `I'`, most invariant
  tori are slightly deformed but preserved.

## Page 40

- Caution: at next order in `epsilon`, the coordinate changes are
  `I=partial S/partial theta
     =I' + epsilon partial S_1/partial theta + ...`,
  `theta'=partial S/partial I'
     =theta + epsilon partial S_1/partial I' + ...`.
- These corrections are `O(epsilon/alpha)`, so they must be small.
- KAM theorem stated:
  there exists `delta>0` such that for `|epsilon| < delta alpha^2`, the
  invariant tori of `H_0(I)` with
  `omega_0 in R_alpha =
    {omega : |k . omega| >= alpha/(sum |k_i|)^tau,
             for all k != 0}`
  persist, only slightly deformed.
- These tori fill phase space up to `O(alpha)` measure.
- Reference note in the source: for more details, see arXiv:0908.2234.

## Page 41

- Begins the question: how does integrability/invariant-torus structure break
  down?
- Takes the `N=2` case.
- Start from integrable `H_0(I_1,I_2)` with angle-action variables
  `(theta_1,theta_2,I_1,I_2)`.
- Work at fixed energy `H=E`.
- Choose a Poincare section `S`, for example `theta_2` fixed.
- Starting from `x in S`, the orbit through `x` next intersects `S` at `T(x)`.
- This defines the Poincare map `T:S -> S`.

## Page 42

- Unperturbed equations:
  `\dot theta_1=omega_1`, `\dot theta_2=omega_2`.
- Going around `theta_2 -> theta_2+2pi` takes
  `Delta t = 2pi/omega_2`.
- The Poincare map twists `theta_1` by
  `Delta theta_1 = 2pi omega_1/omega_2`.
- Consider a resonant torus with `omega_1/omega_2 in Q`; example
  `omega_1/omega_2=1/3`.
- Then `T: theta_1 -> theta_1+2pi/3`; hence `T^3=id`.
- Study the action of `T^3` on nearby tori.
- Without loss, assume `T^3` rotates in opposite directions on curves
  `C_-` and `C_+` surrounding the resonant curve `C`.

## Page 43

- Add perturbation `H=H_0+epsilon H_1`.
- The perturbed Poincare map `T_epsilon` is defined as before, regardless of
  whether invariant tori exist.
- Near `C cap S`, `T_epsilon^3` is close to the identity.
- Local form at fixed energy:
  `T_epsilon^3:(I_1,theta_1) ->
    (I_1+f_epsilon(I_1,theta_1),
     theta_1+g_epsilon(I_1,theta_1))`.
- For small `epsilon`, `T_epsilon^3` still rotates one way on `C_-` and the
  opposite way on `C_+`.
- Therefore there exists a curve `C'` between `C_-` and `C_+` where
  `g_epsilon(I_1,theta_1)=0`, i.e. no twist.

## Page 44

- On the other hand, `T_epsilon` preserves area.
- Formula:
  `int_gamma p . dq = - int_{D_gamma} omega`
  (Liouville's theorem).
- If `f_epsilon(I_1,theta_1) != 0` on `C'`, area preservation implies
  `f_epsilon` has at least a pair of zeros on `C'`.
- These zeros are fixed points of `T_epsilon^3`.
- There is more: if `x` is a fixed point of `T_epsilon^3`, so is
  `T_epsilon(x)`.
- Thus one expects 6 fixed points in the period-three resonance example.

## Page 45

- Diagrammatic conclusion of resonance breakup.
- The period-three resonant curve breaks into a pattern with:
  - periodic points of `T_epsilon^3`;
  - elliptic points and surrounding island structures;
  - hyperbolic points;
  - chaotic layers near hyperbolic structures;
  - persistent tori outside the resonant layer;
  - possible "new tori" or island tori around elliptic points.
- Figure shows the qualitative Poincare-section picture:
  a deformed annular region, elliptic islands, hyperbolic/chaotic separatrix
  behavior, and surrounding persistent tori.
