import pytest
from src.atmosphere import calculate_mean_molecular_weight, calculate_rayleigh_albedo


def test_earth_air_molecular_weight():
    # 78% N2, 21% O2, 1% Ar ~ 28.97 g/mol
    earth_composition = {"N2": 0.78, "O2": 0.21, "Ar": 0.01}
    mw = calculate_mean_molecular_weight(earth_composition)
    assert pytest.approx(mw, rel=1e-2) == 28.97


def test_venus_co2_heavy_atmosphere():
    # 96.5% CO2, 3.5% N2 ~ 43.45 g/mol
    venus_composition = {"CO2": 0.965, "N2": 0.035}
    mw = calculate_mean_molecular_weight(venus_composition)
    assert pytest.approx(mw, rel=1e-2) == 43.45


def test_invalid_composition_sum_raises_error():
    with pytest.raises(ValueError):
        calculate_mean_molecular_weight({"N2": 0.5, "O2": 0.1})  # Sum = 0.6


def test_rayleigh_albedo_scaling():
    a_1bar = calculate_rayleigh_albedo(1.0)
    a_4bar = calculate_rayleigh_albedo(4.0)
    
    assert pytest.approx(a_1bar, rel=1e-2) == 0.06
    assert pytest.approx(a_4bar, rel=1e-2) == 0.12  # Sqrt(4) * 0.06