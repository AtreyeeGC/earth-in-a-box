import pytest
from src.solar_geometry import calculate_instantaneous_distance, calculate_solar_constant


def test_circular_orbit_distance():
    # e = 0 should keep distance constant regardless of day
    r1 = calculate_instantaneous_distance(1.0, 0.0, 3)
    r2 = calculate_instantaneous_distance(1.0, 0.0, 185)
    assert abs(r1 - 1.0) < 1e-5
    assert abs(r2 - 1.0) < 1e-5


def test_eccentric_orbit_periastron_apastron():
    # e = 0.2, semi-major axis = 1.0 AU
    # Periastron r ~ 0.8 AU, Apastron r ~ 1.2 AU
    r_peri = calculate_instantaneous_distance(1.0, 0.2, 3)
    r_ap = calculate_instantaneous_distance(1.0, 0.2, 185)
    
    assert r_peri < r_ap
    assert pytest.approx(r_peri, rel=1e-2) == 0.8
    assert pytest.approx(r_ap, rel=1e-2) == 1.2


def test_eccentricity_solar_flux():
    # Solar flux at periastron should be significantly greater than at apastron
    flux_peri = calculate_solar_constant(1.0, 1.0, eccentricity=0.2, day_of_year=3)
    flux_ap = calculate_solar_constant(1.0, 1.0, eccentricity=0.2, day_of_year=185)
    
    assert flux_peri > flux_ap