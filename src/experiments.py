from src.time_model import temperature_step


def simulate_solar_forcing(
    starting_temperature: float,
    normal_luminosity: float,
    forced_luminosity: float,
    distance_au: float,
    albedo: float,
    forcing_year: float,
    total_years: float,
    time_step: float,
):
    """
    Simulate a planet experiencing a sudden change
    in stellar luminosity.

    Parameters
    ----------
    starting_temperature : float
        Initial planetary temperature in Kelvin.

    normal_luminosity : float
        Stellar luminosity before the forcing.

    forced_luminosity : float
        Stellar luminosity after the forcing.

    distance_au : float
        Orbital distance in AU.

    albedo : float
        Planetary albedo.

    forcing_year : float
        Year when the forcing begins.

    total_years : float
        Total simulation duration.

    time_step : float
        Simulation timestep in years.

    Returns
    -------
    tuple
        Years and temperatures.
    """

    years = [0.0]
    temperatures = [starting_temperature]

    temperature = starting_temperature

    steps = int(total_years / time_step)

    for step in range(1, steps + 1):

        current_year = step * time_step

        if current_year < forcing_year:
            luminosity = normal_luminosity
        else:
            luminosity = forced_luminosity

        temperature = temperature_step(
            temperature=temperature,
            luminosity=luminosity,
            distance_au=distance_au,
            albedo=albedo,
            years=time_step,
        )

        years.append(current_year)
        temperatures.append(temperature)

    return years, temperatures