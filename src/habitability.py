from typing import Dict, List
import numpy as np

FREEZING_POINT_K = 273.15
BOILING_POINT_K = 373.15


def calculate_habitability_metrics(
    temperature_matrix: np.ndarray,
    area_fractions: List[float],
) -> Dict[str, float]:
    """
    Calculate area-weighted habitability metrics for a 1D seasonal climate simulation.

    Parameters
    ----------
    temperature_matrix : np.ndarray
        Array of shape (num_latitudes, 365) containing surface temperatures (K).
    area_fractions : List[float]
        Normalized surface area fractions for each latitude band.

    Returns
    -------
    Dict[str, float]
        Dictionary containing habitability metrics:
        - 'permanently_habitable_fraction': Fraction of planetary surface area maintaining
                                           liquid water conditions 365 days/year.
        - 'seasonally_habitable_fraction': Fraction of planetary surface area supporting
                                          liquid water for at least 1 day/year.
        - 'uninhabitable_frozen_fraction': Area fraction permanently below 273.15 K.
        - 'uninhabitable_boiling_fraction': Area fraction experiencing temperatures above 373.15 K.
    """
    num_lats, num_days = temperature_matrix.shape
    areas = np.array(area_fractions)

    # Boolean matrix: True where liquid water is stable
    is_liquid = (temperature_matrix >= FREEZING_POINT_K) & (
        temperature_matrix <= BOILING_POINT_K
    )

    # Days per year that each latitude band is habitable
    habitable_days_per_band = np.sum(is_liquid, axis=1)

    # Area fractions by habitability regime
    permanently_habitable_mask = habitable_days_per_band == num_days
    seasonally_habitable_mask = (habitable_days_per_band > 0) & (
        habitable_days_per_band < num_days
    )

    permanently_habitable_area = float(np.sum(areas[permanently_habitable_mask]))
    seasonally_habitable_area = float(np.sum(areas[seasonally_habitable_mask]))

    # Identify permanently frozen or boiling bands
    permanently_frozen_mask = np.all(
        temperature_matrix < FREEZING_POINT_K, axis=1
    )
    permanently_boiling_mask = np.any(
        temperature_matrix > BOILING_POINT_K, axis=1
    )

    return {
        "permanently_habitable_fraction": permanently_habitable_area,
        "seasonally_habitable_fraction": seasonally_habitable_area,
        "uninhabitable_frozen_fraction": float(np.sum(areas[permanently_frozen_mask])),
        "uninhabitable_boiling_fraction": float(np.sum(areas[permanently_boiling_mask])),
    }