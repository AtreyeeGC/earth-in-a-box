def calculate_surface_gravity(mass_earth: float, radius_earth: float) -> float:
    """
    Calculate planetary surface gravity relative to Earth (1.0 = 1 g = 9.81 m/s^2).

    Parameters
    ----------
    mass_earth : float
        Planetary mass in Earth masses (M / M_earth).
    radius_earth : float
        Planetary radius in Earth radii (R / R_earth).

    Returns
    -------
    float
        Surface acceleration due to gravity relative to Earth (g / g_earth).
    """
    if mass_earth <= 0 or radius_earth <= 0:
        raise ValueError("Planetary mass and radius must be strictly positive.")

    return float(mass_earth / (radius_earth**2))


def calculate_scale_height(
    temperature_k: float,
    surface_gravity_g: float,
    mean_molecular_weight: float = 28.97,
) -> float:
    """
    Calculate atmospheric scale height H in kilometers.

    Parameters
    ----------
    temperature_k : float
        Mean atmospheric temperature in Kelvin.
    surface_gravity_g : float
        Surface gravity relative to Earth (g / g_earth).
    mean_molecular_weight : float, optional
        Mean molecular weight of the atmosphere in g/mol (default 28.97 for Earth air).

    Returns
    -------
    float
        Atmospheric scale height H in kilometers.
    """
    if surface_gravity_g <= 0:
        raise ValueError("Surface gravity must be strictly positive.")
    if temperature_k <= 0:
        raise ValueError("Temperature must be strictly positive.")
    if mean_molecular_weight <= 0:
        raise ValueError("Mean molecular weight must be strictly positive.")

    h_earth_km = 8.5  # Baseline Earth scale height at 288.15 K
    scale_height = (
        h_earth_km
        * (temperature_k / 288.15)
        * (1.0 / surface_gravity_g)
        * (28.97 / mean_molecular_weight)
    )
    return float(scale_height)