#!/usr/bin/env python3
"""Stable/unstable manifolds and a homoclinic tangle for the standard map.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions
from Anthropic Opus 4.7.

The map convention is

    p_{n+1} = p_n + K sin(q_n),
    q_{n+1} = q_n + p_{n+1},

with both coordinates reduced modulo 2*pi and displayed in the centered square
[-pi, pi] x [-pi, pi].  The fixed point (q,p)=(0,0) is hyperbolic for K>0.
The unstable manifold is computed by iterating a tiny segment tangent to the
unstable eigenvector of the linearized map.  The stable manifold is computed by
iterating a tiny segment tangent to the stable eigenvector under the inverse
map.  This is a visualization of invariant-manifold geometry, not a rigorous
intersection finder.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Iterable

import numpy as np

try:
    from demos.python.common import add_output_args, add_preset_args, configure_standard_outputs, emit_summary
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from common import add_output_args, add_preset_args, configure_standard_outputs, emit_summary


TWOPI = 2.0 * math.pi
DEFAULTS = {"K": 1.8, "samples": 520, "iterates": 20, "local_extent": 3.0e-9}
RUN_PRESETS = {
    "quick": {"samples": 520, "iterates": 20, "local_extent": 3.0e-9},
    "lecture": {"samples": 850, "iterates": 21, "local_extent": 3.0e-9},
    "long": {"samples": 1200, "iterates": 23, "local_extent": 8.0e-10},
}


def centered_mod(x: np.ndarray | float) -> np.ndarray | float:
    """Reduce an angle-like coordinate to [-pi, pi)."""

    return (np.asarray(x) + math.pi) % TWOPI - math.pi


def standard_map_step(q: np.ndarray, p: np.ndarray, K: float) -> tuple[np.ndarray, np.ndarray]:
    """One forward standard-map step on the centered torus."""

    p_next = centered_mod(p + K * np.sin(q))
    q_next = centered_mod(q + p_next)
    return np.asarray(q_next), np.asarray(p_next)


def standard_map_inverse_step(q_next: np.ndarray, p_next: np.ndarray, K: float) -> tuple[np.ndarray, np.ndarray]:
    """One inverse standard-map step on the centered torus."""

    q = centered_mod(q_next - p_next)
    p = centered_mod(p_next - K * np.sin(q))
    return np.asarray(q), np.asarray(p)


def fixed_point_eigendata(K: float) -> dict[str, object]:
    """Eigenvalues and normalized eigenvectors at the hyperbolic fixed point."""

    jacobian = np.array([[1.0 + K, 1.0], [K, 1.0]], dtype=float)
    values, vectors = np.linalg.eig(jacobian)
    unstable_index = int(np.argmax(np.abs(values)))
    stable_index = 1 - unstable_index
    unstable = np.real(vectors[:, unstable_index])
    stable = np.real(vectors[:, stable_index])
    unstable /= float(np.linalg.norm(unstable))
    stable /= float(np.linalg.norm(stable))
    if unstable[0] < 0.0:
        unstable *= -1.0
    if stable[0] < 0.0:
        stable *= -1.0
    return {
        "jacobian": jacobian,
        "unstable_eigenvalue": float(np.real(values[unstable_index])),
        "stable_eigenvalue": float(np.real(values[stable_index])),
        "unstable_eigenvector": unstable,
        "stable_eigenvector": stable,
    }


def local_segment(vector: np.ndarray, extent: float, samples: int) -> tuple[np.ndarray, np.ndarray]:
    """Return a small segment through the fixed point tangent to ``vector``."""

    parameter = np.linspace(-extent, extent, samples)
    points = parameter[:, None] * vector[None, :]
    return points[:, 0], points[:, 1]


def manifold_images(
    *,
    K: float,
    vector: np.ndarray,
    extent: float,
    samples: int,
    iterates: int,
    direction: str,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Images of a local invariant-manifold segment.

    ``direction="unstable"`` applies the forward map to an unstable local
    segment.  ``direction="stable"`` applies the inverse map to a stable local
    segment, producing the global stable manifold.
    """

    if direction not in {"stable", "unstable"}:
        raise ValueError("direction must be 'stable' or 'unstable'")
    q, p = local_segment(vector, extent, samples)
    curves = [(centered_mod(q), centered_mod(p))]
    for _ in range(iterates):
        if direction == "unstable":
            q, p = standard_map_step(q, p, K)
        else:
            q, p = standard_map_inverse_step(q, p, K)
        curves.append((centered_mod(q), centered_mod(p)))
    return [(np.asarray(qi), np.asarray(pi)) for qi, pi in curves]


def split_wrapped_curve(q: np.ndarray, p: np.ndarray, threshold: float = math.pi) -> Iterable[tuple[np.ndarray, np.ndarray]]:
    """Split a torus curve whenever plotting it would draw across the boundary."""

    if len(q) == 0:
        return
    jumps = np.flatnonzero((np.abs(np.diff(q)) > threshold) | (np.abs(np.diff(p)) > threshold))
    start = 0
    for jump in jumps:
        end = int(jump) + 1
        if end - start >= 2:
            yield q[start:end], p[start:end]
        start = end
    if len(q) - start >= 2:
        yield q[start:], p[start:]


def build_summary(args: argparse.Namespace) -> dict[str, object]:
    eigendata = fixed_point_eigendata(args.K)
    stable_curves = manifold_images(
        K=args.K,
        vector=np.asarray(eigendata["stable_eigenvector"]),
        extent=args.local_extent,
        samples=args.samples,
        iterates=args.iterates,
        direction="stable",
    )
    unstable_curves = manifold_images(
        K=args.K,
        vector=np.asarray(eigendata["unstable_eigenvector"]),
        extent=args.local_extent,
        samples=args.samples,
        iterates=args.iterates,
        direction="unstable",
    )
    return {
        "model": "standard map homoclinic tangle",
        "map": {
            "p_next": "p + K sin(q) mod 2*pi",
            "q_next": "q + p_next mod 2*pi",
            "display_domain": "centered torus [-pi, pi] x [-pi, pi]",
        },
        "configuration": {
            "K": args.K,
            "samples": args.samples,
            "iterates": args.iterates,
            "local_extent": args.local_extent,
        },
        "hyperbolic_fixed_point": {"q": 0.0, "p": 0.0},
        "linearization": {
            "unstable_eigenvalue": eigendata["unstable_eigenvalue"],
            "stable_eigenvalue": eigendata["stable_eigenvalue"],
            "unstable_eigenvector": eigendata["unstable_eigenvector"],
            "stable_eigenvector": eigendata["stable_eigenvector"],
        },
        "curve_counts": {
            "stable_images": len(stable_curves),
            "unstable_images": len(unstable_curves),
            "points_per_image": args.samples,
        },
        "diagnostic_note": (
            "Stable branches are generated by inverse iterates of a local stable segment; "
            "unstable branches are generated by forward iterates of a local unstable segment."
        ),
        "outputs": {},
        "_curves": {"stable": stable_curves, "unstable": unstable_curves},
    }


def plot_curve_family(ax, curves: list[tuple[np.ndarray, np.ndarray]], *, color: str, label: str) -> None:
    """Plot a family of wrapped curves without boundary-spanning artifacts."""

    first = True
    for q, p in curves:
        for qs, ps in split_wrapped_curve(q, p):
            ax.plot(qs, ps, color=color, lw=0.72, alpha=0.68, label=label if first else None)
            first = False


def save_plot(path: Path, summary: dict[str, object]) -> None:
    import os

    os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache")))
    os.environ.setdefault("MPLBACKEND", "Agg")
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    curves = summary["_curves"]
    stable_curves = curves["stable"]
    unstable_curves = curves["unstable"]
    K = float(summary["configuration"]["K"])

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8), constrained_layout=True)
    for ax in axes:
        plot_curve_family(ax, unstable_curves, color="#d62728", label=r"$W^u$")
        plot_curve_family(ax, stable_curves, color="#1f77b4", label=r"$W^s$")
        ax.plot([0.0], [0.0], marker="x", markersize=6.5, color="black", mew=1.4, label="hyperbolic fixed point")
        ax.set_xlabel(r"$q$")
        ax.set_ylabel(r"$p$")
        ax.grid(alpha=0.18)
        ax.set_aspect("equal", adjustable="box")

    axes[0].set_title(fr"Standard map manifolds, $K={K:g}$")
    axes[0].set_xlim(-math.pi, math.pi)
    axes[0].set_ylim(-math.pi, math.pi)
    axes[0].set_xticks([-math.pi, 0.0, math.pi])
    axes[0].set_xticklabels([r"$-\pi$", "0", r"$\pi$"])
    axes[0].set_yticks([-math.pi, 0.0, math.pi])
    axes[0].set_yticklabels([r"$-\pi$", "0", r"$\pi$"])

    axes[1].set_title("Homoclinic-tangle zoom")
    axes[1].set_xlim(-2.15, 2.15)
    axes[1].set_ylim(-2.15, 2.15)
    axes[1].legend(frameon=True, loc="upper right", fontsize=8)

    fig.savefig(path, dpi=180)
    plt.close(fig)


def print_summary(summary: dict[str, object]) -> None:
    config = summary["configuration"]
    linear = summary["linearization"]
    counts = summary["curve_counts"]
    print(f"K={config['K']}")
    print(f"samples={config['samples']}")
    print(f"iterates={config['iterates']}")
    print(f"local_extent={config['local_extent']:.12g}")
    print(f"unstable_eigenvalue={linear['unstable_eigenvalue']:.12g}")
    print(f"stable_eigenvalue={linear['stable_eigenvalue']:.12g}")
    print(f"stable_images={counts['stable_images']}")
    print(f"unstable_images={counts['unstable_images']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_preset_args(parser)
    parser.add_argument("--K", type=float, default=None, help="standard-map kick strength")
    parser.add_argument("--samples", type=int, default=None, help="points in the initial local segment")
    parser.add_argument("--iterates", type=int, default=None, help="number of forward/inverse images to draw")
    parser.add_argument("--local-extent", type=float, default=None, help="half-length of the local tangent segment")
    parser.add_argument("--plot", type=Path, default=None, help="write a PNG figure")
    add_output_args(parser)
    args = parser.parse_args()
    defaults = dict(DEFAULTS)
    if args.quick:
        defaults.update(RUN_PRESETS["quick"])
    elif args.lecture:
        defaults.update(RUN_PRESETS["lecture"])
    elif args.long:
        defaults.update(RUN_PRESETS["long"])
    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)
    configure_standard_outputs(args, stem="standard_map_homoclinic_tangle", plot_name="standard_map_homoclinic_tangle.png")
    if args.K <= 0.0:
        parser.error("--K must be positive so that (0,0) is hyperbolic")
    if args.samples < 8:
        parser.error("--samples must be >= 8")
    if args.iterates < 1:
        parser.error("--iterates must be >= 1")
    if args.local_extent <= 0.0:
        parser.error("--local-extent must be positive")
    return args


def main() -> None:
    args = parse_args()
    summary = build_summary(args)
    if args.plot is not None:
        save_plot(args.plot, summary)
    summary.pop("_curves", None)
    emit_summary(summary, args, print_summary)


if __name__ == "__main__":
    main()
