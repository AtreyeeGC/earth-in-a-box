from src.climate import equilibrium_temperature


def test_earth_effective_temperature():
    temperature = equilibrium_temperature(
        luminosity=1.0,
        distance_au=1.0,
        albedo=0.30
    )

    assert 250 < temperature < 260