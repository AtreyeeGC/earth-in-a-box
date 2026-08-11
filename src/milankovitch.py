import numpy as np


def compute_milankovitch_insolation(
    latitude_deg: float,
    year_thousand: float,
    base_solar_constant: float = 1361.0,
) -> float:
    """
    Calculate orbital eccentricity, obliquity, and precession over millennial timescales.

    Parameters
    ----------
    latitude_deg : float
        Latitude in degrees.
    year_thousand : float
        Time in thousands of years (kyr) relative to modern baseline (e.g., 0 = present, 20 = 20 kyr ago).

    Returns
    -------
    float
        Modulated summer solstice insolation (W/m²).
    """
    # Orbital parameter cycles (Approximated spectral frequencies)
    eccentricity = 0.0167 + 0.012 * np.sin(2.0 * np.pi * year_thousand / 100.0)
    obliquity_deg = 23.44 + 1.2 * np.sin(2.0 * np.pi * year_thousand / 41.0)
    precession_angle = 2.0 * np.pi * year_thousand / 23.0

    lat_rad = np.radians(latitude_deg)
    tilt_rad = np.radians(obliquity_deg)

    # Insolation modulation at high summer latitudes
    solar_flux = base_solar_constant * (1.0 + 2.0 * eccentricity * np.cos(precession_angle))
    summer_factor = np.sin(lat_rad) * np.sin(tilt_rad)

    return max(0.0, solar_flux * max(0.1, summer_factor))


def update_ice_sheet_height(
    current_height_m: float,
    surface_temp_k: float,
    dt_years: float = 100.0,
    accumulation_rate_m_yr: float = 0.3,
    ablation_factor: float = 0.05,
) -> float:
    """
    Evolve ice sheet thickness (meters) based on annual accumulation vs. summer ablation.
    """
    if surface_temp_k < 273.15:
        # Snow accumulation below freezing
        net_balance = accumulation_rate_m_yr
    else:
        # Temperature-driven ablation above freezing
        net_balance = -ablation_factor * (surface_temp_k - 273.15) ** 2

    new_height = current_height_m + (net_balance * dt_years)
    return max(0.0, float(new_height))