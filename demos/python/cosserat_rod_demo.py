#!/usr/bin/env python3
"""Planar Cosserat rod reconstruction from a curvature connection.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np


def curvature_field(s: np.ndarray, length: float, base: float, amp: float, mode: int) -> np.ndarray:
    return base + amp * np.sin(2.0 * math.pi * mode * s / length)


def cumulative_trapezoid(values: np.ndarray, dx: float) -> np.ndarray:
    """Small local equivalent of scipy.integrate.cumulative_trapezoid."""
    out = np.zeros_like(values)
    increments = 0.5 * dx * (values[1:] + values[:-1])
    out[1:] = np.cumsum(increments)
    return out


def reconstruct(length: float, points: int, base: float, amp: float, mode: int) -> dict[str, np.ndarray]:
    if length <= 0.0:
        raise ValueError("length must be > 0")
    if points < 2:
        raise ValueError("points must be >= 2")
    if mode < 1:
        raise ValueError("mode must be >= 1")
    s = np.linspace(0.0, length, points)
    ds = s[1] - s[0]
    kappa = curvature_field(s, length, base, amp, mode)
    theta = cumulative_trapezoid(kappa, ds)
    tangent = np.column_stack((np.cos(theta), np.sin(theta)))
    x = cumulative_trapezoid(tangent[:, 0], ds)
    y = cumulative_trapezoid(tangent[:, 1], ds)
    return {"s": s, "kappa": kappa, "theta": theta, "x": x, "y": y}


def save_plot(path: Path, data: dict[str, np.ndarray]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    x = data["x"]
    y = data["y"]
    theta = data["theta"]
    s = data["s"]
    kappa = data["kappa"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].plot(x, y, linewidth=2.0)
    skip = max(1, len(x) // 20)
    axes[0].quiver(
        x[::skip],
        y[::skip],
        np.cos(theta[::skip]),
        np.sin(theta[::skip]),
        angles="xy",
        scale_units="xy",
        scale=8.0,
        width=0.004,
    )
    axes[0].set_aspect("equal", adjustable="box")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_title("reconstructed centerline and frames")

    axes[1].plot(s, kappa)
    axes[1].set_xlabel("material coordinate s")
    axes[1].set_ylabel("connection component kappa(s)")
    axes[1].set_title("planar curvature connection")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=float, default=8.0)
    parser.add_argument("--points", type=int, default=600)
    parser.add_argument("--base", type=float, default=0.18)
    parser.add_argument("--amp", type=float, default=0.55)
    parser.add_argument("--mode", type=int, default=2)
    parser.add_argument("--plot", type=Path, default=None)
    args = parser.parse_args()
    if args.length <= 0.0:
        parser.error("--length must be > 0")
    if args.points < 2:
        parser.error("--points must be >= 2")
    if args.mode < 1:
        parser.error("--mode must be >= 1")
    return args


def main() -> None:
    args = parse_args()
    data = reconstruct(args.length, args.points, args.base, args.amp, args.mode)
    theta = data["theta"]
    x = data["x"]
    y = data["y"]
    print(f"length={args.length}")
    print(f"points={args.points}")
    print(f"frame_holonomy={theta[-1] - theta[0]:.12g}")
    print(f"endpoint_x={x[-1]:.12g}")
    print(f"endpoint_y={y[-1]:.12g}")
    if args.plot is not None:
        save_plot(args.plot, data)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
