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
    axial_tilt_deg: float = 23.44,
    diffusion_coeff: float = 3.8,
    dt_days: float = 1.0,
) -> List[float]:
    """
    Advance 1D planetary surface temperatures by dt_days.
    """
    diffusion_fluxes = calculate_heat_diffusion(
        temperatures, area_fractions, diffusion_coeff
    )

    dt_seconds = dt_days * SECONDS_PER_DAY
    new_temperatures = []

    for i, (lat, temp) in enumerate(zip(latitudes, temperatures)):
        # Calculate daily TOA insolation with custom axial tilt
        insolation = daily_insolation(
            lat, day_of_year, axial_tilt_deg=axial_tilt_deg
        )
        albedo = ice_albedo(temp)
        f_in = insolation * (1.0 - albedo) + forcing_w_m2
        f_out = emissivity_eff * STEFAN_BOLTZMANN * (temp**4)
        f_diff = diffusion_fluxes[i]

        f_net = f_in - f_out + f_diff
        d_temp = (f_net * dt_seconds) / OCEAN_HEAT_CAPACITY
        new_temperatures.append(temp + d_temp)

    return new_temperatures