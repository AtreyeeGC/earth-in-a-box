import math

SOLAR_CONSTANT_EARTH = 1361.0  # W/m² at 1 AU from Sun


def calculate_solar_constant(
    stellar_luminosity_ratio: float = 1.0,
    orbital_distance_au: float = 1.0,
) -> float:
    """
    Calculate top-of-atmosphere solar flux S (W/m²) given stellar luminosity
    relative to the Sun (L/L_sun) and orbital distance in AU.
    """
    if orbital_distance_au <= 0:
        raise ValueError("Orbital distance must be strictly positive.")
    return SOLAR_CONSTANT_EARTH * (stellar_luminosity_ratio / (orbital_distance_au**2))


def solar_declination(day_of_year: float, axial_tilt_deg: float = 23.44) -> float:
    """
    Calculate solar declination angle in radians for a given day of year and axial tilt.
    """
    tilt_rad = math.radians(axial_tilt_deg)
    return -tilt_rad * math.cos(
        2.0 * math.pi * (day_of_year + 10.0) / 365.25
    )


def daily_insolation(
    latitude_deg: float,
    day_of_year: float,
    axial_tilt_deg: float = 23.44,
    solar_constant: float = 1361.0,
) -> float:
    """
    Calculate daily average top-of-atmosphere solar flux (W/m²)
    for a given latitude, day of year, axial tilt, and solar constant.
    """
    lat_rad = math.radians(latitude_deg)
    decl = solar_declination(day_of_year, axial_tilt_deg=axial_tilt_deg)

    cos_h0 = -math.tan(lat_rad) * math.tan(decl)

    if cos_h0 >= 1.0:
        h0 = 0.0  # Polar night
    elif cos_h0 <= -1.0:
        h0 = math.pi  # Midnight sun
    else:
        h0 = math.acos(cos_h0)

    insolation = (solar_constant / math.pi) * (
        h0 * math.sin(lat_rad) * math.sin(decl)
        + math.cos(lat_rad) * math.cos(decl) * math.sin(h0)
    )

    return max(0.0, insolation)