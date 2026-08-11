import matplotlib.pyplot as plt

from src.climate import equilibrium_temperature
from src.time_model import temperature_step


# --------------------------------------------------
# Planet parameters
# --------------------------------------------------

DISTANCE = 1.0
ALBEDO = 0.30

NORMAL_LUMINOSITY = 1.0
FORCED_LUMINOSITY = 1.02


# --------------------------------------------------
# Simulation settings
# --------------------------------------------------

STARTING_TEMPERATURE = 250.0

TOTAL_YEARS = 150
FORCING_YEAR = 50

TIME_STEP = 0.1


# --------------------------------------------------
# Calculate equilibrium temperatures
# --------------------------------------------------

initial_equilibrium = equilibrium_temperature(
    NORMAL_LUMINOSITY,
    DISTANCE,
    ALBEDO,
)

forced_equilibrium = equilibrium_temperature(
    FORCED_LUMINOSITY,
    DISTANCE,
    ALBEDO,
)


# --------------------------------------------------
# Store simulation data
# --------------------------------------------------

years = [0]
temperatures = [STARTING_TEMPERATURE]

temperature = STARTING_TEMPERATURE


# --------------------------------------------------
# Run simulation
# --------------------------------------------------

steps = int(TOTAL_YEARS / TIME_STEP)

for step in range(1, steps + 1):

    current_year = step * TIME_STEP

    # Before year 50: normal Sun
    if current_year < FORCING_YEAR:
        luminosity = NORMAL_LUMINOSITY

    # After year 50: Sun is 2% brighter
    else:
        luminosity = FORCED_LUMINOSITY

    temperature = temperature_step(
        temperature=temperature,
        luminosity=luminosity,
        distance_au=DISTANCE,
        albedo=ALBEDO,
        years=TIME_STEP,
    )

    years.append(current_year)
    temperatures.append(temperature)


# --------------------------------------------------
# Print results
# --------------------------------------------------

print()
print("=== Solar Forcing Experiment ===")
print()

print(
    f"Initial equilibrium: "
    f"{initial_equilibrium:.2f} K"
)

print(
    f"Forced equilibrium: "
    f"{forced_equilibrium:.2f} K"
)

print(
    f"Final temperature: "
    f"{temperature:.2f} K"
)

print(
    f"Temperature increase: "
    f"{temperature - initial_equilibrium:.2f} K"
)

print()


# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    years,
    temperatures,
    color="royalblue",
    linewidth=2,
    label="Planet temperature",
)

plt.axhline(
    initial_equilibrium,
    color="gray",
    linestyle="--",
    label="Initial equilibrium",
)

plt.axhline(
    forced_equilibrium,
    color="red",
    linestyle="--",
    label="New equilibrium",
)

plt.axvline(
    FORCING_YEAR,
    color="orange",
    linestyle=":",
    linewidth=2,
    label="Solar forcing begins",
)

plt.xlabel("Time (years)")
plt.ylabel("Temperature (K)")

plt.title(
    "Earth in a Box — Solar Forcing Experiment"
)

plt.grid(alpha=0.3)

plt.legend()

plt.tight_layout()

plt.savefig(
    "solar_forcing.png",
    dpi=200,
)

plt.show()