import matplotlib.pyplot as plt

from src.climate import equilibrium_temperature
from src.time_model import temperature_step


# Planet parameters
LUMINOSITY = 1.0
DISTANCE = 1.0
ALBEDO = 0.30

# Starting climate state
STARTING_TEMPERATURE = 250.0

# Simulation settings
TOTAL_YEARS = 100
TIME_STEP = 0.1


# Calculate theoretical equilibrium temperature
equilibrium = equilibrium_temperature(
    LUMINOSITY,
    DISTANCE,
    ALBEDO,
)


# Store simulation results
years = [0]
temperatures = [STARTING_TEMPERATURE]

temperature = STARTING_TEMPERATURE


# Number of simulation steps
steps = int(TOTAL_YEARS / TIME_STEP)


# Run simulation
for step in range(1, steps + 1):

    temperature = temperature_step(
        temperature=temperature,
        luminosity=LUMINOSITY,
        distance_au=DISTANCE,
        albedo=ALBEDO,
        years=TIME_STEP,
    )

    years.append(step * TIME_STEP)
    temperatures.append(temperature)


# Print results
print(f"Starting temperature: {STARTING_TEMPERATURE:.2f} K")
print(f"Equilibrium temperature: {equilibrium:.2f} K")
print(f"Final temperature: {temperature:.2f} K")


# Plot results
plt.figure(figsize=(10, 6))

plt.plot(
    years,
    temperatures,
    color="royalblue",
    linewidth=2,
    label="Simulated temperature",
)

plt.axhline(
    equilibrium,
    color="red",
    linestyle="--",
    label="Equilibrium temperature",
)

plt.xlabel("Time (years)")
plt.ylabel("Temperature (K)")
plt.title("Earth in a Box — Climate Relaxation")

plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()

plt.savefig(
    "climate_evolution.png",
    dpi=200,
)

plt.show()