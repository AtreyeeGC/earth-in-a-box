import math
from typing import List

from src.feedbacks import ice_albedo
from src.grid import calculate_heat_diffusion
from src.solar_geometry import daily_insolation

STEFAN_BOLTZMANN = 5.670374419e-8
SECONDS_PER_DAY = 86400.0
OCEAN_HEAT_CAPACITY = 2.1e8


def step_1d_climate(
    temperatures: List[float],
    latitudes: List[float],
    area_fractions: List[float],
    day_of_year: float,
    emissivity_eff: float = 0.61,
    forcing_w_m2: float = 0.0,
    diffusion_coeff: float = 3.8,
    dt_days: float = 1.0,
) -> List[float]:
    """
    Advance 1D planetary surface temperatures by dt_days.

    Parameters
    ----------
    temperatures : List[float]
        Current temperatures (K) across latitude bands.
    latitudes : List[float]
        Centroid latitudes in degrees for each band.
    area_fractions : List[float]
        Normalized surface area fractions for each band.
    day_of_year : float
        Current day of the year (1 to 365).
    emissivity_eff : float
        Baseline effective top-of-atmosphere emissivity.
    forcing_w_m2 : float
        Uniform top-of-atmosphere radiative forcing in W/m² (e.g., +3.7 for 2xCO2).
    diffusion_coeff : float
        Inter-band heat diffusion efficiency in W/(m²·K).
    dt_days : float
        Timestep size in days.

    Returns
    -------
    List[float]
        Updated temperatures (K) across all latitude bands.
    """
    diffusion_fluxes = calculate_heat_diffusion(
        temperatures, area_fractions, diffusion_coeff
    )

    dt_seconds = dt_days * SECONDS_PER_DAY
    new_temperatures = []

    for i, (lat, temp) in enumerate(zip(latitudes, temperatures)):
        # 1. Insolation & dynamic ice-albedo
        insolation = daily_insolation(lat, day_of_year)
        albedo = ice_albedo(temp)
        f_in = insolation * (1.0 - albedo) + forcing_w_m2

        # 2. Outgoing thermal radiation
        f_out = emissivity_eff * STEFAN_BOLTZMANN * (temp**4)

        # 3. Inter-band heat transport
        f_diff = diffusion_fluxes[i]

        # 4. Net flux balance
        f_net = f_in - f_out + f_diff

        # 5. Euler step
        d_temp = (f_net * dt_seconds) / OCEAN_HEAT_CAPACITY
        new_temperatures.append(temp + d_temp)

    return new_temperatures