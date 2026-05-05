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

try:
    from demos.python.common import add_output_args, add_preset_args, configure_standard_outputs, emit_summary, fill_defaults
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from common import add_output_args, add_preset_args, configure_standard_outputs, emit_summary, fill_defaults


E_X = np.array([1.0, 0.0, 0.0])
E_Y = np.array([0.0, 1.0, 0.0])
E_Z = np.array([0.0, 0.0, 1.0])
DEFAULTS = {"i0": 4.0, "i1": 1.0, "i2": 1.5, "delta_alpha": 0.45, "delta_beta": 0.35, "cycles": 1}
PRESETS = {
    "quick": {"delta_alpha": 0.05, "delta_beta": 0.04, "cycles": 1},
    "lecture": {"delta_alpha": 0.45, "delta_beta": 0.35, "cycles": 1},
    "long": {"delta_alpha": 0.45, "delta_beta": 0.35, "cycles": 8},
}


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
    """Return the component vector of dA - 1/2[A wedge A] for constant coefficients."""
    a_alpha, a_beta = connection_components(i0, i1, i2)
    return -np.cross(a_alpha, a_beta)


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


def holonomy_scaling(
    i0: float,
    i1: float,
    i2: float,
    delta_alpha: float,
    delta_beta: float,
    cycles: int,
) -> list[dict[str, object]]:
    curvature = curvature_vector(i0, i1, i2)
    rows: list[dict[str, object]] = []
    for scale in (0.25, 0.5, 0.75, 1.0):
        da = scale * delta_alpha
        db = scale * delta_beta
        rotation = rectangular_stroke(i0, i1, i2, da, db, cycles)
        rotvec = rotation_vector(rotation)
        leading = -curvature * da * db * cycles
        error = rotvec - leading
        rows.append(
            {
                "scale": scale,
                "area": float(da * db),
                "leading_rotation_vector": leading.tolist(),
                "net_rotation_vector": rotvec.tolist(),
                "bch_error_norm": float(np.linalg.norm(error)),
                "bch_relative_error": float(np.linalg.norm(error) / max(np.linalg.norm(leading), 1.0e-18)),
            }
        )
    return rows


def save_plot(
    path: Path,
    delta_alpha: float,
    delta_beta: float,
    rotvec: np.ndarray,
    scaling: list[dict[str, object]],
) -> None:
    os.environ.setdefault("MPLCONFIGDIR", str(Path(".pycache-build") / "matplotlib"))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.0))

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

    areas = [float(row["area"]) for row in scaling]
    errors = [float(row["bch_error_norm"]) for row in scaling]
    axes[2].plot(areas, errors, marker="o")
    axes[2].set_xlabel("shape-loop area")
    axes[2].set_ylabel("BCH error norm")
    axes[2].set_title("small-loop scaling")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def build_summary(
    args: argparse.Namespace,
    a_alpha: np.ndarray,
    a_beta: np.ndarray,
    curvature: np.ndarray,
    leading: np.ndarray,
    rotvec: np.ndarray,
    rotation: np.ndarray,
) -> dict[str, object]:
    error = rotvec - leading
    scaling = holonomy_scaling(args.i0, args.i1, args.i2, args.delta_alpha, args.delta_beta, args.cycles)
    return {
        "model": "finite-dimensional gauge kinematics of a deforming body",
        "interpretation": "helicopter rotor: lift rotor about body z, tail rotor about body y",
        "reconstruction_equation": "Omega = -A_alpha alpha_dot - A_beta beta_dot",
        "configuration": {
            "i0": args.i0,
            "i1": args.i1,
            "i2": args.i2,
            "delta_alpha": args.delta_alpha,
            "delta_beta": args.delta_beta,
            "cycles": args.cycles,
        },
        "A_alpha": a_alpha.tolist(),
        "A_beta": a_beta.tolist(),
        "curvature_vector": curvature.tolist(),
        "shape_area_per_cycle": float(args.delta_alpha * args.delta_beta),
        "leading_rotation_vector": leading.tolist(),
        "net_rotation_vector": rotvec.tolist(),
        "net_rotation_angle": float(np.linalg.norm(rotvec)),
        "bch_error_norm": float(np.linalg.norm(error)),
        "bch_relative_error": float(np.linalg.norm(error) / max(np.linalg.norm(leading), 1.0e-18)),
        "holonomy_scaling": scaling,
        "orthogonality_error": float(np.linalg.norm(rotation.T @ rotation - np.eye(3))),
        "determinant_error": float(abs(np.linalg.det(rotation) - 1.0)),
        "outputs": {},
    }


def print_summary(summary: dict[str, object]) -> None:
    print(f"interpretation={summary['interpretation']}")
    print(f"A_alpha={summary['A_alpha']}")
    print(f"A_beta={summary['A_beta']}")
    print(f"curvature_vector={summary['curvature_vector']}")
    print(f"shape_area_per_cycle={summary['shape_area_per_cycle']:.12g}")
    print(f"leading_rotation_vector={summary['leading_rotation_vector']}")
    print(f"net_rotation_vector={summary['net_rotation_vector']}")
    print(f"net_rotation_angle={summary['net_rotation_angle']:.12g}")
    print(f"bch_error_norm={summary['bch_error_norm']:.12g}")
    print(f"bch_relative_error={summary['bch_relative_error']:.12g}")
    print("holonomy_scaling=scale,area,bch_error_norm,bch_relative_error")
    for row in summary["holonomy_scaling"]:
        print(
            f"{row['scale']:.2f},{row['area']:.12g},"
            f"{row['bch_error_norm']:.12g},{row['bch_relative_error']:.12g}"
        )
    print(f"orthogonality_error={summary['orthogonality_error']:.12g}")
    print(f"determinant_error={summary['determinant_error']:.12g}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_preset_args(parser)
    parser.add_argument("--i0", type=float, default=None, help="carrier inertia")
    parser.add_argument("--i1", type=float, default=None, help="z-rotor inertia")
    parser.add_argument("--i2", type=float, default=None, help="y-rotor inertia")
    parser.add_argument("--delta-alpha", type=float, default=None)
    parser.add_argument("--delta-beta", type=float, default=None)
    parser.add_argument("--cycles", type=int, default=None)
    parser.add_argument("--plot", type=Path, default=None)
    add_output_args(parser)
    args = parser.parse_args()
    defaults = dict(DEFAULTS)
    if args.quick:
        defaults.update(PRESETS["quick"])
    elif args.lecture:
        defaults.update(PRESETS["lecture"])
    elif args.long:
        defaults.update(PRESETS["long"])
    fill_defaults(args, defaults)
    configure_standard_outputs(args, stem="deforming_body_gauge", plot_name="deforming_body_gauge.png")
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
    leading = -curvature * area * args.cycles

    summary = build_summary(args, a_alpha, a_beta, curvature, leading, rotvec, rotation)
    if args.plot is not None:
        save_plot(args.plot, args.delta_alpha, args.delta_beta, rotvec, summary["holonomy_scaling"])
    emit_summary(summary, args, print_summary)


if __name__ == "__main__":
    main()
