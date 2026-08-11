import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.climate_1d import step_1d_climate
from src.exoplanet_api import fetch_nasa_exoplanet_data
from src.exoplanets import EXOPLANET_DATABASE
from src.grid import create_latitude_grid
from src.habitability import calculate_habitability_metrics
from src.solar_geometry import calculate_solar_constant

st.set_page_config(
    page_title="Earth in a Box — Planetary Climate Simulator",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Earth in a Box: 1D Planetary Climate & Habitability Engine")
st.markdown(
    """
An interactive computational climate simulator modeling seasonal solar insolation, 
dynamic ice-albedo feedbacks, longwave radiative transfer, and meridional heat diffusion across real and hypothetical planets.
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
st.sidebar.header("Orbital & Planetary Parameters")

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

axial_tilt = st.sidebar.slider(
    "Axial Tilt (°)",
    min_value=0.0,
    max_value=90.0,
    value=float(preset_info["axial_tilt_deg"]),
    step=0.5,
)

forcing = st.sidebar.slider(
    "Radiative Forcing (W/m²)",
    min_value=-20.0,
    max_value=30.0,
    value=float(preset_info["forcing_w_m2"]),
    step=0.5,
)

diffusion = st.sidebar.slider(
    "Heat Diffusion Coeff D (W/m²K)",
    min_value=0.0,
    max_value=10.0,
    value=3.8,
    step=0.2,
)

sim_years = st.sidebar.slider("Simulation Years", min_value=2, max_value=10, value=5)

solar_constant = calculate_solar_constant(luminosity_ratio, distance_au)
st.sidebar.info(f"Top-of-Atmosphere Solar Flux: **{solar_constant:.1f} W/m²**")

# --------------------------------------------------
# Run Simulation
# --------------------------------------------------

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
        forcing_w_m2=forcing,
        axial_tilt_deg=axial_tilt,
        solar_constant=solar_constant,
        diffusion_coeff=diffusion,
        dt_days=1.0,
    )

    if step > (sim_years - 1) * 365:
        history.append(list(temps))

temp_matrix = np.array(history).T
metrics = calculate_habitability_metrics(temp_matrix, area_fractions)

# --------------------------------------------------
# Render Dashboard Metrics
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Permanently Habitable Area", f"{metrics['permanently_habitable_fraction']*100:.1f}%")
col2.metric("Seasonally Habitable Area", f"{metrics['seasonally_habitable_fraction']*100:.1f}%")
col3.metric("Permanently Frozen Area", f"{metrics['uninhabitable_frozen_fraction']*100:.1f}%")
col4.metric("Boiling Uninhabitable Area", f"{metrics['uninhabitable_boiling_fraction']*100:.1f}%")

st.markdown("---")

# --------------------------------------------------
# Render Plotly Heatmap
# --------------------------------------------------

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
    title=f"Seasonal Latitude-Temperature Profile for {selected_name}",
    xaxis_title="Day of Year",
    yaxis_title="Latitude (Degrees)",
    height=550,
)

st.plotly_chart(fig, use_container_width=True)