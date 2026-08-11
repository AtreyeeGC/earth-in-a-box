import matplotlib.pyplot as plt

from src.feedbacks import ice_albedo
from src.greenhouse import co2_to_emissivity
from src.time_model import temperature_step


# --------------------------------------------------
# Planet & Simulation Parameters
# --------------------------------------------------

LUMINOSITY = 1.0
DISTANCE = 1.0

BASELINE_CO2 = 280.0
DOUBLED_CO2 = 560.0

STARTING_TEMPERATURE = 280.0

FORCING_YEAR = 50
TOTAL_YEARS = 150
TIME_STEP = 0.1


def get_effective_emissivity(co2_ppm: float) -> float:
    """
    Convert atmospheric CO2 concentration into TOA effective emissivity.
    """
    atm_emissivity = co2_to_emissivity(co2_ppm)
    return 1.0 - (atm_emissivity / 2.0)


# --------------------------------------------------
# Run Coupled Simulation
# --------------------------------------------------

years = [0.0]
co2_levels = [BASELINE_CO2]
temperatures = [STARTING_TEMPERATURE]
albedos = [ice_albedo(STARTING_TEMPERATURE)]

temperature = STARTING_TEMPERATURE
steps = int(TOTAL_YEARS / TIME_STEP)

for step in range(1, steps + 1):
    current_year = step * TIME_STEP

    co2_ppm = BASELINE_CO2 if current_year < FORCING_YEAR else DOUBLED_CO2

    # Dynamic feedback coupling
    albedo = ice_albedo(temperature)
    eps_eff = get_effective_emissivity(co2_ppm)

    temperature = temperature_step(
        temperature=temperature,
        luminosity=LUMINOSITY,
        distance_au=DISTANCE,
        albedo=albedo,
        years=TIME_STEP,
        emissivity=eps_eff,
    )

    years.append(current_year)
    co2_levels.append(co2_ppm)
    temperatures.append(temperature)
    albedos.append(albedo)


# --------------------------------------------------
# Output Results
# --------------------------------------------------

initial_temp = temperatures[int(FORCING_YEAR / TIME_STEP)]
final_temp = temperatures[-1]
total_warming = final_temp - initial_temp

initial_albedo = albedos[int(FORCING_YEAR / TIME_STEP)]
final_albedo = albedos[-1]

print()
print("=== Coupled CO2 + Ice-Albedo Experiment ===")
print()
print(f"Pre-forcing temperature (Year {FORCING_YEAR}): {initial_temp:.2f} K")
print(f"Final temperature (Year {TOTAL_YEARS}):     {final_temp:.2f} K")
print(f"Total coupled warming response:         +{total_warming:.2f} K")
print(f"Albedo shift:                           {initial_albedo:.2f} -> {final_albedo:.2f}")
print()


# --------------------------------------------------
# Plotting
# --------------------------------------------------

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top Plot: Temperature
color_temp = "tab:red"
ax1.set_ylabel("Surface Temp (K)", color=color_temp)
ax1.plot(years, temperatures, color=color_temp, linewidth=2, label="Temperature")
ax1.tick_params(axis="y", labelcolor=color_temp)
ax1.grid(alpha=0.3)
ax1.axvline(FORCING_YEAR, color="black", linestyle=":", label="CO2 Doubling")
ax1.set_title("Earth in a Box — Coupled CO2 & Ice-Albedo System")
ax1.legend(loc="upper left")

# Bottom Plot: Albedo Response
color_albedo = "tab:blue"
ax2.set_xlabel("Time (years)")
ax2.set_ylabel("Albedo", color=color_albedo)
ax2.plot(years, albedos, color=color_albedo, linewidth=2, label="Albedo")
ax2.tick_params(axis="y", labelcolor=color_albedo)
ax2.grid(alpha=0.3)
ax2.axvline(FORCING_YEAR, color="black", linestyle=":")
ax2.legend(loc="upper right")

fig.tight_layout()
plt.savefig("coupled_experiment.png", dpi=200)
plt.show()