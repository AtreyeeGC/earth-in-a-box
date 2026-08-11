import matplotlib.pyplot as plt

from src.climate import equilibrium_temperature
from src.experiments import simulate_solar_forcing


# --------------------------------------------------
# Planet
# --------------------------------------------------

DISTANCE = 1.0
ALBEDO = 0.30

NORMAL_LUMINOSITY = 1.0

STARTING_TEMPERATURE = 250.0


# --------------------------------------------------
# Experiment settings
# --------------------------------------------------

FORCING_YEAR = 50
TOTAL_YEARS = 150
TIME_STEP = 0.1


# Different solar forcing experiments
FORCINGS = [
    0.98,
    1.00,
    1.01,
    1.02,
    1.05,
]


# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(10, 6))


for luminosity in FORCINGS:

    years, temperatures = simulate_solar_forcing(
        starting_temperature=STARTING_TEMPERATURE,
        normal_luminosity=NORMAL_LUMINOSITY,
        forced_luminosity=luminosity,
        distance_au=DISTANCE,
        albedo=ALBEDO,
        forcing_year=FORCING_YEAR,
        total_years=TOTAL_YEARS,
        time_step=TIME_STEP,
    )

    percent_change = (luminosity - 1.0) * 100

    plt.plot(
        years,
        temperatures,
        linewidth=2,
        label=f"{percent_change:+.0f}% solar"
    )

    equilibrium = equilibrium_temperature(
        luminosity,
        DISTANCE,
        ALBEDO,
    )

    print(
        f"Solar {percent_change:+.0f}% "
        f"→ equilibrium: {equilibrium:.2f} K"
    )


# --------------------------------------------------
# Mark forcing event
# --------------------------------------------------

plt.axvline(
    FORCING_YEAR,
    color="black",
    linestyle=":",
    alpha=0.7,
    label="Forcing begins",
)


# --------------------------------------------------
# Graph formatting
# --------------------------------------------------

plt.xlabel("Time (years)")
plt.ylabel("Temperature (K)")

plt.title(
    "Earth in a Box — Solar Forcing Comparison"
)

plt.grid(alpha=0.3)

plt.legend()

plt.tight_layout()

plt.savefig(
    "solar_forcing_comparison.png",
    dpi=200,
)

plt.show()