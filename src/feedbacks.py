def ice_albedo(
    temperature: float,
    cold_temperature: float = 250.0,
    warm_temperature: float = 273.15,  # Freezing point of water (0 °C)
    cold_albedo: float = 0.60,
    warm_albedo: float = 0.20,
) -> float:
    """
    Calculate surface albedo based on surface temperature.

    Temperatures above 273.15 K are ice-free (albedo = 0.20).
    Temperatures below 250.0 K are fully ice-covered (albedo = 0.60).
    """
    if temperature <= cold_temperature:
        return cold_albedo
    elif temperature >= warm_temperature:
        return warm_albedo
    else:
        fraction = (warm_temperature - temperature) / (
            warm_temperature - cold_temperature
        )
        return warm_albedo + fraction * (cold_albedo - warm_albedo)