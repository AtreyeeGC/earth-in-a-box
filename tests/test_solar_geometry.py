from src.solar_geometry import daily_insolation, solar_declination


def test_solar_declination_bounds():
    # Solstice declination should reach approximately +/- 23.44 degrees
    dec_june = solar_declination(172)   # Summer solstice (~June 21)
    dec_dec = solar_declination(355)    # Winter solstice (~Dec 21)

    assert dec_june > 0.38   # ~+22.0 to +23.4 degrees in radians
    assert dec_dec < -0.38  # ~-22.0 to -23.4 degrees in radians


def test_polar_night_zero_insolation():
    # North Pole (90N) in December should receive 0 W/m²
    assert daily_insolation(90.0, 355) == 0.0


def test_midnight_sun_high_insolation():
    # North Pole (90N) in June receives continuous 24-hour sunlight
    insolation = daily_insolation(90.0, 172)
    assert insolation > 500.0


def test_equator_insolation_positive_year_round():
    # Equator (0N) should receive high flux every day of the year
    for day in [1, 90, 180, 270, 365]:
        assert daily_insolation(0.0, day) > 300.0