#!/usr/bin/env python3
"""Euler top demo for a free 3D rigid body.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class RigidBody:
    I1: float
    I2: float
    I3: float


def inertia_vector(body: RigidBody) -> np.ndarray:
    return np.array([body.I1, body.I2, body.I3], dtype=float)


def hat(vector: np.ndarray) -> np.ndarray:
    x, y, z = vector
    return np.array(
        [
            [0.0, -z, y],
            [z, 0.0, -x],
            [-y, x, 0.0],
        ]
    )


def rotation_from_rotvec(rotvec: np.ndarray) -> np.ndarray:
    angle = float(np.linalg.norm(rotvec))
    K = hat(rotvec)
    if angle < 1.0e-12:
        return np.eye(3) + K + 0.5 * (K @ K)
    return (
        np.eye(3)
        + (np.sin(angle) / angle) * K
        + ((1.0 - np.cos(angle)) / (angle * angle)) * (K @ K)
    )


def rhs(omega: np.ndarray, body: RigidBody) -> np.ndarray:
    w1, w2, w3 = omega
    return np.array(
        [
            ((body.I2 - body.I3) / body.I1) * w2 * w3,
            ((body.I3 - body.I1) / body.I2) * w3 * w1,
            ((body.I1 - body.I2) / body.I3) * w1 * w2,
        ]
    )


def rk4_step(omega: np.ndarray, dt: float, body: RigidBody) -> np.ndarray:
    k1 = rhs(omega, body)
    k2 = rhs(omega + 0.5 * dt * k1, body)
    k3 = rhs(omega + 0.5 * dt * k2, body)
    k4 = rhs(omega + dt * k3, body)
    return omega + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def invariants(omega: np.ndarray, body: RigidBody) -> tuple[np.ndarray, np.ndarray]:
    I = inertia_vector(body)
    momentum = I * omega
    energy = 0.5 * np.sum(I * omega * omega, axis=-1)
    momentum_sq = np.sum(momentum * momentum, axis=-1)
    return energy, momentum_sq


def simulate(body: RigidBody, omega0: np.ndarray, dt: float, steps: int) -> tuple[np.ndarray, np.ndarray]:
    if min(body.I1, body.I2, body.I3) <= 0.0:
        raise ValueError("principal moments of inertia must be positive")
    if omega0.shape != (3,):
        raise ValueError("omega0 must have shape (3,)")
    if dt <= 0.0:
        raise ValueError("dt must be > 0")
    if steps < 0:
        raise ValueError("steps must be >= 0")
    omega = np.empty((steps + 1, 3))
    time = np.arange(steps + 1) * dt
    omega[0] = omega0
    for i in range(steps):
        omega[i + 1] = rk4_step(omega[i], dt, body)
    return time, omega


def simulate_attitude(
    body: RigidBody,
    omega0: np.ndarray,
    dt: float,
    steps: int,
    attitude0: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    time, omega = simulate(body, omega0, dt, steps)
    attitude = np.empty((steps + 1, 3, 3))
    if attitude0 is None:
        attitude[0] = np.eye(3)
    else:
        if attitude0.shape != (3, 3):
            raise ValueError("attitude0 must have shape (3, 3)")
        attitude[0] = attitude0

    for i in range(steps):
        # Rdot = R Omega_hat.  The midpoint angular velocity gives a
        # second-order reconstruction while the matrix exponential keeps R in SO(3).
        omega_mid = 0.5 * (omega[i] + omega[i + 1])
        attitude[i + 1] = attitude[i] @ rotation_from_rotvec(dt * omega_mid)
    return time, omega, attitude


def spatial_momentum(omega: np.ndarray, attitude: np.ndarray, body: RigidBody) -> np.ndarray:
    body_momentum = inertia_vector(body) * omega
    return np.einsum("...ij,...j->...i", attitude, body_momentum)


def attitude_errors(attitude: np.ndarray) -> tuple[float, float]:
    identity = np.eye(3)
    orthogonality = np.linalg.norm(
        np.einsum("...ji,...jk->...ik", attitude, attitude) - identity,
        axis=(-2, -1),
    )
    determinant = np.linalg.det(attitude)
    return float(np.max(orthogonality)), float(np.max(np.abs(determinant - 1.0)))


def save_plot(
    path: Path,
    time: np.ndarray,
    omega: np.ndarray,
    body: RigidBody,
    attitude: np.ndarray | None = None,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    energy, momentum_sq = invariants(omega, body)

    nrows = 3 if attitude is not None else 2
    fig, axes = plt.subplots(nrows, 1, figsize=(9, 7.5 if attitude is not None else 6), sharex=True)
    axes[0].plot(time, omega[:, 0], label="omega_1")
    axes[0].plot(time, omega[:, 1], label="omega_2")
    axes[0].plot(time, omega[:, 2], label="omega_3")
    axes[0].set_ylabel("body angular velocity")
    axes[0].legend(loc="best")

    axes[1].plot(time, energy - energy[0], label="energy drift")
    axes[1].plot(time, momentum_sq - momentum_sq[0], label="|M|^2 drift")
    axes[1].set_xlabel("time")
    axes[1].set_ylabel("invariant drift")
    axes[1].legend(loc="best")

    if attitude is not None:
        J = spatial_momentum(omega, attitude, body)
        axes[2].plot(time, np.linalg.norm(J - J[0], axis=1), label="|J(t)-J(0)|")
        axes[2].set_xlabel("time")
        axes[2].set_ylabel("spatial momentum drift")
        axes[2].legend(loc="best")

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--I1", type=float, default=1.0)
    parser.add_argument("--I2", type=float, default=2.0)
    parser.add_argument("--I3", type=float, default=3.0)
    parser.add_argument("--omega0", type=float, nargs=3, default=[0.05, 1.0, 0.05])
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--steps", type=int, default=5000)
    parser.add_argument("--plot", type=Path, default=None)
    args = parser.parse_args()
    if min(args.I1, args.I2, args.I3) <= 0.0:
        parser.error("--I1, --I2, and --I3 must be > 0")
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    if args.steps < 0:
        parser.error("--steps must be >= 0")
    return args


def main() -> None:
    args = parse_args()
    body = RigidBody(args.I1, args.I2, args.I3)
    time, omega, attitude = simulate_attitude(
        body, np.array(args.omega0, dtype=float), args.dt, args.steps
    )
    energy, momentum_sq = invariants(omega, body)
    J = spatial_momentum(omega, attitude, body)
    orthogonality_error, determinant_error = attitude_errors(attitude)
    print(f"steps={args.steps}")
    print(f"energy_initial={energy[0]:.12g}")
    print(f"energy_final={energy[-1]:.12g}")
    print(f"energy_drift={energy[-1] - energy[0]:.6e}")
    print(f"momentum_sq_initial={momentum_sq[0]:.12g}")
    print(f"momentum_sq_final={momentum_sq[-1]:.12g}")
    print(f"momentum_sq_drift={momentum_sq[-1] - momentum_sq[0]:.6e}")
    print(f"spatial_momentum_max_drift={np.max(np.linalg.norm(J - J[0], axis=1)):.6e}")
    print(f"attitude_orthogonality_error={orthogonality_error:.6e}")
    print(f"attitude_determinant_error={determinant_error:.6e}")
    if args.plot is not None:
        save_plot(args.plot, time, omega, body, attitude)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
