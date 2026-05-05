#!/usr/bin/env python3
"""Illustrate Jovian resonance locations and pendulum normal-form scaling.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

The script is deliberately analytic and fast. It computes nominal interior
mean-motion resonance locations, an illustrative pendulum half-width scaling,
and a real first-order disturbing-function coefficient for the interior 2:1
Jovian resonance.

    Delta J = 2 sqrt(epsilon |B_r(e)| / |A|)

with B_r(e) modeled as eta e^r. For the 2:1 resonance the script also expands
the heliocentric disturbing function to first order in eccentricity and
computes the resonant Fourier coefficient by quadrature. This promotes the
2:1 width from a pure scaling law to a quantitative classroom estimate within
the planar circular restricted model.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np


A_JUPITER = 5.2044
M_JUPITER_OVER_M_SUN = 9.543e-4
RESONANCE_RATIOS = {
    "3:1": (3, 1),
    "5:2": (5, 2),
    "7:3": (7, 3),
    "2:1": (2, 1),
}


def resonance_locations(a_jupiter: float = A_JUPITER) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for label, (p, q) in RESONANCE_RATIOS.items():
        rows.append(
            {
                "label": label,
                "p": p,
                "q": q,
                "order": p - q,
                "a_au": a_jupiter * (q / p) ** (2.0 / 3.0),
            }
        )
    return rows


def laplace_coefficient(alpha: float, s: float, j: int, samples: int = 8192) -> float:
    """Return b_s^(j)(alpha) using the celestial-mechanics normalization.

    b_s^(j)(alpha) = (1/pi) int_0^{2pi}
        cos(j psi) / (1 - 2 alpha cos psi + alpha^2)^s d psi.
    """

    if not 0.0 <= alpha < 1.0:
        raise ValueError("alpha must satisfy 0 <= alpha < 1")
    if samples < 16:
        raise ValueError("samples must be at least 16")
    psi = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    denom = (1.0 - 2.0 * alpha * np.cos(psi) + alpha * alpha) ** s
    return float(2.0 * np.mean(np.cos(j * psi) / denom))


def two_to_one_resonant_coefficient(alpha: float, samples: int = 8192) -> float:
    """Coefficient of e cos(2 lambda_J - lambda - varpi).

    Units are G m_J / a_J. The calculation differentiates the heliocentric
    disturbing function

        R = 1/|r_J-r| - r dot r_J / |r_J|^3

    with respect to asteroid eccentricity at e=0, then projects onto the 2:1
    resonant angle. The single integral below is the result of analytically
    averaging over the ignorable rotation angle.
    """

    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must satisfy 0 < alpha < 1")
    if samples < 16:
        raise ValueError("samples must be at least 16")
    psi = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    q = 1.0 - 2.0 * alpha * np.cos(psi) + alpha * alpha
    d_direct_d_rho = (alpha * np.cos(psi) - alpha * alpha) * q ** (-1.5)
    d_direct_d_delta = -alpha * np.sin(psi) * q ** (-1.5)
    d_r_d_rho = d_direct_d_rho - alpha * np.cos(psi)
    d_r_d_delta = d_direct_d_delta + alpha * np.sin(psi)
    integrand = -np.cos(2.0 * psi) * d_r_d_rho + 2.0 * np.sin(2.0 * psi) * d_r_d_delta
    return float(np.mean(integrand))


def finite_difference_two_to_one_coefficient(alpha: float, eccentricity: float = 1.0e-5, samples: int = 512) -> float:
    """Independent two-angle check of the 2:1 coefficient."""

    if not 0.0 < eccentricity < 0.1:
        raise ValueError("eccentricity must be small and positive")
    mean_anomaly = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    lambda_jupiter = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    m_grid, lj_grid = np.meshgrid(mean_anomaly, lambda_jupiter, indexing="ij")
    true_longitude = m_grid + 2.0 * eccentricity * np.sin(m_grid)
    radius = alpha * (1.0 - eccentricity * np.cos(m_grid))
    delta = true_longitude - lj_grid
    direct = 1.0 / np.sqrt(1.0 - 2.0 * radius * np.cos(delta) + radius * radius)
    indirect = radius * np.cos(delta)
    disturbing = direct - indirect
    phase = 2.0 * lj_grid - m_grid
    coefficient_at_e = float(np.mean(disturbing * np.cos(phase)))
    direct0 = 1.0 / np.sqrt(1.0 - 2.0 * alpha * np.cos(m_grid - lj_grid) + alpha * alpha)
    indirect0 = alpha * np.cos(m_grid - lj_grid)
    coefficient_at_zero = float(np.mean((direct0 - indirect0) * np.cos(phase)))
    return 2.0 * (coefficient_at_e - coefficient_at_zero) / eccentricity


def two_to_one_width_rows(
    eccentricities: np.ndarray,
    epsilon: float,
    a_jupiter: float,
    samples: int,
) -> list[dict[str, float | str]]:
    alpha = (1.0 / 2.0) ** (2.0 / 3.0)
    coefficient = two_to_one_resonant_coefficient(alpha, samples=samples)
    a_res = a_jupiter * alpha
    rows: list[dict[str, float | str]] = []
    for ecc in eccentricities:
        half_width_au = 4.0 * a_jupiter * math.sqrt(max(0.0, epsilon * abs(coefficient) * float(ecc) * alpha**3 / 3.0))
        rows.append(
            {
                "resonance": "2:1",
                "eccentricity": float(ecc),
                "coefficient_units_gmj_over_aj": coefficient,
                "semimajor_axis_au": a_res,
                "half_width_au": half_width_au,
                "full_width_au": 2.0 * half_width_au,
            }
        )
    return rows


def width_scaling(
    eccentricities: np.ndarray,
    epsilon: float,
    eta: float,
    curvature: float,
) -> list[dict[str, float | int | str]]:
    if epsilon < 0.0:
        raise ValueError("epsilon must be nonnegative")
    if eta < 0.0:
        raise ValueError("eta must be nonnegative")
    if curvature == 0.0:
        raise ValueError("curvature must be nonzero")
    rows: list[dict[str, float | int | str]] = []
    for resonance in resonance_locations():
        order = int(resonance["order"])
        for ecc in eccentricities:
            coefficient = eta * float(ecc) ** order
            half_width = 2.0 * math.sqrt(epsilon * coefficient / abs(curvature))
            rows.append(
                {
                    "resonance": str(resonance["label"]),
                    "order": order,
                    "eccentricity": float(ecc),
                    "coefficient_model": coefficient,
                    "half_width_action_units": half_width,
                }
            )
    return rows


def pendulum_phase_curves(
    eta: float,
    curvature: float,
    points: int,
) -> list[dict[str, float]]:
    if points < 3:
        raise ValueError("points must be at least 3")
    phases = np.linspace(-math.pi, math.pi, points)
    amplitude = 2.0 * math.sqrt(abs(eta / curvature)) if curvature != 0.0 else float("nan")
    rows: list[dict[str, float]] = []
    for phi in phases:
        separatrix = amplitude * abs(math.cos(0.5 * phi))
        rows.append(
            {
                "phi": float(phi),
                "separatrix_positive": float(separatrix),
                "separatrix_negative": float(-separatrix),
            }
        )
    return rows


def json_ready(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else value
    return value


def build_summary(args: argparse.Namespace) -> dict[str, object]:
    eccentricities = np.linspace(args.ecc_min, args.ecc_max, args.ecc_points)
    alpha_21 = (1.0 / 2.0) ** (2.0 / 3.0)
    coefficient_21 = two_to_one_resonant_coefficient(alpha_21, samples=args.quadrature_samples)
    coefficient_check = finite_difference_two_to_one_coefficient(
        alpha_21,
        eccentricity=args.coefficient_check_eccentricity,
        samples=args.check_samples,
    )
    return {
        "model": {
            "name": "resonant pendulum normal form with 2:1 disturbing-function coefficient",
            "a_jupiter": args.a_jupiter,
            "epsilon": args.epsilon,
            "eta": args.eta,
            "curvature": args.curvature,
            "coefficient_note": (
                "B_r(e)=eta e^r is illustrative for generic resonances; the 2:1 rows use a "
                "first-order quadrature coefficient of the heliocentric disturbing function."
            ),
        },
        "resonances": resonance_locations(args.a_jupiter),
        "width_scaling": width_scaling(eccentricities, args.epsilon, args.eta, args.curvature),
        "disturbing_function_2to1": {
            "alpha": alpha_21,
            "laplace_b_half_1": laplace_coefficient(alpha_21, 0.5, 1, samples=args.quadrature_samples),
            "laplace_b_half_2": laplace_coefficient(alpha_21, 0.5, 2, samples=args.quadrature_samples),
            "coefficient_units_gmj_over_aj": coefficient_21,
            "finite_difference_check": coefficient_check,
            "finite_difference_abs_error": abs(coefficient_check - coefficient_21),
            "coefficient_angle": "2 lambda_J - lambda - varpi",
        },
        "width_2to1_disturbing_function": two_to_one_width_rows(
            eccentricities,
            args.epsilon,
            args.a_jupiter,
            args.quadrature_samples,
        ),
        "pendulum": pendulum_phase_curves(args.eta, args.curvature, args.points),
        "outputs": {},
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(json_ready(data), handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")


def save_plot(path: Path, summary: dict[str, object]) -> None:
    import os

    os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache")))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    resonances = summary["resonances"]
    widths = summary["width_scaling"]
    pendulum = summary["pendulum"]

    fig, (ax0, ax1, ax2) = plt.subplots(
        1,
        3,
        figsize=(13.0, 4.2),
        gridspec_kw={"width_ratios": [1.05, 1.15, 0.70]},
    )

    ax0.set_title("Interior Jovian resonances")
    ax0.set_xlabel("semimajor axis [AU]")
    ax0.set_yticks([])
    ax0.set_xlim(1.8, 5.35)
    ax0.set_ylim(-0.12, 0.18)
    ax0.axhline(0.0, color="0.75", linewidth=1.0)
    for item in resonances:
        a = float(item["a_au"])
        ax0.axvline(a, color="tab:red", alpha=0.45)
        ax0.text(a, 0.055, str(item["label"]), rotation=90, va="bottom", ha="right")
    ax0.scatter([A_JUPITER], [0.0], color="tab:orange", s=30, label="Jupiter")
    ax0.legend(frameon=False, loc="upper left")

    for label in RESONANCE_RATIOS:
        data = [row for row in widths if row["resonance"] == label]
        ax1.plot(
            [row["eccentricity"] for row in data],
            [row["half_width_action_units"] for row in data],
            label=label,
        )
    width_21 = summary["width_2to1_disturbing_function"]
    ax1.plot(
        [row["eccentricity"] for row in width_21],
        [row["half_width_au"] for row in width_21],
        color="black",
        linestyle="--",
        linewidth=1.6,
        label="2:1 actual [AU]",
    )
    ax1.set_title("Normal-form width scaling")
    ax1.set_xlabel("eccentricity")
    ax1.set_ylabel(r"half-width: model units or AU")
    ax1.legend(frameon=False)

    phi = [row["phi"] for row in pendulum]
    ax2.plot(phi, [row["separatrix_positive"] for row in pendulum], color="0.25")
    ax2.plot(phi, [row["separatrix_negative"] for row in pendulum], color="0.25")
    ax2.set_title("Pendulum separatrix")
    ax2.set_xlabel(r"$\phi$")
    ax2.set_ylabel(r"$P$")
    ax2.set_xticks([-math.pi, 0, math.pi])
    ax2.set_xticklabels([r"$-\pi$", "0", r"$\pi$"])

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="use a small deterministic grid")
    parser.add_argument("--a-jupiter", type=float, default=A_JUPITER, help="Jupiter semimajor axis in AU")
    parser.add_argument("--epsilon", type=float, default=M_JUPITER_OVER_M_SUN, help="perturbation strength")
    parser.add_argument("--eta", type=float, default=1.0, help="coefficient in B_r(e)=eta e^r")
    parser.add_argument("--curvature", type=float, default=1.0, help="normal-form curvature A")
    parser.add_argument("--ecc-min", type=float, default=0.01, help="minimum eccentricity")
    parser.add_argument("--ecc-max", type=float, default=0.30, help="maximum eccentricity")
    parser.add_argument("--ecc-points", type=int, default=16, help="number of eccentricity samples")
    parser.add_argument("--points", type=int, default=121, help="pendulum phase samples")
    parser.add_argument("--quadrature-samples", type=int, default=8192, help="samples for one-angle quadrature")
    parser.add_argument("--check-samples", type=int, default=384, help="samples per angle for finite-difference check")
    parser.add_argument("--coefficient-check-eccentricity", type=float, default=1.0e-5, help="eccentricity for coefficient check")
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    parser.add_argument("--json-output", type=Path, default=None, help="write JSON summary")
    parser.add_argument("--csv", type=Path, default=None, help="write width-scaling CSV")
    parser.add_argument("--plot", type=Path, default=None, help="write summary plot")
    args = parser.parse_args()
    if args.quick:
        args.ecc_points = min(args.ecc_points, 6)
        args.points = min(args.points, 41)
        args.quadrature_samples = min(args.quadrature_samples, 2048)
        args.check_samples = min(args.check_samples, 160)
    if args.a_jupiter <= 0.0:
        parser.error("--a-jupiter must be > 0")
    if args.epsilon < 0.0:
        parser.error("--epsilon must be >= 0")
    if args.eta < 0.0:
        parser.error("--eta must be >= 0")
    if args.curvature == 0.0:
        parser.error("--curvature must be nonzero")
    if args.ecc_min < 0.0 or args.ecc_max < args.ecc_min:
        parser.error("eccentricity range must satisfy 0 <= ecc-min <= ecc-max")
    if args.ecc_points < 2:
        parser.error("--ecc-points must be >= 2")
    if args.points < 3:
        parser.error("--points must be >= 3")
    if args.quadrature_samples < 16:
        parser.error("--quadrature-samples must be >= 16")
    if args.check_samples < 16:
        parser.error("--check-samples must be >= 16")
    if not 0.0 < args.coefficient_check_eccentricity < 0.1:
        parser.error("--coefficient-check-eccentricity must be small and positive")
    return args


def main() -> None:
    args = parse_args()
    summary = build_summary(args)
    outputs: dict[str, str] = {}
    if args.csv is not None:
        write_csv(args.csv, summary["width_scaling"])
        outputs["csv"] = str(args.csv)
    if args.plot is not None:
        save_plot(args.plot, summary)
        outputs["plot"] = str(args.plot)
    if args.json_output is not None:
        outputs["json"] = str(args.json_output)
    if outputs:
        summary["outputs"] = outputs
    if args.json_output is not None:
        write_json(args.json_output, summary)
    if args.json:
        print(json.dumps(json_ready(summary), indent=2, sort_keys=True, allow_nan=False))
    else:
        print("resonance,p,q,order,a_au")
        for row in summary["resonances"]:
            print(f"{row['label']},{row['p']},{row['q']},{row['order']},{row['a_au']:.6f}")
        if args.csv is not None:
            print(f"wrote_csv={args.csv}")
        if args.plot is not None:
            print(f"wrote_plot={args.plot}")
        if args.json_output is not None:
            print(f"wrote_json={args.json_output}")


if __name__ == "__main__":
    main()
