from src.climate_1d import step_1d_climate
from src.grid import create_latitude_grid


def test_1d_climate_step_runs():
    lats, areas = create_latitude_grid(18)
    temps = [275.0] * 18

    new_temps = step_1d_climate(
        temperatures=temps,
        latitudes=lats,
        area_fractions=areas,
        day_of_year=1.0,
        dt_days=1.0,
    )

    assert len(new_temps) == 18
    assert all(isinstance(t, float) for t in new_temps)


def test_1d_equator_warmer_than_poles_after_steps():
    lats, areas = create_latitude_grid(18)
    temps = [275.0] * 18

    for day in range(1, 30):
        temps = step_1d_climate(
            temperatures=temps,
            latitudes=lats,
            area_fractions=areas,
            day_of_year=float(day),
            dt_days=1.0,
        )

    # Equator (index 9) should be warmer than South Pole (index 0)
    assert temps[9] > temps[0]