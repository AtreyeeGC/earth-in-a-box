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


def test_1d_equator_warmer_than_north_pole_in_january():
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

    # In January, North Pole (index 17) is in polar night and colder than equator (index 9)
    assert temps[9] > temps[17]


def test_1d_annual_equator_warmer_than_poles():
    lats, areas = create_latitude_grid(18)
    temps = [275.0] * 18
    annual_history = []

    for day in range(1, 366):
        temps = step_1d_climate(
            temperatures=temps,
            latitudes=lats,
            area_fractions=areas,
            day_of_year=float(day),
            dt_days=1.0,
        )
        annual_history.append(list(temps))

    equator_mean = sum(h[9] for h in annual_history) / 365.0
    south_pole_mean = sum(h[0] for h in annual_history) / 365.0
    north_pole_mean = sum(h[17] for h in annual_history) / 365.0

    assert equator_mean > south_pole_mean
    assert equator_mean > north_pole_mean