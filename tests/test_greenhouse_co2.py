import pytest
from src.greenhouse import (
    co2_to_emissivity,
    surface_temperature_with_emissivity,
)


def test_baseline_co2_returns_base_emissivity():
    assert co2_to_emissivity(280.0) == 0.78


def test_higher_co2_increases_emissivity():
    base_emissivity = co2_to_emissivity(280.0)
    doubled_emissivity = co2_to_emissivity(560.0)

    assert doubled_emissivity > base_emissivity


def test_doubling_co2_increases_surface_temperature():
    t_eff = 255.0

    eps_280 = co2_to_emissivity(280.0)
    eps_560 = co2_to_emissivity(560.0)

    t_280 = surface_temperature_with_emissivity(t_eff, eps_280)
    t_560 = surface_temperature_with_emissivity(t_eff, eps_560)

    assert t_560 > t_280


def test_invalid_co2_raises_value_error():
    with pytest.raises(ValueError):
        co2_to_emissivity(-50.0)