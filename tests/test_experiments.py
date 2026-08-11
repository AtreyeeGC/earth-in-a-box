import numpy as np
import pytest
from src.experiments import (
    PRESET_SCENARIOS,
    compute_scenario_deltas,
    simulate_solar_forcing,
)


def test_preset_scenarios_structure():
    """Verify essential preset scenarios are present and contain required parameters."""
    required_keys = [
        "axial_tilt",
        "co2_ppm",
        "stellar_luminosity",
        "distance_au",
        "eccentricity",
        "surface_pressure_bar",
        "planet_mass",
        "planet_radius",
        "surface_type",
        "description",
    ]

    expected_scenarios = [
        "Baseline Earth",
        "Extreme Obliquity (45° Tilt)",
        "Double CO₂ (2x Forcing)",
        "Faint Young Sun (80% Flux)",
        "Desert World (0% Oceans)",
    ]

    for name in expected_scenarios:
        assert name in PRESET_SCENARIOS, f"Missing scenario: {name}"
        config = PRESET_SCENARIOS[name]
        for key in required_keys:
            assert key in config, f"Missing key '{key}' in scenario '{name}'"


def test_compute_scenario_deltas_identical_grids():
    """Identical grids should yield zero deltas and RMSE."""
    grid_a = np.full((18, 36), 288.15)
    grid_b = np.full((18, 36), 288.15)

    deltas = compute_scenario_deltas(grid_a, grid_b)

    assert deltas["mean_delta_c"] == pytest.approx(0.0)
    assert deltas["max_delta_c"] == pytest.approx(0.0)
    assert deltas["min_delta_c"] == pytest.approx(0.0)
    assert deltas["rmse_c"] == pytest.approx(0.0)


def test_compute_scenario_deltas_uniform_offset():
    """Uniform +5 K offset should be accurately reflected across all delta metrics."""
    grid_a = np.full((18, 36), 280.0)
    grid_b = np.full((18, 36), 285.0)

    deltas = compute_scenario_deltas(grid_a, grid_b)

    assert deltas["mean_delta_c"] == pytest.approx(5.0)
    assert deltas["max_delta_c"] == pytest.approx(5.0)
    assert deltas["min_delta_c"] == pytest.approx(5.0)
    assert deltas["rmse_c"] == pytest.approx(5.0)


def test_simulate_solar_forcing_output_length():
    """Simulation output length should equal (total_years / time_step) + 1."""
    starting_temp = 288.15
    normal_lum = 1.0
    forced_lum = 1.1
    dist_au = 1.0
    albedo = 0.3
    forcing_year = 50.0
    total_years = 100.0
    time_step = 1.0

    years, temps = simulate_solar_forcing(
        starting_temperature=starting_temp,
        normal_luminosity=normal_lum,
        forced_luminosity=forced_lum,
        distance_au=dist_au,
        albedo=albedo,
        forcing_year=forcing_year,
        total_years=total_years,
        time_step=time_step,
    )

    expected_steps = int(total_years / time_step) + 1
    assert len(years) == expected_steps
    assert len(temps) == expected_steps
    assert years[0] == 0.0
    assert years[-1] == total_years


def test_simulate_solar_forcing_temperature_response():
    """Increased luminosity starting at year 50 should increase planet temperature after year 50."""
    years, temps = simulate_solar_forcing(
        starting_temperature=288.15,
        normal_luminosity=1.0,
        forced_luminosity=1.2,  # +20% flux
        distance_au=1.0,
        albedo=0.3,
        forcing_year=50.0,
        total_years=100.0,
        time_step=1.0,
    )

    # Index 50 corresponds to Year 50
    temp_before_forcing = temps[50]
    temp_after_forcing = temps[-1]

    assert temp_after_forcing > temp_before_forcing