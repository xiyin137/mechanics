#!/usr/bin/env python3
"""Finite-time diagnostics for invariant-curve breakdown in the standard map.

The standard map

    p_{n+1} = p_n + K sin(q_n),    q_{n+1} = q_n + p_{n+1}  mod 2*pi

is a two-dimensional area-preserving twist map.  On the cylinder, invariant
curves are transport barriers: an orbit cannot cross a surviving invariant
curve.  This script follows an ensemble initially concentrated near the
golden-mean rotation number and reports finite-time momentum spreading.

The diagnostic is deliberately modest.  It is a numerical probe of transport,
not a proof that a particular invariant curve has broken.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions
from Anthropic Opus 4.7.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path
from typing import Iterable

import numpy as np

TWOPI = 2.0 * math.pi
GOLDEN_ROTATION = (math.sqrt(5.0) - 1.0) / 2.0
GOLDEN_P = TWOPI * GOLDEN_ROTATION


def iterate_cylinder(
    q0: Iterable[float] | np.ndarray,
    p0: Iterable[float] | np.ndarray,
    K: float,
    steps: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Iterate the standard map on the cylinder.

    Parameters
    ----------
    q0, p0:
        Initial angle and momentum arrays.  ``q`` is treated modulo ``2*pi``;
        ``p`` is left unwrapped so momentum transport is visible.
    K:
        Perturbation strength.
    steps:
        Number of map iterations.

    Returns
    -------
    q_mod, p, q_lift:
        Arrays of shape ``(steps + 1, n_orbits)``.  ``q_mod`` is in
        ``[0, 2*pi)`` and ``q_lift`` is the lifted angle.
    """

    if steps < 0:
        raise ValueError("steps must be nonnegative")

    q0_array = np.asarray(q0, dtype=float)
    p0_array = np.asarray(p0, dtype=float)
    if q0_array.shape != p0_array.shape:
        raise ValueError("q0 and p0 must have the same shape")

    flat_q0 = np.ravel(q0_array)
    flat_p0 = np.ravel(p0_array)
    q_mod = np.empty((steps + 1, flat_q0.size), dtype=float)
    p = np.empty_like(q_mod)
    q_lift = np.empty_like(q_mod)

    q_lift[0] = flat_q0
    q_mod[0] = np.mod(flat_q0, TWOPI)
    p[0] = flat_p0

    for n in range(steps):
        p[n + 1] = p[n] + K * np.sin(q_mod[n])
        q_lift[n + 1] = q_lift[n] + p[n + 1]
        q_mod[n + 1] = np.mod(q_lift[n + 1], TWOPI)

    return q_mod, p, q_lift


def make_initial_conditions(
    orbits: int,
    *,
    seed: int,
    p0_center: float = GOLDEN_P,
    p0_width: float = 1.0e-3,
) -> tuple[np.ndarray, np.ndarray]:
    """Sample an ensemble localized near a chosen unperturbed rotation number."""

    if orbits <= 0:
        raise ValueError("orbits must be positive")
    if p0_width < 0.0:
        raise ValueError("p0_width must be nonnegative")

    rng = np.random.default_rng(seed)
    q0 = rng.uniform(0.0, TWOPI, size=orbits)
    p0 = p0_center + rng.uniform(-p0_width, p0_width, size=orbits)
    return q0, p0


def transport_summary(q_mod: np.ndarray, p: np.ndarray, q_lift: np.ndarray) -> dict[str, float]:
    """Return finite-time transport diagnostics for a standard-map ensemble."""

    if q_mod.shape != p.shape or q_mod.shape != q_lift.shape:
        raise ValueError("q_mod, p, and q_lift must have matching shapes")
    if p.ndim != 2 or p.shape[0] < 1:
        raise ValueError("trajectory arrays must have shape (time, orbit)")

    initial = p[0]
    final = p[-1]
    steps = max(p.shape[0] - 1, 1)
    finite_rotation = (q_lift[-1] - q_lift[0]) / (TWOPI * steps)
    p_span_time = np.max(p, axis=1) - np.min(p, axis=1)
    p_std_time = np.std(p, axis=1)
    delta = final - initial

    return {
        "orbits": float(p.shape[1]),
        "steps": float(p.shape[0] - 1),
        "p_span_initial": float(p_span_time[0]),
        "p_span_final": float(p_span_time[-1]),
        "p_span_max": float(np.max(p_span_time)),
        "p_std_initial": float(p_std_time[0]),
        "p_std_final": float(p_std_time[-1]),
        "p_std_max": float(np.max(p_std_time)),
        "mean_abs_delta_p": float(np.mean(np.abs(delta))),
        "max_abs_delta_p": float(np.max(np.abs(delta))),
        "rotation_mean": float(np.mean(finite_rotation)),
        "rotation_std": float(np.std(finite_rotation)),
    }


def run_ensemble(
    *,
    K: float,
    orbits: int,
    steps: int,
    seed: int,
    p0_center: float = GOLDEN_P,
    p0_width: float = 1.0e-3,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    """Generate initial conditions, iterate them, and summarize transport."""

    q0, p0 = make_initial_conditions(
        orbits,
        seed=seed,
        p0_center=p0_center,
        p0_width=p0_width,
    )
    q_mod, p, q_lift = iterate_cylinder(q0, p0, K, steps)
    return q_mod, p, q_lift, transport_summary(q_mod, p, q_lift)


def save_plot(
    path: str | Path,
    q_mod: np.ndarray,
    p: np.ndarray,
    K: float,
    summary: dict[str, float],
) -> None:
    """Save a two-panel visualization of phase-space spreading."""

    os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".matplotlib-cache"))
    os.environ.setdefault("MPLBACKEND", "Agg")
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    time = np.arange(p.shape[0])
    p_span = np.max(p, axis=1) - np.min(p, axis=1)
    p_std = np.std(p, axis=1)
    stride = max(1, p.shape[0] // 350)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), constrained_layout=True)
    axes[0].scatter(
        q_mod[::stride].ravel(),
        p[::stride].ravel(),
        s=1.2,
        alpha=0.55,
        color="#1f77b4",
        linewidths=0.0,
    )
    axes[0].set_xlim(0.0, TWOPI)
    axes[0].set_xlabel(r"$q\ \mathrm{mod}\ 2\pi$")
    axes[0].set_ylabel(r"unwrapped $p$")
    axes[0].set_title(fr"Standard map ensemble, $K={K:g}$")
    axes[0].grid(alpha=0.18)

    axes[1].plot(time, p_span, color="#d62728", lw=1.8, label=r"$p$ span")
    axes[1].plot(time, p_std, color="#2ca02c", lw=1.8, label=r"$p$ standard deviation")
    axes[1].set_xlabel("iteration")
    axes[1].set_ylabel("momentum spread")
    axes[1].set_title("Finite-time transport diagnostic")
    axes[1].grid(alpha=0.22)
    axes[1].legend(frameon=False)

    text = (
        fr"$\langle |\Delta p| \rangle={summary['mean_abs_delta_p']:.3g}$"
        "\n"
        fr"$\max |\Delta p|={summary['max_abs_delta_p']:.3g}$"
    )
    axes[1].text(
        0.03,
        0.97,
        text,
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "0.85", "alpha": 0.92},
    )

    fig.savefig(output, dpi=170)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--K", type=float, default=1.1, help="standard-map kick strength")
    parser.add_argument("--orbits", type=int, default=128, help="number of ensemble orbits")
    parser.add_argument("--steps", type=int, default=1500, help="number of iterations")
    parser.add_argument("--seed", type=int, default=20260501, help="random seed")
    parser.add_argument(
        "--p0",
        type=float,
        default=GOLDEN_P,
        help="center of initial momentum packet, default 2*pi times the golden rotation number",
    )
    parser.add_argument(
        "--width",
        type=float,
        default=1.0e-3,
        help="half-width of the initial momentum packet",
    )
    parser.add_argument("--plot", type=Path, help="optional output path for a PNG figure")
    args = parser.parse_args()
    if args.orbits <= 0:
        parser.error("--orbits must be > 0")
    if args.steps < 0:
        parser.error("--steps must be >= 0")
    if args.width < 0.0:
        parser.error("--width must be >= 0")
    return args


def main() -> None:
    args = parse_args()
    q_mod, p, q_lift, summary = run_ensemble(
        K=args.K,
        orbits=args.orbits,
        steps=args.steps,
        seed=args.seed,
        p0_center=args.p0,
        p0_width=args.width,
    )

    print("Standard-map invariant-curve breakdown diagnostic")
    print("This is a finite-time transport probe, not a proof of torus destruction.")
    print(f"K={args.K:g}, orbits={args.orbits}, steps={args.steps}, seed={args.seed}")
    print(f"p0_center={args.p0:.12g}, p0_width={args.width:.3g}")
    for key in sorted(summary):
        print(f"{key}={summary[key]:.12g}")

    if args.plot:
        save_plot(args.plot, q_mod, p, args.K, summary)
        print(f"wrote {args.plot}")


if __name__ == "__main__":
    main()
