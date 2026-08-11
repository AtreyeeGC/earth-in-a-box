SECONDS_PER_YEAR = 365.25 * 24 * 60 * 60

SOLAR_CONSTANT = 1361.0

STEFAN_BOLTZMANN = 5.670374419e-8

# Effective heat capacity of the climate system.
# Larger values make the planet respond more slowly.
HEAT_CAPACITY = 1.0e9


def absorbed_solar_flux(
    luminosity: float,
    distance_au: float,
    albedo: float,
) -> float:
    """
    Calculate globally averaged absorbed stellar radiation.

    Returns
    -------
    float
        Absorbed energy in W/m².
    """

    return (
        SOLAR_CONSTANT
        * luminosity
        * (1 - albedo)
        / (4 * distance_au**2)
    )


def outgoing_radiation(temperature: float) -> float:
    """
    Calculate outgoing infrared radiation.

    Parameters
    ----------
    temperature : float
        Planetary temperature in Kelvin.

    Returns
    -------
    float
        Outgoing radiation in W/m².
    """

    return STEFAN_BOLTZMANN * temperature**4


def energy_imbalance(
    temperature: float,
    luminosity: float,
    distance_au: float,
    albedo: float,
) -> float:
    """
    Calculate the planet's net energy imbalance.

    Positive values mean the planet is gaining energy.
    Negative values mean the planet is losing energy.
    """

    incoming = absorbed_solar_flux(
        luminosity,
        distance_au,
        albedo,
    )

    outgoing = outgoing_radiation(temperature)

    return incoming - outgoing


def temperature_step(
    temperature: float,
    luminosity: float,
    distance_au: float,
    albedo: float,
    years: float,
) -> float:
    """
    Advance planetary temperature by a given number of years.
    """

    imbalance = energy_imbalance(
        temperature,
        luminosity,
        distance_au,
        albedo,
    )

    seconds = years * SECONDS_PER_YEAR

    temperature_change = (
        imbalance * seconds / HEAT_CAPACITY
    )

    return temperature + temperature_change