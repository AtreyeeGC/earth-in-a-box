from src.feedbacks import ice_albedo


def test_cold_planet_has_high_albedo():
    assert ice_albedo(240.0) == 0.60


def test_warm_planet_has_low_albedo():
    assert ice_albedo(300.0) == 0.20


def test_intermediate_temperature_has_intermediate_albedo():
    albedo = ice_albedo(270.0)

    assert 0.20 < albedo < 0.60


def test_albedo_decreases_with_temperature():
    cold = ice_albedo(260.0)
    warm = ice_albedo(280.0)

    assert warm < cold