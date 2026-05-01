#!/usr/bin/env python3
"""Hamiltonian point-vortex fluid demo in two dimensions.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np


def velocity(positions: np.ndarray, gamma: np.ndarray, core: float = 1.0e-6) -> np.ndarray:
    n = len(gamma)
    vel = np.zeros_like(positions)
    for i in range(n):
        diff = positions[i] - positions
        r2 = np.sum(diff * diff, axis=1) + core * core
        coeff = gamma / (2.0 * math.pi * r2)
        coeff[i] = 0.0
        vel[i, 0] = np.sum(-coeff * diff[:, 1])
        vel[i, 1] = np.sum(coeff * diff[:, 0])
    return vel


def rk4_step(positions: np.ndarray, gamma: np.ndarray, dt: float) -> np.ndarray:
    k1 = velocity(positions, gamma)
    k2 = velocity(positions + 0.5 * dt * k1, gamma)
    k3 = velocity(positions + 0.5 * dt * k2, gamma)
    k4 = velocity(positions + dt * k3, gamma)
    return positions + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def hamiltonian(positions: np.ndarray, gamma: np.ndarray) -> float:
    total = 0.0
    for i in range(len(gamma)):
        for j in range(i + 1, len(gamma)):
            diff = positions[i] - positions[j]
            r2 = float(np.dot(diff, diff))
            total += gamma[i] * gamma[j] * math.log(max(r2, 1.0e-18))
    return -total / (4.0 * math.pi)


def initial_condition(name: str) -> tuple[np.ndarray, np.ndarray]:
    if name == "dipole":
        gamma = np.array([1.0, -1.0])
        positions = np.array([[-0.5, 0.0], [0.5, 0.0]], dtype=float)
        return positions, gamma
    if name == "four-vortex":
        gamma = np.array([1.0, 1.0, -1.0, -1.0])
        positions = np.array(
            [
                [-0.7, -0.3],
                [0.7, -0.3],
                [-0.4, 0.6],
                [0.4, 0.6],
            ],
            dtype=float,
        )
        return positions, gamma
    raise ValueError(f"unknown initial condition: {name}")


def simulate(steps: int, dt: float, scenario: str = "dipole") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if steps < 0:
        raise ValueError("steps must be >= 0")
    if dt <= 0.0:
        raise ValueError("dt must be > 0")
    positions, gamma = initial_condition(scenario)
    traj = np.empty((steps + 1, len(gamma), 2))
    energy = np.empty(steps + 1)
    traj[0] = positions
    energy[0] = hamiltonian(positions, gamma)
    for n in range(steps):
        positions = rk4_step(positions, gamma, dt)
        traj[n + 1] = positions
        energy[n + 1] = hamiltonian(positions, gamma)
    return traj, gamma, energy


def save_plot(path: Path, traj: np.ndarray, gamma: np.ndarray, energy: np.ndarray, dt: float) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    time = np.arange(len(energy)) * dt
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for i, g in enumerate(gamma):
        label = f"Gamma={g:g}"
        axes[0].plot(traj[:, i, 0], traj[:, i, 1], label=label, linewidth=1.0)
        axes[0].plot(traj[0, i, 0], traj[0, i, 1], "o", color=axes[0].lines[-1].get_color())
    axes[0].set_aspect("equal", adjustable="box")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_title("point-vortex trajectories")

    axes[1].plot(time, energy - energy[0])
    axes[1].set_xlabel("time")
    axes[1].set_ylabel("Hamiltonian drift")
    axes[1].set_title("numerical invariant drift")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ic", choices=["dipole", "four-vortex"], default="dipole")
    parser.add_argument("--steps", type=int, default=3000)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--plot", type=Path, default=None)
    args = parser.parse_args()
    if args.steps < 0:
        parser.error("--steps must be >= 0")
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    return args


def main() -> None:
    args = parse_args()
    traj, gamma, energy = simulate(args.steps, args.dt, scenario=args.ic)
    print(f"initial_condition={args.ic}")
    print(f"vortices={len(gamma)}")
    print(f"steps={args.steps}")
    print(f"hamiltonian_initial={energy[0]:.12g}")
    print(f"hamiltonian_final={energy[-1]:.12g}")
    print(f"hamiltonian_drift={energy[-1] - energy[0]:.6e}")
    if args.plot is not None:
        save_plot(args.plot, traj, gamma, energy, args.dt)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
