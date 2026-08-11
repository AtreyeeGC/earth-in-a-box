import pytest
from src.grid import calculate_heat_diffusion, create_latitude_grid


def test_grid_area_fractions_sum_to_one():
    lats, areas = create_latitude_grid(18)

    assert len(lats) == 18
    assert len(areas) == 18
    assert abs(sum(areas) - 1.0) < 1e-6


def test_equator_area_larger_than_pole_area():
    lats, areas = create_latitude_grid(18)

    # Equatorial band (index 8 or 9) should have a larger area than polar band (index 0)
    assert areas[9] > areas[0]


def test_heat_diffusion_conserves_energy():
    lats, areas = create_latitude_grid(18)

    # Hot equator (300 K), cold poles (240 K)
    temperatures = [240.0 + 60.0 * (1.0 - abs(lat) / 90.0) for lat in lats]

    fluxes = calculate_heat_diffusion(temperatures, areas, diffusion_coeff=3.8)

    # Total area-weighted sum of diffusion fluxes must equal zero (energy conservation)
    total_net_flux = sum(f * a for f, a in zip(fluxes, areas))
    assert abs(total_net_flux) < 1e-6


def test_heat_diffuses_from_warm_to_cold():
    lats, areas = create_latitude_grid(18)

    # Hot equator, cold poles
    temperatures = [240.0 + 60.0 * (1.0 - abs(lat) / 90.0) for lat in lats]

    fluxes = calculate_heat_diffusion(temperatures, areas, diffusion_coeff=3.8)

    # Equatorial band (index 9) should lose heat (negative flux)
    # Polar band (index 0) should gain heat (positive flux)
    assert fluxes[9] < 0.0
    assert fluxes[0] > 0.0