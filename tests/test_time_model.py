from src.time_model import (
    absorbed_solar_flux,
    outgoing_radiation,
    energy_imbalance,
)


def test_earth_absorbed_solar_flux():
    flux = absorbed_solar_flux(
        luminosity=1.0,
        distance_au=1.0,
        albedo=0.30,
    )

    assert abs(flux - 238.175) < 0.01


def test_outgoing_radiation():
    flux = outgoing_radiation(254.59)

    assert abs(flux - 238.0) < 1.0


def test_energy_imbalance_at_equilibrium():
    imbalance = energy_imbalance(
        temperature=254.59,
        luminosity=1.0,
        distance_au=1.0,
        albedo=0.30,
    )

    assert abs(imbalance) < 1.0