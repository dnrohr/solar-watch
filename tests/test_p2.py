import numpy as np
import pytest

from solar_watch.model import generate_reference_table
from solar_watch.p2 import (
    P2Envelope,
    P2Ratios,
    TIME_DEG_PER_MIN,
    azimuth_follower_from_degrees,
    daylight_follower_from_minutes,
    dial_tick_spacing_mm,
    mirrored_sunset_azimuth_deg,
    recovered_sunrise_azimuth_deg,
    recovered_sunset_angle_deg,
    sunset_minutes,
    time_dial_angle_deg,
    time_summer_rack_positions,
)


def test_p2_envelope_and_readability() -> None:
    envelope = P2Envelope()
    assert envelope.width_mm <= 24.0 * 25.4
    assert envelope.height_mm <= 36.0 * 25.4
    assert envelope.depth_mm < 12.0 * 25.4
    assert dial_tick_spacing_mm(envelope.time_dial_diameter_mm, 2.5) > 5.0
    assert dial_tick_spacing_mm(envelope.azimuth_dial_diameter_mm, 5.0) > 15.0


def test_ratios_are_small_calibration_adjustments() -> None:
    ratios = P2Ratios()
    assert ratios.daylight_span_ratio == pytest.approx(1.0, abs=1e-12)
    assert ratios.azimuth_span_ratio == pytest.approx(1.0, abs=1e-12)


def test_linear_differential_exactly_sums_sunrise_and_daylight() -> None:
    table = generate_reference_table()
    daylight = table["daylight_min"].to_numpy()
    follower = daylight_follower_from_minutes(daylight)
    for sunrise in np.arange(0.0, 720.0, 15.0):
        _, _, carrier = time_summer_rack_positions(sunrise, follower)
        # The cam datum contributes a constant phase removed by the independent
        # sunset zero adjustment.
        phase = TIME_DEG_PER_MIN * 545.0
        actual = recovered_sunset_angle_deg(carrier, phase_deg=phase)
        expected = time_dial_angle_deg(sunset_minutes(sunrise, daylight))
        error = (actual - expected + 180.0) % 360.0 - 180.0
        assert np.max(np.abs(error)) < 1e-10


def test_azimuth_linkage_and_mirror_match_reference_all_year() -> None:
    table = generate_reference_table()
    expected = table["sunrise_azimuth_deg"].to_numpy()
    follower = azimuth_follower_from_degrees(expected)
    actual = recovered_sunrise_azimuth_deg(follower)
    assert np.max(np.abs(actual - expected)) < 1e-10
    mirrored = mirrored_sunset_azimuth_deg(actual)
    model_sunset = table["sunset_azimuth_deg"].to_numpy()
    error = (mirrored - model_sunset + 180.0) % 360.0 - 180.0
    assert np.max(np.abs(error)) < 0.28
