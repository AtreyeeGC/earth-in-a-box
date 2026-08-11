import numpy as np

STEFAN_BOLTZMANN = 5.670374419e-8
L_V = 2.5e6        # Latent heat of vaporization (J/kg)
R_V = 461.5        # Gas constant for water vapor (J/(kg K))
P0 = 101325.0      # Reference atmospheric surface pressure (Pa)


def saturation_vapor_pressure(temp_k: float | np.ndarray) -> float | np.ndarray:
    """
    Compute saturation vapor pressure e_s(T) in Pa via Clausius-Clapeyron equation.
    """
    return 611.0 * np.exp((L_V / R_V) * ((1.0 / 273.15) - (1.0 / temp_k)))


def calculate_specific_humidity(
    temp_k: float | np.ndarray, relative_humidity: float = 0.60
) -> float | np.ndarray:
    """
    Calculate atmospheric specific humidity q (kg/kg) assuming fixed relative humidity.
    """
    e_s = saturation_vapor_pressure(temp_k)
    e = relative_humidity * e_s
    # Specific humidity approximation: q ~ 0.622 * e / P0
    return (0.622 * e) / P0


def calculate_co2_forcing(co2_ppm: float) -> float:
    """
    Calculate radiative forcing (W/m²) relative to pre-industrial baseline (280 ppm).
    """
    if co2_ppm <= 0:
        raise ValueError("CO2 concentration must be strictly positive.")
    return 5.35 * np.log(co2_ppm / 280.0)


def calculate_dynamic_olr(
    temp_k: float | np.ndarray,
    co2_ppm: float = 280.0,
    relative_humidity: float = 0.60,
    base_emissivity: float = 0.61,
) -> float | np.ndarray:
    """
    Calculate Outgoing Longwave Radiation (OLR in W/m²) accounting for
    temperature-dependent water vapor opacity and CO2 forcing.
    """
    q = calculate_specific_humidity(temp_k, relative_humidity=relative_humidity)
    
    # Water vapor increases atmospheric optical depth, lowering effective emissivity
    # Normalized against reference surface humidity q_ref at 288 K (~0.006 kg/kg)
    q_ref = 0.006
    water_vapor_opacity_factor = 0.08 * np.log(1.0 + (q / q_ref))
    
    # Effective emissivity decreases as atmospheric greenhouse gases increase
    eff_emissivity = np.maximum(0.15, base_emissivity - water_vapor_opacity_factor)
    
    # Net longwave flux leaving top of atmosphere
    f_co2 = calculate_co2_forcing(co2_ppm)
    olr = eff_emissivity * STEFAN_BOLTZMANN * (temp_k**4) - f_co2
    
    return olr