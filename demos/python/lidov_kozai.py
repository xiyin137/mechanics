#!/usr/bin/env python3
"""Quadrupole Lidov-Kozai dynamics for a test-particle hierarchical triple.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

The model is the circular, test-particle quadrupole limit.  The outer
angular-momentum axis is fixed.  The inner orbit is described by

    j = sqrt(1 - e^2),          h = j cos(i),

where e is inner eccentricity and i is the mutual inclination.  The component
h is conserved after double averaging.  With the irrelevant scale removed, the
quadrupole Hamiltonian is

    H = 1 - 6 e^2 - 3 h^2
        + 15 e^2 (1 - h^2 / j^2) sin^2(omega),

where omega is the argument of periapse.  The pair (omega, j) is canonical up
to the fixed Kepler action scale.

The trajectory integrator is classical RK4.  It is intentionally transparent
for lecture use, but it is not symplectic and does not preserve the reduced
Hamiltonian exactly.  The JSON and text output report Hamiltonian drift; the
regression test for the quick configuration requires drift below 5e-5.
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
    inclination_deg: float
    eccentricity: float
    omega_deg: float
    tau_max: float
    dt: float
    grid: int
    j_floor: float = 1.0e-8


def h_from_elements(eccentricity: float, inclination_rad: float) -> float:
    if not 0.0 <= eccentricity < 1.0:
        raise ValueError("eccentricity must satisfy 0 <= e < 1")
    return math.sqrt(1.0 - eccentricity * eccentricity) * math.cos(inclination_rad)


def hamiltonian(j: np.ndarray | float, omega: np.ndarray | float, h: float) -> np.ndarray | float:
    j_arr = np.asarray(j)
    omega_arr = np.asarray(omega)
    safe_j2 = np.maximum(j_arr * j_arr, 1.0e-15)
    e2 = 1.0 - j_arr * j_arr
    sin_i2 = 1.0 - h * h / safe_j2
    value = 1.0 - 6.0 * e2 - 3.0 * h * h + 15.0 * e2 * sin_i2 * np.sin(omega_arr) ** 2
    if np.isscalar(j) and np.isscalar(omega):
        return float(value)
    return value


def j_domain(h: float, j_floor: float) -> tuple[float, float]:
    """Return the regular numerical chart used for the (omega, j) variables."""
    return max(abs(h), j_floor), 1.0


def equations(state: np.ndarray, h: float) -> np.ndarray:
    omega, j = float(state[0]), float(state[1])
    if j <= 0.0:
        raise ValueError("j must remain positive in the Lidov-Kozai chart")
    e2 = 1.0 - j * j
    sin_i2 = 1.0 - h * h / (j * j)
    d_h_d_omega = 15.0 * e2 * sin_i2 * math.sin(2.0 * omega)
    d_ab_d_j = -2.0 * j + 2.0 * h * h / (j**3)
    d_h_d_j = 12.0 * j + 15.0 * math.sin(omega) ** 2 * d_ab_d_j
    return np.array([d_h_d_j, -d_h_d_omega], dtype=float)


def rk4_step(state: np.ndarray, dt: float, h: float) -> np.ndarray:
    k1 = equations(state, h)
    k2 = equations(state + 0.5 * dt * k1, h)
    k3 = equations(state + 0.5 * dt * k2, h)
    k4 = equations(state + dt * k3, h)
    out = state + dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    out[0] = (out[0] + math.pi) % (2.0 * math.pi) - math.pi
    return out


def integrate(cfg: Config) -> dict[str, object]:
    inclination = math.radians(cfg.inclination_deg)
    omega0 = math.radians(cfg.omega_deg)
    h = h_from_elements(cfg.eccentricity, inclination)
    j0_physical = math.sqrt(1.0 - cfg.eccentricity * cfg.eccentricity)
    j_lower, j_upper = j_domain(h, cfg.j_floor)
    j_seed_upper = 1.0 - cfg.j_floor
    if j_lower >= j_upper:
        raise ValueError("j_floor leaves no regular Lidov-Kozai chart for this inclination")
    j0 = min(max(j0_physical, j_lower), j_seed_upper)
    initial_j_adjusted = abs(j0 - j0_physical) > 0.0
    steps = int(round(cfg.tau_max / cfg.dt))
    times = [0.0]
    states = [np.array([omega0, j0], dtype=float)]
    termination: dict[str, object] | None = None
    for index in range(steps):
        try:
            proposed = rk4_step(states[-1], cfg.dt, h)
        except ValueError as exc:
            termination = {
                "reason": "intermediate_state_left_regular_chart",
                "message": str(exc),
                "step": index,
                "tau": times[-1],
            }
            break
        if not j_lower <= proposed[1] <= j_upper:
            termination = {
                "reason": "j_boundary",
                "step": index + 1,
                "tau": times[-1] + cfg.dt,
                "proposed_j": float(proposed[1]),
                "j_lower": j_lower,
                "j_upper": j_upper,
            }
            break
        states.append(proposed)
        times.append(times[-1] + cfg.dt)
    states_array = np.vstack(states)
    times_array = np.array(times)
    completed_steps = len(states_array) - 1
    eccentricity = np.sqrt(np.maximum(0.0, 1.0 - states_array[:, 1] ** 2))
    inclination_series = np.degrees(np.arccos(np.clip(h / states_array[:, 1], -1.0, 1.0)))
    energy = hamiltonian(states_array[:, 1], states_array[:, 0], h)
    critical = math.degrees(math.acos(math.sqrt(3.0 / 5.0)))
    emax_formula = (
        math.sqrt(max(0.0, 1.0 - (5.0 / 3.0) * math.cos(inclination) ** 2))
        if cfg.eccentricity == 0.0
        else float("nan")
    )
    return {
        "model": {
            "name": "quadrupole Lidov-Kozai test-particle limit",
            "hamiltonian_scale": "dimensionless; positive constant factors omitted",
            "canonical_pair": "(omega, j) at fixed Kepler action and fixed h=j cos(i)",
            "integrator": "classical RK4; transparent but not symplectic",
            "diagnostic_note": "monitor hamiltonian_max_abs_drift and repeat with smaller dt for long runs",
        },
        "configuration": {
            "inclination_deg": cfg.inclination_deg,
            "eccentricity": cfg.eccentricity,
            "omega_deg": cfg.omega_deg,
            "tau_max": cfg.tau_max,
            "dt": cfg.dt,
            "j_floor": cfg.j_floor,
        },
        "constants": {
            "h": h,
            "critical_inclination_deg": critical,
            "analytic_emax_initially_circular": emax_formula,
            "j_lower_limit": j_lower,
            "j_upper_limit": j_upper,
            "initial_j_upper_seed_limit": j_seed_upper,
        },
        "diagnostics": {
            "eccentricity_max_numeric": float(np.max(eccentricity)),
            "eccentricity_min_numeric": float(np.min(eccentricity)),
            "inclination_min_deg": float(np.min(inclination_series)),
            "inclination_max_deg": float(np.max(inclination_series)),
            "hamiltonian_initial": float(energy[0]),
            "hamiltonian_max_abs_drift": float(np.max(np.abs(energy - energy[0]))),
            "quick_test_hamiltonian_drift_bound": 5.0e-5,
            "initial_j_physical": j0_physical,
            "initial_j_used": j0,
            "initial_eccentricity_used": float(math.sqrt(max(0.0, 1.0 - j0 * j0))),
            "initial_j_adjusted_for_regular_chart": initial_j_adjusted,
            "steps_requested": steps,
            "steps_completed": completed_steps,
            "boundary_termination": termination,
        },
        "trajectory": [
            {
                "tau": float(times_array[i]),
                "omega": float(states_array[i, 0]),
                "j": float(states_array[i, 1]),
                "eccentricity": float(eccentricity[i]),
                "inclination_deg": float(inclination_series[i]),
            }
            for i in np.linspace(0, completed_steps, min(201, completed_steps + 1), dtype=int)
        ],
        "outputs": {},
    }


def phase_portrait_rows(h: float, grid: int) -> list[dict[str, float | None]]:
    omegas = np.linspace(-math.pi, math.pi, grid)
    j_min = abs(h) + 1.0e-4
    js = np.linspace(j_min, 0.999, grid)
    rows: list[dict[str, float | None]] = []
    for omega in omegas:
        for j in js:
            e = math.sqrt(max(0.0, 1.0 - j * j))
            inc = math.degrees(math.acos(np.clip(h / j, -1.0, 1.0)))
            rows.append(
                {
                    "omega": float(omega),
                    "j": float(j),
                    "eccentricity": e,
                    "inclination_deg": inc,
                    "hamiltonian": float(hamiltonian(j, omega, h)),
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
    h = float(summary["constants"]["h"])
    rows = phase_portrait_rows(h, cfg.grid)
    omega = np.array([row["omega"] for row in rows])
    ecc = np.array([row["eccentricity"] for row in rows])
    energy = np.array([row["hamiltonian"] for row in rows])
    trajectory = summary["trajectory"]
    traj_omega = np.array([row["omega"] for row in trajectory])
    traj_e = np.array([row["eccentricity"] for row in trajectory])
    traj_tau = np.array([row["tau"] for row in trajectory])
    phase_omega = traj_omega.copy()
    phase_e = traj_e.copy()
    singular_mask = phase_e < max(5.0e-3, 2.0 * float(summary["diagnostics"]["initial_eccentricity_used"]))
    phase_omega[singular_mask] = np.nan
    phase_e[singular_mask] = np.nan
    wrap_jumps = np.abs(np.diff(traj_omega)) > math.pi
    jump_indices = np.nonzero(wrap_jumps)[0] + 1
    phase_omega[jump_indices] = np.nan
    phase_e[jump_indices] = np.nan

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10.5, 4.4))
    contour = ax0.tricontour(omega, ecc, energy, levels=18, colors="0.55", linewidths=0.8)
    ax0.clabel(contour, inline=True, fontsize=7, fmt="%.1f")
    ax0.plot(phase_omega, phase_e, color="tab:blue", linewidth=2.0)
    ax0.scatter(phase_omega, phase_e, color="tab:blue", s=8, zorder=3)
    ax0.set_xlabel(r"$\omega$")
    ax0.set_ylabel("eccentricity")
    ax0.set_title("Lidov-Kozai phase portrait")
    ax0.set_xlim(-math.pi, math.pi)
    ax0.set_ylim(0.0, 1.0)

    ax1.plot(traj_tau, traj_e, color="tab:blue", label="e")
    emax = summary["constants"]["analytic_emax_initially_circular"]
    if emax is not None:
        ax1.axhline(float(emax), color="tab:red", linestyle="--", label="analytic emax")
    ax1.set_xlabel(r"dimensionless time $\tau$")
    ax1.set_ylabel("eccentricity")
    ax1.set_title("Eccentricity-inclination exchange")
    ax1.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="short deterministic classroom run")
    parser.add_argument("--inclination-deg", type=float, default=65.0, help="initial mutual inclination")
    parser.add_argument("--eccentricity", type=float, default=0.0, help="initial inner eccentricity")
    parser.add_argument("--omega-deg", type=float, default=10.0, help="initial argument of periapse")
    parser.add_argument("--tau-max", type=float, default=8.0, help="dimensionless integration horizon")
    parser.add_argument("--dt", type=float, default=0.002, help="dimensionless step")
    parser.add_argument("--grid", type=int, default=80, help="phase-portrait grid per axis")
    parser.add_argument(
        "--j-floor",
        type=float,
        default=1.0e-8,
        help="regular-chart floor for j; exact circular starts are seeded at j=1-j_floor",
    )
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    parser.add_argument("--json-output", type=Path, default=None, help="write JSON summary")
    parser.add_argument("--plot", type=Path, default=None, help="write phase-portrait plot")
    args = parser.parse_args()
    if args.quick:
        args.tau_max = min(args.tau_max, 4.0)
        args.grid = min(args.grid, 48)
    if not 0.0 <= args.eccentricity < 1.0:
        parser.error("--eccentricity must satisfy 0 <= e < 1")
    if args.tau_max < 0.0:
        parser.error("--tau-max must be >= 0")
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    if args.grid < 12:
        parser.error("--grid must be >= 12")
    if not 0.0 < args.j_floor < 1.0e-3:
        parser.error("--j-floor must satisfy 0 < j_floor < 1e-3")
    h = h_from_elements(args.eccentricity, math.radians(args.inclination_deg))
    if abs(h) >= 1.0:
        parser.error("initial j cos(i) must have absolute value < 1")
    return args


def main() -> None:
    args = parse_args()
    cfg = Config(
        inclination_deg=args.inclination_deg,
        eccentricity=args.eccentricity,
        omega_deg=args.omega_deg,
        tau_max=args.tau_max,
        dt=args.dt,
        grid=args.grid,
        j_floor=args.j_floor,
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
        print(f"h={summary['constants']['h']:.8f}")
        print(f"critical_inclination_deg={summary['constants']['critical_inclination_deg']:.6f}")
        print(f"eccentricity_max_numeric={summary['diagnostics']['eccentricity_max_numeric']:.6f}")
        print(f"hamiltonian_max_abs_drift={summary['diagnostics']['hamiltonian_max_abs_drift']:.6e}")
        print(f"initial_eccentricity_used={summary['diagnostics']['initial_eccentricity_used']:.6e}")
        termination = summary["diagnostics"]["boundary_termination"]
        if termination is not None:
            print(f"terminated={termination['reason']}")
        if args.plot is not None:
            print(f"wrote_plot={args.plot}")
        if args.json_output is not None:
            print(f"wrote_json={args.json_output}")


if __name__ == "__main__":
    main()
