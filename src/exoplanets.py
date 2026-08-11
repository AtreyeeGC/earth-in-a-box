from typing import Dict, Any

EXOPLANET_DATABASE: Dict[str, Dict[str, Any]] = {
    "Modern Earth": {
        "distance_au": 1.00,
        "luminosity_ratio": 1.00,
        "axial_tilt_deg": 23.44,
        "forcing_w_m2": 0.0,
        "description": "Standard modern terrestrial baseline.",
    },
    "Mars": {
        "distance_au": 1.52,
        "luminosity_ratio": 1.00,
        "axial_tilt_deg": 25.19,
        "forcing_w_m2": -15.0,  # Weak atmosphere
        "description": "Cold, thin atmosphere, high orbital distance.",
    },
    "TRAPPIST-1e": {
        "distance_au": 0.029,
        "luminosity_ratio": 0.000553,  # Ultra-cool M-dwarf star
        "axial_tilt_deg": 0.0,  # Tidally influenced / low tilt
        "forcing_w_m2": 2.0,
        "description": "Potentially habitable Earth-sized exoplanet orbiting an M-dwarf star.",
    },
    "Proxima Centauri b": {
        "distance_au": 0.0485,
        "luminosity_ratio": 0.00155,
        "axial_tilt_deg": 3.0,
        "forcing_w_m2": 5.0,
        "description": "Closest known exoplanet in the habitable zone of a red dwarf.",
    },
    "Kepler-186f": {
        "distance_au": 0.432,
        "luminosity_ratio": 0.055,
        "axial_tilt_deg": 20.0,
        "forcing_w_m2": 10.0,  # Requires greenhouse warming to prevent freezing
        "description": "First validated Earth-sized exoplanet in the habitable zone of an M-star.",
    },
}