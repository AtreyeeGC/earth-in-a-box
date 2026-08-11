import matplotlib.pyplot as plt
import numpy as np

from src.climate_1d import step_1d_climate
from src.grid import create_latitude_grid

NUM_BANDS = 18
DT_DAYS = 1.0

latitudes, area_fractions = create_latitude_grid(NUM_BANDS)


def run_tilt_simulation(axial_tilt: float, years: int = 5) -> np.ndarray:
    temps = [275.0] * NUM_BANDS
    final_year_history = []

    total_days = int(years * 365)
    for step in range(1, total_days + 1):
        day_of_year = ((step - 1) % 365) + 1

        temps = step_1d_climate(
            temperatures=temps,
            latitudes=latitudes,
            area_fractions=area_fractions,
            day_of_year=day_of_year,
            axial_tilt_deg=axial_tilt,
            dt_days=DT_DAYS,
        )

        if step > (years - 1) * 365:
            final_year_history.append(list(temps))

    return np.array(final_year_history).T  # Shape: (latitudes, days)


# --------------------------------------------------
# Run Simulations
# --------------------------------------------------

tilts = [23.44, 45.0, 90.0]
results = {tilt: run_tilt_simulation(tilt) for tilt in tilts}

# --------------------------------------------------
# Output Summary Statistics
# --------------------------------------------------

north_pole_idx = NUM_BANDS - 1

print()
print("=== Exoplanet Axial Tilt Experiment ===")
print()
for tilt in tilts:
    pole_temps = results[tilt][north_pole_idx]
    print(
        f"Tilt {tilt:5.1f}° | North Pole Seasonal Range: "
        f"{np.min(pole_temps):.1f} K - {np.max(pole_temps):.1f} K "
        f"(ΔT = {np.max(pole_temps) - np.min(pole_temps):.1f} K)"
    )
print()

# --------------------------------------------------
# Plot Seasonal Temperature Comparison
# --------------------------------------------------

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

for ax, tilt in zip(axes, tilts):
    contour = ax.contourf(
        range(1, 366),
        latitudes,
        results[tilt],
        levels=20,
        cmap="RdYlBu_r",
    )
    ax.set_title(f"Axial Tilt = {tilt}°")
    ax.set_xlabel("Day of Year")
    ax.grid(alpha=0.3, linestyle="--")

axes[0].set_ylabel("Latitude (Degrees)")
cbar = fig.colorbar(contour, ax=axes.ravel().tolist(), shrink=0.85)
cbar.set_label("Surface Temperature (K)")

plt.suptitle("Earth in a Box — Exoplanet Obliquity Comparison", fontsize=14)
plt.savefig("exoplanet_tilt_experiment.png", dpi=200)
plt.show()