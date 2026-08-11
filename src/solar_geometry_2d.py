import numpy as np

SOLAR_CONSTANT_EARTH = 1361.0  # W/m²


def calculate_2d_insolation(
    lat_grid_deg: np.ndarray,
    lon_grid_deg: np.ndarray,
    day_of_year: float,
    axial_tilt_deg: float = 23.44,
    solar_constant: float = SOLAR_CONSTANT_EARTH,
    tidally_locked: bool = False,
    hour_of_day: float = 12.0,
) -> np.ndarray:
    """
    Calculate 2D top-of-atmosphere solar flux (W/m²).

    Parameters
    ----------
    tidally_locked : bool
        If True, the sub-stellar point is locked at (0°, 0°). The nightside receives zero flux.
    hour_of_day : float
        Local solar time in hours (0 to 24) for rotating planets.
    """
    lat_rad = np.radians(lat_grid_deg)
    lon_rad = np.radians(lon_grid_deg)

    if tidally_locked:
        # Sub-stellar point fixed at (lat=0°, lon=0°)
        # Dayside corresponds to longitudes between -90° and +90°
        cos_zenith = np.cos(lat_rad) * np.cos(lon_rad)
        return np.maximum(0.0, solar_constant * cos_zenith)
    else:
        # Rotating planet insolation based on hour angle
        tilt_rad = np.radians(axial_tilt_deg)
        decl = -tilt_rad * np.cos(2.0 * np.pi * (day_of_year + 10.0) / 365.25)

        # Local hour angle based on longitude and time of day
        hour_angle = np.radians((lon_grid_deg + (hour_of_day - 12.0) * 15.0))

        cos_zenith = np.sin(lat_rad) * np.sin(decl) + np.cos(lat_rad) * np.cos(
            decl
        ) * np.cos(hour_angle)
        return np.maximum(0.0, solar_constant * cos_zenith)