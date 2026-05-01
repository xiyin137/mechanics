#!/usr/bin/env python3
"""Estimate asteroid ejection probability in a restricted Sun-Jupiter model.

Authors: GPT 5.5 and Xi Yin.

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
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


G = 4.0 * math.pi * math.pi
M_SUN = 1.0
M_JUPITER = 9.543e-4
A_JUPITER = 5.2044

ALIVE = 0
EJECTED = 1
SUN_COLLISION = 2
JUPITER_CLOSE = 3


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
    rows: list[dict[str, float | int]] = []
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
        else:
            ej = 0
            loss = 0
            frac = float("nan")
            loss_frac = float("nan")
        rows.append(
            {
                "a_low": float(lo),
                "a_high": float(hi),
                "count": count,
                "ejected": ej,
                "lost": loss,
                "ejection_fraction": frac,
                "loss_fraction": loss_frac,
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
        "loss_probability": (ejected + sun + jupiter) / total if total else 0.0,
        "bin_rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_plot(path: Path, rows: list[dict[str, float | int]]) -> None:
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

    resonances = {
        "3:1": A_JUPITER * (1.0 / 3.0) ** (2.0 / 3.0),
        "5:2": A_JUPITER * (2.0 / 5.0) ** (2.0 / 3.0),
        "7:3": A_JUPITER * (3.0 / 7.0) ** (2.0 / 3.0),
        "2:1": A_JUPITER * (1.0 / 2.0) ** (2.0 / 3.0),
    }
    for label, a_res in resonances.items():
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
    print(f"loss_probability={summary['loss_probability']:.6f}")
    print()
    print("a_low,a_high,count,ejected,lost,ejection_fraction,loss_fraction")
    for row in summary["bin_rows"]:
        print(
            f"{row['a_low']:.4f},{row['a_high']:.4f},{row['count']},"
            f"{row['ejected']},{row['lost']},"
            f"{row['ejection_fraction']:.6f},{row['loss_fraction']:.6f}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=512, help="number of asteroids")
    parser.add_argument("--years", type=float, default=100.0, help="integration horizon")
    parser.add_argument("--dt", type=float, default=0.02, help="time step in years; elapsed time is rounded to whole steps")
    parser.add_argument("--seed", type=int, default=1, help="random seed")
    parser.add_argument("--a-min", type=float, default=2.05, help="minimum initial semimajor axis")
    parser.add_argument("--a-max", type=float, default=3.75, help="maximum initial semimajor axis")
    parser.add_argument("--e-max", type=float, default=0.08, help="maximum initial eccentricity")
    parser.add_argument("--bins", type=int, default=20, help="semimajor-axis bins")
    parser.add_argument("--jupiter-mass-scale", type=float, default=1.0, help="scale Jupiter mass")
    parser.add_argument("--ejection-radius", type=float, default=20.0, help="ejection radius in AU")
    parser.add_argument("--sun-radius", type=float, default=0.02, help="solar collision radius in AU")
    parser.add_argument("--jupiter-close-radius", type=float, default=0.03, help="close Jupiter encounter radius in AU")
    parser.add_argument("--no-indirect", action="store_true", help="omit heliocentric indirect term")
    parser.add_argument("--csv", type=Path, default=None, help="write binned summary CSV")
    plot_group = parser.add_mutually_exclusive_group()
    plot_group.add_argument("--plot", type=Path, default=None, help="save binned ejection plot")
    plot_group.add_argument("--no-plot", action="store_true", help="do not make a plot")
    args = parser.parse_args()
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
    print_summary(summary)

    rows = summary["bin_rows"]
    if args.csv is not None:
        write_csv(args.csv, rows)
        print(f"wrote_csv={args.csv}")
    if args.plot is not None:
        save_plot(args.plot, rows)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
