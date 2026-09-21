import numpy as np
import pytest

from solar_watch.cam import AZIMUTH_CAM, DAYLIGHT_CAM, cam_outline, periodic_profile
from solar_watch.model import generate_reference_table


@pytest.fixture(scope="module")
def table():
    return generate_reference_table()


@pytest.mark.parametrize("spec", [DAYLIGHT_CAM, AZIMUTH_CAM])
def test_profile_interpolates_every_reference_day(table, spec) -> None:
    pitch = periodic_profile(table, spec)(np.arange(len(table), dtype=float))
    recovered = spec.datum_value + (pitch - spec.pitch_base_mm) / spec.scale_mm_per_unit
    assert np.max(np.abs(recovered - table[spec.source_column].to_numpy())) < 1e-9


@pytest.mark.parametrize("spec", [DAYLIGHT_CAM, AZIMUTH_CAM])
def test_profile_is_closed_and_follower_friendly(table, spec) -> None:
    pitch_fn = periodic_profile(table, spec)
    assert pitch_fn(np.array([0.0]))[0] == pytest.approx(
        pitch_fn(np.array([365.0]))[0], abs=1e-12
    )
    outline = cam_outline(table, spec)
    assert outline["pressure_angle_deg"].max() < 30.0
    assert outline["pitch_curvature_radius_mm"].min() > spec.roller_radius_mm
    assert outline["surface_radius_mm"].min() > 35.0
    assert outline["surface_radius_mm"].max() < 92.0

    theta = np.radians(outline["cam_angle_deg"].to_numpy())
    pitch_x = outline["pitch_radius_mm"].to_numpy() * np.cos(theta)
    pitch_y = outline["pitch_radius_mm"].to_numpy() * np.sin(theta)
    offset = np.hypot(
        pitch_x - outline["surface_x_mm"].to_numpy(),
        pitch_y - outline["surface_y_mm"].to_numpy(),
    )
    assert np.max(np.abs(offset - spec.roller_radius_mm)) < 1e-9
