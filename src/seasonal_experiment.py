import matplotlib.pyplot as plt
import numpy as np

from src.climate_1d import step_1d_climate
from src.grid import create_latitude_grid


# --------------------------------------------------
# Setup Grid & Initial State
# --------------------------------------------------

NUM_BANDS = 18
SIMULATION_YEARS = 5
DT_DAYS = 1.0

latitudes, area_fractions = create_latitude_grid(NUM_BANDS)

# Start with a uniform 275 K guess
temperatures = [275.0] * NUM_BANDS

# History tracking for the final year
history_days = []
history_temperatures = []


# --------------------------------------------------
# Run Multi-Year Simulation
# --------------------------------------------------

total_days = int(SIMULATION_YEARS * 365)

for current_day_step in range(1, total_days + 1):
    day_of_year = ((current_day_step - 1) % 365) + 1

    temperatures = step_1d_climate(
        temperatures=temperatures,
        latitudes=latitudes,
        area_fractions=area_fractions,
        day_of_year=day_of_year,
        emissivity_eff=0.61,
        diffusion_coeff=3.8,
        dt_days=DT_DAYS,
    )

    # Store data during the final year
    if current_day_step > (SIMULATION_YEARS - 1) * 365:
        history_days.append(day_of_year)
        history_temperatures.append(list(temperatures))


# --------------------------------------------------
# Print Summary Statistics
# --------------------------------------------------

equator_idx = NUM_BANDS // 2
north_pole_idx = NUM_BANDS - 1
south_pole_idx = 0

equator_temps = [t[equator_idx] for t in history_temperatures]
npole_temps = [t[north_pole_idx] for t in history_temperatures]

print()
print("=== 1D Seasonal Climate Simulation ===")
print()
print(f"Equator Mean Temperature:    {np.mean(equator_temps):.2f} K")
print(f"Equator Seasonal Range:     {min(equator_temps):.1f} K - {max(equator_temps):.1f} K")
print(f"North Pole Mean Temperature:  {np.mean(npole_temps):.2f} K")
print(f"North Pole Seasonal Range:   {min(npole_temps):.1f} K - {max(npole_temps):.1f} K")
print()


# --------------------------------------------------
# Plot Latitude vs. Time Seasonal Heatmap
# --------------------------------------------------

temp_matrix = np.array(history_temperatures).T  # Shape: (latitudes, days)

plt.figure(figsize=(10, 6))
contour = plt.contourf(
    range(1, 366),
    latitudes,
    temp_matrix,
    levels=20,
    cmap="RdYlBu_r",
)

cbar = plt.colorbar(contour)
cbar.set_label("Surface Temperature (K)")

plt.xlabel("Day of Year")
plt.ylabel("Latitude (Degrees)")
plt.title("Earth in a Box — 1D Seasonal Temperature Distribution")
plt.grid(alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("seasonal_1d_climate.png", dpi=200)
plt.show()