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

def surface_temperature_with_emissivity(
    effective_temperature: float,
    emissivity: float,
) -> float:
    """
    Calculate surface temperature using a simple one-layer
    greenhouse model with adjustable atmospheric emissivity.

    Parameters
    ----------
    effective_temperature : float
        Planet's effective radiating temperature in Kelvin.

    emissivity : float
        Atmospheric infrared emissivity, from 0 to 1.

    Returns
    -------
    float
        Estimated surface temperature in Kelvin.
    """

    if not 0 <= emissivity <= 1:
        raise ValueError("Emissivity must be between 0 and 1.")

    return effective_temperature * (
        1 / (1 - emissivity / 2)
    ) ** 0.25