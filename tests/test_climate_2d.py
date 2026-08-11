import numpy as np

from src.climate_2d import step_2d_climate
from src.grid_2d import create_2d_grid, create_land_ocean_mask, get_heat_capacity_matrix
from src.solar_geometry_2d import calculate_2d_insolation


def test_tidally_locked_insolation_symmetry():
    _, _, lat_grid, lon_grid = create_2d_grid(18, 36)
    insolation = calculate_2d_insolation(
        lat_grid, lon_grid, day_of_year=1.0, tidally_locked=True
    )

    # Sub-stellar point (center) should have maximum insolation
    mid_lat, mid_lon = 9, 18
    assert insolation[mid_lat, mid_lon] > 1300.0

    # Anti-stellar point (nightside edge) should have zero insolation
    assert insolation[mid_lat, 0] == 0.0


def test_land_ocean_thermal_inertia_difference():
    _, _, lat_grid, lon_grid = create_2d_grid(18, 36)
    land_mask = create_land_ocean_mask(lat_grid, lon_grid, mask_type="tidally_locked_continent")
    c_matrix = get_heat_capacity_matrix(land_mask)

    # Land should have lower heat capacity than ocean
    assert np.min(c_matrix) == 1.0e7
    assert np.max(c_matrix) == 2.1e8


def test_2d_climate_stepping_stability():
    _, _, lat_grid, lon_grid = create_2d_grid(18, 36)
    land_mask = create_land_ocean_mask(lat_grid, lon_grid, mask_type="aqua")
    c_matrix = get_heat_capacity_matrix(land_mask)
    temps = np.full((18, 36), 280.0)

    insolation = calculate_2d_insolation(
        lat_grid, lon_grid, day_of_year=1.0, tidally_locked=True
    )

    new_temps = step_2d_climate(
        temp_matrix=temps,
        lat_grid_deg=lat_grid,
        lon_grid_deg=lon_grid,
        heat_capacity_matrix=c_matrix,
        insolation_matrix=insolation,
        dt_seconds=3600.0,
    )

    assert new_temps.shape == (18, 36)
    assert not np.isnan(new_temps).any()