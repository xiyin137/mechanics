#!/usr/bin/env python3
"""Hamiltonian pendulum demo with a symplectic Euler integrator.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

try:
    from demos.python.common import add_output_args, add_preset_args, configure_standard_outputs, emit_summary, fill_defaults
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from common import add_output_args, add_preset_args, configure_standard_outputs, emit_summary, fill_defaults


DEFAULTS = {"q0": 1.0, "p0": 0.0, "dt": 0.02, "steps": 5000}
PRESETS = {
    "quick": {"dt": 0.02, "steps": 200},
    "lecture": {"dt": 0.02, "steps": 5000},
    "long": {"dt": 0.01, "steps": 50000},
}
SEPARATRIX_ENERGY = 2.0


def integrate(q0: float, p0: float, dt: float, steps: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if dt <= 0.0:
        raise ValueError("dt must be > 0")
    if steps < 0:
        raise ValueError("steps must be >= 0")
    time = np.arange(steps + 1) * dt
    q = np.empty(steps + 1)
    p = np.empty(steps + 1)
    q[0] = q0
    p[0] = p0
    for n in range(steps):
        p[n + 1] = p[n] - dt * math.sin(q[n])
        q[n + 1] = q[n] + dt * p[n + 1]
    return time, q, p


def hamiltonian(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    return 0.5 * p * p + 1.0 - np.cos(q)


def phase_region(energy: float, tolerance: float = 1.0e-3) -> str:
    if abs(energy - SEPARATRIX_ENERGY) <= tolerance:
        return "near_separatrix"
    if energy < SEPARATRIX_ENERGY:
        return "libration"
    return "rotation"


def save_plot(path: Path, time: np.ndarray, q: np.ndarray, p: np.ndarray) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    H = hamiltonian(q, p)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].plot(((q + math.pi) % (2.0 * math.pi)) - math.pi, p, linewidth=0.9)
    axes[0].set_xlabel("q mod 2pi")
    axes[0].set_ylabel("p")
    axes[0].set_title("phase curve")

    axes[1].plot(time, H - H[0])
    axes[1].set_xlabel("time")
    axes[1].set_ylabel("energy drift")
    axes[1].set_title("symplectic Euler drift")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def build_summary(args: argparse.Namespace, time: np.ndarray, q: np.ndarray, p: np.ndarray) -> dict[str, object]:
    energy = hamiltonian(q, p)
    drift = energy - energy[0]
    return {
        "model": "Hamiltonian pendulum",
        "equations": {"q_dot": "p", "p_dot": "-sin(q)"},
        "integrator": "symplectic Euler kick-drift",
        "configuration": {
            "q0": args.q0,
            "p0": args.p0,
            "dt": args.dt,
            "steps": args.steps,
        },
        "separatrix_energy": SEPARATRIX_ENERGY,
        "phase_region": phase_region(float(energy[0])),
        "elapsed_time": float(time[-1]) if len(time) else 0.0,
        "energy_initial": float(energy[0]),
        "energy_final": float(energy[-1]),
        "energy_drift": float(energy[-1] - energy[0]),
        "energy_max_abs_drift": float(np.max(np.abs(drift))),
        "q_final": float(q[-1]),
        "p_final": float(p[-1]),
        "outputs": {},
    }


def print_summary(summary: dict[str, object]) -> None:
    print(f"steps={summary['configuration']['steps']}")
    print(f"energy_initial={summary['energy_initial']:.12g}")
    print(f"energy_final={summary['energy_final']:.12g}")
    print(f"energy_drift={summary['energy_drift']:.6e}")
    print(f"energy_max_abs_drift={summary['energy_max_abs_drift']:.6e}")
    print(f"separatrix_energy={summary['separatrix_energy']:.12g}")
    print(f"phase_region={summary['phase_region']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_preset_args(parser)
    parser.add_argument("--q0", type=float, default=None)
    parser.add_argument("--p0", type=float, default=None)
    parser.add_argument("--dt", type=float, default=None)
    parser.add_argument("--steps", type=int, default=None)
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
    configure_standard_outputs(args, stem="hamiltonian_pendulum", plot_name="hamiltonian_pendulum.png")
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    if args.steps < 0:
        parser.error("--steps must be >= 0")
    return args


def main() -> None:
    args = parse_args()
    time, q, p = integrate(args.q0, args.p0, args.dt, args.steps)
    if args.plot is not None:
        save_plot(args.plot, time, q, p)
    summary = build_summary(args, time, q, p)
    emit_summary(summary, args, print_summary)


if __name__ == "__main__":
    main()
