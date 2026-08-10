from src.greenhouse import surface_temperature_from_effective


def test_one_layer_greenhouse():
    effective_temperature = 254.59

    surface_temperature = surface_temperature_from_effective(
        effective_temperature
    )

    assert 300 < surface_temperature < 304