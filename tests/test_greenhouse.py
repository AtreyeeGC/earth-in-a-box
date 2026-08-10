from src.greenhouse import (
    surface_temperature_from_effective,
    surface_temperature_with_emissivity,
)


def test_one_layer_greenhouse():
    effective_temperature = 254.59

    surface_temperature = surface_temperature_from_effective(
        effective_temperature
    )

    assert 300 < surface_temperature < 304


def test_zero_emissivity():
    temperature = surface_temperature_with_emissivity(
        effective_temperature=254.59,
        emissivity=0.0
    )

    assert abs(temperature - 254.59) < 0.01


def test_full_emissivity():
    temperature = surface_temperature_with_emissivity(
        effective_temperature=254.59,
        emissivity=1.0
    )

    assert 302 < temperature < 304


def test_invalid_emissivity():
    try:
        surface_temperature_with_emissivity(
            effective_temperature=254.59,
            emissivity=1.5
        )
        assert False
    except ValueError:
        assert True