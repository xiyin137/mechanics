#!/usr/bin/env python3
"""Estimate capture and exchange statistics in a planar binary-single encounter.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions from Anthropic Opus 4.7.

This is a compact classroom scattering experiment, not a production stellar
dynamics code. Bodies 1 and 2 begin as a circular binary. Body 3 enters from a
large finite distance with a launch speed chosen so that the initial outer
binary-single energy corresponds to the stated asymptotic speed v_inf.
Outcomes are finite-horizon classifications from final pair binding energies.
When cross sections are reported, the planar trajectories are interpreted as an
area-weighted axisymmetric scattering experiment.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


G = 1.0
PAIR_LABELS = ((0, 1, "12"), (0, 2, "13"), (1, 2, "23"))
EXCLUSIVE_OUTCOMES = ("flyby", "capture", "exchange", "ionization", "collision")


@dataclass(frozen=True)
class Config:
    samples: int
    seed: int
    m1: float
    m2: float
    m3: float
    a_binary: float
    v_inf: float
    b_max: float
    start_distance: float
    years: float
    dt: float
    close_radius: float
    uniform_area: bool

    @property
    def masses(self) -> np.ndarray:
        return np.array([self.m1, self.m2, self.m3], dtype=float)


def binary_state(cfg: Config, phase: float) -> tuple[np.ndarray, np.ndarray]:
    masses = cfg.masses
    m12 = cfg.m1 + cfg.m2
    separation = cfg.a_binary * np.array([math.cos(phase), math.sin(phase)])
    tangent = np.array([-math.sin(phase), math.cos(phase)])
    omega = math.sqrt(G * m12 / cfg.a_binary**3)
    relative_velocity = omega * cfg.a_binary * tangent

    pos = np.zeros((3, 2), dtype=float)
    vel = np.zeros((3, 2), dtype=float)
    pos[0] = -cfg.m2 / m12 * separation
    pos[1] = cfg.m1 / m12 * separation
    vel[0] = -cfg.m2 / m12 * relative_velocity
    vel[1] = cfg.m1 / m12 * relative_velocity
    return pos, vel


def sample_impact_parameter(rng: np.random.Generator, cfg: Config) -> float:
    sign = -1.0 if rng.random() < 0.5 else 1.0
    if cfg.uniform_area:
        return sign * cfg.b_max * math.sqrt(float(rng.random()))
    return sign * rng.uniform(0.0, cfg.b_max)


def outer_reduced_mass(cfg: Config) -> float:
    m12 = cfg.m1 + cfg.m2
    return cfg.m3 * m12 / (cfg.m3 + m12)


def incoming_interaction_potential(pos: np.ndarray, cfg: Config) -> float:
    r13 = float(np.linalg.norm(pos[2] - pos[0]))
    r23 = float(np.linalg.norm(pos[2] - pos[1]))
    return -G * cfg.m3 * (cfg.m1 / r13 + cfg.m2 / r23)


def incoming_launch_speed(pos: np.ndarray, cfg: Config) -> float:
    """Convert the requested asymptotic speed to a finite-start launch speed."""

    reduced_mass = outer_reduced_mass(cfg)
    interaction = incoming_interaction_potential(pos, cfg)
    speed_sq = cfg.v_inf**2 - 2.0 * interaction / reduced_mass
    return math.sqrt(max(speed_sq, 0.0))


def incoming_outer_energy(pos: np.ndarray, relative_speed: float, cfg: Config) -> float:
    return 0.5 * outer_reduced_mass(cfg) * relative_speed**2 + incoming_interaction_potential(pos, cfg)


def initial_conditions(cfg: Config, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    phase = rng.uniform(0.0, 2.0 * math.pi)
    impact_parameter = sample_impact_parameter(rng, cfg)
    pos, vel = binary_state(cfg, phase)
    pos[2] = np.array([-cfg.start_distance, impact_parameter])
    launch_speed = incoming_launch_speed(pos, cfg)
    vel[2] = np.array([launch_speed, 0.0])
    outer_energy_initial = incoming_outer_energy(pos, launch_speed, cfg)
    outer_energy_asymptotic = 0.5 * outer_reduced_mass(cfg) * cfg.v_inf**2

    masses = cfg.masses
    center = np.average(pos, axis=0, weights=masses)
    center_velocity = np.average(vel, axis=0, weights=masses)
    pos -= center
    vel -= center_velocity
    return pos, vel, {
        "phase": phase,
        "impact_parameter": impact_parameter,
        "launch_speed": launch_speed,
        "outer_energy_initial": outer_energy_initial,
        "outer_energy_asymptotic": outer_energy_asymptotic,
    }


def cross_section_estimates(cfg: Config, encounters: list[dict[str, object]]) -> dict[str, float]:
    labels = {
        "capture_or_exchange": {"capture", "exchange"},
        "capture": {"capture"},
        "exchange": {"exchange"},
        "collision": {"collision"},
    }
    if cfg.samples == 0:
        return {name: 0.0 for name in labels}
    if cfg.uniform_area:
        area = math.pi * cfg.b_max**2
        return {
            name: area * sum(str(row["outcome"]) in outcome_labels for row in encounters) / cfg.samples
            for name, outcome_labels in labels.items()
        }
    return {
        name: sum(
            2.0 * math.pi * cfg.b_max * abs(float(row["impact_parameter"]))
            for row in encounters
            if str(row["outcome"]) in outcome_labels
        )
        / cfg.samples
        for name, outcome_labels in labels.items()
    }


def accelerations(pos: np.ndarray, masses: np.ndarray) -> np.ndarray:
    acc = np.zeros_like(pos)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            diff = pos[j] - pos[i]
            dist_sq = float(np.dot(diff, diff))
            dist = math.sqrt(max(dist_sq, 1.0e-18))
            acc[i] += G * masses[j] * diff / dist**3
    return acc


def rk4_step(pos: np.ndarray, vel: np.ndarray, dt: float, masses: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    def rhs(p: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        return v, accelerations(p, masses)

    k1p, k1v = rhs(pos, vel)
    k2p, k2v = rhs(pos + 0.5 * dt * k1p, vel + 0.5 * dt * k1v)
    k3p, k3v = rhs(pos + 0.5 * dt * k2p, vel + 0.5 * dt * k2v)
    k4p, k4v = rhs(pos + dt * k3p, vel + dt * k3v)
    new_pos = pos + dt * (k1p + 2.0 * k2p + 2.0 * k3p + k4p) / 6.0
    new_vel = vel + dt * (k1v + 2.0 * k2v + 2.0 * k3v + k4v) / 6.0
    return new_pos, new_vel


def total_energy(pos: np.ndarray, vel: np.ndarray, masses: np.ndarray) -> float:
    kinetic = 0.5 * float(np.sum(masses[:, None] * vel * vel))
    potential = 0.0
    for i, j, _ in PAIR_LABELS:
        potential -= G * masses[i] * masses[j] / float(np.linalg.norm(pos[i] - pos[j]))
    return kinetic + potential


def pair_binding_energies(pos: np.ndarray, vel: np.ndarray, masses: np.ndarray) -> dict[str, float]:
    energies: dict[str, float] = {}
    for i, j, label in PAIR_LABELS:
        reduced_mass = masses[i] * masses[j] / (masses[i] + masses[j])
        rel_v = vel[i] - vel[j]
        rel_r = pos[i] - pos[j]
        energies[label] = 0.5 * reduced_mass * float(np.dot(rel_v, rel_v)) - G * masses[i] * masses[j] / float(
            np.linalg.norm(rel_r)
        )
    return energies


def min_pair_distance(pos: np.ndarray) -> float:
    return min(float(np.linalg.norm(pos[i] - pos[j])) for i, j, _ in PAIR_LABELS)


def classify_outcome(pair_energies: dict[str, float], close_encounter: bool) -> str:
    if close_encounter:
        return "collision"
    bound_pairs = {label for label, energy in pair_energies.items() if energy < 0.0}
    if not bound_pairs:
        return "ionization"
    incoming_bound = bool({"13", "23"} & bound_pairs)
    original_bound = "12" in bound_pairs
    if incoming_bound and original_bound:
        return "capture"
    if incoming_bound:
        return "exchange"
    return "flyby"


def integrate_one(cfg: Config, rng: np.random.Generator) -> dict[str, object]:
    masses = cfg.masses
    pos, vel, sample = initial_conditions(cfg, rng)
    energy0 = total_energy(pos, vel, masses)
    steps = int(round(cfg.years / cfg.dt))
    min_distance = min_pair_distance(pos)
    close_encounter = min_distance < cfg.close_radius
    for _ in range(steps):
        pos, vel = rk4_step(pos, vel, cfg.dt, masses)
        min_distance = min(min_distance, min_pair_distance(pos))
        if min_distance < cfg.close_radius:
            close_encounter = True
    energy1 = total_energy(pos, vel, masses)
    pair_energies = pair_binding_energies(pos, vel, masses)
    outcome = classify_outcome(pair_energies, close_encounter)
    return {
        "phase": sample["phase"],
        "impact_parameter": sample["impact_parameter"],
        "launch_speed": sample["launch_speed"],
        "outcome": outcome,
        "pair_binding_energies": pair_energies,
        "min_pair_distance": min_distance,
        "energy_initial": energy0,
        "energy_final": energy1,
        "energy_abs_drift": abs(energy1 - energy0),
        "outer_energy_initial": sample["outer_energy_initial"],
        "outer_energy_asymptotic": sample["outer_energy_asymptotic"],
        "outer_energy_abs_error": abs(sample["outer_energy_initial"] - sample["outer_energy_asymptotic"]),
    }


def summarize(cfg: Config) -> dict[str, object]:
    rng = np.random.default_rng(cfg.seed)
    encounters = [integrate_one(cfg, rng) for _ in range(cfg.samples)]
    counts = {name: 0 for name in EXCLUSIVE_OUTCOMES}
    for row in encounters:
        counts[str(row["outcome"])] += 1
    fractions = {name: counts[name] / cfg.samples if cfg.samples else 0.0 for name in EXCLUSIVE_OUTCOMES}
    capture_or_exchange = counts["capture"] + counts["exchange"]
    cross_sections = cross_section_estimates(cfg, encounters)
    max_energy_drift = max((float(row["energy_abs_drift"]) for row in encounters), default=0.0)
    max_outer_energy_error = max((float(row["outer_energy_abs_error"]) for row in encounters), default=0.0)
    min_distance = min((float(row["min_pair_distance"]) for row in encounters), default=float("nan"))
    launch_speeds = [float(row["launch_speed"]) for row in encounters]
    return {
        "model": {
            "name": "planar Newtonian binary-single scattering",
            "units": {"G": G, "length": "binary semimajor axis units", "mass": "input masses"},
            "outcome_note": (
                "capture is a finite-horizon binding-energy class; in conservative Newtonian dynamics "
                "a bound triple can later dissolve"
            ),
            "cross_section_note": (
                "planar trajectories are interpreted with the conventional axisymmetric area measure "
                "when cross sections are reported"
            ),
        },
        "ensemble": {
            "samples": cfg.samples,
            "seed": cfg.seed,
            "masses": [cfg.m1, cfg.m2, cfg.m3],
            "a_binary": cfg.a_binary,
            "v_inf": cfg.v_inf,
            "velocity_convention": (
                "v_inf is the asymptotic binary-single relative speed; finite launch speeds are "
                "derived from the initial interaction energy"
            ),
            "b_max": cfg.b_max,
            "start_distance": cfg.start_distance,
            "impact_parameter_sampling": "uniform in area" if cfg.uniform_area else "uniform in signed impact parameter",
        },
        "integration": {
            "years": cfg.years,
            "dt": cfg.dt,
            "steps": int(round(cfg.years / cfg.dt)),
            "integrator": "fixed-step RK4",
            "close_radius": cfg.close_radius,
        },
        "outcome_counts": counts,
        "outcome_fractions": fractions,
        "derived_counts": {
            "capture_or_exchange": capture_or_exchange,
            "incoming_escaped": counts["flyby"],
        },
        "cross_sections": cross_sections,
        "diagnostics": {
            "max_energy_abs_drift": max_energy_drift,
            "max_outer_energy_abs_error": max_outer_energy_error,
            "launch_speed_min": min(launch_speeds, default=float("nan")),
            "launch_speed_mean": sum(launch_speeds) / len(launch_speeds) if launch_speeds else float("nan"),
            "launch_speed_max": max(launch_speeds, default=float("nan")),
            "min_pair_distance": min_distance,
            "exclusive_outcome_fraction_sum": sum(fractions.values()),
        },
        "encounters": encounters,
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


def save_plot(path: Path, summary: dict[str, object]) -> None:
    import os

    os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache")))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    counts = summary["outcome_counts"]
    labels = list(EXCLUSIVE_OUTCOMES)
    values = [counts[label] for label in labels]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(labels, values, color=["0.55", "tab:green", "tab:blue", "tab:purple", "tab:red"])
    ax.set_ylabel("count")
    ax.set_title("Binary-single scattering outcomes")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="short deterministic classroom run")
    parser.add_argument("--samples", type=int, default=32, help="number of scattering encounters")
    parser.add_argument("--seed", type=int, default=2, help="random seed")
    parser.add_argument("--m1", type=float, default=1.0, help="mass of binary body 1")
    parser.add_argument("--m2", type=float, default=1.0, help="mass of binary body 2")
    parser.add_argument("--m3", type=float, default=0.2, help="mass of incoming body")
    parser.add_argument("--a-binary", type=float, default=1.0, help="initial binary semimajor axis")
    parser.add_argument("--v-inf", type=float, default=0.8, help="asymptotic incoming relative speed")
    parser.add_argument("--b-max", type=float, default=2.0, help="maximum impact parameter")
    parser.add_argument("--start-distance", type=float, default=8.0, help="finite launch distance")
    parser.add_argument("--years", type=float, default=12.0, help="integration horizon")
    parser.add_argument("--dt", type=float, default=0.02, help="time step")
    parser.add_argument("--close-radius", type=float, default=0.05, help="close-encounter/collision cutoff")
    parser.add_argument("--uniform-b", action="store_true", help="sample b uniformly instead of uniformly in area")
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    parser.add_argument("--json-output", type=Path, default=None, help="write JSON summary")
    parser.add_argument("--plot", type=Path, default=None, help="write outcome-count plot")
    args = parser.parse_args()
    if args.quick:
        args.samples = min(args.samples, 12)
        args.years = min(args.years, 6.0)
        args.dt = min(args.dt, 0.01)
    if args.samples < 0:
        parser.error("--samples must be >= 0")
    if min(args.m1, args.m2, args.m3) <= 0.0:
        parser.error("masses must be positive")
    if args.a_binary <= 0.0:
        parser.error("--a-binary must be > 0")
    if args.v_inf <= 0.0:
        parser.error("--v-inf must be > 0")
    if args.b_max < 0.0:
        parser.error("--b-max must be >= 0")
    if args.start_distance <= args.a_binary:
        parser.error("--start-distance must be larger than --a-binary")
    if args.years < 0.0:
        parser.error("--years must be >= 0")
    if args.dt <= 0.0:
        parser.error("--dt must be > 0")
    if args.close_radius < 0.0:
        parser.error("--close-radius must be >= 0")
    return args


def config_from_args(args: argparse.Namespace) -> Config:
    return Config(
        samples=args.samples,
        seed=args.seed,
        m1=args.m1,
        m2=args.m2,
        m3=args.m3,
        a_binary=args.a_binary,
        v_inf=args.v_inf,
        b_max=args.b_max,
        start_distance=args.start_distance,
        years=args.years,
        dt=args.dt,
        close_radius=args.close_radius,
        uniform_area=not args.uniform_b,
    )


def main() -> None:
    args = parse_args()
    summary = summarize(config_from_args(args))
    outputs: dict[str, str] = {}
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
        print("outcome,count,fraction")
        for label in EXCLUSIVE_OUTCOMES:
            print(f"{label},{summary['outcome_counts'][label]},{summary['outcome_fractions'][label]:.6f}")
        print(f"capture_or_exchange_cross_section={summary['cross_sections']['capture_or_exchange']:.6f}")
        print(f"max_energy_abs_drift={summary['diagnostics']['max_energy_abs_drift']:.6e}")
        if args.plot is not None:
            print(f"wrote_plot={args.plot}")
        if args.json_output is not None:
            print(f"wrote_json={args.json_output}")


if __name__ == "__main__":
    main()
