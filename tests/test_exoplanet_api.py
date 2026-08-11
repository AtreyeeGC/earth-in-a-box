from src.exoplanet_api import fetch_nasa_exoplanet_data


def test_fetch_nasa_exoplanet_trappist():
    data = fetch_nasa_exoplanet_data("TRAPPIST-1 e")
    if data is not None:
        assert "distance_au" in data
        assert data["distance_au"] > 0.0


def test_invalid_exoplanet_returns_none():
    data = fetch_nasa_exoplanet_data("NonExistentPlanet99999")
    assert data is None