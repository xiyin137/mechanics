#!/usr/bin/env python3
"""Exact and reduced Navier-Stokes solutions for classroom use.

This script evaluates standard closed-form solutions:

* Couette-Poiseuille channel flow
* Hagen-Poiseuille pipe flow
* Stokes' first problem
* oscillatory Stokes layer
* Taylor-Green vortex

The formulas are exact under the assumptions stated in the lecture notes.  The
Taylor-Green residual is computed analytically as a check on the nonlinear
Navier-Stokes equation.

Authors: OpenAI GPT 5.5 under the supervision of Xi Yin; review contributions
from Anthropic Opus 4.7.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

import numpy as np

try:
    from demos.python.common import add_output_args, add_preset_args, configure_standard_outputs, emit_summary, fill_defaults
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from common import add_output_args, add_preset_args, configure_standard_outputs, emit_summary, fill_defaults


DEFAULTS = {"points": 160, "nu": 0.1, "mu": 1.0, "h": 1.0, "pipe_radius": 1.0}
PRESETS = {
    "quick": {"points": 16},
    "lecture": {"points": 160},
    "long": {"points": 600},
}


def _as_array(values: np.ndarray | float) -> np.ndarray:
    return np.asarray(values, dtype=float)


def _require_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")


def couette_poiseuille_profile(
    y: np.ndarray | float,
    *,
    h: float = 1.0,
    mu: float = 1.0,
    pressure_gradient: float = 0.0,
    lower_speed: float = 0.0,
    upper_speed: float = 1.0,
) -> np.ndarray:
    """Velocity between plates with wall motion and constant pressure gradient.

    ``pressure_gradient`` uses the positive forcing convention ``G = -dp/dx``,
    so positive values drive positive x-velocity.
    """

    _require_positive("h", h)
    _require_positive("mu", mu)
    y_array = _as_array(y)
    return (
        lower_speed
        + (upper_speed - lower_speed) * y_array / h
        + pressure_gradient * y_array * (h - y_array) / (2.0 * mu)
    )


def couette_poiseuille_flux(
    *,
    h: float = 1.0,
    mu: float = 1.0,
    pressure_gradient: float = 0.0,
    lower_speed: float = 0.0,
    upper_speed: float = 1.0,
) -> float:
    """Volume flux per unit span for Couette-Poiseuille channel flow."""

    _require_positive("h", h)
    _require_positive("mu", mu)
    return 0.5 * h * (lower_speed + upper_speed) + pressure_gradient * h**3 / (12.0 * mu)


def plane_couette_profile(y: np.ndarray | float, *, h: float = 1.0, wall_speed: float = 1.0) -> np.ndarray:
    return couette_poiseuille_profile(
        y,
        h=h,
        mu=1.0,
        pressure_gradient=0.0,
        lower_speed=0.0,
        upper_speed=wall_speed,
    )


def plane_poiseuille_profile(
    y: np.ndarray | float,
    *,
    h: float = 1.0,
    mu: float = 1.0,
    pressure_gradient: float = 1.0,
) -> np.ndarray:
    return couette_poiseuille_profile(
        y,
        h=h,
        mu=mu,
        pressure_gradient=pressure_gradient,
        lower_speed=0.0,
        upper_speed=0.0,
    )


def plane_poiseuille_flux(*, h: float = 1.0, mu: float = 1.0, pressure_gradient: float = 1.0) -> float:
    _require_positive("h", h)
    _require_positive("mu", mu)
    return pressure_gradient * h**3 / (12.0 * mu)


def pipe_poiseuille_profile(
    r: np.ndarray | float,
    *,
    radius: float = 1.0,
    mu: float = 1.0,
    pressure_gradient: float = 1.0,
) -> np.ndarray:
    """Axial velocity in a circular pipe of radius ``radius``."""

    _require_positive("radius", radius)
    _require_positive("mu", mu)
    r_array = _as_array(r)
    return pressure_gradient * (radius**2 - r_array**2) / (4.0 * mu)


def pipe_poiseuille_flux(*, radius: float = 1.0, mu: float = 1.0, pressure_gradient: float = 1.0) -> float:
    _require_positive("radius", radius)
    _require_positive("mu", mu)
    return math.pi * radius**4 * pressure_gradient / (8.0 * mu)


def stokes_first_problem(
    y: np.ndarray | float,
    t: float,
    *,
    wall_speed: float = 1.0,
    nu: float = 1.0,
) -> np.ndarray:
    """Velocity in Stokes' first problem for an impulsively moved wall."""

    _require_positive("t", t)
    _require_positive("nu", nu)
    eta = _as_array(y) / (2.0 * math.sqrt(nu * t))
    erfc_values = np.array([math.erfc(float(v)) for v in eta.ravel()], dtype=float)
    return wall_speed * erfc_values.reshape(eta.shape)


def oscillatory_stokes_layer(
    y: np.ndarray | float,
    t: float,
    *,
    wall_speed: float = 1.0,
    angular_frequency: float = 1.0,
    nu: float = 1.0,
) -> np.ndarray:
    """Velocity in the oscillatory Stokes layer over an infinite plate."""

    _require_positive("angular_frequency", angular_frequency)
    _require_positive("nu", nu)
    y_array = _as_array(y)
    delta = math.sqrt(2.0 * nu / angular_frequency)
    return wall_speed * np.exp(-y_array / delta) * np.cos(angular_frequency * t - y_array / delta)


def taylor_green_amplitude(t: float, *, nu: float = 1.0, wave_number: float = 1.0, speed: float = 1.0) -> float:
    _require_positive("nu", nu)
    _require_positive("wave_number", wave_number)
    return speed * math.exp(-2.0 * nu * wave_number**2 * t)


def taylor_green_velocity_pressure(
    x: np.ndarray | float,
    y: np.ndarray | float,
    t: float,
    *,
    nu: float = 1.0,
    wave_number: float = 1.0,
    speed: float = 1.0,
    rho: float = 1.0,
    p0: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Velocity and pressure for the two-dimensional Taylor-Green vortex."""

    _require_positive("rho", rho)
    x_array = _as_array(x)
    y_array = _as_array(y)
    k = wave_number
    amplitude = taylor_green_amplitude(t, nu=nu, wave_number=k, speed=speed)
    u = amplitude * np.sin(k * x_array) * np.cos(k * y_array)
    v = -amplitude * np.cos(k * x_array) * np.sin(k * y_array)
    p = p0 + 0.25 * rho * amplitude**2 * (np.cos(2.0 * k * x_array) + np.cos(2.0 * k * y_array))
    return u, v, p


def taylor_green_vorticity(
    x: np.ndarray | float,
    y: np.ndarray | float,
    t: float,
    *,
    nu: float = 1.0,
    wave_number: float = 1.0,
    speed: float = 1.0,
) -> np.ndarray:
    k = wave_number
    amplitude = taylor_green_amplitude(t, nu=nu, wave_number=k, speed=speed)
    return 2.0 * k * amplitude * np.sin(k * _as_array(x)) * np.sin(k * _as_array(y))


def taylor_green_energy_density(
    t: float,
    *,
    nu: float = 1.0,
    wave_number: float = 1.0,
    speed: float = 1.0,
    rho: float = 1.0,
) -> float:
    _require_positive("rho", rho)
    amplitude = taylor_green_amplitude(t, nu=nu, wave_number=wave_number, speed=speed)
    return 0.25 * rho * amplitude**2


def taylor_green_residual_norm(
    x: np.ndarray,
    y: np.ndarray,
    t: float,
    *,
    nu: float = 1.0,
    wave_number: float = 1.0,
    speed: float = 1.0,
    rho: float = 1.0,
) -> float:
    """Analytic maximum residual in the Taylor-Green Navier-Stokes equation."""

    _require_positive("rho", rho)
    k = wave_number
    amplitude = taylor_green_amplitude(t, nu=nu, wave_number=k, speed=speed)
    u, v, _ = taylor_green_velocity_pressure(
        x,
        y,
        t,
        nu=nu,
        wave_number=k,
        speed=speed,
        rho=rho,
    )
    sin2x = np.sin(2.0 * k * x)
    sin2y = np.sin(2.0 * k * y)
    du_dt = -2.0 * nu * k**2 * u
    dv_dt = -2.0 * nu * k**2 * v
    lap_u = -2.0 * k**2 * u
    lap_v = -2.0 * k**2 * v
    adv_u = 0.5 * amplitude**2 * k * sin2x
    adv_v = 0.5 * amplitude**2 * k * sin2y
    gradp_u_over_rho = -0.5 * amplitude**2 * k * sin2x
    gradp_v_over_rho = -0.5 * amplitude**2 * k * sin2y
    residual_u = du_dt + adv_u + gradp_u_over_rho - nu * lap_u
    residual_v = dv_dt + adv_v + gradp_v_over_rho - nu * lap_v
    return float(max(np.max(np.abs(residual_u)), np.max(np.abs(residual_v))))


def save_plot(path: Path, *, points: int, nu: float, mu: float, h: float, radius: float) -> None:
    """Save a four-panel figure of exact Navier-Stokes solution families."""

    os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".matplotlib-cache"))
    os.environ.setdefault("MPLBACKEND", "Agg")
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    y = np.linspace(0.0, h, points)
    r = np.linspace(0.0, radius, points)
    halfspace_y = np.linspace(0.0, 4.0, points)
    grid = np.linspace(0.0, 2.0 * math.pi, points)
    xx, yy = np.meshgrid(grid, grid)
    vort = taylor_green_vorticity(xx, yy, t=0.15, nu=nu)

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8.0), constrained_layout=True)

    axes[0, 0].plot(plane_couette_profile(y, h=h), y, label="Couette", lw=2.0)
    axes[0, 0].plot(plane_poiseuille_profile(y, h=h, mu=mu), y, label="Poiseuille", lw=2.0)
    axes[0, 0].plot(
        couette_poiseuille_profile(y, h=h, mu=mu, pressure_gradient=1.0, upper_speed=0.5),
        y,
        label="combined",
        lw=2.0,
    )
    axes[0, 0].set_xlabel("velocity")
    axes[0, 0].set_ylabel("channel coordinate y")
    axes[0, 0].set_title("channel profiles")
    axes[0, 0].legend(frameon=False)
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].plot(pipe_poiseuille_profile(r, radius=radius, mu=mu), r, color="#d62728", lw=2.0)
    axes[0, 1].set_xlabel("axial velocity")
    axes[0, 1].set_ylabel("pipe radius r")
    axes[0, 1].set_title("Hagen-Poiseuille pipe flow")
    axes[0, 1].grid(alpha=0.22)

    for t, color in [(0.05, "#1f77b4"), (0.20, "#2ca02c"), (0.80, "#9467bd")]:
        axes[1, 0].plot(
            stokes_first_problem(halfspace_y, t, nu=nu),
            halfspace_y,
            color=color,
            lw=2.0,
            label=f"t={t:g}",
        )
    axes[1, 0].set_xlabel("velocity")
    axes[1, 0].set_ylabel("distance from wall y")
    axes[1, 0].set_title("Stokes' first problem")
    axes[1, 0].legend(frameon=False)
    axes[1, 0].grid(alpha=0.22)

    image = axes[1, 1].imshow(
        vort,
        origin="lower",
        extent=(0.0, 2.0 * math.pi, 0.0, 2.0 * math.pi),
        cmap="coolwarm",
        aspect="equal",
    )
    axes[1, 1].set_xlabel("x")
    axes[1, 1].set_ylabel("y")
    axes[1, 1].set_title("Taylor-Green vorticity")
    fig.colorbar(image, ax=axes[1, 1], shrink=0.82, label="vorticity")

    fig.savefig(path, dpi=165)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_preset_args(parser)
    parser.add_argument("--points", type=int, default=None, help="grid/profile points")
    parser.add_argument("--nu", type=float, default=None, help="kinematic viscosity")
    parser.add_argument("--mu", type=float, default=None, help="dynamic viscosity")
    parser.add_argument("--h", type=float, default=None, help="channel height")
    parser.add_argument("--pipe-radius", type=float, default=None, help="pipe radius")
    parser.add_argument("--plot", type=Path, default=None, help="optional output PNG")
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
    configure_standard_outputs(args, stem="navier_stokes_solutions", plot_name="navier_stokes_solutions.png")
    if args.points < 4:
        parser.error("--points must be at least 4")
    if args.nu <= 0.0:
        parser.error("--nu must be > 0")
    if args.mu <= 0.0:
        parser.error("--mu must be > 0")
    if args.h <= 0.0:
        parser.error("--h must be > 0")
    if args.pipe_radius <= 0.0:
        parser.error("--pipe-radius must be > 0")
    return args


def build_summary(args: argparse.Namespace) -> dict[str, object]:
    y = np.linspace(0.0, args.h, args.points)
    grid = np.linspace(0.0, 2.0 * math.pi, args.points)
    xx, yy = np.meshgrid(grid, grid)
    channel_profile = couette_poiseuille_profile(y, h=args.h, mu=args.mu, pressure_gradient=1.0, upper_speed=0.5)

    channel_flux = couette_poiseuille_flux(
        h=args.h,
        mu=args.mu,
        pressure_gradient=1.0,
        lower_speed=0.0,
        upper_speed=0.5,
    )
    pipe_flux = pipe_poiseuille_flux(radius=args.pipe_radius, mu=args.mu, pressure_gradient=1.0)
    stokes_wall = stokes_first_problem(np.array([0.0]), 0.2, nu=args.nu)[0]
    stokes_far = stokes_first_problem(np.array([4.0]), 0.2, nu=args.nu)[0]
    residual = taylor_green_residual_norm(xx, yy, t=0.15, nu=args.nu)
    energy = taylor_green_energy_density(t=0.15, nu=args.nu)
    return {
        "model": "exact and reduced Navier-Stokes solutions",
        "configuration": {
            "points": args.points,
            "nu": args.nu,
            "mu": args.mu,
            "h": args.h,
            "pipe_radius": args.pipe_radius,
        },
        "channel_velocity_min": float(np.min(channel_profile)),
        "channel_velocity_max": float(np.max(channel_profile)),
        "channel_flux": channel_flux,
        "pipe_center_velocity": float(pipe_poiseuille_profile(np.array([0.0]), radius=args.pipe_radius, mu=args.mu)[0]),
        "pipe_wall_velocity": float(pipe_poiseuille_profile(np.array([args.pipe_radius]), radius=args.pipe_radius, mu=args.mu)[0]),
        "pipe_flux": pipe_flux,
        "stokes_first_wall_value": float(stokes_wall),
        "stokes_first_far_value": float(stokes_far),
        "taylor_green_energy_density": energy,
        "taylor_green_residual_norm": residual,
        "diagnostic_note": "The Taylor-Green residual is evaluated analytically at grid points.",
        "outputs": {},
    }


def print_summary(summary: dict[str, object]) -> None:
    config = summary["configuration"]
    print("Navier-Stokes exact-solution diagnostics")
    print(f"points={config['points']}")
    print(f"channel_velocity_min={summary['channel_velocity_min']:.12g}")
    print(f"channel_velocity_max={summary['channel_velocity_max']:.12g}")
    print(f"channel_flux={summary['channel_flux']:.12g}")
    print(f"pipe_center_velocity={summary['pipe_center_velocity']:.12g}")
    print(f"pipe_wall_velocity={summary['pipe_wall_velocity']:.12g}")
    print(f"pipe_flux={summary['pipe_flux']:.12g}")
    print(f"stokes_first_wall_value={summary['stokes_first_wall_value']:.12g}")
    print(f"stokes_first_far_value={summary['stokes_first_far_value']:.12g}")
    print(f"taylor_green_energy_density={summary['taylor_green_energy_density']:.12g}")
    print(f"taylor_green_residual_norm={summary['taylor_green_residual_norm']:.12g}")


def main() -> None:
    args = parse_args()

    if args.plot is not None:
        save_plot(args.plot, points=args.points, nu=args.nu, mu=args.mu, h=args.h, radius=args.pipe_radius)
    emit_summary(build_summary(args), args, print_summary)


if __name__ == "__main__":
    main()
