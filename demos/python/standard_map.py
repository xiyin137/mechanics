#!/usr/bin/env python3
"""Standard map phase portrait demo on the compact two-torus.

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


TWOPI = 2.0 * math.pi
K_PRESETS = {"small": 0.25, "near-critical": 0.95, "large": 1.6}
DEFAULTS = {"K": 0.95, "orbits": 80, "steps": 800, "seed": 3}
RUN_PRESETS = {
    "quick": {"orbits": 8, "steps": 40},
    "lecture": {"orbits": 80, "steps": 800},
    "long": {"orbits": 200, "steps": 5000},
}


def iterate_standard_map(q0: np.ndarray, p0: np.ndarray, K: float, steps: int) -> tuple[np.ndarray, np.ndarray]:
    if q0.shape != p0.shape:
        raise ValueError("q0 and p0 must have the same shape")
    if steps < 0:
        raise ValueError("steps must be >= 0")
    q = np.empty((steps + 1, len(q0)))
    p = np.empty_like(q)
    q[0] = q0 % TWOPI
    p[0] = p0 % TWOPI
    for n in range(steps):
        p[n + 1] = (p[n] + K * np.sin(q[n])) % TWOPI
        q[n + 1] = (q[n] + p[n + 1]) % TWOPI
    return q, p


def iterate_standard_map_lift(q0: np.ndarray, p0: np.ndarray, K: float, steps: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if q0.shape != p0.shape:
        raise ValueError("q0 and p0 must have the same shape")
    if steps < 0:
        raise ValueError("steps must be >= 0")
    q_mod = np.empty((steps + 1, len(q0)))
    q_lift = np.empty_like(q_mod)
    p = np.empty_like(q_mod)
    q_lift[0] = q0
    q_mod[0] = q0 % TWOPI
    p[0] = p0 % TWOPI
    for n in range(steps):
        p[n + 1] = (p[n] + K * np.sin(q_mod[n])) % TWOPI
        q_lift[n + 1] = q_lift[n] + p[n + 1]
        q_mod[n + 1] = q_lift[n + 1] % TWOPI
    return q_mod, p, q_lift


def finite_rotation_numbers(q_lift: np.ndarray) -> np.ndarray:
    steps = q_lift.shape[0] - 1
    if steps <= 0:
        return np.zeros(q_lift.shape[1])
    return (q_lift[-1] - q_lift[0]) / (TWOPI * steps)


def save_plot(path: Path, q: np.ndarray, p: np.ndarray, K: float) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.plot(q.reshape(-1), p.reshape(-1), ".", markersize=0.35, alpha=0.65)
    ax.set_xlim(0.0, TWOPI)
    ax.set_ylim(0.0, TWOPI)
    ax.set_xlabel("q mod 2pi")
    ax.set_ylabel("p mod 2pi")
    ax.set_title(f"Standard map, K={K:g}")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def build_summary(args: argparse.Namespace, q: np.ndarray, p: np.ndarray, q_lift: np.ndarray) -> dict[str, object]:
    rotation = finite_rotation_numbers(q_lift)
    return {
        "model": "standard map on the two-torus",
        "map": {
            "p_next": "p + K sin(q) mod 2*pi",
            "q_next": "q + p_next mod 2*pi",
        },
        "configuration": {"K": args.K, "orbits": args.orbits, "steps": args.steps, "seed": args.seed},
        "points": int(q.size),
        "finite_rotation_mean": float(np.mean(rotation)),
        "finite_rotation_std": float(np.std(rotation)),
        "q_range": [float(np.min(q)), float(np.max(q))],
        "p_range": [float(np.min(p)), float(np.max(p))],
        "diagnostic_note": "Finite rotation numbers over short times are descriptive diagnostics, not invariant-torus proofs.",
        "outputs": {},
    }


def print_summary(summary: dict[str, object]) -> None:
    config = summary["configuration"]
    print(f"K={config['K']}")
    print(f"orbits={config['orbits']}")
    print(f"steps={config['steps']}")
    print(f"points={summary['points']}")
    print(f"finite_rotation_mean={summary['finite_rotation_mean']:.12g}")
    print(f"finite_rotation_std={summary['finite_rotation_std']:.12g}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_preset_args(parser)
    parser.add_argument("--preset", choices=sorted(K_PRESETS), default=None, help="standard K preset")
    parser.add_argument("--K", type=float, default=None)
    parser.add_argument("--orbits", type=int, default=None)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--plot", type=Path, default=None)
    add_output_args(parser)
    args = parser.parse_args()
    defaults = dict(DEFAULTS)
    if args.quick:
        defaults.update(RUN_PRESETS["quick"])
    elif args.lecture:
        defaults.update(RUN_PRESETS["lecture"])
    elif args.long:
        defaults.update(RUN_PRESETS["long"])
    if args.preset is not None and args.K is None:
        defaults["K"] = K_PRESETS[args.preset]
    fill_defaults(args, defaults)
    configure_standard_outputs(args, stem="standard_map", plot_name="standard_map.png")
    if args.orbits < 1:
        parser.error("--orbits must be >= 1")
    if args.steps < 0:
        parser.error("--steps must be >= 0")
    return args


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    q0 = rng.uniform(0.0, TWOPI, args.orbits)
    p0 = rng.uniform(0.0, TWOPI, args.orbits)
    q, p, q_lift = iterate_standard_map_lift(q0, p0, args.K, args.steps)
    if args.plot is not None:
        save_plot(args.plot, q, p, args.K)
    summary = build_summary(args, q, p, q_lift)
    emit_summary(summary, args, print_summary)


if __name__ == "__main__":
    main()
