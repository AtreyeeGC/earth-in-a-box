from typing import Dict


def calculate_mean_molecular_weight(gas_fractions: Dict[str, float]) -> float:
    """
    Calculate atmosphere mean molecular weight (g/mol) from volume/molar fractions.
    """
    molar_masses = {
        "N2": 28.013,
        "O2": 31.998,
        "CO2": 44.01,
        "H2O": 18.015,
        "Ar": 39.948,
        "H2": 2.016,
        "He": 4.002,
    }

    total_fraction = sum(gas_fractions.values())
    if not (0.99 <= total_fraction <= 1.01):
        raise ValueError("Gas volume fractions must sum to approximately 1.0 (100%).")

    mean_mw = 0.0
    for gas, fraction in gas_fractions.items():
        mw = molar_masses.get(gas, 28.97)  # Fallback to air if unknown
        mean_mw += fraction * mw

    return float(mean_mw)


def calculate_rayleigh_albedo(surface_pressure_bar: float) -> float:
    """
    Estimate atmospheric Rayleigh scattering albedo contribution based on surface pressure.
    """
    if surface_pressure_bar < 0:
        raise ValueError("Surface pressure cannot be negative.")

    # Baseline Earth Rayleigh scattering contribution ~0.06 at 1.0 bar
    albedo = 0.06 * (surface_pressure_bar**0.5)
    return float(min(0.35, albedo))  # Upper cap at 0.35