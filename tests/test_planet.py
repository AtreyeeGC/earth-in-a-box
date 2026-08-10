from src.planet import Planet


def test_earth_temperature():
    earth = Planet(
        name="Earth",
        star_luminosity=1.0,
        orbital_distance=1.0,
        albedo=0.30,
        atmospheric_emissivity=0.80,
    )

    assert abs(earth.effective_temperature() - 254.59) < 0.01
    assert abs(earth.surface_temperature() - 289.27) < 0.01


def test_hotter_star():
    planet = Planet(
        name="Hot Planet",
        star_luminosity=2.0,
        orbital_distance=1.0,
        albedo=0.30,
        atmospheric_emissivity=0.0,
    )

    assert planet.effective_temperature() > 300