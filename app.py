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
from src.gravity import calculate_scale_height, calculate_surface_gravity


st.set_page_config(
    page_title="Earth in a Box — Planetary Climate Simulator",
    page_icon="🌍",
    layout="wide",
)

# --------------------------------------------------
# Custom Glassmorphism & Cyber-Space UI Styling
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e1b4b 0%, #0f172a 60%, #020617 100%);
        color: #f8fafc;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sleek Glassmorphism Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 16px;
        border-radius: 14px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.6);
    }
    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 0.85rem !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        letter-spacing: -0.03em;
    }
    
    /* Custom Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(2, 6, 23, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌍 Earth in a Box: Planetary Climate & Habitability Engine")
st.markdown(
    """
    <p style='color: #94a3b8; font-size: 1.1rem; margin-top: -10px;'>
    An interactive computational astrophysics platform modeling stellar insolation, dynamic ice-albedo feedbacks, 
    Clausius-Clapeyron atmospheric vapor transport, and multidimensional heat diffusion across worlds.
    </p>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Sidebar Controls & Exoplanet Selector
# --------------------------------------------------

st.sidebar.markdown("### 🔭 Target Body Selector")
input_mode = st.sidebar.radio("Selection Mode", ["Preset Catalog", "Search NASA Archive"], label_visibility="collapsed")

preset_info = EXOPLANET_DATABASE["Modern Earth"]
selected_name = "Modern Earth"

if input_mode == "Preset Catalog":
    selected_preset = st.sidebar.selectbox(
        "Load Planetary Preset", list(EXOPLANET_DATABASE.keys())
    )
    preset_info = EXOPLANET_DATABASE[selected_preset]
    selected_name = selected_preset
    st.sidebar.caption(f"💡 {preset_info['description']}")
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
st.sidebar.markdown("### 🌐 Model Configuration")

sim_mode = st.sidebar.radio("Simulation Dimension", ["1D Seasonal Profile", "2D Spherical Surface Map"], label_visibility="collapsed")
tidally_locked = st.sidebar.checkbox("Tidally Locked (Synchronous Rotation)", value=(selected_name == "TRAPPIST-1e"))

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Orbital & Atmospheric Parameters")

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

eccentricity = st.sidebar.slider(
    "Orbital Eccentricity (e)",
    min_value=0.0,
    max_value=0.6,
    value=0.0167,  # Earth's eccentricity default
    step=0.005,
    help="0.0 = Circular Orbit, >0.0 = Elliptical Orbit"
)


st.sidebar.markdown("### 🪐 Planetary Dimensions")

planet_mass = st.sidebar.slider(
    "Planetary Mass (M / M_Earth)",
    min_value=0.1,
    max_value=10.0,
    value=1.0,
    step=0.1,
)

planet_radius = st.sidebar.slider(
    "Planetary Radius (R / R_Earth)",
    min_value=0.3,
    max_value=3.0,
    value=1.0,
    step=0.05,
)

surface_g = calculate_surface_gravity(planet_mass, planet_radius)
scale_height_km = calculate_scale_height(288.15, surface_g)


# Compute derived parameters prior to sidebar info display
solar_constant = calculate_solar_constant(luminosity_ratio, distance_au)
co2_forcing = calculate_co2_forcing(co2_ppm)
hz_limits = calculate_habitable_zone_limits(luminosity_ratio)

st.sidebar.markdown("---")
st.sidebar.info(
    f"☀️ **TOA Solar Flux:** `{solar_constant:.1f} W/m²`\n\n"
    f"☁️ **CO₂ Forcing:** `{co2_forcing:+.2f} W/m²`\n\n"
    f"⚓ **Surface Gravity:** `{surface_g:.2f} g`\n\n"
    f"📏 **Scale Height:** `{scale_height_km:.1f} km`\n\n"
    f"🪐 **Habitable Zone:** `{hz_limits['inner_edge_au']} - {hz_limits['outer_edge_au']} AU`"
)

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
    col1.metric("Permanently Habitable", f"{metrics['permanently_habitable_fraction']*100:.1f}%")
    col2.metric("Seasonally Habitable", f"{metrics['seasonally_habitable_fraction']*100:.1f}%")
    col3.metric("Permanently Frozen", f"{metrics['uninhabitable_frozen_fraction']*100:.1f}%")
    col4.metric("Boiling Uninhabitable", f"{metrics['uninhabitable_boiling_fraction']*100:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    fig = go.Figure(
        data=go.Contour(
            z=temp_matrix,
            x=list(range(1, 366)),
            y=latitudes,
            colorscale="RdYlBu_r",
            colorbar=dict(title="Temp (K)"),
            contours=dict(coloring="heatmap", showlabels=True),
        )
    )
    fig.update_layout(
        title=dict(text=f"1D Seasonal Latitude-Temperature Profile: {selected_name}", font=dict(size=18, color="#f8fafc")),
        xaxis_title="Day of Year",
        yaxis_title="Latitude (Degrees)",
        height=550,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

    # CSV Exporter for 1D Data
    np.savetxt("temp_1d.csv", temp_matrix, delimiter=",", fmt="%.2f")
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
    
    with st.spinner("⏳ Integrating 2D Spherical Heat Transport Engine..."):
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
    col4.metric("Habitable Surface", f"{habitable_pct:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Map projection selector
    render_style = st.radio("Map Projection Style", ["2D Surface Map", "3D Interactive Globe"], horizontal=True, label_visibility="collapsed")

    if render_style == "2D Surface Map":
        fig_2d = go.Figure(
            data=go.Heatmap(
                z=temp_matrix_2d,
                x=lons,
                y=lats,
                colorscale="Plasma",
                colorbar=dict(title="Temp (K)"),
            )
        )
        fig_2d.update_layout(
            title=dict(text=f"2D Surface Temperature Map: {selected_name} ({'Tidally Locked' if tidally_locked else 'Rotating'})", font=dict(size=18, color="#f8fafc")),
            xaxis_title="Longitude (Degrees)",
            yaxis_title="Latitude (Degrees)",
            height=550,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_2d, use_container_width=True)
    else:
        fig_3d = create_3d_globe_figure(
            temp_matrix=temp_matrix_2d,
            latitudes=lats,
            longitudes=lons,
            title=f"3D Surface Temperature Globe: {selected_name}",
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