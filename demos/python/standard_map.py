#!/usr/bin/env python3
"""Standard map phase portrait demo on the compact two-torus.

Authors: GPT 5.5 and Xi Yin.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np


TWOPI = 2.0 * math.pi


def iterate_standard_map(q0: np.ndarray, p0: np.ndarray, K: float, steps: int) -> tuple[np.ndarray, np.ndarray]:
    if q0.shape != p0.shape:
        raise ValueError("q0 and p0 must have the same shape")
    if steps < 0:
        raise ValueError("steps must be >= 0")
    q = np.empty((steps + 1, len(q0)))
    p = np.empty_like(q)
    q[0] = q0 % TWOPI
    p[0] = p0 % TWOPI
    for n in range(steps):
        p[n + 1] = (p[n] + K * np.sin(q[n])) % TWOPI
        q[n + 1] = (q[n] + p[n + 1]) % TWOPI
    return q, p


def save_plot(path: Path, q: np.ndarray, p: np.ndarray, K: float) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.plot(q.reshape(-1), p.reshape(-1), ".", markersize=0.35, alpha=0.65)
    ax.set_xlim(0.0, TWOPI)
    ax.set_ylim(0.0, TWOPI)
    ax.set_xlabel("q mod 2pi")
    ax.set_ylabel("p mod 2pi")
    ax.set_title(f"Standard map, K={K:g}")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--K", type=float, default=0.95)
    parser.add_argument("--orbits", type=int, default=80)
    parser.add_argument("--steps", type=int, default=800)
    parser.add_argument("--seed", type=int, default=3)
    parser.add_argument("--plot", type=Path, default=None)
    args = parser.parse_args()
    if args.orbits < 1:
        parser.error("--orbits must be >= 1")
    if args.steps < 0:
        parser.error("--steps must be >= 0")
    return args


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    q0 = rng.uniform(0.0, TWOPI, args.orbits)
    p0 = rng.uniform(0.0, TWOPI, args.orbits)
    q, p = iterate_standard_map(q0, p0, args.K, args.steps)
    print(f"K={args.K}")
    print(f"orbits={args.orbits}")
    print(f"steps={args.steps}")
    print(f"points={(args.steps + 1) * args.orbits}")
    if args.plot is not None:
        save_plot(args.plot, q, p, args.K)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
