import pytest
from src.exoplanets import EXOPLANET_DATABASE
from src.solar_geometry import calculate_solar_constant


def test_earth_solar_constant():
    # 1 AU from Sun should yield baseline 1361 W/m²
    s0 = calculate_solar_constant(stellar_luminosity_ratio=1.0, orbital_distance_au=1.0)
    assert abs(s0 - 1361.0) < 1e-3


def test_inverse_square_law_distance():
    # At 2 AU, solar flux should be 1/4 of 1 AU
    s0_2au = calculate_solar_constant(stellar_luminosity_ratio=1.0, orbital_distance_au=2.0)
    assert abs(s0_2au - (1361.0 / 4.0)) < 1e-3


def test_zero_or_negative_distance_raises_error():
    with pytest.raises(ValueError):
        calculate_solar_constant(orbital_distance_au=0.0)


def test_exoplanet_database_integrity():
    assert "Modern Earth" in EXOPLANET_DATABASE
    assert "TRAPPIST-1e" in EXOPLANET_DATABASE
    
    for planet, data in EXOPLANET_DATABASE.items():
        assert "distance_au" in data
        assert "luminosity_ratio" in data
        assert "axial_tilt_deg" in data
        assert data["distance_au"] > 0