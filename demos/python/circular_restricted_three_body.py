#!/usr/bin/env python3
"""Circular restricted three-body problem in rotating barycentric units.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

The primaries have total mass one, separation one, and angular velocity one.
The mass parameter mu is the mass of the smaller primary.  The larger primary
is fixed at (-mu, 0) and the smaller primary is fixed at (1 - mu, 0) in the
rotating frame.

The script prints the five Lagrange points, integrates a sample test-particle
trajectory, and reports the drift in the Jacobi integral.  With --plot it also
draws the trajectory and the zero-velocity curve for the particle's Jacobi
constant.

The integrator is classical fourth-order Runge-Kutta.  It is intentionally
simple for classroom inspection, but it is not symplectic and it does not
preserve the Jacobi integral exactly.  Use the printed Jacobi drift as a
short-time accuracy diagnostic; long-time transport studies should compare
against a structure-preserving method such as an implicit midpoint rule or a
problem-specific splitting integrator.
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np


M_SUN = 1.0
M_JUPITER = 9.543e-4
SUN_JUPITER_MU = M_JUPITER / (M_SUN + M_JUPITER)
TWOPI = 2.0 * math.pi


@dataclass(frozen=True)
class LagrangePoints:
    l1: float
    l2: float
    l3: float
    l4: tuple[float, float]
    l5: tuple[float, float]


def validate_mu(mu: float) -> None:
    if not (0.0 < mu < 0.5):
        raise ValueError("mu must satisfy 0 < mu < 1/2")


def primary_positions(mu: float) -> tuple[np.ndarray, np.ndarray]:
    validate_mu(mu)
    return np.array([-mu, 0.0]), np.array([1.0 - mu, 0.0])


def distances(x: float | np.ndarray, y: float | np.ndarray, mu: float) -> tuple[np.ndarray, np.ndarray]:
    """Distances to the large and small primaries."""
    validate_mu(mu)
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    r1 = np.sqrt((x_arr + mu) ** 2 + y_arr * y_arr)
    r2 = np.sqrt((x_arr - 1.0 + mu) ** 2 + y_arr * y_arr)
    return r1, r2


def effective_potential(x: float | np.ndarray, y: float | np.ndarray, mu: float) -> np.ndarray:
    r"""Return Omega = (x^2+y^2)/2 + (1-mu)/r1 + mu/r2."""
    r1, r2 = distances(x, y, mu)
    return 0.5 * (np.asarray(x) ** 2 + np.asarray(y) ** 2) + (1.0 - mu) / r1 + mu / r2


def grad_effective_potential(x: float | np.ndarray, y: float | np.ndarray, mu: float) -> np.ndarray:
    """Return grad Omega as an array whose final axis is (x, y)."""
    r1, r2 = distances(x, y, mu)
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    inv_r1_3 = 1.0 / np.maximum(r1**3, 1.0e-18)
    inv_r2_3 = 1.0 / np.maximum(r2**3, 1.0e-18)
    ox = x_arr - (1.0 - mu) * (x_arr + mu) * inv_r1_3 - mu * (x_arr - 1.0 + mu) * inv_r2_3
    oy = y_arr - (1.0 - mu) * y_arr * inv_r1_3 - mu * y_arr * inv_r2_3
    return np.stack((ox, oy), axis=-1)


def rhs(_t: float, state: np.ndarray, mu: float) -> np.ndarray:
    """Rotating-frame CR3BP vector field for state (x, y, vx, vy)."""
    x, y, vx, vy = state
    ox, oy = grad_effective_potential(x, y, mu)
    return np.array([vx, vy, 2.0 * vy + ox, -2.0 * vx + oy])


def jacobi_constant(state: np.ndarray, mu: float) -> float | np.ndarray:
    state = np.asarray(state, dtype=float)
    x = state[..., 0]
    y = state[..., 1]
    vx = state[..., 2]
    vy = state[..., 3]
    return 2.0 * effective_potential(x, y, mu) - vx * vx - vy * vy


def rk4_step(t: float, state: np.ndarray, dt: float, mu: float) -> np.ndarray:
    k1 = rhs(t, state, mu)
    k2 = rhs(t + 0.5 * dt, state + 0.5 * dt * k1, mu)
    k3 = rhs(t + 0.5 * dt, state + 0.5 * dt * k2, mu)
    k4 = rhs(t + dt, state + dt * k3, mu)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate(mu: float, state0: np.ndarray, dt: float, periods: float) -> tuple[np.ndarray, np.ndarray]:
    """Integrate the rotating-frame CR3BP equations with classical RK4.

    RK4 is intentionally transparent for lecture use, but it is not symplectic
    and does not preserve the Jacobi integral exactly. Long transport claims
    should therefore be checked against the printed Jacobi drift and, for
    research use, a structure-aware integrator.
    """

    validate_mu(mu)
    if dt <= 0.0:
        raise ValueError("dt must be positive")
    if periods < 0.0:
        raise ValueError("periods must be nonnegative")
    steps = int(round(periods * TWOPI / dt))
    time = np.linspace(0.0, steps * dt, steps + 1)
    states = np.empty((steps + 1, 4), dtype=float)
    states[0] = np.asarray(state0, dtype=float)
    for i in range(steps):
        states[i + 1] = rk4_step(time[i], states[i], dt, mu)
    return time, states


def collinear_equation(x: float, mu: float) -> float:
    return float(grad_effective_potential(x, 0.0, mu)[0])


def bisect_root(func, lo: float, hi: float, iterations: int = 100) -> float:
    flo = func(lo)
    fhi = func(hi)
    if flo == 0.0:
        return lo
    if fhi == 0.0:
        return hi
    if flo * fhi > 0.0:
        raise ValueError(f"root is not bracketed on [{lo}, {hi}]")
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        fmid = func(mid)
        if flo * fmid <= 0.0:
            hi = mid
            fhi = fmid
        else:
            lo = mid
            flo = fmid
    return 0.5 * (lo + hi)


def lagrange_points(mu: float) -> LagrangePoints:
    validate_mu(mu)
    eps = 1.0e-8
    left_primary = -mu
    right_primary = 1.0 - mu
    f = lambda x: collinear_equation(x, mu)
    l1 = bisect_root(f, left_primary + eps, right_primary - eps)
    l2 = bisect_root(f, right_primary + eps, 2.5)
    l3 = bisect_root(f, -2.5, left_primary - eps)
    l4 = (0.5 - mu, math.sqrt(3.0) / 2.0)
    l5 = (0.5 - mu, -math.sqrt(3.0) / 2.0)
    return LagrangePoints(l1=l1, l2=l2, l3=l3, l4=l4, l5=l5)


def initial_state(kind: str, mu: float) -> np.ndarray:
    points = lagrange_points(mu)
    if kind == "l4":
        x = points.l4[0] + 0.02
        y = points.l4[1]
        return np.array([x, y, 0.0, 0.0])
    if kind == "l1":
        return np.array([points.l1 - 0.02, 0.02, 0.0, -0.08])
    if kind == "asteroid":
        # A rough rotating-frame asteroid-belt initial condition interior to Jupiter.
        x = 0.55
        y = 0.0
        inertial_speed = math.sqrt((1.0 - mu) / abs(x + mu))
        rotating_speed = inertial_speed - x
        return np.array([x, y, 0.0, rotating_speed])
    raise ValueError(f"unknown initial state kind {kind!r}")


def save_plot(path: Path, time: np.ndarray, states: np.ndarray, mu: float) -> None:
    os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache")))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    c = float(jacobi_constant(states[0], mu))
    points = lagrange_points(mu)
    p1, p2 = primary_positions(mu)

    grid_x = np.linspace(-1.55, 1.55, 400)
    grid_y = np.linspace(-1.25, 1.25, 320)
    xg, yg = np.meshgrid(grid_x, grid_y)
    zvc = 2.0 * effective_potential(xg, yg, mu)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.contour(xg, yg, zvc, levels=[c], colors=["tab:gray"], linewidths=1.2)
    ax.plot(states[:, 0], states[:, 1], color="tab:blue", linewidth=1.0, label="trajectory")
    ax.scatter([states[0, 0]], [states[0, 1]], color="tab:green", s=30, zorder=4, label="start")
    ax.scatter([p1[0], p2[0]], [0.0, 0.0], color=["gold", "tab:orange"], s=[90, 45], zorder=5)
    ax.scatter(
        [points.l1, points.l2, points.l3, points.l4[0], points.l5[0]],
        [0.0, 0.0, 0.0, points.l4[1], points.l5[1]],
        color="tab:red",
        marker="x",
        s=38,
        zorder=5,
        label="Lagrange points",
    )
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("rotating-frame x")
    ax.set_ylabel("rotating-frame y")
    ax.set_title(f"CR3BP trajectory and zero-velocity curve, C={c:.6g}")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mu", type=float, default=SUN_JUPITER_MU, help="smaller-primary mass fraction")
    parser.add_argument("--periods", type=float, default=3.0, help="integration time in rotating-frame periods")
    parser.add_argument("--dt", type=float, default=0.0025, help="time step in dimensionless units")
    parser.add_argument("--initial", choices=["l4", "l1", "asteroid"], default="l4")
    parser.add_argument("--plot", type=Path, default=None)
    args = parser.parse_args()
    if not (0.0 < args.mu < 0.5):
        parser.error("--mu must satisfy 0 < mu < 1/2")
    if args.periods < 0.0:
        parser.error("--periods must be >= 0")
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    return args


def main() -> None:
    args = parse_args()
    points = lagrange_points(args.mu)
    state0 = initial_state(args.initial, args.mu)
    time, states = integrate(args.mu, state0, args.dt, args.periods)
    jacobi = jacobi_constant(states, args.mu)
    drift = float(np.max(np.abs(jacobi - jacobi[0]))) if len(jacobi) else 0.0

    print(f"mu={args.mu:.12g}")
    print(f"L1=({points.l1:.12g}, 0)")
    print(f"L2=({points.l2:.12g}, 0)")
    print(f"L3=({points.l3:.12g}, 0)")
    print(f"L4=({points.l4[0]:.12g}, {points.l4[1]:.12g})")
    print(f"L5=({points.l5[0]:.12g}, {points.l5[1]:.12g})")
    print(f"initial_state={state0.tolist()}")
    print(f"steps={len(time) - 1}")
    print(f"elapsed_time={time[-1]:.12g}")
    print(f"jacobi_initial={float(jacobi[0]):.12g}")
    print(f"jacobi_max_abs_drift={drift:.12g}")
    print(f"final_state={states[-1].tolist()}")

    if args.plot is not None:
        save_plot(args.plot, time, states, args.mu)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
