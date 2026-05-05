#!/usr/bin/env python3
"""Heavy symmetric top reduced to a one-dimensional nutation problem.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

The top has a fixed point, principal moments I1=I2 and I3, and center of mass
on the symmetry axis.  Euler angles give two cyclic momenta:

    p_phi = space-vertical angular momentum,
    p_psi = body-axis spin angular momentum.

The remaining angle theta evolves in the effective potential

    U(theta) = (p_phi - p_psi cos theta)^2 / (2 I1 sin^2 theta)
             + p_psi^2 / (2 I3) + m g ell cos theta.

This script integrates (theta, p_theta), reconstructs phi and psi, and reports
the conserved quantities.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class Config:
    i1: float
    i3: float
    mgl: float
    p_phi: float
    p_psi: float
    theta0: float
    p_theta0: float
    t_max: float
    dt: float
    grid: int


def effective_potential(theta: np.ndarray | float, cfg: Config) -> np.ndarray | float:
    theta_arr = np.asarray(theta)
    sin_theta = np.sin(theta_arr)
    safe_sin2 = np.maximum(sin_theta * sin_theta, 1.0e-14)
    cos_theta = np.cos(theta_arr)
    value = (
        (cfg.p_phi - cfg.p_psi * cos_theta) ** 2 / (2.0 * cfg.i1 * safe_sin2)
        + cfg.p_psi**2 / (2.0 * cfg.i3)
        + cfg.mgl * cos_theta
    )
    if np.isscalar(theta):
        return float(value)
    return value


def d_effective_potential(theta: float, cfg: Config) -> float:
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)
    safe_sin = math.copysign(max(abs(sin_theta), 1.0e-8), sin_theta if sin_theta != 0.0 else 1.0)
    a = cfg.p_phi - cfg.p_psi * cos_theta
    return (
        a * cfg.p_psi / (cfg.i1 * safe_sin)
        - a * a * cos_theta / (cfg.i1 * safe_sin**3)
        - cfg.mgl * sin_theta
    )


def rates(theta: float, p_theta: float, cfg: Config) -> tuple[float, float, float]:
    sin_theta = math.sin(theta)
    safe_sin2 = max(sin_theta * sin_theta, 1.0e-14)
    cos_theta = math.cos(theta)
    theta_dot = p_theta / cfg.i1
    phi_dot = (cfg.p_phi - cfg.p_psi * cos_theta) / (cfg.i1 * safe_sin2)
    psi_dot = cfg.p_psi / cfg.i3 - phi_dot * cos_theta
    return theta_dot, phi_dot, psi_dot


def rhs(state: np.ndarray, cfg: Config) -> np.ndarray:
    theta, p_theta, phi, psi = map(float, state)
    theta_dot, phi_dot, psi_dot = rates(theta, p_theta, cfg)
    return np.array([theta_dot, -d_effective_potential(theta, cfg), phi_dot, psi_dot], dtype=float)


def rk4_step(state: np.ndarray, dt: float, cfg: Config) -> np.ndarray:
    k1 = rhs(state, cfg)
    k2 = rhs(state + 0.5 * dt * k1, cfg)
    k3 = rhs(state + 0.5 * dt * k2, cfg)
    k4 = rhs(state + dt * k3, cfg)
    out = state + dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    eps = 1.0e-6
    if out[0] < eps:
        out[0] = eps
        out[1] *= -1.0
    if out[0] > math.pi - eps:
        out[0] = math.pi - eps
        out[1] *= -1.0
    return out


def energy(theta: np.ndarray, p_theta: np.ndarray, cfg: Config) -> np.ndarray:
    return p_theta * p_theta / (2.0 * cfg.i1) + effective_potential(theta, cfg)


def steady_precession_residual(theta: float, cfg: Config) -> float:
    return d_effective_potential(theta, cfg)


def integrate(cfg: Config) -> dict[str, object]:
    steps = int(round(cfg.t_max / cfg.dt))
    times = np.linspace(0.0, steps * cfg.dt, steps + 1)
    states = np.zeros((steps + 1, 4), dtype=float)
    states[0] = np.array([cfg.theta0, cfg.p_theta0, 0.0, 0.0], dtype=float)
    for index in range(steps):
        states[index + 1] = rk4_step(states[index], cfg.dt, cfg)
    energies = energy(states[:, 0], states[:, 1], cfg)
    theta_grid = np.linspace(0.04, math.pi - 0.04, cfg.grid)
    potential = effective_potential(theta_grid, cfg)
    turning_mask = potential <= energies[0]
    turning_angles = theta_grid[turning_mask]
    return {
        "model": {
            "name": "heavy symmetric top",
            "coordinates": "Euler angles with cyclic phi and psi",
            "effective_potential": "theta-only reduction at fixed p_phi and p_psi",
        },
        "configuration": {
            "i1": cfg.i1,
            "i3": cfg.i3,
            "mgl": cfg.mgl,
            "p_phi": cfg.p_phi,
            "p_psi": cfg.p_psi,
            "theta0": cfg.theta0,
            "p_theta0": cfg.p_theta0,
            "t_max": cfg.t_max,
            "dt": cfg.dt,
        },
        "diagnostics": {
            "energy_initial": float(energies[0]),
            "energy_max_abs_drift": float(np.max(np.abs(energies - energies[0]))),
            "theta_min": float(np.min(states[:, 0])),
            "theta_max": float(np.max(states[:, 0])),
            "turning_theta_min_grid": float(np.min(turning_angles)) if len(turning_angles) else None,
            "turning_theta_max_grid": float(np.max(turning_angles)) if len(turning_angles) else None,
            "steady_precession_residual_theta0": steady_precession_residual(cfg.theta0, cfg),
        },
        "trajectory": [
            {
                "t": float(times[i]),
                "theta": float(states[i, 0]),
                "p_theta": float(states[i, 1]),
                "phi": float(states[i, 2]),
                "psi": float(states[i, 3]),
                "energy": float(energies[i]),
            }
            for i in np.linspace(0, steps, min(201, steps + 1), dtype=int)
        ],
        "outputs": {},
    }


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


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(json_ready(data), handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")


def save_plot(path: Path, summary: dict[str, object], cfg: Config) -> None:
    import os

    os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache")))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    theta_grid = np.linspace(0.04, math.pi - 0.04, 500)
    potential = effective_potential(theta_grid, cfg)
    trajectory = summary["trajectory"]
    t = np.array([row["t"] for row in trajectory])
    theta = np.array([row["theta"] for row in trajectory])
    energy0 = float(summary["diagnostics"]["energy_initial"])
    theta_turn_min = summary["diagnostics"].get("turning_theta_min_grid")
    theta_turn_max = summary["diagnostics"].get("turning_theta_max_grid")

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10.5, 4.4))
    ax0.plot(theta_grid, potential, color="0.25")
    ax0.axhline(energy0, color="tab:red", linestyle="--", label="energy")
    ax0.axvline(cfg.theta0, color="tab:blue", alpha=0.65, label="initial theta")
    if theta_turn_min is not None and theta_turn_max is not None:
        ax0.axvline(float(theta_turn_min), color="tab:green", linestyle=":", linewidth=1.4, label="turning points")
        ax0.axvline(float(theta_turn_max), color="tab:green", linestyle=":", linewidth=1.4)
    accessible = potential[potential <= energy0]
    if len(accessible):
        margin = max(0.08, 0.18 * max(1.0, float(np.ptp(accessible))))
        ax0.set_ylim(float(np.min(accessible) - margin), float(energy0 + margin))
    ax0.set_xlabel(r"$\theta$")
    ax0.set_ylabel(r"$U_{\rm eff}(\theta)$")
    ax0.set_title("Heavy-top effective potential")
    ax0.legend(frameon=False)

    ax1.plot(t, theta, color="tab:blue")
    if theta_turn_min is not None and theta_turn_max is not None:
        ax1.axhline(float(theta_turn_min), color="tab:green", linestyle=":", linewidth=1.4, label="turning points")
        ax1.axhline(float(theta_turn_max), color="tab:green", linestyle=":", linewidth=1.4)
    ax1.set_xlabel("time")
    ax1.set_ylabel(r"$\theta(t)$")
    ax1.set_title("Nutation")
    if theta_turn_min is not None and theta_turn_max is not None:
        ax1.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="short deterministic classroom run")
    parser.add_argument("--i1", type=float, default=1.0, help="transverse moment of inertia")
    parser.add_argument("--i3", type=float, default=0.45, help="symmetry-axis moment of inertia")
    parser.add_argument("--mgl", type=float, default=0.4, help="gravity parameter m g ell")
    parser.add_argument("--p-phi", type=float, default=1.15, help="space-vertical angular momentum")
    parser.add_argument("--p-psi", type=float, default=0.9, help="body-axis spin momentum")
    parser.add_argument("--theta0", type=float, default=0.75, help="initial nutation angle")
    parser.add_argument("--p-theta0", type=float, default=0.08, help="initial theta momentum")
    parser.add_argument("--t-max", type=float, default=40.0, help="integration horizon")
    parser.add_argument("--dt", type=float, default=0.004, help="time step")
    parser.add_argument("--grid", type=int, default=600, help="effective-potential diagnostic grid")
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    parser.add_argument("--json-output", type=Path, default=None, help="write JSON summary")
    parser.add_argument("--plot", type=Path, default=None, help="write potential/nutation plot")
    args = parser.parse_args()
    if args.quick:
        args.t_max = min(args.t_max, 16.0)
        args.dt = max(args.dt, 0.008)
        args.grid = min(args.grid, 300)
    if min(args.i1, args.i3) <= 0.0:
        parser.error("moments of inertia must be positive")
    if not 0.0 < args.theta0 < math.pi:
        parser.error("--theta0 must lie between 0 and pi")
    if args.t_max < 0.0:
        parser.error("--t-max must be >= 0")
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    if args.grid < 20:
        parser.error("--grid must be >= 20")
    return args


def main() -> None:
    args = parse_args()
    cfg = Config(
        i1=args.i1,
        i3=args.i3,
        mgl=args.mgl,
        p_phi=args.p_phi,
        p_psi=args.p_psi,
        theta0=args.theta0,
        p_theta0=args.p_theta0,
        t_max=args.t_max,
        dt=args.dt,
        grid=args.grid,
    )
    summary = integrate(cfg)
    outputs: dict[str, str] = {}
    if args.plot is not None:
        save_plot(args.plot, summary, cfg)
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
        print(f"energy_initial={summary['diagnostics']['energy_initial']:.8f}")
        print(f"energy_max_abs_drift={summary['diagnostics']['energy_max_abs_drift']:.6e}")
        print(f"theta_min={summary['diagnostics']['theta_min']:.6f}")
        print(f"theta_max={summary['diagnostics']['theta_max']:.6f}")
        if args.plot is not None:
            print(f"wrote_plot={args.plot}")
        if args.json_output is not None:
            print(f"wrote_json={args.json_output}")


if __name__ == "__main__":
    main()
