#!/usr/bin/env python3
"""Classical exact formulas from linear elasticity.

The script evaluates small-strain isotropic elastic constants, axial bar
extension, circular-shaft torsion, Euler-Bernoulli beam deflection, and
one-dimensional longitudinal bar modes.  These are reductions of the same
linear elastic body model discussed in the notes.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

import numpy as np


def _as_array(values: np.ndarray | float) -> np.ndarray:
    return np.asarray(values, dtype=float)


def _require_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")


def lame_from_young_poisson(young: float, poisson: float) -> tuple[float, float]:
    """Return Lame parameters ``(lambda, mu)`` from Young modulus and Poisson ratio."""

    _require_positive("young", young)
    if not (-1.0 < poisson < 0.5):
        raise ValueError("poisson must satisfy -1 < poisson < 1/2")
    mu = young / (2.0 * (1.0 + poisson))
    lam = young * poisson / ((1.0 + poisson) * (1.0 - 2.0 * poisson))
    return lam, mu


def young_poisson_from_lame(lam: float, mu: float) -> tuple[float, float]:
    """Return ``(Young modulus, Poisson ratio)`` from Lame parameters."""

    _require_positive("mu", mu)
    if lam + mu == 0.0:
        raise ValueError("lambda + mu must be nonzero")
    young = mu * (3.0 * lam + 2.0 * mu) / (lam + mu)
    poisson = lam / (2.0 * (lam + mu))
    return young, poisson


def bulk_modulus(lam: float, mu: float) -> float:
    _require_positive("mu", mu)
    bulk = lam + 2.0 * mu / 3.0
    if bulk <= 0.0:
        raise ValueError("bulk modulus must be positive for stable isotropic elasticity")
    return bulk


def wave_speeds(lam: float, mu: float, rho: float) -> tuple[float, float]:
    """Return longitudinal and shear wave speeds."""

    _require_positive("rho", rho)
    _require_positive("mu", mu)
    cp2 = (lam + 2.0 * mu) / rho
    cs2 = mu / rho
    if cp2 <= 0.0:
        raise ValueError("longitudinal wave speed squared must be positive")
    return math.sqrt(cp2), math.sqrt(cs2)


def axial_bar_elongation(force: float, length: float, area: float, young: float) -> float:
    """Elongation of a slender bar in uniaxial tension."""

    _require_positive("length", length)
    _require_positive("area", area)
    _require_positive("young", young)
    return force * length / (young * area)


def axial_bar_stress(force: float, area: float) -> float:
    _require_positive("area", area)
    return force / area


def circular_polar_moment(radius: float) -> float:
    _require_positive("radius", radius)
    return 0.5 * math.pi * radius**4


def torsion_twist(torque: float, length: float, mu: float, polar_moment: float) -> float:
    _require_positive("length", length)
    _require_positive("mu", mu)
    _require_positive("polar_moment", polar_moment)
    return torque * length / (mu * polar_moment)


def torsion_shear_stress(r: np.ndarray | float, torque: float, polar_moment: float) -> np.ndarray:
    _require_positive("polar_moment", polar_moment)
    return torque * _as_array(r) / polar_moment


def cantilever_end_load_deflection(
    x: np.ndarray | float,
    *,
    length: float,
    young: float,
    area_moment: float,
    end_force: float,
) -> np.ndarray:
    """Euler-Bernoulli cantilever deflection under an end force."""

    _require_positive("length", length)
    _require_positive("young", young)
    _require_positive("area_moment", area_moment)
    x_array = _as_array(x)
    return end_force * x_array**2 * (3.0 * length - x_array) / (6.0 * young * area_moment)


def cantilever_tip_deflection(*, length: float, young: float, area_moment: float, end_force: float) -> float:
    return float(
        cantilever_end_load_deflection(
            np.array([length]),
            length=length,
            young=young,
            area_moment=area_moment,
            end_force=end_force,
        )[0]
    )


def simply_supported_uniform_deflection(
    x: np.ndarray | float,
    *,
    length: float,
    young: float,
    area_moment: float,
    load: float,
) -> np.ndarray:
    """Euler-Bernoulli simply supported beam deflection under uniform load."""

    _require_positive("length", length)
    _require_positive("young", young)
    _require_positive("area_moment", area_moment)
    x_array = _as_array(x)
    return load * x_array * (length**3 - 2.0 * length * x_array**2 + x_array**3) / (
        24.0 * young * area_moment
    )


def simply_supported_uniform_residual(*, young: float, area_moment: float, load: float) -> float:
    """Analytic residual of ``E I w'''' = q`` for the uniform-load solution."""

    _require_positive("young", young)
    _require_positive("area_moment", area_moment)
    return young * area_moment * (load / (young * area_moment)) - load


def fixed_fixed_bar_frequencies(*, modes: int, length: float, young: float, rho: float) -> np.ndarray:
    """Longitudinal frequencies for a fixed-fixed elastic bar."""

    if modes <= 0:
        raise ValueError("modes must be positive")
    _require_positive("length", length)
    _require_positive("young", young)
    _require_positive("rho", rho)
    c = math.sqrt(young / rho)
    n = np.arange(1, modes + 1, dtype=float)
    return n * math.pi * c / length


def fixed_fixed_bar_mode_shape(x: np.ndarray | float, mode: int, *, length: float) -> np.ndarray:
    if mode <= 0:
        raise ValueError("mode must be positive")
    _require_positive("length", length)
    return np.sin(mode * math.pi * _as_array(x) / length)


def save_plot(path: Path, *, points: int, young: float, poisson: float, rho: float) -> None:
    """Save a compact figure of standard elastic-body formulas."""

    os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".matplotlib-cache"))
    os.environ.setdefault("MPLBACKEND", "Agg")
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    lam, mu = lame_from_young_poisson(young, poisson)
    length = 1.0
    area = 0.4
    area_moment = 2.0e-2
    radius = 0.12
    force = 1.0
    torque = 0.008
    x = np.linspace(0.0, length, points)
    r = np.linspace(0.0, radius, points)

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.8), constrained_layout=True)

    for mode in (1, 2, 3):
        axes[0, 0].plot(x, fixed_fixed_bar_mode_shape(x, mode, length=length), lw=2.0, label=f"mode {mode}")
    axes[0, 0].set_title("fixed-fixed bar modes")
    axes[0, 0].set_xlabel("x/L")
    axes[0, 0].set_ylabel("normalized displacement")
    axes[0, 0].legend(frameon=False)
    axes[0, 0].grid(alpha=0.22)

    cantilever = cantilever_end_load_deflection(
        x,
        length=length,
        young=young,
        area_moment=area_moment,
        end_force=force,
    )
    supported = simply_supported_uniform_deflection(
        x,
        length=length,
        young=young,
        area_moment=area_moment,
        load=force,
    )
    axes[0, 1].plot(x, cantilever, lw=2.0, label="cantilever end load")
    axes[0, 1].plot(x, supported, lw=2.0, label="simply supported uniform load")
    axes[0, 1].set_title("Euler-Bernoulli deflection")
    axes[0, 1].set_xlabel("x/L")
    axes[0, 1].set_ylabel("deflection")
    axes[0, 1].legend(frameon=False)
    axes[0, 1].grid(alpha=0.22)

    polar_moment = circular_polar_moment(radius)
    axes[1, 0].plot(r, torsion_shear_stress(r, torque, polar_moment), color="#d62728", lw=2.0)
    axes[1, 0].set_title("circular shaft torsion")
    axes[1, 0].set_xlabel("radius")
    axes[1, 0].set_ylabel("shear stress")
    axes[1, 0].grid(alpha=0.22)

    poisson_values = np.linspace(-0.2, 0.49, points)
    bulk_values = []
    shear_values = []
    cp_values = []
    cs_values = []
    for nu_p in poisson_values:
        lam_i, mu_i = lame_from_young_poisson(young, float(nu_p))
        bulk_values.append(bulk_modulus(lam_i, mu_i))
        shear_values.append(mu_i)
        cp, cs = wave_speeds(lam_i, mu_i, rho)
        cp_values.append(cp)
        cs_values.append(cs)
    axes[1, 1].plot(poisson_values, np.asarray(bulk_values), lw=2.0, label="bulk modulus")
    axes[1, 1].plot(poisson_values, np.asarray(shear_values), lw=2.0, label="shear modulus")
    axes[1, 1].plot(poisson_values, np.asarray(cp_values), lw=1.4, linestyle="--", label="P-wave speed")
    axes[1, 1].plot(poisson_values, np.asarray(cs_values), lw=1.4, linestyle="--", label="S-wave speed")
    axes[1, 1].set_yscale("log")
    axes[1, 1].set_title("approach to incompressibility")
    axes[1, 1].set_xlabel("Poisson ratio")
    axes[1, 1].set_ylabel("value")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)

    fig.savefig(path, dpi=165)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--points", type=int, default=160, help="profile/grid points")
    parser.add_argument("--young", type=float, default=20.0, help="Young modulus")
    parser.add_argument("--poisson", type=float, default=0.3, help="Poisson ratio")
    parser.add_argument("--rho", type=float, default=1.0, help="mass density")
    parser.add_argument("--plot", type=Path, default=None, help="optional output PNG")
    args = parser.parse_args()
    if args.points < 8:
        parser.error("--points must be at least 8")
    return args


def main() -> None:
    args = parse_args()
    lam, mu = lame_from_young_poisson(args.young, args.poisson)
    recovered_young, recovered_poisson = young_poisson_from_lame(lam, mu)
    bulk = bulk_modulus(lam, mu)
    cp, cs = wave_speeds(lam, mu, args.rho)
    frequencies = fixed_fixed_bar_frequencies(modes=3, length=1.0, young=args.young, rho=args.rho)
    elongation = axial_bar_elongation(force=1.0, length=1.0, area=0.4, young=args.young)
    polar_moment = circular_polar_moment(0.12)
    twist = torsion_twist(torque=0.008, length=1.0, mu=mu, polar_moment=polar_moment)
    tip = cantilever_tip_deflection(length=1.0, young=args.young, area_moment=2.0e-2, end_force=1.0)
    beam_residual = simply_supported_uniform_residual(young=args.young, area_moment=2.0e-2, load=1.0)

    print("Linear elasticity diagnostics")
    print(f"young={args.young:.12g}")
    print(f"poisson={args.poisson:.12g}")
    print(f"lambda={lam:.12g}")
    print(f"mu={mu:.12g}")
    print(f"bulk_modulus={bulk:.12g}")
    print(f"recovered_young={recovered_young:.12g}")
    print(f"recovered_poisson={recovered_poisson:.12g}")
    print(f"p_wave_speed={cp:.12g}")
    print(f"s_wave_speed={cs:.12g}")
    print(f"bar_frequency_1={frequencies[0]:.12g}")
    print(f"bar_frequency_2={frequencies[1]:.12g}")
    print(f"bar_frequency_3={frequencies[2]:.12g}")
    print(f"axial_bar_elongation={elongation:.12g}")
    print(f"circular_polar_moment={polar_moment:.12g}")
    print(f"torsion_twist={twist:.12g}")
    print(f"cantilever_tip_deflection={tip:.12g}")
    print(f"simply_supported_uniform_residual={beam_residual:.12g}")

    if args.plot is not None:
        save_plot(args.plot, points=args.points, young=args.young, poisson=args.poisson, rho=args.rho)
        print(f"wrote_plot={args.plot}")


if __name__ == "__main__":
    main()
