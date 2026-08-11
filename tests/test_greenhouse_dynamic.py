import numpy as np
import pytest

from src.greenhouse_dynamic import (
    calculate_co2_forcing,
    calculate_dynamic_olr,
    calculate_specific_humidity,
    saturation_vapor_pressure,
)
from src.time_model import (
    energy_imbalance,
    outgoing_radiation,
)

# --------------------------------------------------
# Static Emissivity & Time Model Tests
# --------------------------------------------------


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


# --------------------------------------------------
# Dynamic Radiative Transfer & Water Vapor Tests
# --------------------------------------------------


def test_clausius_clapeyron_temperature_scaling():
    e_273 = saturation_vapor_pressure(273.15)
    e_300 = saturation_vapor_pressure(300.0)
    assert e_300 > 3.0 * e_273


def test_co2_logarithmic_forcing():
    f_2x = calculate_co2_forcing(560.0)
    assert abs(f_2x - 3.708) < 1e-2


def test_invalid_co2_raises_error():
    with pytest.raises(ValueError):
        calculate_co2_forcing(-100.0)


def test_water_vapor_greenhouse_trap():
    olr_cold = calculate_dynamic_olr(260.0, co2_ppm=280.0)
    olr_hot = calculate_dynamic_olr(320.0, co2_ppm=280.0)

    blackbody_cold = 5.670374419e-8 * (260.0**4)
    blackbody_hot = 5.670374419e-8 * (320.0**4)

    ratio_cold = olr_cold / blackbody_cold
    ratio_hot = olr_hot / blackbody_hot

    assert ratio_hot < ratio_cold