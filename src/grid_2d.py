import numpy as np

OCEAN_HEAT_CAPACITY = 2.1e8  # J / (m² K) - 50m mixed ocean layer
LAND_HEAT_CAPACITY = 1.0e7   # J / (m² K) - 1m soil thermal layer


def create_2d_grid(num_lats: int = 18, num_lons: int = 36):
    """
    Generate 2D spherical grid arrays for latitudes and longitudes.

    Returns
    -------
    latitudes : np.ndarray
        1D array of latitude centers in degrees (-85 to 85).
    longitudes : np.ndarray
        1D array of longitude centers in degrees (-175 to 175).
    lat_grid : np.ndarray
        2D meshgrid of latitudes (shape: num_lats x num_lons).
    lon_grid : np.ndarray
        2D meshgrid of longitudes (shape: num_lats x num_lons).
    """
    latitudes = np.linspace(-85.0, 85.0, num_lats)
    longitudes = np.linspace(-175.0, 175.0, num_lons)
    lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)
    return latitudes, longitudes, lat_grid, lon_grid


def create_land_ocean_mask(
    lat_grid: np.ndarray, lon_grid: np.ndarray, mask_type: str = "earth_like"
) -> np.ndarray:
    """
    Generate a boolean land/ocean surface mask where True = Land, False = Ocean.
    """
    if mask_type == "aqua":
        return np.zeros_like(lat_grid, dtype=bool)
    elif mask_type == "tidally_locked_continent":
        # Dayside continent centered around the sub-stellar point (0°, 0°)
        return (np.abs(lat_grid) <= 30.0) & (np.abs(lon_grid) <= 45.0)
    else:
        # Earth-like northern-heavy continent distribution
        mask = (lat_grid > 15.0) & (np.abs(lon_grid) < 90.0)
        mask |= (lat_grid < -20.0) & (lat_grid > -50.0) & (lon_grid > -80.0) & (lon_grid < -40.0)
        return mask


def get_heat_capacity_matrix(land_mask: np.ndarray) -> np.ndarray:
    """
    Map land/ocean boolean mask to physical thermal inertia values (J / m² K).
    """
    return np.where(land_mask, LAND_HEAT_CAPACITY, OCEAN_HEAT_CAPACITY)