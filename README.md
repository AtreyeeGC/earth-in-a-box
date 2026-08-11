# Earth in a Box 🌍

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/AtreyeeGC/earth-in-a-box)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://earth-in-a-box.streamlit.app)

**Earth in a Box** is an open-source, interactive computational climate and habitability engine. It models seasonal solar insolation geometry, dynamic ice-albedo feedbacks, longwave radiative transfer, and meridional heat diffusion across 1D planetary latitude bands to evaluate surface liquid water stability and habitability regimes across Solar System worlds and exoplanets.

---

## 🌟 Interactive Live Demo

Experience the simulator directly in your browser: **[earth-in-a-box.streamlit.app](https://earth-in-a-box.streamlit.app)**

---

## 🔬 Core Physical Modeling Features

- **1D Latitudinal Heat Balance:** Divides planetary surfaces into equal-area latitude bands with a 50m ocean thermal mixed layer ($C = 2.1 \times 10^8 \text{ J/m}^2\text{K}$).
- **Seasonal Solar Geometry:** Calculates top-of-atmosphere insolation dynamically based on day of year, latitude, axial tilt ($\theta = 0^\circ - 90^\circ$), orbital distance ($r$ in AU), and stellar luminosity ($L/L_\odot$).
- **Dynamic Ice-Albedo Feedback:** Surface albedo scales dynamically from $0.20$ (ice-free water) to $0.60$ (glaciated) anchored at $273.15\text{ K}$ ($0^\circ\text{C}$).
- **Meridional Heat Diffusion:** Models atmospheric and oceanic heat transport via second-order spatial discretization (Budyko transport kernel).
- **Quantitative Habitability Metrics:** Evaluates planetary surface area fractions for permanent habitability, seasonal habitability, and uninhabitable glaciated/runaway regimes ($273.15\text{ K} \le T \le 373.15\text{ K}$).

---

## 🛠️ Repository Architecture

```text
earth-in-a-box/
├── app.py                         # Streamlit interactive dashboard UI
├── src/
│   ├── climate_1d.py              # Time-stepping numerical integration engine
│   ├── exoplanet_api.py           # NASA Exoplanet Archive TAP API client
│   ├── exoplanets.py              # Pre-configured astronomical target profiles
│   ├── feedbacks.py               # Dynamic ice-albedo feedback module
│   ├── grid.py                    # Equal-area latitudinal grid & Budyko diffusion
│   ├── habitability.py            # Area-weighted surface liquid water metrics
│   └── solar_geometry.py          # Orbital insolation & declination algorithms
├── tests/                         # Pytest test suite (>30 unit tests)
└── experiments/                   # Scientific validation write-ups and markdown reports