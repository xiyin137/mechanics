#!/usr/bin/env python3
"""Run compact benchmark statistical studies for three-body course labs.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

The benchmark has two deliberately modest parts:

1. an accelerated Sun-Jupiter-asteroid loss experiment with several random
   seeds, used to demonstrate finite-time resonance-labelled statistics;
2. a planar binary-single scattering sweep in v_inf, used to demonstrate
   outcome fractions and capture/exchange cross sections.

The asteroid benchmark scales Jupiter's mass by default so that a small
classroom run produces visible losses. It is a stress test of the mechanism,
not a Solar-System measurement.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import asteroid_ejection_probability as asteroid
import binary_capture_scattering as binary


@dataclass(frozen=True)
class BenchmarkConfig:
    asteroid_n: int
    asteroid_years: float
    asteroid_dt: float
    asteroid_bins: int
    asteroid_jupiter_mass_scale: float
    asteroid_seeds: tuple[int, ...]
    binary_samples: int
    binary_years: float
    binary_dt: float
    binary_v_infs: tuple[float, ...]
    binary_b_max: float


def binomial_standard_error(successes: int, count: int) -> float:
    if count <= 0:
        return float("nan")
    p = successes / count
    return math.sqrt(p * (1.0 - p) / count)


def mean_and_se(values: list[float]) -> tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    if len(values) == 1:
        return float(values[0]), 0.0
    arr = np.array(values, dtype=float)
    return float(np.mean(arr)), float(np.std(arr, ddof=1) / math.sqrt(len(arr)))


def asteroid_cfg(seed: int, cfg: BenchmarkConfig) -> asteroid.Config:
    return asteroid.Config(
        n=cfg.asteroid_n,
        years=cfg.asteroid_years,
        dt=cfg.asteroid_dt,
        seed=seed,
        a_min=asteroid.DEFAULT_CONFIG["a_min"],
        a_max=asteroid.DEFAULT_CONFIG["a_max"],
        e_max=asteroid.DEFAULT_CONFIG["e_max"],
        bins=cfg.asteroid_bins,
        m_sun=asteroid.M_SUN,
        m_jupiter=asteroid.M_JUPITER * cfg.asteroid_jupiter_mass_scale,
        a_jupiter=asteroid.A_JUPITER,
        ejection_radius=20.0,
        sun_radius=0.02,
        jupiter_close_radius=0.03,
        include_indirect=True,
        resonance_window=0.05,
    )


def run_asteroid_benchmark(cfg: BenchmarkConfig) -> dict[str, object]:
    summaries = [asteroid.integrate(asteroid_cfg(seed, cfg)) for seed in cfg.asteroid_seeds]
    seed_rows = []
    for seed, summary in zip(cfg.asteroid_seeds, summaries):
        seed_rows.append(
            {
                "seed": seed,
                "n": int(summary["n"]),
                "ejected": int(summary["ejected"]),
                "lost": int(summary["ejected"]) + int(summary["sun_collision"]) + int(summary["jupiter_close"]),
                "ejection_probability": float(summary["ejection_probability"]),
                "loss_probability": float(summary["loss_probability"]),
                "max_recorded_eccentricity": float(summary["diagnostics"]["max_recorded_eccentricity"]),
            }
        )

    bin_rows = []
    for bin_index in range(cfg.asteroid_bins):
        template = summaries[0]["summary_by_bin"][bin_index]
        ejected = sum(int(summary["summary_by_bin"][bin_index]["ejected"]) for summary in summaries)
        lost = sum(int(summary["summary_by_bin"][bin_index]["lost"]) for summary in summaries)
        count = sum(int(summary["summary_by_bin"][bin_index]["count"]) for summary in summaries)
        bin_rows.append(
            {
                "a_low": float(template["a_low"]),
                "a_high": float(template["a_high"]),
                "count": count,
                "ejected": ejected,
                "lost": lost,
                "ejection_fraction": ejected / count if count else float("nan"),
                "ejection_standard_error": binomial_standard_error(ejected, count),
                "loss_fraction": lost / count if count else float("nan"),
                "loss_standard_error": binomial_standard_error(lost, count),
                "nearest_resonance": str(template["nearest_resonance"]),
                "resonance_distance": float(template["resonance_distance"]),
            }
        )

    resonance_rows = []
    for label, (p, q) in asteroid.RESONANCE_RATIOS.items():
        rows = [
            next(row for row in summary["summary_by_resonance"] if row["resonance"] == label)
            for summary in summaries
        ]
        count = sum(int(row["count"]) for row in rows)
        ejected = sum(int(row["ejected"]) for row in rows)
        lost = sum(int(row["lost"]) for row in rows)
        max_e = max(float(row["max_eccentricity"]) for row in rows)
        resonance_rows.append(
            {
                "resonance": label,
                "p": p,
                "q": q,
                "order": p - q,
                "location": float(rows[0]["location"]),
                "count": count,
                "ejected": ejected,
                "lost": lost,
                "ejection_fraction": ejected / count if count else float("nan"),
                "ejection_standard_error": binomial_standard_error(ejected, count),
                "loss_fraction": lost / count if count else float("nan"),
                "loss_standard_error": binomial_standard_error(lost, count),
                "max_eccentricity": max_e,
            }
        )

    total_n = sum(int(summary["n"]) for summary in summaries)
    total_ejected = sum(int(summary["ejected"]) for summary in summaries)
    total_lost = sum(int(summary["ejected"]) + int(summary["sun_collision"]) + int(summary["jupiter_close"]) for summary in summaries)
    return {
        "model": "accelerated planar restricted Sun-Jupiter-asteroid ensemble",
        "note": "Jupiter mass is scaled to make a short benchmark visibly lossy; this is not a Solar-System probability.",
        "configuration": {
            "n_per_seed": cfg.asteroid_n,
            "years": cfg.asteroid_years,
            "dt": cfg.asteroid_dt,
            "bins": cfg.asteroid_bins,
            "jupiter_mass_scale": cfg.asteroid_jupiter_mass_scale,
            "seeds": list(cfg.asteroid_seeds),
        },
        "summary": {
            "total_particles": total_n,
            "total_ejected": total_ejected,
            "total_lost": total_lost,
            "ejection_probability": total_ejected / total_n if total_n else 0.0,
            "ejection_standard_error": binomial_standard_error(total_ejected, total_n),
            "loss_probability": total_lost / total_n if total_n else 0.0,
            "loss_standard_error": binomial_standard_error(total_lost, total_n),
        },
        "seed_rows": seed_rows,
        "bin_rows": bin_rows,
        "resonance_rows": resonance_rows,
    }


def binary_cfg(seed: int, v_inf: float, cfg: BenchmarkConfig) -> binary.Config:
    return binary.Config(
        samples=cfg.binary_samples,
        seed=seed,
        m1=1.0,
        m2=1.0,
        m3=0.2,
        a_binary=1.0,
        v_inf=v_inf,
        b_max=cfg.binary_b_max,
        start_distance=8.0,
        years=cfg.binary_years,
        dt=cfg.binary_dt,
        close_radius=0.05,
        uniform_area=True,
    )


def run_binary_benchmark(cfg: BenchmarkConfig) -> dict[str, object]:
    rows = []
    for index, v_inf in enumerate(cfg.binary_v_infs):
        run_cfg = binary_cfg(seed=11 + index, v_inf=v_inf, cfg=cfg)
        summary = binary.summarize(run_cfg)
        capture_or_exchange = int(summary["derived_counts"]["capture_or_exchange"])
        rows.append(
            {
                "v_inf": v_inf,
                "samples": cfg.binary_samples,
                "capture": int(summary["outcome_counts"]["capture"]),
                "exchange": int(summary["outcome_counts"]["exchange"]),
                "capture_or_exchange": capture_or_exchange,
                "capture_or_exchange_fraction": capture_or_exchange / cfg.binary_samples if cfg.binary_samples else 0.0,
                "capture_or_exchange_standard_error": binomial_standard_error(capture_or_exchange, cfg.binary_samples),
                "capture_or_exchange_cross_section": float(summary["cross_sections"]["capture_or_exchange"]),
                "flyby_fraction": float(summary["outcome_fractions"]["flyby"]),
                "collision_fraction": float(summary["outcome_fractions"]["collision"]),
                "max_energy_abs_drift": float(summary["diagnostics"]["max_energy_abs_drift"]),
            }
        )
    return {
        "model": "planar Newtonian binary-single scattering sweep",
        "note": "Capture is a finite-horizon binding-energy class in a conservative calculation.",
        "configuration": {
            "samples_per_v_inf": cfg.binary_samples,
            "years": cfg.binary_years,
            "dt": cfg.binary_dt,
            "b_max": cfg.binary_b_max,
            "v_infs": list(cfg.binary_v_infs),
            "orientation_convention": (
                "Before subtracting the total center of mass, the binary center of mass is at the origin. "
                "The incoming body starts at (-8 a_bin, b) in the quick run and moves initially in the +x direction. "
                "The binary separation vector has random phase: a_bin*(cos phi, sin phi), with phi uniform on [0, 2*pi)."
            ),
        },
        "rows": rows,
    }


def run_benchmark(cfg: BenchmarkConfig) -> dict[str, object]:
    asteroid_result = run_asteroid_benchmark(cfg)
    binary_result = run_binary_benchmark(cfg)
    asteroid_seed_probs = [float(row["ejection_probability"]) for row in asteroid_result["seed_rows"]]
    asteroid_mean, asteroid_seed_se = mean_and_se(asteroid_seed_probs)
    return {
        "model": "three-body benchmark statistical studies",
        "scope_note": "Compact benchmark suite for course notes; not a production celestial-mechanics survey.",
        "asteroid": asteroid_result,
        "binary_scattering": binary_result,
        "headline": {
            "asteroid_seed_mean_ejection_probability": asteroid_mean,
            "asteroid_seed_standard_error": asteroid_seed_se,
            "binary_low_speed_capture_or_exchange_cross_section": binary_result["rows"][0][
                "capture_or_exchange_cross_section"
            ]
            if binary_result["rows"]
            else float("nan"),
        },
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


def configure_matplotlib() -> object:
    import os

    os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache")))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def draw_asteroid_loss_panel(ax: object, summary: dict[str, object]) -> None:
    bins = summary["asteroid"]["bin_rows"]
    asteroid_cfg = summary["asteroid"]["configuration"]
    asteroid_summary = summary["asteroid"]["summary"]

    centers = [0.5 * (row["a_low"] + row["a_high"]) for row in bins]
    widths = [row["a_high"] - row["a_low"] for row in bins]
    losses = [row["loss_fraction"] for row in bins]
    loss_errors = [row["loss_standard_error"] for row in bins]

    ax.bar(
        centers,
        losses,
        width=widths,
        color="#8bb9d6",
        edgecolor="#2f4f5f",
        linewidth=0.9,
        alpha=0.72,
        label=r"bin fraction",
        zorder=2,
    )
    ax.errorbar(
        centers,
        losses,
        yerr=loss_errors,
        fmt="o",
        color="#0b4f8a",
        ecolor="#0b4f8a",
        markersize=4.8,
        capsize=3,
        label="estimate ± SE",
        zorder=4,
        clip_on=False,
    )
    for row in summary["asteroid"]["resonance_rows"]:
        ax.axvline(row["location"], color="tab:red", alpha=0.25)
        ax.text(
            row["location"],
            0.98,
            row["resonance"],
            rotation=90,
            va="top",
            ha="right",
            transform=ax.get_xaxis_transform(),
        )
    ax.set_xlabel("initial semimajor axis [AU]")
    ax.set_ylabel("finite-time loss fraction by bin")
    ax.set_title(
        "Restricted asteroid loss\n"
        f"Jupiter mass x{asteroid_cfg['jupiter_mass_scale']:g}, "
        f"N={asteroid_summary['total_particles']}, T={asteroid_cfg['years']:g} yr"
    )
    ax.axhline(0.0, color="0.20", linewidth=0.8, zorder=1)
    ax.set_ylim(-0.03, max(0.2, min(1.0, max(losses, default=0.0) + 0.15)))
    ax.legend(frameon=False, loc="upper left", fontsize=8)


def draw_binary_scattering_panel(ax: object, summary: dict[str, object]) -> None:
    binary_rows = summary["binary_scattering"]["rows"]
    binary_cfg = summary["binary_scattering"]["configuration"]

    v = [row["v_inf"] for row in binary_rows]
    sigma = [row["capture_or_exchange_cross_section"] for row in binary_rows]
    frac = [row["capture_or_exchange_fraction"] for row in binary_rows]
    line_sigma = ax.plot(v, sigma, "o-", color="tab:green", label="cross section")[0]
    ax.set_xlabel(r"$v_\infty$")
    ax.set_ylabel(r"area cross section $\sigma_{\rm cap/exch}$")
    axb = ax.twinx()
    line_fraction = axb.plot(v, frac, "s--", color="tab:purple", label="fraction")[0]
    axb.set_ylabel("capture/exchange fraction")
    ax.set_title(
        "Binary-single scattering\n"
        f"N={binary_cfg['samples_per_v_inf']} per speed, "
        rf"$b_{{\max}}$={binary_cfg['b_max']:g}, T={binary_cfg['years']:g}"
    )
    ax.legend(handles=[line_sigma, line_fraction], frameon=False, loc="upper right")


def save_asteroid_plot(path: Path, summary: dict[str, object]) -> None:
    plt = configure_matplotlib()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(1, 1, figsize=(7.2, 5.0))
    draw_asteroid_loss_panel(ax, summary)
    fig.text(
        0.5,
        0.01,
        "Accelerated restricted Sun-Jupiter-asteroid stress test; not a Solar-System probability.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0.0, 0.06, 1.0, 1.0))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_binary_plot(path: Path, summary: dict[str, object]) -> None:
    plt = configure_matplotlib()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(1, 1, figsize=(7.2, 5.0))
    draw_binary_scattering_panel(ax, summary)
    fig.text(
        0.5,
        0.01,
        "Finite-horizon binary-single classifier; capture/exchange is ensemble and stopping-rule dependent.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0.0, 0.06, 1.0, 1.0))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_plot(path: Path, summary: dict[str, object]) -> None:
    plt = configure_matplotlib()
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12.2, 5.0))
    draw_asteroid_loss_panel(ax0, summary)
    ax0.set_title("A. " + ax0.get_title())
    draw_binary_scattering_panel(ax1, summary)
    ax1.set_title("B. " + ax1.get_title())
    fig.suptitle("Two independent three-body statistical benchmarks", y=0.98)
    fig.text(
        0.5,
        0.01,
        "Panels share the same estimator-and-diagnostics workflow; they are not two views of one simulation.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0.0, 0.06, 1.0, 0.92))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_seed_list(text: str) -> tuple[int, ...]:
    seeds = tuple(int(item.strip()) for item in text.split(",") if item.strip())
    if not seeds:
        raise argparse.ArgumentTypeError("seed list cannot be empty")
    return seeds


def parse_float_list(text: str) -> tuple[float, ...]:
    values = tuple(float(item.strip()) for item in text.split(",") if item.strip())
    if not values:
        raise argparse.ArgumentTypeError("list cannot be empty")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="short deterministic benchmark")
    parser.add_argument("--asteroid-n", type=int, default=96, help="asteroids per seed")
    parser.add_argument("--asteroid-years", type=float, default=20.0, help="asteroid integration horizon")
    parser.add_argument("--asteroid-dt", type=float, default=0.03, help="asteroid timestep")
    parser.add_argument("--asteroid-bins", type=int, default=10, help="asteroid semimajor-axis bins")
    parser.add_argument("--asteroid-jupiter-mass-scale", type=float, default=25.0, help="Jupiter mass scale for asteroid stress test")
    parser.add_argument("--asteroid-seeds", type=parse_seed_list, default=(3, 4, 5), help="comma-separated asteroid seeds")
    parser.add_argument("--binary-samples", type=int, default=32, help="samples per binary v_inf")
    parser.add_argument("--binary-years", type=float, default=5.0, help="binary integration horizon")
    parser.add_argument("--binary-dt", type=float, default=0.0125, help="binary timestep")
    parser.add_argument("--binary-v-infs", type=parse_float_list, default=(0.35, 0.55, 0.8), help="comma-separated v_inf grid")
    parser.add_argument("--binary-b-max", type=float, default=1.5, help="maximum binary impact parameter")
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    parser.add_argument("--json-output", type=Path, default=None, help="write JSON summary")
    parser.add_argument("--plot", type=Path, default=None, help="write benchmark plot")
    parser.add_argument("--asteroid-plot", type=Path, default=None, help="write asteroid-loss benchmark plot")
    parser.add_argument("--binary-plot", type=Path, default=None, help="write binary-scattering benchmark plot")
    args = parser.parse_args()
    if args.quick:
        args.asteroid_n = min(args.asteroid_n, 48)
        args.asteroid_years = min(args.asteroid_years, 12.0)
        args.asteroid_dt = max(args.asteroid_dt, 0.04)
        args.asteroid_bins = min(args.asteroid_bins, 8)
        args.asteroid_seeds = tuple(args.asteroid_seeds[:2])
        args.binary_samples = min(args.binary_samples, 16)
        args.binary_years = min(args.binary_years, 4.0)
        args.binary_dt = max(args.binary_dt, 0.015)
        args.binary_v_infs = tuple(args.binary_v_infs[:3])
    if args.asteroid_n <= 0 or args.binary_samples <= 0:
        parser.error("sample counts must be positive")
    if args.asteroid_years < 0.0 or args.binary_years < 0.0:
        parser.error("integration horizons must be >= 0")
    if args.asteroid_dt <= 0.0 or args.binary_dt <= 0.0:
        parser.error("timesteps must be > 0")
    if args.asteroid_bins < 1:
        parser.error("--asteroid-bins must be >= 1")
    if args.asteroid_jupiter_mass_scale < 0.0:
        parser.error("--asteroid-jupiter-mass-scale must be >= 0")
    if args.binary_b_max <= 0.0:
        parser.error("--binary-b-max must be > 0")
    return args


def main() -> None:
    args = parse_args()
    cfg = BenchmarkConfig(
        asteroid_n=args.asteroid_n,
        asteroid_years=args.asteroid_years,
        asteroid_dt=args.asteroid_dt,
        asteroid_bins=args.asteroid_bins,
        asteroid_jupiter_mass_scale=args.asteroid_jupiter_mass_scale,
        asteroid_seeds=args.asteroid_seeds,
        binary_samples=args.binary_samples,
        binary_years=args.binary_years,
        binary_dt=args.binary_dt,
        binary_v_infs=args.binary_v_infs,
        binary_b_max=args.binary_b_max,
    )
    summary = run_benchmark(cfg)
    outputs: dict[str, str] = {}
    if args.plot is not None:
        save_plot(args.plot, summary)
        outputs["plot"] = str(args.plot)
    if args.asteroid_plot is not None:
        save_asteroid_plot(args.asteroid_plot, summary)
        outputs["asteroid_plot"] = str(args.asteroid_plot)
    if args.binary_plot is not None:
        save_binary_plot(args.binary_plot, summary)
        outputs["binary_plot"] = str(args.binary_plot)
    if args.json_output is not None:
        outputs["json"] = str(args.json_output)
    if outputs:
        summary["outputs"] = outputs
    if args.json_output is not None:
        write_json(args.json_output, summary)
    if args.json:
        print(json.dumps(json_ready(summary), indent=2, sort_keys=True, allow_nan=False))
    else:
        asteroid_summary = summary["asteroid"]["summary"]
        print(f"asteroid_ejection_probability={asteroid_summary['ejection_probability']:.6f}")
        print(f"asteroid_loss_probability={asteroid_summary['loss_probability']:.6f}")
        for row in summary["binary_scattering"]["rows"]:
            print(
                "binary_v_inf={v_inf:.3f},capture_or_exchange_fraction={frac:.6f},cross_section={sigma:.6f}".format(
                    v_inf=row["v_inf"],
                    frac=row["capture_or_exchange_fraction"],
                    sigma=row["capture_or_exchange_cross_section"],
                )
            )
        if args.plot is not None:
            print(f"wrote_plot={args.plot}")
        if args.asteroid_plot is not None:
            print(f"wrote_asteroid_plot={args.asteroid_plot}")
        if args.binary_plot is not None:
            print(f"wrote_binary_plot={args.binary_plot}")
        if args.json_output is not None:
            print(f"wrote_json={args.json_output}")


if __name__ == "__main__":
    main()
