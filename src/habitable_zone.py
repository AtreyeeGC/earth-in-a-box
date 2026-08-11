def calculate_habitable_zone_limits(stellar_luminosity_ratio: float) -> dict:
    """
    Calculate conservative Habitable Zone (HZ) orbital boundaries in AU
    based on Kopparapu et al. (2013) stellar flux models.

    Parameters
    ----------
    stellar_luminosity_ratio : float
        Stellar luminosity relative to the Sun (L / L_sun).

    Returns
    -------
    dict
        Inner and outer habitable zone boundaries in astronomical units (AU).
    """
    if stellar_luminosity_ratio <= 0:
        raise ValueError("Stellar luminosity must be strictly positive.")

    # Effective solar flux thresholds (S_eff) relative to Earth
    s_eff_runaway = 1.06   # Inner edge: Runaway greenhouse limit
    s_eff_maximum = 0.32   # Outer edge: Maximum greenhouse CO2 condensation limit

    r_inner_au = (stellar_luminosity_ratio / s_eff_runaway) ** 0.5
    r_outer_au = (stellar_luminosity_ratio / s_eff_maximum) ** 0.5

    return {
        "inner_edge_au": round(r_inner_au, 3),
        "outer_edge_au": round(r_outer_au, 3),
    }