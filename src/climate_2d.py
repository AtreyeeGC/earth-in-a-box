import numpy as np

from src.feedbacks import ice_albedo

STEFAN_BOLTZMANN = 5.670374419e-8


def calculate_2d_heat_diffusion(
    temp_matrix: np.ndarray,
    lat_grid_deg: np.ndarray,
    diffusion_coeff: float = 0.5,
) -> np.ndarray:
    """
    Compute 2D spherical surface heat diffusion fluxes (W/m²)
    across latitude and longitude boundaries using finite differences.
    """
    num_lats, num_lons = temp_matrix.shape
    lat_rad = np.radians(lat_grid_deg)

    dlat = np.radians(170.0 / (num_lats - 1))
    dlon = np.radians(350.0 / (num_lons - 1))

    # Longitudinal Diffusion (Periodic Boundary Conditions)
    temp_east = np.roll(temp_matrix, shift=-1, axis=1)
    temp_west = np.roll(temp_matrix, shift=1, axis=1)
    cos_lat = np.maximum(1e-2, np.cos(lat_rad))

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
    emissivity_eff: float = 0.61,
    forcing_w_m2: float = 0.0,
    diffusion_coeff: float = 0.5,
    dt_seconds: float = 3600.0,
) -> np.ndarray:
    """
    Advance 2D planetary surface temperatures by dt_seconds.
    """
    albedo_func = np.vectorize(ice_albedo)
    albedo_matrix = albedo_func(temp_matrix)

    f_in = insolation_matrix * (1.0 - albedo_matrix) + forcing_w_m2
    f_out = emissivity_eff * STEFAN_BOLTZMANN * (temp_matrix**4)
    f_diff = calculate_2d_heat_diffusion(
        temp_matrix, lat_grid_deg, diffusion_coeff
    )

    f_net = f_in - f_out + f_diff
    d_temp = (f_net * dt_seconds) / heat_capacity_matrix

    return temp_matrix + d_temp