import pytest
from src.habitable_zone import calculate_habitable_zone_limits


def test_habitable_zone_solar_system():
    # For a Sun-like star (L = 1.0), HZ inner edge ~0.97 AU, outer edge ~1.77 AU
    hz = calculate_habitable_zone_limits(1.0)
    assert 0.95 < hz["inner_edge_au"] < 1.00
    assert 1.70 < hz["outer_edge_au"] < 1.85


def test_habitable_zone_m_dwarf():
    # For a dim M-dwarf star (L = 0.00055, e.g., TRAPPIST-1)
    hz = calculate_habitable_zone_limits(0.00055)
    assert hz["inner_edge_au"] < 0.1
    assert hz["outer_edge_au"] < 0.05 + hz["inner_edge_au"]


def test_invalid_luminosity_raises_error():
    with pytest.raises(ValueError):
        calculate_habitable_zone_limits(-1.0)