import math
from typing import List, Tuple


def create_latitude_grid(num_bands: int = 18) -> Tuple[List[float], List[float]]:
    """
    Divide the planet into equal-width horizontal latitude bands.

    Parameters
    ----------
    num_bands : int
        Number of latitude bands (default 18, giving 10-degree bands).

    Returns
    -------
    Tuple[List[float], List[float]]
        Centroid latitudes in degrees and normalized surface area fractions.
    """
    if num_bands <= 0:
        raise ValueError("Number of bands must be greater than zero.")

    band_width = 180.0 / num_bands
    center_latitudes = []
    area_fractions = []

    for i in range(num_bands):
        south_lat = -90.0 + i * band_width
        north_lat = south_lat + band_width
        center_lat = south_lat + band_width / 2.0

        south_rad = math.radians(south_lat)
        north_rad = math.radians(north_lat)

        # Spherical segment area fraction = (sin(lat_north) - sin(lat_south)) / 2
        area = (math.sin(north_rad) - math.sin(south_rad)) / 2.0

        center_latitudes.append(center_lat)
        area_fractions.append(area)

    return center_latitudes, area_fractions


def calculate_heat_diffusion(
    temperatures: List[float],
    area_fractions: List[float],
    diffusion_coeff: float = 3.8,
) -> List[float]:
    """
    Calculate inter-band heat transport flux (W/m²) for each latitude band.

    Positive flux indicates net energy gain; negative flux indicates net heat loss.

    Parameters
    ----------
    temperatures : List[float]
        Current temperatures (K) for each latitude band.
    area_fractions : List[float]
        Normalized surface area fractions for each band.
    diffusion_coeff : float
        Meridional transport efficiency in W/(m²·K). Default is 3.8.

    Returns
    -------
    List[float]
        Net diffusion heat flux (W/m²) added to each band.
    """
    if len(temperatures) != len(area_fractions):
        raise ValueError("Temperatures and area_fractions must have the same length.")

    # Calculate area-weighted global mean temperature
    weighted_mean_temp = sum(
        t * a for t, a in zip(temperatures, area_fractions)
    )

    # Budyko transport: heat moves from warm regions (T_i > T_mean) to cold regions
    return [-diffusion_coeff * (t - weighted_mean_temp) for t in temperatures]