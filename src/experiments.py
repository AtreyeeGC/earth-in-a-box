from typing import Any, Dict, List, Tuple
import numpy as np
from src.time_model import temperature_step

PRESET_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "Baseline Earth": {
        "axial_tilt": 23.44,
        "co2_ppm": 420.0,
        "stellar_luminosity": 1.0,
        "distance_au": 1.0,
        "eccentricity": 0.0167,
        "surface_pressure_bar": 1.0,
        "planet_mass": 1.0,
        "planet_radius": 1.0,
        "surface_type": "earth_like",
        "description": "Present-day Earth baseline parameters.",
    },
    "Extreme Obliquity (45° Tilt)": {
        "axial_tilt": 45.0,
        "co2_ppm": 420.0,
        "stellar_luminosity": 1.0,
        "distance_au": 1.0,
        "eccentricity": 0.0167,
        "surface_pressure_bar": 1.0,
        "planet_mass": 1.0,
        "planet_radius": 1.0,
        "surface_type": "earth_like",
        "description": "High axial tilt driving intense polar summer heating and dark winter freezes.",
    },
    "Double CO₂ (2x Forcing)": {
        "axial_tilt": 23.44,
        "co2_ppm": 840.0,
        "stellar_luminosity": 1.0,
        "distance_au": 1.0,
        "eccentricity": 0.0167,
        "surface_pressure_bar": 1.0,
        "planet_mass": 1.0,
        "planet_radius": 1.0,
        "surface_type": "earth_like",
        "description": "Logarithmic radiative forcing boost (+3.7 W/m²) triggering water vapor feedback.",
    },
    "Faint Young Sun (80% Flux)": {
        "axial_tilt": 23.44,
        "co2_ppm": 420.0,
        "stellar_luminosity": 0.80,
        "distance_au": 1.0,
        "eccentricity": 0.0167,
        "surface_pressure_bar": 1.0,
        "planet_mass": 1.0,
        "planet_radius": 1.0,
        "surface_type": "earth_like",
        "description": "Early stellar evolution flux drop testing runaway ice-albedo threshold.",
    },
    "Desert World (0% Oceans)": {
        "axial_tilt": 23.44,
        "co2_ppm": 420.0,
        "stellar_luminosity": 1.0,
        "distance_au": 1.0,
        "eccentricity": 0.0167,
        "surface_pressure_bar": 1.0,
        "planet_mass": 1.0,
        "planet_radius": 1.0,
        "surface_type": "desert_land",
        "description": "Zero ocean surface area; low land heat capacity drives rapid thermal response.",
    },
}


def compute_scenario_deltas(
    temp_grid_a: np.ndarray, temp_grid_b: np.ndarray
) -> Dict[str, float]:
    """
    Compute temperature grid comparison metrics between Scenario B (Experiment) and Scenario A (Control).
    """
    delta_grid = temp_grid_b - temp_grid_a
    return {
        "mean_delta_c": float(np.mean(delta_grid)),
        "max_delta_c": float(np.max(delta_grid)),
        "min_delta_c": float(np.min(delta_grid)),
        "rmse_c": float(np.sqrt(np.mean(delta_grid**2))),
    }


def simulate_solar_forcing(
    starting_temperature: float,
    normal_luminosity: float,
    forced_luminosity: float,
    distance_au: float,
    albedo: float,
    forcing_year: float,
    total_years: float,
    time_step: float,
) -> Tuple[List[float], List[float]]:
    """
    Simulate a planet experiencing a sudden change
    in stellar luminosity.
    """
    years = [0.0]
    temperatures = [starting_temperature]

    temperature = starting_temperature
    steps = int(total_years / time_step)

    for step in range(1, steps + 1):
        current_year = step * time_step

        if current_year < forcing_year:
            luminosity = normal_luminosity
        else:
            luminosity = forced_luminosity

        temperature = temperature_step(
            temperature=temperature,
            luminosity=luminosity,
            distance_au=distance_au,
            albedo=albedo,
            years=time_step,
        )

        years.append(current_year)
        temperatures.append(temperature)

    return years, temperatures