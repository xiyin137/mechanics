from __future__ import annotations

import csv
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_demo_module(name: str):
    path = ROOT / "demos" / "python" / name
    module_name = f"_mechanics_demo_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_python_demo(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("PYTHONPYCACHEPREFIX", str(ROOT / ".pycache-build"))
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def run_python_demo_unchecked(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("PYTHONPYCACHEPREFIX", str(ROOT / ".pycache-build"))
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_python_demos_compile() -> None:
    run_python_demo("-m", "compileall", "-q", "demos/python")


def test_major_python_demos_expose_help() -> None:
    scripts = [
        "asteroid_ejection_probability.py",
        "circular_restricted_three_body.py",
        "cosserat_rod_demo.py",
        "deforming_body_gauge.py",
        "fluids_vorticity.py",
        "hamiltonian_pendulum.py",
        "linear_elasticity.py",
        "navier_stokes_solutions.py",
        "rigid_body_euler_top.py",
        "standard_map.py",
        "standard_map_torus_breakdown.py",
    ]
    for script in scripts:
        result = run_python_demo("demos/python/" + script, "--help")
        assert "usage:" in result.stdout


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_core_demos_run_small_cases() -> None:
    run_python_demo("demos/python/rigid_body_euler_top.py", "--steps", "20")
    run_python_demo("demos/python/hamiltonian_pendulum.py", "--steps", "20")
    run_python_demo("demos/python/standard_map.py", "--orbits", "3", "--steps", "5")
    run_python_demo("demos/python/standard_map_torus_breakdown.py", "--orbits", "4", "--steps", "8")
    run_python_demo("demos/python/fluids_vorticity.py", "--steps", "10")
    run_python_demo("demos/python/navier_stokes_solutions.py", "--points", "12")
    run_python_demo("demos/python/linear_elasticity.py", "--points", "12")
    run_python_demo("demos/python/cosserat_rod_demo.py", "--points", "20")
    run_python_demo("demos/python/deforming_body_gauge.py", "--delta-alpha", "0.05", "--delta-beta", "0.04")
    run_python_demo("demos/python/circular_restricted_three_body.py", "--periods", "0.05", "--dt", "0.02")


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_asteroid_ejection_probability_runs_small_case() -> None:
    result = run_python_demo(
        "demos/python/asteroid_ejection_probability.py",
        "--n",
        "12",
        "--years",
        "0.2",
        "--dt",
        "0.05",
        "--bins",
        "4",
        "--no-plot",
    )
    assert "ejection_probability=" in result.stdout


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_core_demos_emit_quick_json() -> None:
    cases = [
        ("demos/python/hamiltonian_pendulum.py", ["--quick", "--json"], "model"),
        ("demos/python/rigid_body_euler_top.py", ["--quick", "--json"], "energy_max_abs_drift"),
        ("demos/python/standard_map.py", ["--quick", "--json"], "finite_rotation_mean"),
        ("demos/python/standard_map_torus_breakdown.py", ["--quick", "--json"], "diagnostics"),
        ("demos/python/circular_restricted_three_body.py", ["--quick", "--json"], "jacobi_max_abs_drift"),
        ("demos/python/asteroid_ejection_probability.py", ["--quick", "--no-plot", "--json"], "ejection_standard_error"),
        ("demos/python/linear_elasticity.py", ["--quick", "--json"], "moduli_round_trip_error"),
        ("demos/python/deforming_body_gauge.py", ["--quick", "--json"], "bch_error_norm"),
        ("demos/python/cosserat_rod_demo.py", ["--quick", "--json"], "frame_holonomy"),
        ("demos/python/navier_stokes_solutions.py", ["--quick", "--json"], "taylor_green_residual_norm"),
        ("demos/python/fluids_vorticity.py", ["--quick", "--json"], "hamiltonian_max_abs_drift"),
    ]
    for script, args, required_key in cases:
        result = run_python_demo(script, *args)
        data = json.loads(result.stdout)
        assert required_key in data
        assert "outputs" in data


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_asteroid_ejection_probability_writes_json(tmp_path: Path) -> None:
    output = tmp_path / "asteroid_summary.json"
    result = run_python_demo(
        "demos/python/asteroid_ejection_probability.py",
        "--n",
        "12",
        "--years",
        "0.2",
        "--dt",
        "0.05",
        "--bins",
        "4",
        "--no-plot",
        "--json-output",
        str(output),
    )
    data = json.loads(output.read_text())
    assert "wrote_json=" in result.stdout
    assert data["model"]["name"] == "planar restricted Sun-Jupiter-asteroid ensemble"
    assert data["configuration"]["dt"] == pytest.approx(0.05)
    assert "ejection_standard_error" in data
    assert "ejection_standard_error" in data["bin_rows"][0]


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_cr3bp_json_stdout_and_file_are_machine_readable(tmp_path: Path) -> None:
    output = tmp_path / "cr3bp_summary.json"
    result = run_python_demo(
        "demos/python/circular_restricted_three_body.py",
        "--quick",
        "--json",
        "--json-output",
        str(output),
    )
    stdout_data = json.loads(result.stdout)
    file_data = json.loads(output.read_text())
    assert stdout_data["model"] == "circular restricted three-body problem"
    assert file_data["preset"] == "sun-jupiter"
    assert "jacobi_max_abs_drift" in stdout_data
    assert "L4" in stdout_data["lagrange_points"]


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_rigid_body_invariants_have_small_drift() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("rigid_body_euler_top.py")
    body = demo.RigidBody(1.0, 2.0, 3.0)
    _, omega = demo.simulate(body, np.array([0.05, 1.0, 0.05]), dt=0.005, steps=200)
    energy, momentum_sq = demo.invariants(omega, body)
    assert np.max(np.abs(energy - energy[0])) < 1.0e-12
    assert np.max(np.abs(momentum_sq - momentum_sq[0])) < 1.0e-11


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_rigid_body_attitude_reconstruction_conserves_spatial_momentum() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("rigid_body_euler_top.py")
    body = demo.RigidBody(1.0, 2.0, 3.0)
    _, omega, attitude = demo.simulate_attitude(
        body, np.array([0.12, 0.9, 0.16]), dt=0.001, steps=500
    )
    orthogonality_error, determinant_error = demo.attitude_errors(attitude)
    spatial_momentum = demo.spatial_momentum(omega, attitude, body)
    assert orthogonality_error < 1.0e-12
    assert determinant_error < 1.0e-12
    assert np.max(np.linalg.norm(spatial_momentum - spatial_momentum[0], axis=1)) < 5.0e-7


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_pendulum_symplectic_euler_energy_stays_bounded() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("hamiltonian_pendulum.py")
    _, q, p = demo.integrate(q0=1.0, p0=0.0, dt=0.01, steps=1000)
    energy = demo.hamiltonian(q, p)
    assert np.max(np.abs(energy - energy[0])) < 3.0e-3


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_standard_map_is_area_preserving_away_from_wrap() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("standard_map.py")
    K = 0.95
    h = 1.0e-6

    def one_step(q0: float, p0: float) -> np.ndarray:
        q, p = demo.iterate_standard_map(np.array([q0]), np.array([p0]), K=K, steps=1)
        return np.array([q[1, 0], p[1, 0]])

    q0 = 1.1
    p0 = 1.4
    dq_column = (one_step(q0 + h, p0) - one_step(q0 - h, p0)) / (2.0 * h)
    dp_column = (one_step(q0, p0 + h) - one_step(q0, p0 - h)) / (2.0 * h)
    jacobian = np.column_stack((dq_column, dp_column))
    assert np.linalg.det(jacobian) == pytest.approx(1.0, abs=1.0e-9)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_standard_map_zero_k_is_exact_twist_map() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("standard_map.py")
    q0 = np.array([0.2, 2.0, 5.1])
    p0 = np.array([0.3, 1.2, 2.7])
    steps = 6
    q, p = demo.iterate_standard_map(q0, p0, K=0.0, steps=steps)
    expected_steps = np.arange(steps + 1)[:, None]
    assert np.allclose(p, p0[None, :])
    assert np.allclose(q, (q0[None, :] + expected_steps * p0[None, :]) % demo.TWOPI)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_standard_map_cylinder_zero_k_has_constant_momentum() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("standard_map_torus_breakdown.py")
    q0 = np.array([0.2, 2.0, 5.1])
    p0 = np.array([0.3, 1.2, 2.7])
    steps = 7
    q_mod, p, q_lift = demo.iterate_cylinder(q0, p0, K=0.0, steps=steps)
    expected_steps = np.arange(steps + 1)[:, None]
    assert np.allclose(p, p0[None, :])
    assert np.allclose(q_lift, q0[None, :] + expected_steps * p0[None, :])
    assert np.allclose(q_mod, q_lift % demo.TWOPI)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_standard_map_breakdown_summary_is_sensible() -> None:
    demo = load_demo_module("standard_map_torus_breakdown.py")
    q_mod, p, q_lift, summary = demo.run_ensemble(K=1.1, orbits=6, steps=12, seed=3)
    assert q_mod.shape == p.shape == q_lift.shape == (13, 6)
    assert summary["p_span_initial"] >= 0.0
    assert summary["p_span_final"] >= 0.0
    assert summary["mean_abs_delta_p"] >= 0.0
    assert summary["max_abs_delta_p"] >= summary["mean_abs_delta_p"]


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_point_vortex_hamiltonian_has_small_drift() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("fluids_vorticity.py")
    _, _, energy = demo.simulate(steps=80, dt=0.005)
    assert np.max(np.abs(energy - energy[0])) < 1.0e-12


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_opposite_point_vortex_pair_translates_without_stretching() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("fluids_vorticity.py")
    positions = np.array([[-0.5, 0.0], [0.5, 0.0]])
    gamma = np.array([1.0, -1.0])
    vel = demo.velocity(positions, gamma)
    assert np.allclose(vel[0], vel[1])
    assert np.dot(vel[1] - vel[0], positions[1] - positions[0]) == pytest.approx(0.0)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_couette_poiseuille_profile_matches_boundaries_and_flux() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("navier_stokes_solutions.py")
    h = 2.0
    mu = 3.0
    lower_speed = -0.25
    upper_speed = 0.75
    pressure_gradient = 1.2
    y = np.array([0.0, h])
    values = demo.couette_poiseuille_profile(
        y,
        h=h,
        mu=mu,
        pressure_gradient=pressure_gradient,
        lower_speed=lower_speed,
        upper_speed=upper_speed,
    )
    assert values[0] == pytest.approx(lower_speed)
    assert values[1] == pytest.approx(upper_speed)
    assert demo.couette_poiseuille_flux(
        h=h,
        mu=mu,
        pressure_gradient=pressure_gradient,
        lower_speed=lower_speed,
        upper_speed=upper_speed,
    ) == pytest.approx(0.5 * h * (lower_speed + upper_speed) + pressure_gradient * h**3 / (12.0 * mu))


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_poiseuille_and_stokes_exact_solution_formulas() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("navier_stokes_solutions.py")
    radius = 1.7
    mu = 0.8
    pressure_gradient = 2.5
    center = demo.pipe_poiseuille_profile(np.array([0.0]), radius=radius, mu=mu, pressure_gradient=pressure_gradient)[0]
    wall = demo.pipe_poiseuille_profile(np.array([radius]), radius=radius, mu=mu, pressure_gradient=pressure_gradient)[0]
    assert center == pytest.approx(pressure_gradient * radius**2 / (4.0 * mu))
    assert wall == pytest.approx(0.0)
    assert demo.pipe_poiseuille_flux(radius=radius, mu=mu, pressure_gradient=pressure_gradient) == pytest.approx(
        np.pi * radius**4 * pressure_gradient / (8.0 * mu)
    )
    stokes = demo.stokes_first_problem(np.array([0.0, 10.0]), 0.4, wall_speed=1.3, nu=0.2)
    assert stokes[0] == pytest.approx(1.3)
    assert stokes[1] < 1.0e-20


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_taylor_green_vortex_solves_navier_stokes_analytically() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("navier_stokes_solutions.py")
    grid = np.linspace(0.0, 2.0 * np.pi, 17)
    x, y = np.meshgrid(grid, grid)
    residual = demo.taylor_green_residual_norm(x, y, t=0.3, nu=0.07, wave_number=1.0, speed=1.2)
    assert residual < 1.0e-12
    assert demo.taylor_green_energy_density(t=0.3, nu=0.07, wave_number=1.0, speed=1.2) == pytest.approx(
        0.25 * 1.2**2 * np.exp(-4.0 * 0.07 * 0.3)
    )
    with pytest.raises(ValueError):
        demo.taylor_green_energy_density(t=0.3, rho=-1.0)


def test_linear_elasticity_moduli_round_trip_and_wave_speeds() -> None:
    demo = load_demo_module("linear_elasticity.py")
    young = 12.0
    poisson = 0.25
    lam, mu = demo.lame_from_young_poisson(young, poisson)
    recovered_young, recovered_poisson = demo.young_poisson_from_lame(lam, mu)
    assert recovered_young == pytest.approx(young)
    assert recovered_poisson == pytest.approx(poisson)
    assert demo.bulk_modulus(lam, mu) == pytest.approx(young / (3.0 * (1.0 - 2.0 * poisson)))
    cp, cs = demo.wave_speeds(lam, mu, rho=3.0)
    assert cp == pytest.approx(((lam + 2.0 * mu) / 3.0) ** 0.5)
    assert cs == pytest.approx((mu / 3.0) ** 0.5)
    with pytest.raises(ValueError):
        demo.lame_from_young_poisson(young, 0.5)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_linear_elasticity_bar_torsion_and_beam_formulas() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("linear_elasticity.py")
    assert demo.axial_bar_elongation(force=5.0, length=2.0, area=0.5, young=10.0) == pytest.approx(2.0)
    polar = demo.circular_polar_moment(0.4)
    assert polar == pytest.approx(0.5 * np.pi * 0.4**4)
    assert demo.torsion_twist(torque=3.0, length=2.0, mu=4.0, polar_moment=polar) == pytest.approx(
        3.0 * 2.0 / (4.0 * polar)
    )
    tip = demo.cantilever_tip_deflection(length=2.0, young=10.0, area_moment=0.25, end_force=3.0)
    assert tip == pytest.approx(3.0 * 2.0**3 / (3.0 * 10.0 * 0.25))
    x = np.array([0.0, 1.0, 2.0])
    simply_supported = demo.simply_supported_uniform_deflection(
        x,
        length=2.0,
        young=10.0,
        area_moment=0.25,
        load=4.0,
    )
    assert simply_supported[0] == pytest.approx(0.0)
    assert simply_supported[-1] == pytest.approx(0.0)
    assert demo.simply_supported_uniform_residual(young=10.0, area_moment=0.25, load=4.0) == pytest.approx(0.0)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_linear_elasticity_fixed_fixed_modes() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("linear_elasticity.py")
    frequencies = demo.fixed_fixed_bar_frequencies(modes=3, length=2.0, young=18.0, rho=2.0)
    assert np.allclose(frequencies, np.array([1.0, 2.0, 3.0]) * np.pi * 3.0 / 2.0)
    x = np.array([0.0, 1.0, 2.0])
    shape = demo.fixed_fixed_bar_mode_shape(x, 1, length=2.0)
    assert shape[0] == pytest.approx(0.0)
    assert shape[-1] == pytest.approx(0.0, abs=1.0e-15)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_kepler_solver_residual_is_tiny_for_demo_eccentricities() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("asteroid_ejection_probability.py")
    mean = np.linspace(0.0, 2.0 * np.pi, 17)
    ecc = np.linspace(0.0, 0.08, 17)
    anomaly = demo.solve_kepler(mean, ecc)
    residual = anomaly - ecc * np.sin(anomaly) - mean
    assert np.max(np.abs(residual)) < 1.0e-13


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_kepler_solver_handles_moderately_high_eccentricity() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("asteroid_ejection_probability.py")
    mean = np.linspace(0.0, 2.0 * np.pi, 29)
    ecc = np.linspace(0.0, 0.8, 29)
    anomaly = demo.solve_kepler(mean, ecc)
    residual = anomaly - ecc * np.sin(anomaly) - mean
    assert np.max(np.abs(residual)) < 1.0e-12
    with pytest.raises(ValueError):
        demo.solve_kepler(np.array([0.0]), np.array([1.0]))


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_cosserat_frame_holonomy_matches_integrated_curvature() -> None:
    demo = load_demo_module("cosserat_rod_demo.py")
    length = 8.0
    base = 0.18
    data = demo.reconstruct(length=length, points=801, base=base, amp=0.55, mode=2)
    assert data["theta"][-1] - data["theta"][0] == pytest.approx(base * length, abs=1.0e-12)
    assert data["x"][0] == pytest.approx(0.0)
    assert data["y"][0] == pytest.approx(0.0)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_cosserat_constant_curvature_closes_unit_circle() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("cosserat_rod_demo.py")
    data = demo.reconstruct(length=2.0 * np.pi, points=2001, base=1.0, amp=0.0, mode=1)
    assert data["theta"][-1] == pytest.approx(2.0 * np.pi, abs=1.0e-12)
    assert data["x"][-1] == pytest.approx(0.0, abs=1.0e-6)
    assert data["y"][-1] == pytest.approx(0.0, abs=1.0e-6)
    with pytest.raises(ValueError):
        demo.reconstruct(length=1.0, points=1, base=1.0, amp=0.0, mode=1)
    with pytest.raises(ValueError):
        demo.reconstruct(length=0.0, points=10, base=1.0, amp=0.0, mode=1)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_deforming_body_gauge_small_loop_matches_curvature() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("deforming_body_gauge.py")
    da = 1.0e-4
    db = 1.3e-4
    rotation = demo.rectangular_stroke(4.0, 1.0, 1.5, da, db)
    rotvec = demo.rotation_vector(rotation)
    expected = demo.curvature_vector(4.0, 1.0, 1.5) * da * db
    assert np.allclose(rotvec, expected, rtol=1.0e-5, atol=1.0e-12)
    assert np.linalg.norm(rotation.T @ rotation - np.eye(3)) < 1.0e-14
    assert abs(np.linalg.det(rotation) - 1.0) < 1.0e-14


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_deforming_body_gauge_validates_inertias() -> None:
    demo = load_demo_module("deforming_body_gauge.py")
    with pytest.raises(ValueError):
        demo.connection_components(0.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        demo.rectangular_stroke(1.0, 1.0, 1.0, 0.1, 0.1, cycles=0)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_helicopter_rotor_wrappers_match_two_rotor_model() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("deforming_body_gauge.py")
    body = 4.0
    lift = 1.0
    tail = 1.5
    a_lift, a_tail = demo.helicopter_rotor_connection(body, lift, tail)
    expected_lift, expected_tail = demo.connection_components(body, lift, tail)
    assert np.allclose(a_lift, expected_lift)
    assert np.allclose(a_tail, expected_tail)
    assert np.allclose(
        demo.helicopter_rotor_stroke(body, lift, tail, 0.08, 0.05),
        demo.rectangular_stroke(body, lift, tail, 0.08, 0.05),
    )


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_asteroid_summary_probabilities_and_counts_are_consistent() -> None:
    demo = load_demo_module("asteroid_ejection_probability.py")
    cfg = demo.Config(
        n=12,
        years=0.2,
        dt=0.05,
        seed=1,
        a_min=2.05,
        a_max=3.75,
        e_max=0.08,
        bins=4,
        m_sun=demo.M_SUN,
        m_jupiter=demo.M_JUPITER,
        a_jupiter=demo.A_JUPITER,
        ejection_radius=20.0,
        sun_radius=0.02,
        jupiter_close_radius=0.03,
        include_indirect=True,
        resonance_window=0.05,
    )
    summary = demo.integrate(cfg)
    status_total = (
        summary["alive"]
        + summary["ejected"]
        + summary["sun_collision"]
        + summary["jupiter_close"]
    )
    assert status_total == summary["n"]
    assert sum(row["count"] for row in summary["bin_rows"]) == summary["n"]
    assert 0.0 <= summary["ejection_probability"] <= summary["loss_probability"] <= 1.0
    assert all("nearest_resonance" in row for row in summary["bin_rows"])


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_asteroid_summary_includes_right_bin_endpoint() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("asteroid_ejection_probability.py")
    cfg = demo.Config(
        n=3,
        years=0.0,
        dt=0.05,
        seed=1,
        a_min=2.0,
        a_max=3.0,
        e_max=0.08,
        bins=2,
        m_sun=demo.M_SUN,
        m_jupiter=demo.M_JUPITER,
        a_jupiter=demo.A_JUPITER,
        ejection_radius=20.0,
        sun_radius=0.02,
        jupiter_close_radius=0.03,
        include_indirect=True,
        resonance_window=0.05,
    )
    status = np.array([demo.ALIVE, demo.EJECTED, demo.ALIVE], dtype=np.int8)
    elements = {
        "a": np.array([2.0, 2.5, 3.0]),
        "mean_anomaly": np.zeros(3),
        "periapse_longitude": np.zeros(3),
    }
    summary = demo.summarize(elements, status, cfg, elapsed_years=0.0)
    assert sum(row["count"] for row in summary["bin_rows"]) == 3
    assert summary["bin_rows"][-1]["count"] == 2


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_asteroid_zero_particles_is_well_defined() -> None:
    demo = load_demo_module("asteroid_ejection_probability.py")
    cfg = demo.Config(
        n=0,
        years=0.2,
        dt=0.05,
        seed=1,
        a_min=2.05,
        a_max=3.75,
        e_max=0.08,
        bins=4,
        m_sun=demo.M_SUN,
        m_jupiter=demo.M_JUPITER,
        a_jupiter=demo.A_JUPITER,
        ejection_radius=20.0,
        sun_radius=0.02,
        jupiter_close_radius=0.03,
        include_indirect=True,
        resonance_window=0.05,
    )
    summary = demo.integrate(cfg)
    assert summary["n"] == 0
    assert summary["alive"] == 0
    assert summary["ejection_probability"] == 0.0
    assert summary["loss_probability"] == 0.0


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_asteroid_kepler_initial_conditions_match_orbital_elements() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("asteroid_ejection_probability.py")
    cfg = demo.Config(
        n=48,
        years=0.0,
        dt=0.05,
        seed=9,
        a_min=2.05,
        a_max=3.75,
        e_max=0.08,
        bins=4,
        m_sun=demo.M_SUN,
        m_jupiter=demo.M_JUPITER,
        a_jupiter=demo.A_JUPITER,
        ejection_radius=20.0,
        sun_radius=0.02,
        jupiter_close_radius=0.03,
        include_indirect=True,
        resonance_window=0.05,
    )
    pos, vel, elements = demo.sample_initial_conditions(cfg)
    a0 = elements["a"]
    radius = np.linalg.norm(pos, axis=1)
    speed_sq = np.sum(vel * vel, axis=1)
    specific_energy = 0.5 * speed_sq - cfg.gm_sun / radius
    assert np.allclose(specific_energy, -cfg.gm_sun / (2.0 * a0), rtol=1.0e-12, atol=1.0e-12)

    angular_momentum = pos[:, 0] * vel[:, 1] - pos[:, 1] * vel[:, 0]
    eccentricity_sq = 1.0 - angular_momentum * angular_momentum / (cfg.gm_sun * a0)
    assert np.all(eccentricity_sq >= -1.0e-12)
    assert np.all(eccentricity_sq <= cfg.e_max * cfg.e_max + 1.0e-12)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_asteroid_acceleration_matches_finite_difference_potential() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("asteroid_ejection_probability.py")
    cfg = demo.Config(
        n=1,
        years=0.0,
        dt=0.05,
        seed=1,
        a_min=2.05,
        a_max=3.75,
        e_max=0.08,
        bins=4,
        m_sun=demo.M_SUN,
        m_jupiter=demo.M_JUPITER,
        a_jupiter=demo.A_JUPITER,
        ejection_radius=20.0,
        sun_radius=0.02,
        jupiter_close_radius=0.03,
        include_indirect=True,
        resonance_window=0.05,
    )
    t = 0.3
    pos = np.array([2.4, 0.7])
    rj = demo.jupiter_position(t, cfg)

    def potential(x: np.ndarray) -> float:
        return (
            -cfg.gm_sun / np.linalg.norm(x)
            - cfg.gm_jupiter / np.linalg.norm(x - rj)
            + cfg.gm_jupiter * float(np.dot(rj, x)) / float(np.linalg.norm(rj) ** 3)
        )

    h = 1.0e-6
    grad = np.array(
        [
            (potential(pos + np.array([h, 0.0])) - potential(pos - np.array([h, 0.0]))) / (2.0 * h),
            (potential(pos + np.array([0.0, h])) - potential(pos - np.array([0.0, h]))) / (2.0 * h),
        ]
    )
    acc = demo.acceleration(t, pos[None, :], cfg)[0]
    assert acc == pytest.approx(-grad, rel=1.0e-8, abs=1.0e-8)


def test_asteroid_resonance_locations_match_kepler_scaling() -> None:
    demo = load_demo_module("asteroid_ejection_probability.py")
    locations = demo.resonance_locations(demo.A_JUPITER)
    assert locations["3:1"] == pytest.approx(demo.A_JUPITER * (1.0 / 3.0) ** (2.0 / 3.0))
    assert locations["3:1"] < locations["5:2"] < locations["7:3"] < locations["2:1"]
    label, distance = demo.nearest_resonance(locations["5:2"] + 0.01, demo.A_JUPITER)
    assert label == "5:2"
    assert distance == pytest.approx(0.01)


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_cr3bp_lagrange_points_are_equilibria() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("circular_restricted_three_body.py")
    mu = demo.SUN_JUPITER_MU
    points = demo.lagrange_points(mu)
    assert -mu < points.l1 < 1.0 - mu < points.l2
    assert points.l3 < -mu
    for x, y in [(points.l1, 0.0), (points.l2, 0.0), (points.l3, 0.0), points.l4, points.l5]:
        assert np.linalg.norm(demo.grad_effective_potential(x, y, mu)) < 1.0e-12


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_cr3bp_jacobi_integral_has_small_drift() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("circular_restricted_three_body.py")
    mu = demo.SUN_JUPITER_MU
    state0 = demo.initial_state("l4", mu)
    _, states = demo.integrate(mu, state0, dt=0.005, periods=0.5)
    jacobi = demo.jacobi_constant(states, mu)
    assert np.max(np.abs(jacobi - jacobi[0])) < 1.0e-11


def test_cr3bp_rejects_invalid_mass_parameter() -> None:
    demo = load_demo_module("circular_restricted_three_body.py")
    with pytest.raises(ValueError):
        demo.lagrange_points(0.0)
    with pytest.raises(ValueError):
        demo.integrate(0.1, [0.0, 0.0, 0.0, 0.0], dt=0.0, periods=1.0)


@pytest.mark.skipif(importlib.util.find_spec("matplotlib") is None, reason="matplotlib is not installed")
def test_asteroid_csv_and_png_outputs_are_written(tmp_path: Path) -> None:
    csv_path = tmp_path / "asteroid.csv"
    plot_path = tmp_path / "asteroid.png"
    run_python_demo(
        "demos/python/asteroid_ejection_probability.py",
        "--n",
        "6",
        "--years",
        "0",
        "--dt",
        "0.05",
        "--bins",
        "3",
        "--csv",
        str(csv_path),
        "--plot",
        str(plot_path),
    )
    assert plot_path.exists()
    assert plot_path.stat().st_size > 0
    with csv_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 3
    assert set(rows[0]) == {
        "a_low",
        "a_high",
        "count",
        "ejected",
        "lost",
        "ejection_fraction",
        "ejection_standard_error",
        "loss_fraction",
        "loss_standard_error",
        "nearest_resonance",
        "resonance_distance",
    }


def test_asteroid_plot_flags_are_mutually_exclusive() -> None:
    result = run_python_demo_unchecked(
        "demos/python/asteroid_ejection_probability.py",
        "--n",
        "1",
        "--years",
        "0",
        "--dt",
        "0.05",
        "--plot",
        "figures/unused.png",
        "--no-plot",
    )
    assert result.returncode != 0
    assert "not allowed with argument" in result.stderr


def test_demo_cli_validation_reports_clean_errors() -> None:
    cases = [
        ("demos/python/standard_map_torus_breakdown.py", "--orbits", "0"),
        ("demos/python/navier_stokes_solutions.py", "--mu", "-1"),
        ("demos/python/linear_elasticity.py", "--poisson", "0.5"),
    ]
    for script, option, value in cases:
        result = run_python_demo_unchecked(script, option, value)
        assert result.returncode != 0
        assert "error:" in result.stderr
