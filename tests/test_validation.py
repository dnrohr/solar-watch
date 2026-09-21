from pathlib import Path

import pandas as pd

from solar_watch.model import generate_reference_table
from solar_watch.validation import compare_models


ROOT = Path(__file__).resolve().parents[1]


def test_full_year_against_frozen_jpl_de421_ephemeris() -> None:
    independent = pd.read_csv(ROOT / "data" / "skyfield_de421_42p1N_2025.csv")
    errors = compare_models(generate_reference_table(), independent)
    assert len(errors) == 365
    assert errors[["sunrise_error_min", "sunset_error_min"]].abs().max().max() <= 0.1
    assert (
        errors[["sunrise_azimuth_error_deg", "sunset_azimuth_error_deg"]]
        .abs()
        .max()
        .max()
        <= 0.1
    )
