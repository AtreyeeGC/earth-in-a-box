import matplotlib.pyplot as plt

from climate import equilibrium_temperature
from greenhouse import surface_temperature_with_emissivity


earth_effective_temperature = equilibrium_temperature(
    luminosity=1.0,
    distance_au=1.0,
    albedo=0.30
)


emissivities = [
    i / 100
    for i in range(0, 101)
]

temperatures = []

for emissivity in emissivities:
    temperature = surface_temperature_with_emissivity(
        effective_temperature=earth_effective_temperature,
        emissivity=emissivity
    )

    temperatures.append(temperature - 273.15)


plt.figure(figsize=(9, 5))

plt.plot(
    emissivities,
    temperatures,
    color="royalblue",
    linewidth=2
)

plt.axhline(
    y=15,
    color="red",
    linestyle="--",
    label="Approx. Earth surface temperature"
)

plt.xlabel("Atmospheric infrared emissivity")
plt.ylabel("Surface temperature (°C)")
plt.title("Earth in a Box — Greenhouse Effect")

plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()

plt.savefig("emissivity_temperature.png", dpi=200)

plt.show()