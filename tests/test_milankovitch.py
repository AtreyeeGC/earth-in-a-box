from src.milankovitch import compute_milankovitch_insolation, update_ice_sheet_height


def test_ice_growth_below_freezing():
    height = update_ice_sheet_height(
        current_height_m=10.0, surface_temp_k=260.0, dt_years=100.0
    )
    assert height > 10.0


def test_ice_melt_above_freezing():
    height = update_ice_sheet_height(
        current_height_m=50.0, surface_temp_k=280.0, dt_years=100.0
    )
    assert height < 50.0


def test_milankovitch_41kyr_obliquity_oscillation():
    flux_t0 = compute_milankovitch_insolation(latitude_deg=65.0, year_thousand=0.0)
    flux_t20 = compute_milankovitch_insolation(latitude_deg=65.0, year_thousand=20.5)

    assert flux_t0 != flux_t20