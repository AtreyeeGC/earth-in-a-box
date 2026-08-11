import numpy as np
from src.grid import create_latitude_grid
from src.habitability import calculate_habitability_metrics


def test_perfectly_habitable_planet():
    lats, areas = create_latitude_grid(18)
    # Uniform 290 K planet across all 365 days
    temp_matrix = np.full((18, 365), 290.0)

    metrics = calculate_habitability_metrics(temp_matrix, areas)

    assert abs(metrics["permanently_habitable_fraction"] - 1.0) < 1e-5
    assert metrics["seasonally_habitable_fraction"] == 0.0
    assert metrics["uninhabitable_frozen_fraction"] == 0.0


def test_frozen_snowball_planet():
    lats, areas = create_latitude_grid(18)
    # Uniform 240 K planet
    temp_matrix = np.full((18, 365), 240.0)

    metrics = calculate_habitability_metrics(temp_matrix, areas)

    assert metrics["permanently_habitable_fraction"] == 0.0
    assert abs(metrics["uninhabitable_frozen_fraction"] - 1.0) < 1e-5