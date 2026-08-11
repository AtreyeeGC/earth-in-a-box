import numpy as np

from src.feedbacks import ice_albedo
from src.greenhouse_dynamic import calculate_dynamic_olr


def calculate_2d_heat_diffusion(
    temp_matrix: np.ndarray,
    lat_grid_deg: np.ndarray,
    diffusion_coeff: float = 0.5,
) -> np.ndarray:
    """
    Compute 2D spherical heat diffusion fluxes (W/m²) with polar metric stabilization.
    """
    num_lats, num_lons = temp_matrix.shape
    lat_rad = np.radians(lat_grid_deg)

    dlat = np.radians(170.0 / max(1, num_lats - 1))
    dlon = np.radians(350.0 / max(1, num_lons - 1))

    # Longitudinal Diffusion (Periodic Boundary Conditions)
    temp_east = np.roll(temp_matrix, shift=-1, axis=1)
    temp_west = np.roll(temp_matrix, shift=1, axis=1)
    
    # Cap 1/cos^2(lat) factor at high latitudes to prevent CFL explosion
    cos_lat = np.maximum(0.20, np.cos(lat_rad))

    d2T_dlon2 = (temp_east - 2.0 * temp_matrix + temp_west) / (dlon**2)
    diff_lon = (diffusion_coeff / (cos_lat**2)) * d2T_dlon2

    # Latitudinal Diffusion (Zero-Flux Boundary Conditions at Poles)
    diff_lat = np.zeros_like(temp_matrix)
    for i in range(1, num_lats - 1):
        dT_dlat_north = (temp_matrix[i + 1, :] - temp_matrix[i, :]) / dlat
        dT_dlat_south = (temp_matrix[i, :] - temp_matrix[i - 1, :]) / dlat

        cos_n = np.cos(0.5 * (lat_rad[i, :] + lat_rad[i + 1, :]))
        cos_s = np.cos(0.5 * (lat_rad[i, :] + lat_rad[i - 1, :]))

        diff_lat[i, :] = (diffusion_coeff / cos_lat[i, :]) * (
            (cos_n * dT_dlat_north - cos_s * dT_dlat_south) / dlat
        )

    return diff_lon + diff_lat


def step_2d_climate(
    temp_matrix: np.ndarray,
    lat_grid_deg: np.ndarray,
    lon_grid_deg: np.ndarray,
    heat_capacity_matrix: np.ndarray,
    insolation_matrix: np.ndarray,
    co2_ppm: float = 280.0,
    forcing_w_m2: float = 0.0,
    diffusion_coeff: float = 0.5,
    dt_seconds: float = 86400.0,
    max_substep_seconds: float = 900.0,
) -> np.ndarray:
    """
    Advance 2D surface temperatures using internal CFL-stable sub-stepping.
    """
    substeps = int(np.ceil(dt_seconds / max_substep_seconds))
    dt_sub = dt_seconds / substeps

    current_temps = np.copy(temp_matrix)
    albedo_func = np.vectorize(ice_albedo)

    for _ in range(substeps):
        albedo_matrix = albedo_func(current_temps)

        f_in = insolation_matrix * (1.0 - albedo_matrix) + forcing_w_m2
        f_out = calculate_dynamic_olr(current_temps, co2_ppm=co2_ppm)
        f_diff = calculate_2d_heat_diffusion(
            current_temps, lat_grid_deg, diffusion_coeff=diffusion_coeff
        )

        f_net = f_in - f_out + f_diff
        d_temp = (f_net * dt_sub) / heat_capacity_matrix
        
        # Advance state and enforce physical sanity bounds (100 K to 400 K)
        current_temps = np.clip(current_temps + d_temp, 100.0, 400.0)

    return current_temps