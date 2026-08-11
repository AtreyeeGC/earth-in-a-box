import matplotlib.pyplot as plt

from src.climate import equilibrium_temperature
from src.time_model import temperature_step


# --------------------------------------------------
# Planet parameters
# --------------------------------------------------

LUMINOSITY = 1.0
DISTANCE = 1.0
ALBEDO = 0.30


# --------------------------------------------------
# Greenhouse parameters
# --------------------------------------------------

INITIAL_EMISSIVITY = 1.0
FORCED_EMISSIVITY = 0.8


# --------------------------------------------------
# Simulation settings
# --------------------------------------------------

STARTING_TEMPERATURE = 250.0

FORCING_YEAR = 50
TOTAL_YEARS = 150
TIME_STEP = 0.1


# --------------------------------------------------
# Calculate equilibrium temperatures
# --------------------------------------------------

initial_equilibrium = equilibrium_temperature(
    LUMINOSITY,
    DISTANCE,
    ALBEDO,
)


# For the one-layer greenhouse model:
#
# absorbed solar radiation = emissivity * sigma * T^4
#
# Therefore the equilibrium temperature depends
# on emissivity.

forced_equilibrium = initial_equilibrium / (
    FORCED_EMISSIVITY ** 0.25
)


# --------------------------------------------------
# Store simulation data
# --------------------------------------------------

years = [0.0]
temperatures = [STARTING_TEMPERATURE]

temperature = STARTING_TEMPERATURE


# --------------------------------------------------
# Run simulation
# --------------------------------------------------

steps = int(TOTAL_YEARS / TIME_STEP)

for step in range(1, steps + 1):

    current_year = step * TIME_STEP

    if current_year < FORCING_YEAR:
        emissivity = INITIAL_EMISSIVITY
    else:
        emissivity = FORCED_EMISSIVITY

    temperature = temperature_step(
        temperature=temperature,
        luminosity=LUMINOSITY,
        distance_au=DISTANCE,
        albedo=ALBEDO,
        years=TIME_STEP,
        emissivity=emissivity,
    )

    years.append(current_year)
    temperatures.append(temperature)


# --------------------------------------------------
# Print results
# --------------------------------------------------

print()
print("=== Greenhouse Forcing Experiment ===")
print()

print(
    f"Initial emissivity: "
    f"{INITIAL_EMISSIVITY:.2f}"
)

print(
    f"Forced emissivity: "
    f"{FORCED_EMISSIVITY:.2f}"
)

print(
    f"Initial equilibrium: "
    f"{initial_equilibrium:.2f} K"
)

print(
    f"New equilibrium: "
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
    color="darkorange",
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
    color="black",
    linestyle=":",
    linewidth=2,
    label="Greenhouse forcing begins",
)

plt.xlabel("Time (years)")
plt.ylabel("Temperature (K)")

plt.title(
    "Earth in a Box — Greenhouse Forcing Experiment"
)

plt.grid(alpha=0.3)

plt.legend()

plt.tight_layout()

plt.savefig(
    "greenhouse_forcing.png",
    dpi=200,
)

plt.show()