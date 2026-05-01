#!/usr/bin/env python3
"""Hamiltonian pendulum demo with a symplectic Euler integrator.

Authors: GPT 5.5 and Xi Yin.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np


def integrate(q0: float, p0: float, dt: float, steps: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if dt <= 0.0:
        raise ValueError("dt must be > 0")
    if steps < 0:
        raise ValueError("steps must be >= 0")
    time = np.arange(steps + 1) * dt
    q = np.empty(steps + 1)
    p = np.empty(steps + 1)
    q[0] = q0
    p[0] = p0
    for n in range(steps):
        p[n + 1] = p[n] - dt * math.sin(q[n])
        q[n + 1] = q[n] + dt * p[n + 1]
    return time, q, p


def hamiltonian(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    return 0.5 * p * p + 1.0 - np.cos(q)


def save_plot(path: Path, time: np.ndarray, q: np.ndarray, p: np.ndarray) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    H = hamiltonian(q, p)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].plot(((q + math.pi) % (2.0 * math.pi)) - math.pi, p, linewidth=0.9)
    axes[0].set_xlabel("q mod 2pi")
    axes[0].set_ylabel("p")
    axes[0].set_title("phase curve")

    axes[1].plot(time, H - H[0])
    axes[1].set_xlabel("time")
    axes[1].set_ylabel("energy drift")
    axes[1].set_title("symplectic Euler drift")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q0", type=float, default=1.0)
    parser.add_argument("--p0", type=float, default=0.0)
    parser.add_argument("--dt", type=float, default=0.02)
    parser.add_argument("--steps", type=int, default=5000)
    parser.add_argument("--plot", type=Path, default=None)
    args = parser.parse_args()
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    if args.steps < 0:
        parser.error("--steps must be >= 0")
    return args


def main() -> None:
    args = parse_args()
    time, q, p = integrate(args.q0, args.p0, args.dt, args.steps)
    H = hamiltonian(q, p)
    print(f"steps={args.steps}")
    print(f"energy_initial={H[0]:.12g}")
    print(f"energy_final={H[-1]:.12g}")
    print(f"energy_drift={H[-1] - H[0]:.6e}")
    if args.plot is not None:
        save_plot(args.plot, time, q, p)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
