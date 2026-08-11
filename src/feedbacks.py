def ice_albedo(
    temperature: float,
    cold_temperature: float = 250.0,
    warm_temperature: float = 290.0,
    cold_albedo: float = 0.60,
    warm_albedo: float = 0.20,
) -> float:
    """
    Calculate planetary albedo from temperature.

    Colder planets have more ice and therefore higher albedo.
    Warmer planets have less ice and therefore lower albedo.

    Parameters
    ----------
    temperature : float
        Planetary temperature in Kelvin.

    cold_temperature : float
        Temperature below which the planet has maximum albedo.

    warm_temperature : float
        Temperature above which the planet has minimum albedo.

    cold_albedo : float
        Albedo of a very cold planet.

    warm_albedo : float
        Albedo of a warm, mostly ice-free planet.
    """

    if temperature <= cold_temperature:
        return cold_albedo

    if temperature >= warm_temperature:
        return warm_albedo

    fraction = (
        (temperature - cold_temperature)
        / (warm_temperature - cold_temperature)
    )

    return cold_albedo + fraction * (
        warm_albedo - cold_albedo
    )