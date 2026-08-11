import matplotlib.pyplot as plt

from src.greenhouse import co2_to_emissivity
from src.time_model import temperature_step


# --------------------------------------------------
# Planet & Atmosphere Parameters
# --------------------------------------------------

LUMINOSITY = 1.0
DISTANCE = 1.0
ALBEDO = 0.30

BASELINE_CO2 = 280.0  # pre-industrial (ppm)
DOUBLED_CO2 = 560.0   # doubled CO2 (ppm)

STARTING_TEMPERATURE = 250.0
FORCING_YEAR = 50
TOTAL_YEARS = 150
TIME_STEP = 0.1


def get_effective_emissivity(co2_ppm: float) -> float:
    """
    Convert atmospheric CO2 concentration into TOA effective emissivity
    for the time_model energy balance engine.
    """
    atm_emissivity = co2_to_emissivity(co2_ppm)
    return 1.0 - (atm_emissivity / 2.0)


# --------------------------------------------------
# Run Simulation
# --------------------------------------------------

years = [0.0]
co2_levels = [BASELINE_CO2]
temperatures = [STARTING_TEMPERATURE]

temperature = STARTING_TEMPERATURE
steps = int(TOTAL_YEARS / TIME_STEP)

for step in range(1, steps + 1):
    current_year = step * TIME_STEP

    if current_year < FORCING_YEAR:
        co2_ppm = BASELINE_CO2
    else:
        co2_ppm = DOUBLED_CO2

    eps_eff = get_effective_emissivity(co2_ppm)

    temperature = temperature_step(
        temperature=temperature,
        luminosity=LUMINOSITY,
        distance_au=DISTANCE,
        albedo=ALBEDO,
        years=TIME_STEP,
        emissivity=eps_eff,
    )

    years.append(current_year)
    co2_levels.append(co2_ppm)
    temperatures.append(temperature)


# --------------------------------------------------
# Output Results
# --------------------------------------------------

initial_temp = temperatures[int(FORCING_YEAR / TIME_STEP)]
final_temp = temperatures[-1]
warming = final_temp - initial_temp

print()
print("=== CO2 Doubling Experiment ===")
print()
print(f"Baseline CO2: {BASELINE_CO2:.1f} ppm")
print(f"Doubled CO2:  {DOUBLED_CO2:.1f} ppm")
print(f"Pre-forcing temperature (Year {FORCING_YEAR}): {initial_temp:.2f} K")
print(f"Final temperature (Year {TOTAL_YEARS}):     {final_temp:.2f} K")
print(f"Equilibrium warming response:           +{warming:.2f} K")
print()


# --------------------------------------------------
# Plotting
# --------------------------------------------------

fig, ax1 = plt.subplots(figsize=(10, 6))

color_temp = "tab:red"
ax1.set_xlabel("Time (years)")
ax1.set_ylabel("Surface Temperature (K)", color=color_temp)
ax1.plot(years, temperatures, color=color_temp, linewidth=2, label="Temperature")
ax1.tick_params(axis="y", labelcolor=color_temp)
ax1.grid(alpha=0.3)

ax2 = ax1.twinx()
color_co2 = "tab:gray"
ax2.set_ylabel("CO2 Concentration (ppm)", color=color_co2)
ax2.plot(years, co2_levels, color=color_co2, linestyle="--", linewidth=2, label="CO2 (ppm)")
ax2.tick_params(axis="y", labelcolor=color_co2)

plt.axvline(
    FORCING_YEAR,
    color="black",
    linestyle=":",
    linewidth=1.5,
    label="CO2 Doubling Step",
)

plt.title("Earth in a Box — CO2 Doubling Forcing Experiment")
fig.tight_layout()

plt.savefig("co2_forcing_experiment.png", dpi=200)
plt.show()