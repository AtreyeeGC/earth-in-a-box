import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.climate_1d import step_1d_climate
from src.climate_2d import step_2d_climate
from src.exoplanet_api import fetch_nasa_exoplanet_data
from src.exoplanets import EXOPLANET_DATABASE
from src.greenhouse_dynamic import calculate_co2_forcing
from src.grid import create_latitude_grid
from src.grid_2d import create_2d_grid, create_land_ocean_mask, get_heat_capacity_matrix
from src.habitability import calculate_habitability_metrics
from src.solar_geometry import calculate_solar_constant
from src.solar_geometry_2d import calculate_2d_insolation
from src.viz_3d import create_3d_globe_figure
from src.habitable_zone import calculate_habitable_zone_limits

st.set_page_config(
    page_title="Earth in a Box — Planetary Climate Simulator",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Earth in a Box: 2D Planetary Climate & Habitability Engine")
st.markdown(
    """
An interactive computational climate simulator modeling seasonal solar insolation, 
dynamic ice-albedo feedbacks, Clausius-Clapeyron water vapor greenhouse transport, 
and 2D spherical meridional heat diffusion across real and hypothetical worlds.
"""
)

# --------------------------------------------------
# Sidebar Controls & Exoplanet Selector
# --------------------------------------------------

st.sidebar.header("Target Body Selector")

input_mode = st.sidebar.radio("Selection Mode", ["Preset Catalog", "Search NASA Archive"])

preset_info = EXOPLANET_DATABASE["Modern Earth"]
selected_name = "Modern Earth"

if input_mode == "Preset Catalog":
    selected_preset = st.sidebar.selectbox(
        "Load Planetary Preset", list(EXOPLANET_DATABASE.keys())
    )
    preset_info = EXOPLANET_DATABASE[selected_preset]
    selected_name = selected_preset
    st.sidebar.caption(preset_info["description"])
else:
    search_query = st.sidebar.text_input("Exoplanet Name (e.g. TRAPPIST-1 e, Kepler-22 b)", value="TRAPPIST-1 e")
    if search_query:
        with st.sidebar.spinner("Querying NASA Exoplanet Archive..."):
            api_result = fetch_nasa_exoplanet_data(search_query)
            if api_result and api_result.get("distance_au"):
                st.sidebar.success(f"Loaded {api_result['planet_name']} from NASA TAP API")
                preset_info = {
                    "distance_au": api_result["distance_au"],
                    "luminosity_ratio": api_result.get("luminosity_ratio") or 1.0,
                    "axial_tilt_deg": 0.0,
                    "forcing_w_m2": 0.0,
                }
                selected_name = api_result["planet_name"]
            else:
                st.sidebar.warning("Planet not found or missing orbital data. Using defaults.")

st.sidebar.markdown("---")
st.sidebar.header("Model Dimension & Rotation")

sim_mode = st.sidebar.radio("Simulation Dimension", ["1D Seasonal Profile", "2D Spherical Surface Map"])
tidally_locked = st.sidebar.checkbox("Tidally Locked (Synchronous Rotation)", value=(selected_name == "TRAPPIST-1e"))

st.sidebar.markdown("---")
st.sidebar.header("Atmosphere & Orbital Parameters")

distance_au = st.sidebar.slider(
    "Orbital Distance (AU)",
    min_value=0.01,
    max_value=3.0,
    value=float(preset_info["distance_au"]),
    step=0.01,
)

luminosity_ratio = st.sidebar.number_input(
    "Stellar Luminosity (L / L_sun)",
    min_value=0.0001,
    max_value=10.0,
    value=float(preset_info["luminosity_ratio"]),
    format="%.6f",
)

co2_ppm = st.sidebar.slider("Atmospheric CO₂ (ppm)", min_value=10, max_value=2800, value=280, step=10)

axial_tilt = st.sidebar.slider(
    "Axial Tilt (°)",
    min_value=0.0,
    max_value=90.0,
    value=float(preset_info["axial_tilt_deg"]),
    step=0.5,
)

diffusion = st.sidebar.slider(
    "Heat Diffusion Coeff D (W/m²K)",
    min_value=0.0,
    max_value=10.0,
    value=0.5 if sim_mode == "2D Spherical Surface Map" else 3.8,
    step=0.1,
)

hz_limits = calculate_habitable_zone_limits(luminosity_ratio)

st.sidebar.info(
    f"Top-of-Atmosphere Solar Flux: **{solar_constant:.1f} W/m²**\n\n"
    f"CO₂ Forcing: **{co2_forcing:+.2f} W/m²**\n\n"
    f"🪐 **Habitable Zone (AU):**\n"
    f"Inner: `{hz_limits['inner_edge_au']} AU` | Outer: `{hz_limits['outer_edge_au']} AU`"
)

solar_constant = calculate_solar_constant(luminosity_ratio, distance_au)
co2_forcing = calculate_co2_forcing(co2_ppm)
st.sidebar.info(f"Top-of-Atmosphere Solar Flux: **{solar_constant:.1f} W/m²**\n\nCO₂ Forcing: **{co2_forcing:+.2f} W/m²**")

# --------------------------------------------------
# Execution & Visualization Logic
# --------------------------------------------------

if sim_mode == "1D Seasonal Profile":
    sim_years = st.sidebar.slider("Simulation Years", min_value=2, max_value=10, value=5)
    NUM_BANDS = 18
    latitudes, area_fractions = create_latitude_grid(NUM_BANDS)

    temps = [275.0] * NUM_BANDS
    history = []

    total_days = int(sim_years * 365)
    for step in range(1, total_days + 1):
        day_of_year = ((step - 1) % 365) + 1

        temps = step_1d_climate(
            temperatures=temps,
            latitudes=latitudes,
            area_fractions=area_fractions,
            day_of_year=day_of_year,
            forcing_w_m2=co2_forcing,
            axial_tilt_deg=axial_tilt,
            solar_constant=solar_constant,
            diffusion_coeff=diffusion,
            dt_days=1.0,
        )

        if step > (sim_years - 1) * 365:
            history.append(list(temps))

    temp_matrix = np.array(history).T
    metrics = calculate_habitability_metrics(temp_matrix, area_fractions)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Permanently Habitable Area", f"{metrics['permanently_habitable_fraction']*100:.1f}%")
    col2.metric("Seasonally Habitable Area", f"{metrics['seasonally_habitable_fraction']*100:.1f}%")
    col3.metric("Permanently Frozen Area", f"{metrics['uninhabitable_frozen_fraction']*100:.1f}%")
    col4.metric("Boiling Uninhabitable Area", f"{metrics['uninhabitable_boiling_fraction']*100:.1f}%")

    st.markdown("---")

    fig = go.Figure(
        data=go.Contour(
            z=temp_matrix,
            x=list(range(1, 366)),
            y=latitudes,
            colorscale="RdYlBu_r",
            colorbar=dict(title="Temperature (K)"),
            contours=dict(coloring="heatmap", showlabels=True),
        )
    )
    fig.update_layout(
        title=f"1D Seasonal Latitude-Temperature Profile for {selected_name}",
        xaxis_title="Day of Year",
        yaxis_title="Latitude (Degrees)",
        height=550,
    )
    st.plotly_chart(fig, use_container_width=True)

    # CSV Exporter for 1D Data
    csv_1d = np.savetxt("temp_1d.csv", temp_matrix, delimiter=",", fmt="%.2f")
    with open("temp_1d.csv", "rb") as f:
        st.download_button(
            label="📥 Export 1D Temperature Matrix (CSV)",
            data=f,
            file_name=f"{selected_name}_1d_temperature.csv",
            mime="text/csv",
        )

else:
    # 2D Spherical Surface Map Integration
    surface_type = st.sidebar.selectbox("Surface Mask", ["aqua", "tidally_locked_continent", "earth_like"])
    
    lats, lons, lat_grid, lon_grid = create_2d_grid(18, 36)
    land_mask = create_land_ocean_mask(lat_grid, lon_grid, mask_type=surface_type)
    c_matrix = get_heat_capacity_matrix(land_mask)

    temp_matrix_2d = np.full((18, 36), 288.0)
    
    with st.spinner("Integrating 2D Spherical Heat Transport Engine..."):
        for day in range(1, 31):
            insolation_2d = calculate_2d_insolation(
                lat_grid_deg=lat_grid,
                lon_grid_deg=lon_grid,
                day_of_year=day,
                axial_tilt_deg=axial_tilt,
                solar_constant=solar_constant,
                tidally_locked=tidally_locked,
            )
            temp_matrix_2d = step_2d_climate(
                temp_matrix=temp_matrix_2d,
                lat_grid_deg=lat_grid,
                lon_grid_deg=lon_grid,
                heat_capacity_matrix=c_matrix,
                insolation_matrix=insolation_2d,
                co2_ppm=co2_ppm,
                forcing_w_m2=0.0,
                diffusion_coeff=diffusion,
                dt_seconds=86400.0,
                max_substep_seconds=900.0,
            )

    mean_temp = float(np.mean(temp_matrix_2d))
    max_temp = float(np.max(temp_matrix_2d))
    min_temp = float(np.min(temp_matrix_2d))
    habitable_pct = float(np.mean((temp_matrix_2d >= 273.15) & (temp_matrix_2d <= 373.15)) * 100)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean Global Temp", f"{mean_temp:.1f} K")
    col2.metric("Max Temperature", f"{max_temp:.1f} K")
    col3.metric("Min Temperature", f"{min_temp:.1f} K")
    col4.metric("Habitable Surface Area", f"{habitable_pct:.1f}%")

    st.markdown("---")

    # Map projection selector
    render_style = st.radio("Map Projection", ["2D Surface Map", "3D Interactive Globe"], horizontal=True)

    if render_style == "2D Surface Map":
        fig_2d = go.Figure(
            data=go.Heatmap(
                z=temp_matrix_2d,
                x=lons,
                y=lats,
                colorscale="Plasma",
                colorbar=dict(title="Temperature (K)"),
            )
        )
        fig_2d.update_layout(
            title=f"2D Surface Temperature Map for {selected_name} ({'Tidally Locked' if tidally_locked else 'Rotating'})",
            xaxis_title="Longitude (Degrees)",
            yaxis_title="Latitude (Degrees)",
            height=550,
        )
        st.plotly_chart(fig_2d, use_container_width=True)
    else:
        fig_3d = create_3d_globe_figure(
            temp_matrix=temp_matrix_2d,
            latitudes=lats,
            longitudes=lons,
            title=f"3D Surface Temperature Globe for {selected_name}",
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    # CSV Exporter for 2D Data
    np.savetxt("temp_2d.csv", temp_matrix_2d, delimiter=",", fmt="%.2f")
    with open("temp_2d.csv", "rb") as f:
        st.download_button(
            label="📥 Export 2D Temperature Grid (CSV)",
            data=f,
            file_name=f"{selected_name}_2d_temperature.csv",
            mime="text/csv",
        )