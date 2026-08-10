from dataclasses import dataclass

from .climate import equilibrium_temperature
from .greenhouse import surface_temperature_with_emissivity


@dataclass
class Planet:
    """
    Represents a simplified planet in the Earth in a Box model.
    """

    name: str
    star_luminosity: float
    orbital_distance: float
    albedo: float
    atmospheric_emissivity: float

    def effective_temperature(self) -> float:
        """
        Calculate the planet's effective radiating temperature.
        """

        return equilibrium_temperature(
            luminosity=self.star_luminosity,
            distance_au=self.orbital_distance,
            albedo=self.albedo,
        )

    def surface_temperature(self) -> float:
        """
        Calculate the planet's estimated surface temperature
        including the simplified greenhouse effect.
        """

        effective_temperature = self.effective_temperature()

        return surface_temperature_with_emissivity(
            effective_temperature=effective_temperature,
            emissivity=self.atmospheric_emissivity,
        )