from src.time_model import (
    outgoing_radiation,
    energy_imbalance,
)


def test_emissivity_reduces_outgoing_radiation():
    temperature = 288.0

    full_emission = outgoing_radiation(
        temperature,
        emissivity=1.0,
    )

    reduced_emission = outgoing_radiation(
        temperature,
        emissivity=0.8,
    )

    assert reduced_emission < full_emission


def test_zero_emissivity_means_no_outgoing_radiation():
    radiation = outgoing_radiation(
        temperature=288.0,
        emissivity=0.0,
    )

    assert radiation == 0.0


def test_lower_emissivity_creates_more_energy_imbalance():
    temperature = 288.0

    imbalance_high_emissivity = energy_imbalance(
        temperature=temperature,
        luminosity=1.0,
        distance_au=1.0,
        albedo=0.30,
        emissivity=1.0,
    )

    imbalance_low_emissivity = energy_imbalance(
        temperature=temperature,
        luminosity=1.0,
        distance_au=1.0,
        albedo=0.30,
        emissivity=0.8,
    )

    assert imbalance_low_emissivity > imbalance_high_emissivity