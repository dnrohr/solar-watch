from datetime import date

import numpy as np
import pandas as pd
import pytest
from pvlib import solarposition

from solar_watch.model import (
    ReferenceConfig,
    analytical_event_geometry,
    generate_reference_table,
    validate_calendar_date,
)


def test_reference_table_covers_non_leap_year() -> None:
    table = generate_reference_table()
    assert len(table) == 365
    assert table.iloc[0]["date"] == "2025-01-01"
    assert table.iloc[-1]["date"] == "2025-12-31"
    assert np.isfinite(table.select_dtypes(include=[float, int])).all().all()


def test_events_use_exact_project_altitude() -> None:
    table = generate_reference_table()
    for column in ("sunrise_utc", "sunset_utc"):
        positions = solarposition.spa_python(
            pd.DatetimeIndex(pd.to_datetime(table[column], utc=True)),
            42.1,
            0.0,
            altitude=0.0,
            pressure=0.0,
            delta_t=None,
        )
        assert np.max(np.abs(positions["elevation"].to_numpy() + 0.833)) < 1e-6


def test_equinox_geometry_is_nearly_twelve_hours() -> None:
    daylight, azimuth = analytical_event_geometry(42.1, 0.0)
    # The standard -0.833 degree event altitude makes standardized daylight
    # about nine minutes longer than the geometric 12-hour equinox day.
    assert daylight == pytest.approx(728.98, abs=0.02)
    assert azimuth == pytest.approx(89.25, abs=0.02)


def test_rejects_unsupported_latitude() -> None:
    with pytest.raises(ValueError, match="outside supported"):
        generate_reference_table(ReferenceConfig(latitude_deg=60.01))


def test_calendar_date_does_not_silently_cross_year() -> None:
    with pytest.raises(ValueError, match="outside reference year"):
        validate_calendar_date(date(2026, 1, 1), 2025)
