#!/usr/bin/env python3
"""Finite-dimensional gauge kinematics for a deforming body.

The model is the two-rotor shape-space example from the notes, including the
literal helicopter-rotor interpretation used in the laboratory discussion. The
internal shape coordinates are rotor angles (alpha, beta): alpha is the
collective spin/feather coordinate of a lift rotor about the body z-axis, while
beta is the corresponding coordinate of a tail rotor about the body y-axis. At
zero total angular momentum, shape velocity forces a body angular velocity

    Omega = -A_alpha alpha_dot - A_beta beta_dot.

A closed rectangle in shape space can therefore generate a net body rotation.
The example is deliberately small: it is a reproducible numerical microscope
for nonabelian holonomy.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

import numpy as np


E_X = np.array([1.0, 0.0, 0.0])
E_Y = np.array([0.0, 1.0, 0.0])
E_Z = np.array([0.0, 0.0, 1.0])


def hat(v: np.ndarray) -> np.ndarray:
    """Return the skew matrix satisfying hat(v) @ w = v x w."""
    x, y, z = np.asarray(v, dtype=float)
    return np.array(
        [
            [0.0, -z, y],
            [z, 0.0, -x],
            [-y, x, 0.0],
        ]
    )


def vee(a: np.ndarray) -> np.ndarray:
    """Inverse of hat on skew matrices."""
    return np.array([a[2, 1], a[0, 2], a[1, 0]], dtype=float)


def exp_so3(v: np.ndarray) -> np.ndarray:
    """Rodrigues formula for exp(hat(v))."""
    v = np.asarray(v, dtype=float)
    angle = float(np.linalg.norm(v))
    k = hat(v)
    if angle < 1.0e-12:
        return np.eye(3) + k + 0.5 * (k @ k)
    s = math.sin(angle) / angle
    c = (1.0 - math.cos(angle)) / (angle * angle)
    return np.eye(3) + s * k + c * (k @ k)


def rotation_vector(rotation: np.ndarray) -> np.ndarray:
    """Return the principal rotation vector of an SO(3) matrix."""
    trace = float(np.trace(rotation))
    cos_angle = max(-1.0, min(1.0, 0.5 * (trace - 1.0)))
    angle = math.acos(cos_angle)
    skew = 0.5 * (rotation - rotation.T)
    if angle < 1.0e-8:
        return vee(skew)
    return angle / math.sin(angle) * vee(skew)


def connection_components(i0: float, i1: float, i2: float) -> tuple[np.ndarray, np.ndarray]:
    """Return A_alpha and A_beta for the two-rotor zero-momentum connection."""
    if min(i0, i1, i2) <= 0.0:
        raise ValueError("all inertias must be positive")
    a = i1 / (i0 + i1)
    b = i2 / (i0 + i2)
    return a * E_Z, b * E_Y


def curvature_vector(i0: float, i1: float, i2: float) -> np.ndarray:
    """Return the nonabelian curvature vector [A_alpha, A_beta]."""
    a_alpha, a_beta = connection_components(i0, i1, i2)
    return np.cross(a_alpha, a_beta)


def helicopter_rotor_connection(
    body_inertia: float,
    lift_rotor_inertia: float,
    tail_rotor_inertia: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Connection for the helicopter-rotor version of the two-rotor model.

    The lift rotor is idealized as an internal rotor about body e_z and the
    tail rotor as an internal rotor about body e_y. The returned vectors
    (A_lift, A_tail) enter Omega = -A_lift alpha_dot - A_tail beta_dot.
    """

    return connection_components(body_inertia, lift_rotor_inertia, tail_rotor_inertia)


def helicopter_rotor_stroke(
    body_inertia: float,
    lift_rotor_inertia: float,
    tail_rotor_inertia: float,
    delta_lift: float,
    delta_tail: float,
    cycles: int = 1,
) -> np.ndarray:
    """Net attitude from a rectangular helicopter-rotor shape stroke."""

    return rectangular_stroke(
        body_inertia,
        lift_rotor_inertia,
        tail_rotor_inertia,
        delta_lift,
        delta_tail,
        cycles,
    )


def rectangular_stroke(
    i0: float,
    i1: float,
    i2: float,
    delta_alpha: float,
    delta_beta: float,
    cycles: int = 1,
) -> np.ndarray:
    """Exact product for an alpha-beta-alpha^-1-beta^-1 rectangle.

    The reconstruction convention is Rdot = R hat(Omega_body) with
    Omega_body = -A_alpha alpha_dot - A_beta beta_dot.
    """
    if cycles < 1:
        raise ValueError("cycles must be >= 1")
    a_alpha, a_beta = connection_components(i0, i1, i2)
    segments = [
        -a_alpha * delta_alpha,
        -a_beta * delta_beta,
        a_alpha * delta_alpha,
        a_beta * delta_beta,
    ]
    rotation = np.eye(3)
    for _ in range(cycles):
        for segment in segments:
            rotation = rotation @ exp_so3(segment)
    return rotation


def save_plot(path: Path, delta_alpha: float, delta_beta: float, rotvec: np.ndarray) -> None:
    os.environ.setdefault("MPLCONFIGDIR", str(Path(".pycache-build") / "matplotlib"))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.0))

    rectangle_x = [0.0, delta_alpha, delta_alpha, 0.0, 0.0]
    rectangle_y = [0.0, 0.0, delta_beta, delta_beta, 0.0]
    axes[0].plot(rectangle_x, rectangle_y, marker="o")
    axes[0].set_aspect("equal", adjustable="box")
    axes[0].set_xlabel("alpha")
    axes[0].set_ylabel("beta")
    axes[0].set_title("closed shape stroke")

    axes[1].bar(["x", "y", "z"], rotvec)
    axes[1].axhline(0.0, color="black", linewidth=0.8)
    axes[1].set_ylabel("rotation vector")
    axes[1].set_title("net body rotation")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--i0", type=float, default=4.0, help="carrier inertia")
    parser.add_argument("--i1", type=float, default=1.0, help="z-rotor inertia")
    parser.add_argument("--i2", type=float, default=1.5, help="y-rotor inertia")
    parser.add_argument("--delta-alpha", type=float, default=0.45)
    parser.add_argument("--delta-beta", type=float, default=0.35)
    parser.add_argument("--cycles", type=int, default=1)
    parser.add_argument("--plot", type=Path, default=None)
    args = parser.parse_args()
    if min(args.i0, args.i1, args.i2) <= 0.0:
        parser.error("all inertias must be positive")
    if args.cycles < 1:
        parser.error("--cycles must be >= 1")
    return args


def main() -> None:
    args = parse_args()
    a_alpha, a_beta = connection_components(args.i0, args.i1, args.i2)
    curvature = curvature_vector(args.i0, args.i1, args.i2)
    rotation = rectangular_stroke(
        args.i0,
        args.i1,
        args.i2,
        args.delta_alpha,
        args.delta_beta,
        args.cycles,
    )
    rotvec = rotation_vector(rotation)
    area = args.delta_alpha * args.delta_beta
    leading = curvature * area * args.cycles

    print("interpretation=helicopter rotor: lift rotor about body z, tail rotor about body y")
    print(f"A_alpha={a_alpha.tolist()}")
    print(f"A_beta={a_beta.tolist()}")
    print(f"curvature_vector={curvature.tolist()}")
    print(f"shape_area_per_cycle={area:.12g}")
    print(f"leading_rotation_vector={leading.tolist()}")
    print(f"net_rotation_vector={rotvec.tolist()}")
    print(f"net_rotation_angle={np.linalg.norm(rotvec):.12g}")
    print(f"orthogonality_error={np.linalg.norm(rotation.T @ rotation - np.eye(3)):.12g}")
    print(f"determinant_error={abs(np.linalg.det(rotation) - 1.0):.12g}")

    if args.plot is not None:
        save_plot(args.plot, args.delta_alpha, args.delta_beta, rotvec)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
