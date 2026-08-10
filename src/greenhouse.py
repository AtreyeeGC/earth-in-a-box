def atmospheric_temperature(surface_temperature: float) -> float:
    """
    Calculate the temperature of a simple one-layer atmosphere.

    Parameters
    ----------
    surface_temperature : float
        Surface temperature in Kelvin.

    Returns
    -------
    float
        Atmospheric temperature in Kelvin.
    """

    return surface_temperature / (2 ** 0.25)


def surface_temperature_from_effective(
    effective_temperature: float,
) -> float:
    """
    Calculate surface temperature for a fully infrared-absorbing
    one-layer atmosphere.

    Parameters
    ----------
    effective_temperature : float
        Planet's effective radiating temperature in Kelvin.

    Returns
    -------
    float
        Estimated surface temperature in Kelvin.
    """

    return effective_temperature * (2 ** 0.25)