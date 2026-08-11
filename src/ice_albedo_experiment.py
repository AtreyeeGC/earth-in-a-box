import matplotlib.pyplot as plt

from src.climate import equilibrium_temperature
from src.feedbacks import ice_albedo
from src.time_model import temperature_step


# --------------------------------------------------
# Planet parameters
# --------------------------------------------------

LUMINOSITY = 1.0
DISTANCE = 1.0

STARTING_TEMPERATURE = 250.0

# Initial albedo used only to calculate
# the starting reference equilibrium.
INITIAL_ALBEDO = ice_albedo(STARTING_TEMPERATURE)


# --------------------------------------------------
# Simulation settings
# --------------------------------------------------

TOTAL_YEARS = 200
TIME_STEP = 0.1


# --------------------------------------------------
# Initial equilibrium
# --------------------------------------------------

initial_equilibrium = equilibrium_temperature(
    LUMINOSITY,
    DISTANCE,
    INITIAL_ALBEDO,
)


# --------------------------------------------------
# Store simulation data
# --------------------------------------------------

years = [0.0]
temperatures = [STARTING_TEMPERATURE]
albedos = [INITIAL_ALBEDO]

temperature = STARTING_TEMPERATURE


# --------------------------------------------------
# Run simulation
# --------------------------------------------------

steps = int(TOTAL_YEARS / TIME_STEP)

for step in range(1, steps + 1):

    current_year = step * TIME_STEP

    # Calculate albedo from the current temperature.
    albedo = ice_albedo(temperature)

    temperature = temperature_step(
        temperature=temperature,
        luminosity=LUMINOSITY,
        distance_au=DISTANCE,
        albedo=albedo,
        years=TIME_STEP,
        emissivity=1.0,
    )

    years.append(current_year)
    temperatures.append(temperature)
    albedos.append(albedo)


# --------------------------------------------------
# Results
# --------------------------------------------------

final_temperature = temperatures[-1]
final_albedo = albedos[-1]

print()
print("=== Ice-Albedo Feedback Experiment ===")
print()

print(
    f"Starting temperature: "
    f"{STARTING_TEMPERATURE:.2f} K"
)

print(
    f"Starting albedo: "
    f"{INITIAL_ALBEDO:.2f}"
)

print(
    f"Final temperature: "
    f"{final_temperature:.2f} K"
)

print(
    f"Final albedo: "
    f"{final_albedo:.2f}"
)

print()


# --------------------------------------------------
# Plot
# --------------------------------------------------

fig, temperature_axis = plt.subplots(
    figsize=(10, 6)
)

temperature_axis.plot(
    years,
    temperatures,
    color="royalblue",
    linewidth=2,
    label="Temperature",
)

temperature_axis.set_xlabel("Time (years)")
temperature_axis.set_ylabel(
    "Temperature (K)",
    color="royalblue",
)

temperature_axis.tick_params(
    axis="y",
    labelcolor="royalblue",
)

# Second axis for albedo.
albedo_axis = temperature_axis.twinx()

albedo_axis.plot(
    years,
    albedos,
    color="darkcyan",
    linewidth=2,
    label="Albedo",
)

albedo_axis.set_ylabel(
    "Albedo",
    color="darkcyan",
)

albedo_axis.tick_params(
    axis="y",
    labelcolor="darkcyan",
)

plt.title(
    "Earth in a Box — Ice-Albedo Feedback"
)

temperature_axis.grid(alpha=0.3)

fig.tight_layout()

plt.savefig(
    "ice_albedo_feedback.png",
    dpi=200,
)

plt.show()