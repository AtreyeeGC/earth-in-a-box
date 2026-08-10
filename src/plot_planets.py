import matplotlib.pyplot as plt

from src.planet import Planet


planets = [
    Planet("Earth", 1.0, 1.0, 0.30, 0.80),
    Planet("Hot Planet", 2.0, 1.0, 0.30, 0.80),
    Planet("Ice Planet", 1.0, 1.0, 0.70, 0.80),
    Planet("Distant Planet", 1.0, 2.0, 0.30, 0.80),
]


names = []
temperatures = []

for planet in planets:
    names.append(planet.name)

    temperature = planet.surface_temperature() - 273.15
    temperatures.append(temperature)


plt.figure(figsize=(10, 6))

bars = plt.bar(
    names,
    temperatures,
    color=["royalblue", "red", "lightcyan", "gray"],
)

plt.axhline(
    0,
    color="black",
    linewidth=0.8,
)

plt.ylabel("Surface Temperature (°C)")
plt.title("Earth in a Box — Four Worlds")

plt.grid(
    axis="y",
    alpha=0.25,
)

for bar, temperature in zip(bars, temperatures):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        temperature,
        f"{temperature:.1f}°C",
        ha="center",
        va="bottom" if temperature >= 0 else "top",
    )

plt.tight_layout()

plt.savefig(
    "planet_comparison.png",
    dpi=200,
)

plt.show()