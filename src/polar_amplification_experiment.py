import matplotlib.pyplot as plt
import numpy as np

from src.climate_1d import step_1d_climate
from src.grid import create_latitude_grid

# --------------------------------------------------
# Setup Model Grid & Parameters
# --------------------------------------------------

NUM_BANDS = 18
DT_DAYS = 1.0

latitudes, area_fractions = create_latitude_grid(NUM_BANDS)


def run_to_steady_state(
    initial_temps: list,
    forcing_w_m2: float = 0.0,
    years: int = 5,
) -> tuple[list, list]:
    """
    Spin up the 1D climate model to seasonal steady state.
    Returns final day band temperatures and annual mean temperatures.
    """
    temps = list(initial_temps)
    annual_history = []

    total_days = int(years * 365)
    for step in range(1, total_days + 1):
        day_of_year = ((step - 1) % 365) + 1

        temps = step_1d_climate(
            temperatures=temps,
            latitudes=latitudes,
            area_fractions=area_fractions,
            day_of_year=day_of_year,
            emissivity_eff=0.61,
            forcing_w_m2=forcing_w_m2,
            diffusion_coeff=3.8,
            dt_days=DT_DAYS,
        )

        if step > (years - 1) * 365:
            annual_history.append(list(temps))

    annual_means = list(np.mean(annual_history, axis=0))
    return temps, annual_means


# --------------------------------------------------
# Run Baseline & Doubled CO2 Simulations
# --------------------------------------------------

# 1. Pre-Industrial Baseline (Forcing = 0.0 W/m²)
initial_guess = [275.0] * NUM_BANDS
state_baseline, mean_temps_baseline = run_to_steady_state(
    initial_guess, forcing_w_m2=0.0, years=5
)

# 2. Doubled CO2 (Uniform Radiative Forcing = +3.7 W/m²)
_, mean_temps_2xco2 = run_to_steady_state(
    state_baseline, forcing_w_m2=3.7, years=5
)

# Calculate warming per latitude band
delta_t = [t2x - t0 for t0, t2x in zip(mean_temps_baseline, mean_temps_2xco2)]

# --------------------------------------------------
# Output Results
# --------------------------------------------------

equator_idx = NUM_BANDS // 2
north_pole_idx = NUM_BANDS - 1

print()
print("=== 1D Polar Amplification Experiment ===")
print()
print(f"Equatorial Warming (0°N):    +{delta_t[equator_idx]:.2f} K")
print(f"Polar Warming (90°N):         +{delta_t[north_pole_idx]:.2f} K")
print(
    f"Amplification Ratio (Pole/Equator): {delta_t[north_pole_idx] / delta_t[equator_idx]:.2f}x"
)
print()

# --------------------------------------------------
# Plot Latitudinal Warming Profile
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    latitudes,
    delta_t,
    color="crimson",
    linewidth=2.5,
    marker="o",
    label="ΔT (Warming Profile)",
)

plt.axhline(
    delta_t[equator_idx],
    color="gray",
    linestyle="--",
    alpha=0.7,
    label=f"Equatorial Baseline (+{delta_t[equator_idx]:.2f} K)",
)

plt.xlabel("Latitude (Degrees)")
plt.ylabel("Temperature Change ΔT (K)")
plt.title("Earth in a Box — Latitudinal Warming & Polar Amplification")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig("polar_amplification.png", dpi=200)
plt.show()