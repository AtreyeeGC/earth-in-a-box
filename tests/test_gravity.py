import pytest
from src.gravity import calculate_scale_height, calculate_surface_gravity


def test_earth_baseline_gravity():
    g = calculate_surface_gravity(1.0, 1.0)
    assert g == 1.0


def test_super_earth_gravity():
    # Super-Earth: 2.0 Earth masses, 1.25 Earth radii -> g ~ 2.0 / 1.5625 = 1.28 g
    g = calculate_surface_gravity(2.0, 1.25)
    assert pytest.approx(g, rel=1e-2) == 1.28


def test_invalid_mass_radius_raises_error():
    with pytest.raises(ValueError):
        calculate_surface_gravity(0.0, 1.0)
    with pytest.raises(ValueError):
        calculate_surface_gravity(1.0, -0.5)


def test_earth_baseline_scale_height():
    h = calculate_scale_height(288.15, 1.0, 28.97)
    assert pytest.approx(h, rel=1e-2) == 8.5


def test_high_gravity_compresses_atmosphere():
    # Doubling gravity halves scale height
    h = calculate_scale_height(288.15, 2.0, 28.97)
    assert pytest.approx(h, rel=1e-2) == 4.25