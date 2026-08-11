import math

SOLAR_CONSTANT = 1361.0  # W/m²
AXIAL_TILT_RAD = math.radians(23.44)  # Earth tilt ~23.44 degrees


def solar_declination(day_of_year: float) -> float:
    """
    Calculate solar declination angle in radians for a given day of the year.

    Parameters
    ----------
    day_of_year : float
        Day of the year (1 to 365).

    Returns
    -------
    float
        Solar declination angle in radians.
    """
    return -AXIAL_TILT_RAD * math.cos(
        2.0 * math.pi * (day_of_year + 10.0) / 365.25
    )


def daily_insolation(latitude_deg: float, day_of_year: float) -> float:
    """
    Calculate daily average top-of-atmosphere solar flux (W/m²)
    for a given latitude and day of the year.

    Parameters
    ----------
    latitude_deg : float
        Latitude in degrees (-90 to +90).
    day_of_year : float
        Day of the year (1 to 365).

    Returns
    -------
    float
        Daily average insolation in W/m².
    """
    lat_rad = math.radians(latitude_deg)
    decl = solar_declination(day_of_year)

    cos_h0 = -math.tan(lat_rad) * math.tan(decl)

    # Handle Polar Night and Midnight Sun bounds
    if cos_h0 >= 1.0:
        h0 = 0.0  # Sun never rises
    elif cos_h0 <= -1.0:
        h0 = math.pi  # Sun never sets
    else:
        h0 = math.acos(cos_h0)

    insolation = (SOLAR_CONSTANT / math.pi) * (
        h0 * math.sin(lat_rad) * math.sin(decl)
        + math.cos(lat_rad) * math.cos(decl) * math.sin(h0)
    )

    return max(0.0, insolation)