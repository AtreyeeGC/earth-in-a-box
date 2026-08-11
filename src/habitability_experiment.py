import numpy as np

from src.climate_1d import step_1d_climate
from src.grid import create_latitude_grid
from src.habitability import calculate_habitability_metrics

NUM_BANDS = 18
DT_DAYS = 1.0

latitudes, area_fractions = create_latitude_grid(NUM_BANDS)


def run_habitability_simulation(
    axial_tilt: float = 23.44,
    forcing_w_m2: float = 0.0,
    years: int = 5,
) -> dict:
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
            forcing_w_m2=forcing_w_m2,
            axial_tilt_deg=axial_tilt,
            dt_days=DT_DAYS,
        )

        if step > (years - 1) * 365:
            final_year_history.append(list(temps))

    # Shape: (latitudes, days)
    temp_matrix = np.array(final_year_history).T

    return calculate_habitability_metrics(temp_matrix, area_fractions)


# --------------------------------------------------
# Run Comparative Scenarios
# --------------------------------------------------

scenarios = {
    "Earth Baseline (23.44° Tilt)": {"tilt": 23.44, "forcing": 0.0},
    "2x CO2 Atmosphere (+3.7 W/m²)": {"tilt": 23.44, "forcing": 3.7},
    "Sideways Planet (90.0° Tilt)": {"tilt": 90.0, "forcing": 0.0},
}

print()
print("=== Quantitative Habitability Analysis ===")
print()

for name, params in scenarios.items():
    metrics = run_habitability_simulation(
        axial_tilt=params["tilt"], forcing_w_m2=params["forcing"]
    )
    print(f"--- {name} ---")
    print(
        f"  Permanently Habitable Area: {metrics['permanently_habitable_fraction']*100:.1f}%"
    )
    print(
        f"  Seasonally Habitable Area:  {metrics['seasonally_habitable_fraction']*100:.1f}%"
    )
    print(
        f"  Permanently Frozen Area:    {metrics['uninhabitable_frozen_fraction']*100:.1f}%"
    )
    print()