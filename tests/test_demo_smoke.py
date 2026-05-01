from __future__ import annotations

import csv
import importlib.util
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


@pytest.mark.skipif(importlib.util.find_spec("numpy") is None, reason="numpy is not installed")
def test_core_demos_run_small_cases() -> None:
    run_python_demo("demos/python/rigid_body_euler_top.py", "--steps", "20")
    run_python_demo("demos/python/hamiltonian_pendulum.py", "--steps", "20")
    run_python_demo("demos/python/standard_map.py", "--orbits", "3", "--steps", "5")
    run_python_demo("demos/python/fluids_vorticity.py", "--steps", "10")
    run_python_demo("demos/python/cosserat_rod_demo.py", "--points", "20")


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
def test_rigid_body_invariants_have_small_drift() -> None:
    np = pytest.importorskip("numpy")
    demo = load_demo_module("rigid_body_euler_top.py")
    body = demo.RigidBody(1.0, 2.0, 3.0)
    _, omega = demo.simulate(body, np.array([0.05, 1.0, 0.05]), dt=0.005, steps=200)
    energy, momentum_sq = demo.invariants(omega, body)
    assert np.max(np.abs(energy - energy[0])) < 1.0e-12
    assert np.max(np.abs(momentum_sq - momentum_sq[0])) < 1.0e-11


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
    )
    status = np.array([demo.ALIVE, demo.EJECTED, demo.ALIVE], dtype=np.int8)
    summary = demo.summarize(np.array([2.0, 2.5, 3.0]), status, cfg, elapsed_years=0.0)
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
    )
    pos, vel, a0 = demo.sample_initial_conditions(cfg)
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
        "loss_fraction",
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
