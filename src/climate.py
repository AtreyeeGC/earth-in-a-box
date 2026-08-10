import math


# Stefan-Boltzmann constant
STEFAN_BOLTZMANN = 5.670374419e-8  # W m^-2 K^-4

# Solar luminosity
SOLAR_LUMINOSITY = 3.828e26  # W

# Astronomical Unit
AU = 1.495978707e11  # m


def equilibrium_temperature(
    luminosity: float,
    distance_au: float,
    albedo: float
) -> float:
    """
    Calculate the effective equilibrium temperature of a planet.

    Parameters
    ----------
    luminosity : float
        Stellar luminosity in units of solar luminosity.
    distance_au : float
        Planet-star distance in astronomical units.
    albedo : float
        Fraction of incoming radiation reflected by the planet.

    Returns
    -------
    float
        Effective temperature in Kelvin.
    """

    distance_m = distance_au * AU
    luminosity_watts = luminosity * SOLAR_LUMINOSITY

    temperature = (
        luminosity_watts * (1 - albedo)
        / (16 * math.pi * STEFAN_BOLTZMANN * distance_m**2)
    ) ** 0.25

    return temperature