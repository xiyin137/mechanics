#!/usr/bin/env python3
"""Estimate asteroid ejection probability in a restricted Sun-Jupiter model.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

Units:
    distance: AU
    time: years
    mass: solar masses

The model is planar and deliberately teachable. Jupiter is prescribed on a
circular orbit. Test particles are massless and start on low-eccentricity
Keplerian orbits in an asteroid-belt-like annulus. The integration uses a
kick-drift-kick style scheme with a time-dependent acceleration.

This is not a high-precision Solar System integrator. It is a course lab for
resonance, perturbation, chaos, and ensemble probabilities.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


G = 4.0 * math.pi * math.pi
M_SUN = 1.0
M_JUPITER = 9.543e-4
A_JUPITER = 5.2044

RESONANCE_RATIOS = {
    "3:1": (3, 1),
    "5:2": (5, 2),
    "7:3": (7, 3),
    "2:1": (2, 1),
}

ALIVE = 0
EJECTED = 1
SUN_COLLISION = 2
JUPITER_CLOSE = 3

DEFAULT_CONFIG = {
    "n": 512,
    "years": 100.0,
    "dt": 0.02,
    "seed": 1,
    "a_min": 2.05,
    "a_max": 3.75,
    "e_max": 0.08,
    "bins": 20,
}

PRESET_CONFIG = {
    "quick": {"n": 32, "years": 2.0, "dt": 0.05, "bins": 6},
    "lecture": {"n": 256, "years": 100.0, "dt": 0.02, "bins": 16},
    "long": {"n": 2048, "years": 1000.0, "dt": 0.01, "bins": 32},
}


@dataclass(frozen=True)
class Config:
    n: int
    years: float
    dt: float
    seed: int
    a_min: float
    a_max: float
    e_max: float
    bins: int
    m_sun: float
    m_jupiter: float
    a_jupiter: float
    ejection_radius: float
    sun_radius: float
    jupiter_close_radius: float
    include_indirect: bool

    @property
    def gm_sun(self) -> float:
        return G * self.m_sun

    @property
    def gm_jupiter(self) -> float:
        return G * self.m_jupiter


def solve_kepler(mean_anomaly: np.ndarray, eccentricity: np.ndarray) -> np.ndarray:
    """Solve M = E - e sin(E) for elliptic orbits."""
    if np.any(eccentricity < 0.0) or np.any(eccentricity >= 1.0):
        raise ValueError("eccentricity must satisfy 0 <= e < 1")
    E = mean_anomaly + eccentricity * np.sin(mean_anomaly)
    for _ in range(12):
        f = E - eccentricity * np.sin(E) - mean_anomaly
        fp = 1.0 - eccentricity * np.cos(E)
        E -= f / fp
    return E


def true_anomaly(mean_anomaly: np.ndarray, eccentricity: np.ndarray) -> np.ndarray:
    E = solve_kepler(mean_anomaly, eccentricity)
    numerator = np.sqrt(1.0 + eccentricity) * np.sin(0.5 * E)
    denominator = np.sqrt(1.0 - eccentricity) * np.cos(0.5 * E)
    return 2.0 * np.arctan2(numerator, denominator)


def sample_initial_conditions(cfg: Config) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample heliocentric Keplerian initial data for test particles."""
    rng = np.random.default_rng(cfg.seed)
    a0 = rng.uniform(cfg.a_min, cfg.a_max, cfg.n)
    e0 = rng.uniform(0.0, cfg.e_max, cfg.n)
    mean = rng.uniform(0.0, 2.0 * math.pi, cfg.n)
    periapse = rng.uniform(0.0, 2.0 * math.pi, cfg.n)
    f = true_anomaly(mean, e0)

    p = a0 * (1.0 - e0 * e0)
    r = p / (1.0 + e0 * np.cos(f))
    root = np.sqrt(cfg.gm_sun / p)

    x_orb = r * np.cos(f)
    y_orb = r * np.sin(f)
    vx_orb = -root * np.sin(f)
    vy_orb = root * (e0 + np.cos(f))

    c = np.cos(periapse)
    s = np.sin(periapse)
    pos = np.column_stack((c * x_orb - s * y_orb, s * x_orb + c * y_orb))
    vel = np.column_stack((c * vx_orb - s * vy_orb, s * vx_orb + c * vy_orb))
    return pos, vel, a0


def jupiter_position(t: float, cfg: Config) -> np.ndarray:
    n_jupiter = math.sqrt(G * (cfg.m_sun + cfg.m_jupiter) / cfg.a_jupiter**3)
    theta = n_jupiter * t
    return cfg.a_jupiter * np.array([math.cos(theta), math.sin(theta)])


def resonance_locations(a_jupiter: float) -> dict[str, float]:
    """Return nominal interior mean-motion resonance locations."""
    return {
        label: a_jupiter * (q / p) ** (2.0 / 3.0)
        for label, (p, q) in RESONANCE_RATIOS.items()
    }


def nearest_resonance(a: float, a_jupiter: float) -> tuple[str, float]:
    locations = resonance_locations(a_jupiter)
    label, location = min(locations.items(), key=lambda item: abs(a - item[1]))
    return label, abs(a - location)


def binomial_standard_error(successes: int, count: int) -> float:
    if count <= 0:
        return float("nan")
    p = successes / count
    return math.sqrt(p * (1.0 - p) / count)


def acceleration(t: float, pos: np.ndarray, cfg: Config) -> np.ndarray:
    if len(pos) == 0:
        return np.zeros_like(pos)

    r2 = np.sum(pos * pos, axis=1)
    r = np.sqrt(r2)
    inv_r3 = 1.0 / np.maximum(r2 * r, 1.0e-18)
    acc = -cfg.gm_sun * pos * inv_r3[:, None]

    rj = jupiter_position(t, cfg)
    diff = pos - rj
    d2 = np.sum(diff * diff, axis=1)
    d = np.sqrt(d2)
    inv_d3 = 1.0 / np.maximum(d2 * d, 1.0e-18)
    acc += -cfg.gm_jupiter * diff * inv_d3[:, None]

    if cfg.include_indirect:
        rj_norm = float(np.linalg.norm(rj))
        acc += -cfg.gm_jupiter * rj / (rj_norm**3)

    return acc


def classify_losses(
    t: float,
    pos: np.ndarray,
    vel: np.ndarray,
    status: np.ndarray,
    cfg: Config,
) -> None:
    active = status == ALIVE
    if not np.any(active):
        return

    p = pos[active]
    v = vel[active]
    idx = np.flatnonzero(active)
    r = np.linalg.norm(p, axis=1)
    energy = 0.5 * np.sum(v * v, axis=1) - cfg.gm_sun / np.maximum(r, 1.0e-18)
    rj = jupiter_position(t, cfg)
    dj = np.linalg.norm(p - rj, axis=1)

    sun_hit = r < cfg.sun_radius
    jupiter_close = dj < cfg.jupiter_close_radius
    ejected = (r > cfg.ejection_radius) | ((energy > 0.0) & (r > cfg.a_jupiter))

    status[idx[ejected]] = EJECTED
    status[idx[jupiter_close]] = JUPITER_CLOSE
    status[idx[sun_hit]] = SUN_COLLISION


def integrate(cfg: Config) -> dict[str, object]:
    pos, vel, a0 = sample_initial_conditions(cfg)
    status = np.zeros(cfg.n, dtype=np.int8)
    steps = int(round(cfg.years / cfg.dt))
    t = 0.0

    acc0 = acceleration(t, pos, cfg)
    vhalf = vel + 0.5 * cfg.dt * acc0

    for step in range(1, steps + 1):
        active = status == ALIVE
        if not np.any(active):
            break

        pos[active] += cfg.dt * vhalf[active]
        t = step * cfg.dt

        acc_new = np.zeros_like(pos)
        acc_new[active] = acceleration(t, pos[active], cfg)
        vhalf[active] += cfg.dt * acc_new[active]
        vel_now = vhalf - 0.5 * cfg.dt * acc_new
        classify_losses(t, pos, vel_now, status, cfg)

    return summarize(a0, status, cfg, elapsed_years=t)


def summarize(
    a0: np.ndarray,
    status: np.ndarray,
    cfg: Config,
    elapsed_years: float,
) -> dict[str, object]:
    total = len(status)
    ejected = int(np.count_nonzero(status == EJECTED))
    sun = int(np.count_nonzero(status == SUN_COLLISION))
    jupiter = int(np.count_nonzero(status == JUPITER_CLOSE))
    alive = int(np.count_nonzero(status == ALIVE))

    edges = np.linspace(cfg.a_min, cfg.a_max, cfg.bins + 1)
    rows: list[dict[str, float | int | str]] = []
    for bin_index, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
        if bin_index == cfg.bins - 1:
            in_bin = (a0 >= lo) & (a0 <= hi)
        else:
            in_bin = (a0 >= lo) & (a0 < hi)
        count = int(np.count_nonzero(in_bin))
        if count:
            ej = int(np.count_nonzero(in_bin & (status == EJECTED)))
            loss = int(np.count_nonzero(in_bin & (status != ALIVE)))
            frac = ej / count
            loss_frac = loss / count
            frac_se = binomial_standard_error(ej, count)
            loss_frac_se = binomial_standard_error(loss, count)
        else:
            ej = 0
            loss = 0
            frac = float("nan")
            loss_frac = float("nan")
            frac_se = float("nan")
            loss_frac_se = float("nan")
        center = 0.5 * (lo + hi)
        nearest_label, resonance_distance = nearest_resonance(center, cfg.a_jupiter)
        rows.append(
            {
                "a_low": float(lo),
                "a_high": float(hi),
                "count": count,
                "ejected": ej,
                "lost": loss,
                "ejection_fraction": frac,
                "ejection_standard_error": frac_se,
                "loss_fraction": loss_frac,
                "loss_standard_error": loss_frac_se,
                "nearest_resonance": nearest_label,
                "resonance_distance": resonance_distance,
            }
        )

    return {
        "n": total,
        "elapsed_years": elapsed_years,
        "ejected": ejected,
        "sun_collision": sun,
        "jupiter_close": jupiter,
        "alive": alive,
        "ejection_probability": ejected / total if total else 0.0,
        "ejection_standard_error": binomial_standard_error(ejected, total) if total else 0.0,
        "loss_probability": (ejected + sun + jupiter) / total if total else 0.0,
        "loss_standard_error": binomial_standard_error(ejected + sun + jupiter, total) if total else 0.0,
        "model": {
            "name": "planar restricted Sun-Jupiter-asteroid ensemble",
            "units": {"distance": "AU", "time": "years", "mass": "solar masses"},
            "m_sun": cfg.m_sun,
            "m_jupiter": cfg.m_jupiter,
            "a_jupiter": cfg.a_jupiter,
            "include_indirect": cfg.include_indirect,
            "integrator": "kick-drift-kick style restricted-field integrator",
        },
        "configuration": {
            "seed": cfg.seed,
            "years": cfg.years,
            "dt": cfg.dt,
            "a_min": cfg.a_min,
            "a_max": cfg.a_max,
            "e_max": cfg.e_max,
            "bins": cfg.bins,
            "ejection_radius": cfg.ejection_radius,
            "sun_radius": cfg.sun_radius,
            "jupiter_close_radius": cfg.jupiter_close_radius,
        },
        "resonance_locations": resonance_locations(cfg.a_jupiter),
        "bin_rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


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


def save_plot(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    import os

    os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache")))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    centers = [0.5 * (row["a_low"] + row["a_high"]) for row in rows]
    widths = [row["a_high"] - row["a_low"] for row in rows]
    values = [
        0.0 if math.isnan(float(row["ejection_fraction"])) else row["ejection_fraction"]
        for row in rows
    ]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bar(centers, values, width=widths, align="center", edgecolor="black")
    ax.set_xlabel("initial semimajor axis [AU]")
    ax.set_ylabel("ejection fraction")
    ax.set_title("Restricted Sun-Jupiter asteroid ejection estimate")
    ax.set_ylim(0.0, 1.0)

    for label, a_res in resonance_locations(A_JUPITER).items():
        ax.axvline(a_res, color="tab:red", alpha=0.35, linewidth=1.0)
        ax.text(a_res, 0.98, label, rotation=90, va="top", ha="right")

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def print_summary(summary: dict[str, object]) -> None:
    print(f"particles={summary['n']}")
    print(f"elapsed_years={summary['elapsed_years']:.6g}")
    print(f"ejected={summary['ejected']}")
    print(f"sun_collision={summary['sun_collision']}")
    print(f"jupiter_close={summary['jupiter_close']}")
    print(f"alive={summary['alive']}")
    print(f"ejection_probability={summary['ejection_probability']:.6f}")
    print(f"ejection_standard_error={summary['ejection_standard_error']:.6f}")
    print(f"loss_probability={summary['loss_probability']:.6f}")
    print(f"loss_standard_error={summary['loss_standard_error']:.6f}")
    print()
    print("a_low,a_high,count,ejected,lost,ejection_fraction,ejection_standard_error,loss_fraction,loss_standard_error,nearest_resonance,resonance_distance")
    for row in summary["bin_rows"]:
        print(
            f"{row['a_low']:.4f},{row['a_high']:.4f},{row['count']},"
            f"{row['ejected']},{row['lost']},"
            f"{row['ejection_fraction']:.6f},{row['ejection_standard_error']:.6f},"
            f"{row['loss_fraction']:.6f},{row['loss_standard_error']:.6f},"
            f"{row['nearest_resonance']},{row['resonance_distance']:.6f}"
        )


def apply_presets(args: argparse.Namespace) -> None:
    defaults = dict(DEFAULT_CONFIG)
    if args.quick:
        defaults.update(PRESET_CONFIG["quick"])
    elif args.lecture:
        defaults.update(PRESET_CONFIG["lecture"])
    elif args.long:
        defaults.update(PRESET_CONFIG["long"])

    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        if args.csv is None:
            args.csv = args.output_dir / "asteroid_ejection_bins.csv"
        if args.json_output is None:
            args.json_output = args.output_dir / "asteroid_ejection_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    preset_group = parser.add_mutually_exclusive_group()
    preset_group.add_argument("--quick", action="store_true", help="short classroom/smoke-test configuration unless overridden")
    preset_group.add_argument("--lecture", action="store_true", help="moderate lecture-demo configuration unless overridden")
    preset_group.add_argument("--long", action="store_true", help="larger long-horizon configuration unless overridden")
    parser.add_argument("--n", type=int, default=None, help="number of asteroids")
    parser.add_argument("--years", type=float, default=None, help="integration horizon")
    parser.add_argument("--dt", type=float, default=None, help="time step in years; elapsed time is rounded to whole steps")
    parser.add_argument("--seed", type=int, default=None, help="random seed")
    parser.add_argument("--a-min", type=float, default=None, help="minimum initial semimajor axis")
    parser.add_argument("--a-max", type=float, default=None, help="maximum initial semimajor axis")
    parser.add_argument("--e-max", type=float, default=None, help="maximum initial eccentricity")
    parser.add_argument("--bins", type=int, default=None, help="semimajor-axis bins")
    parser.add_argument("--jupiter-mass-scale", type=float, default=1.0, help="scale Jupiter mass")
    parser.add_argument("--ejection-radius", type=float, default=20.0, help="ejection radius in AU")
    parser.add_argument("--sun-radius", type=float, default=0.02, help="solar collision radius in AU")
    parser.add_argument("--jupiter-close-radius", type=float, default=0.03, help="close Jupiter encounter radius in AU")
    parser.add_argument("--no-indirect", action="store_true", help="omit heliocentric indirect term")
    parser.add_argument("--csv", type=Path, default=None, help="write binned summary CSV")
    parser.add_argument("--json", action="store_true", help="print a machine-readable JSON summary instead of text")
    parser.add_argument("--json-output", type=Path, default=None, help="write a machine-readable JSON summary")
    parser.add_argument("--output-dir", type=Path, default=None, help="write standard CSV and JSON outputs to this directory")
    plot_group = parser.add_mutually_exclusive_group()
    plot_group.add_argument("--plot", type=Path, default=None, help="save binned ejection plot")
    plot_group.add_argument("--no-plot", action="store_true", help="do not make a plot")
    args = parser.parse_args()
    apply_presets(args)
    if args.n < 0:
        parser.error("--n must be >= 0")
    if args.years < 0.0:
        parser.error("--years must be >= 0")
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    if args.bins < 1:
        parser.error("--bins must be >= 1")
    if args.a_max <= args.a_min:
        parser.error("--a-max must be greater than --a-min")
    if args.e_max < 0.0:
        parser.error("--e-max must be >= 0")
    if args.e_max >= 1.0:
        parser.error("--e-max must be < 1")
    if args.jupiter_mass_scale < 0.0:
        parser.error("--jupiter-mass-scale must be >= 0")
    if args.ejection_radius <= 0.0:
        parser.error("--ejection-radius must be > 0")
    if args.sun_radius < 0.0:
        parser.error("--sun-radius must be >= 0")
    if args.jupiter_close_radius < 0.0:
        parser.error("--jupiter-close-radius must be >= 0")
    return args


def main() -> None:
    args = parse_args()
    cfg = Config(
        n=args.n,
        years=args.years,
        dt=args.dt,
        seed=args.seed,
        a_min=args.a_min,
        a_max=args.a_max,
        e_max=args.e_max,
        bins=args.bins,
        m_sun=M_SUN,
        m_jupiter=M_JUPITER * args.jupiter_mass_scale,
        a_jupiter=A_JUPITER,
        ejection_radius=args.ejection_radius,
        sun_radius=args.sun_radius,
        jupiter_close_radius=args.jupiter_close_radius,
        include_indirect=not args.no_indirect,
    )
    summary = integrate(cfg)
    outputs: dict[str, str] = {}
    rows = summary["bin_rows"]
    if args.csv is not None:
        write_csv(args.csv, rows)
        outputs["csv"] = str(args.csv)
    if args.plot is not None:
        save_plot(args.plot, rows)
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
        print_summary(summary)
        if args.csv is not None:
            print(f"wrote_csv={args.csv}")
        if args.plot is not None:
            print(f"wrote_plot={args.plot}")
        if args.json_output is not None:
            print(f"wrote_json={args.json_output}")


if __name__ == "__main__":
    main()
