import numpy as np


def solar_declination(day_of_year: float, axial_tilt_deg: float = 23.44) -> float:
    """
    Calculate solar declination angle in radians for a given day of year.
    """
    tilt_rad = np.radians(axial_tilt_deg)
    decl = tilt_rad * np.sin(2 * np.pi * (day_of_year - 80) / 365.25)
    return float(decl)


def daily_insolation(
    latitude_deg: float,
    day_of_year: float,
    solar_constant: float = 1361.0,
    axial_tilt_deg: float = 23.44,
) -> float:
    """
    Calculate daily average solar insolation in W/m^2 for a given latitude and day.
    """
    lat_rad = np.radians(latitude_deg)
    decl_rad = solar_declination(day_of_year, axial_tilt_deg)

    # Hour angle at sunrise/sunset
    cos_h0 = -np.tan(lat_rad) * np.tan(decl_rad)
    cos_h0 = np.clip(cos_h0, -1.0, 1.0)
    h0 = np.arccos(cos_h0)

    # Integrated daily insolation formula
    term1 = h0 * np.sin(lat_rad) * np.sin(decl_rad)
    term2 = np.cos(lat_rad) * np.cos(decl_rad) * np.sin(h0)
    insolation = (solar_constant / np.pi) * (term1 + term2)
    return max(0.0, float(insolation))


def calculate_instantaneous_distance(
    semi_major_axis_au: float, eccentricity: float, day_of_year: float, total_days: float = 365.25
) -> float:
    """
    Calculate instantaneous orbital distance (r) in AU for an elliptical orbit.
    """
    if semi_major_axis_au <= 0:
        raise ValueError("Orbital distance must be strictly positive.")
    if eccentricity < 0 or eccentricity >= 1:
        raise ValueError("Orbital eccentricity must be in the range [0, 1).")

    mean_anomaly = 2 * np.pi * ((day_of_year - 3) % total_days) / total_days
    true_anomaly = mean_anomaly + (2 * eccentricity - 0.25 * eccentricity**3) * np.sin(mean_anomaly)

    r_au = (semi_major_axis_au * (1 - eccentricity**2)) / (1 + eccentricity * np.cos(true_anomaly))
    return float(r_au)


def calculate_solar_constant(
    luminosity_ratio: float = 1.0,
    distance_au: float = 1.0,
    eccentricity: float = 0.0,
    day_of_year: float = 1.0,
    **kwargs,
) -> float:
    """
    Calculate Top-of-Atmosphere (TOA) solar flux (W/m^2) accounting for orbital distance and eccentricity.
    Supports alias keyword arguments 'stellar_luminosity_ratio' and 'orbital_distance_au'.
    """
    if "stellar_luminosity_ratio" in kwargs:
        luminosity_ratio = kwargs["stellar_luminosity_ratio"]
    if "orbital_distance_au" in kwargs:
        distance_au = kwargs["orbital_distance_au"]

    if distance_au <= 0:
        raise ValueError("Orbital distance must be strictly positive.")

    solar_constant_earth = 1361.0  # W/m^2

    if eccentricity > 0:
        inst_distance = calculate_instantaneous_distance(distance_au, eccentricity, day_of_year)
    else:
        inst_distance = distance_au

    return float(solar_constant_earth * (luminosity_ratio / (inst_distance**2)))