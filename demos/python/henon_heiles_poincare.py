#!/usr/bin/env python3
"""Poincare sections for the Henon-Heiles Hamiltonian.

The Hamiltonian is

    H = 1/2 (p_x^2 + p_y^2 + x^2 + y^2) + x^2 y - y^3/3.

This script integrates the flow with velocity Verlet and records upward
crossings of the section y=0, p_y>0.  It is designed to produce reproducible
lecture figures with explicit numerical diagnostics.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions
from Anthropic Opus 4.7.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path
from typing import Iterable

import numpy as np

try:
    from demos.python.common import (
        add_output_args,
        add_preset_args,
        configure_standard_outputs,
        emit_summary,
        fill_defaults,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from common import (
        add_output_args,
        add_preset_args,
        configure_standard_outputs,
        emit_summary,
        fill_defaults,
    )


ESCAPE_ENERGY = 1.0 / 6.0
DEFAULT_ENERGIES = (1.0 / 12.0, 1.0 / 8.0)
DEFAULTS = {"dt": 0.018, "crossings": 80, "rings": 4, "angles": 5}
RUN_PRESETS = {
    "quick": {"dt": 0.03, "crossings": 10, "rings": 2, "angles": 3},
    "lecture": {"dt": 0.018, "crossings": 80, "rings": 4, "angles": 5},
    "long": {"dt": 0.012, "crossings": 320, "rings": 8, "angles": 7},
}


def potential(x: np.ndarray | float, y: np.ndarray | float) -> np.ndarray | float:
    """Return the Henon-Heiles potential."""

    return 0.5 * (x * x + y * y) + x * x * y - y * y * y / 3.0


def hamiltonian(
    x: np.ndarray | float,
    y: np.ndarray | float,
    px: np.ndarray | float,
    py: np.ndarray | float,
) -> np.ndarray | float:
    """Return the total Henon-Heiles energy."""

    return 0.5 * (px * px + py * py) + potential(x, y)


def force(x: float, y: float) -> tuple[float, float]:
    """Return -grad V at the current configuration."""

    return -x * (1.0 + 2.0 * y), -y - x * x + y * y


def section_seeds(energy: float, *, rings: int, angles: int) -> list[tuple[float, float]]:
    """Choose deterministic initial points on the section y=0.

    The allowed disk on this section is x^2+p_x^2 <= 2E.  Ring sampling gives a
    stable lecture figure without relying on a random seed.
    """

    if energy <= 0.0:
        raise ValueError("energy must be positive")
    if energy >= ESCAPE_ENERGY:
        raise ValueError("use an energy below the escape value 1/6 for this demo")
    if rings <= 0 or angles <= 0:
        raise ValueError("rings and angles must be positive")

    radius = math.sqrt(2.0 * energy) * 0.995
    seeds: list[tuple[float, float]] = []
    for i, fraction in enumerate(np.linspace(0.12, 0.95, rings)):
        r = radius * float(fraction)
        count = max(5, int(round(angles * (1.0 + 0.25 * i))))
        phase = 0.37 * i
        for j in range(count):
            theta = 2.0 * math.pi * j / count + phase
            seeds.append((r * math.cos(theta), r * math.sin(theta)))
    return seeds


def initial_py(energy: float, x: float, px: float) -> float:
    """Return the positive p_y on y=0 at fixed energy."""

    remaining = 2.0 * (energy - 0.5 * (x * x + px * px))
    if remaining <= 0.0:
        raise ValueError("initial point lies outside the section energy disk")
    return math.sqrt(remaining)


def integrate_section_orbit(
    energy: float,
    x0: float,
    px0: float,
    *,
    dt: float,
    crossings: int,
    max_steps: int,
) -> tuple[np.ndarray, float]:
    """Integrate one orbit and return upward section crossings (x, p_x)."""

    if dt <= 0.0:
        raise ValueError("dt must be positive")
    if crossings <= 0:
        raise ValueError("crossings must be positive")

    x = float(x0)
    y = 0.0
    px = float(px0)
    py = initial_py(energy, x, px)
    h0 = float(hamiltonian(x, y, px, py))
    old_x, old_y, old_px, old_py = x, y, px, py
    section_points: list[tuple[float, float]] = []
    max_energy_drift = 0.0

    for step in range(max_steps):
        fx, fy = force(x, y)
        px_half = px + 0.5 * dt * fx
        py_half = py + 0.5 * dt * fy
        new_x = x + dt * px_half
        new_y = y + dt * py_half
        new_fx, new_fy = force(new_x, new_y)
        new_px = px_half + 0.5 * dt * new_fx
        new_py = py_half + 0.5 * dt * new_fy

        if step > 0 and old_y < 0.0 <= new_y:
            alpha = -old_y / (new_y - old_y)
            x_cross = old_x + alpha * (new_x - old_x)
            px_cross = old_px + alpha * (new_px - old_px)
            py_cross = old_py + alpha * (new_py - old_py)
            if py_cross > 0.0:
                section_points.append((x_cross, px_cross))
                if len(section_points) >= crossings:
                    max_energy_drift = max(
                        max_energy_drift,
                        abs(float(hamiltonian(new_x, new_y, new_px, new_py)) - h0),
                    )
                    break

        max_energy_drift = max(
            max_energy_drift,
            abs(float(hamiltonian(new_x, new_y, new_px, new_py)) - h0),
        )
        old_x, old_y, old_px, old_py = new_x, new_y, new_px, new_py
        x, y, px, py = new_x, new_y, new_px, new_py
    else:
        raise RuntimeError(
            f"orbit from x={x0:g}, px={px0:g} did not produce {crossings} crossings"
        )

    return np.asarray(section_points, dtype=float), max_energy_drift


def integrate_section(
    energy: float,
    seeds: Iterable[tuple[float, float]],
    *,
    dt: float,
    crossings: int,
) -> tuple[np.ndarray, dict[str, float]]:
    """Integrate a seed ensemble and collect all section crossings."""

    max_steps = max(10000, int(math.ceil(crossings * 180.0 / dt)))
    all_points: list[np.ndarray] = []
    max_drift = 0.0
    orbit_count = 0
    for x0, px0 in seeds:
        points, drift = integrate_section_orbit(
            energy,
            x0,
            px0,
            dt=dt,
            crossings=crossings,
            max_steps=max_steps,
        )
        all_points.append(points)
        max_drift = max(max_drift, drift)
        orbit_count += 1

    table = np.vstack(all_points) if all_points else np.empty((0, 2), dtype=float)
    diagnostics = {
        "energy": float(energy),
        "orbits": float(orbit_count),
        "points": float(table.shape[0]),
        "dt": float(dt),
        "crossings_per_orbit": float(crossings),
        "max_abs_energy_drift": float(max_drift),
    }
    return table, diagnostics


def data_name(energy: float) -> str:
    """Return a stable TeX-data filename stem."""

    return f"henon_heiles_section_E{int(round(energy * 1000000)):06d}.dat"


def write_section_table(path: Path, points: np.ndarray) -> None:
    """Write a pgfplots-friendly table with columns x and px."""

    path.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(path, points, fmt="%.10f", header="x px", comments="")


def save_plot(path: Path, sections: list[tuple[float, np.ndarray]]) -> None:
    """Save a Matplotlib preview of the computed Poincare sections."""

    os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".matplotlib-cache"))
    os.environ.setdefault("MPLBACKEND", "Agg")
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(
        1,
        len(sections),
        figsize=(4.8 * len(sections), 4.4),
        constrained_layout=True,
    )
    if len(sections) == 1:
        axes = [axes]

    for ax, (energy, points) in zip(axes, sections):
        ax.scatter(
            points[:, 0],
            points[:, 1],
            s=0.35,
            alpha=0.52,
            color="black",
            linewidths=0.0,
        )
        radius = math.sqrt(2.0 * energy)
        theta = np.linspace(0.0, 2.0 * math.pi, 300)
        ax.plot(radius * np.cos(theta), radius * np.sin(theta), "--", color="#b22222", lw=0.9)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-0.55, 0.55)
        ax.set_ylim(-0.55, 0.55)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$p_x$")
        ax.set_title(fr"$E={energy:.6g}$")
        ax.grid(alpha=0.18)

    fig.savefig(path, dpi=180)
    plt.close(fig)


def run_sections(
    args: argparse.Namespace,
) -> tuple[list[tuple[float, np.ndarray]], list[dict[str, float]]]:
    """Generate section tables and diagnostics for all requested energies."""

    sections: list[tuple[float, np.ndarray]] = []
    diagnostics: list[dict[str, float]] = []
    for energy in args.energy:
        seeds = section_seeds(energy, rings=args.rings, angles=args.angles)
        points, diag = integrate_section(energy, seeds, dt=args.dt, crossings=args.crossings)
        if args.tex_data_dir is not None:
            write_section_table(args.tex_data_dir / data_name(energy), points)
        sections.append((energy, points))
        diagnostics.append(diag)
    return sections, diagnostics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_preset_args(parser)
    parser.add_argument(
        "--energy",
        type=float,
        action="append",
        default=None,
        help="section energy; repeatable",
    )
    parser.add_argument("--dt", type=float, default=None, help="velocity-Verlet step size")
    parser.add_argument(
        "--crossings",
        type=int,
        default=None,
        help="crossings recorded per initial condition",
    )
    parser.add_argument(
        "--rings",
        type=int,
        default=None,
        help="number of deterministic seed rings",
    )
    parser.add_argument("--angles", type=int, default=None, help="base number of seeds per ring")
    parser.add_argument(
        "--tex-data-dir",
        type=Path,
        default=None,
        help="write pgfplots .dat files to this directory",
    )
    parser.add_argument("--plot", type=Path, default=None, help="optional preview PNG path")
    add_output_args(parser)
    args = parser.parse_args()

    preset = "lecture"
    if args.quick:
        preset = "quick"
    elif args.long:
        preset = "long"
    fill_defaults(args, {**DEFAULTS, **RUN_PRESETS[preset]})
    if args.energy is None:
        args.energy = list(DEFAULT_ENERGIES)
    configure_standard_outputs(
        args,
        stem="henon_heiles_poincare",
        plot_name="henon_heiles_poincare.png",
    )
    args.run_preset = preset
    return args


def print_text(summary: dict[str, object]) -> None:
    print("model=Henon-Heiles Hamiltonian")
    for section in summary["sections"]:  # type: ignore[index]
        diag = section  # type: ignore[assignment]
        print(
            "section "
            f"E={diag['energy']:.8g} "
            f"orbits={int(diag['orbits'])} "
            f"points={int(diag['points'])} "
            f"max_abs_energy_drift={diag['max_abs_energy_drift']:.3e}"
        )


def main() -> None:
    args = parse_args()
    sections, diagnostics = run_sections(args)
    if args.plot is not None:
        save_plot(args.plot, sections)
    summary = {
        "model": "Henon-Heiles Hamiltonian",
        "section": "y=0, p_y>0",
        "escape_energy": ESCAPE_ENERGY,
        "preset": args.run_preset,
        "configuration": {
            "dt": args.dt,
            "crossings": args.crossings,
            "rings": args.rings,
            "angles": args.angles,
            "energies": args.energy,
        },
        "sections": diagnostics,
    }
    if args.tex_data_dir is not None:
        summary["outputs"] = {"tex_data_dir": str(args.tex_data_dir)}
    emit_summary(summary, args, print_text)


if __name__ == "__main__":
    main()
