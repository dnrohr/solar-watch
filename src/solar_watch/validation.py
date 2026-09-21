"""Independent JPL DE421 / Skyfield validation for the SPA reference table."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from skyfield import almanac
from skyfield.api import Loader, wgs84

from .model import ReferenceConfig, generate_reference_table


def generate_skyfield_table(
    cache_directory: Path,
    config: ReferenceConfig = ReferenceConfig(),
) -> pd.DataFrame:
    """Generate an independent table using JPL DE421 through Skyfield.

    The first run downloads ``de421.bsp`` into the supplied cache.  It is not a
    system-wide installation and is intentionally not committed to the project.
    """

    config.validate()
    load = Loader(str(cache_directory))
    ts = load.timescale()
    eph = load("de421.bsp")
    earth, sun = eph["earth"], eph["sun"]
    site = earth + wgs84.latlon(
        latitude_degrees=config.latitude_deg,
        longitude_degrees=config.longitude_deg,
        elevation_m=0.0,
    )
    start = ts.utc(config.year, 1, 1)
    end = ts.utc(config.year + 1, 1, 1)
    rises, rise_ok = almanac.find_risings(
        site, sun, start, end, horizon_degrees=-0.833
    )
    sets, set_ok = almanac.find_settings(
        site, sun, start, end, horizon_degrees=-0.833
    )
    if not np.all(rise_ok) or not np.all(set_ok):
        raise ValueError("Skyfield reported a non-crossing event")
    rise_times = pd.to_datetime(rises.utc_datetime(), utc=True)
    set_times = pd.to_datetime(sets.utc_datetime(), utc=True)
    if len(rise_times) != len(set_times):
        raise ValueError("different number of sunrise and sunset events")

    rise_az = site.at(rises).observe(sun).apparent().altaz()[1].degrees
    set_az = site.at(sets).observe(sun).apparent().altaz()[1].degrees
    return pd.DataFrame(
        {
            "date": rise_times.strftime("%Y-%m-%d"),
            "sunrise_utc": rise_times.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "sunset_utc": set_times.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "daylight_min": (set_times - rise_times).total_seconds() / 60.0,
            "sunrise_azimuth_deg": rise_az,
            "sunset_azimuth_deg": set_az,
        }
    )


def compare_models(spa: pd.DataFrame, skyfield: pd.DataFrame) -> pd.DataFrame:
    merged = spa.merge(skyfield, on="date", suffixes=("_spa", "_jpl"), validate="1:1")
    sunrise_spa = pd.to_datetime(merged["sunrise_utc_spa"], utc=True)
    sunrise_jpl = pd.to_datetime(merged["sunrise_utc_jpl"], utc=True)
    sunset_spa = pd.to_datetime(merged["sunset_utc_spa"], utc=True)
    sunset_jpl = pd.to_datetime(merged["sunset_utc_jpl"], utc=True)
    return pd.DataFrame(
        {
            "date": merged["date"],
            "sunrise_error_min": (sunrise_spa - sunrise_jpl).dt.total_seconds() / 60.0,
            "sunset_error_min": (sunset_spa - sunset_jpl).dt.total_seconds() / 60.0,
            "daylight_error_min": merged["daylight_min_spa"] - merged["daylight_min_jpl"],
            "sunrise_azimuth_error_deg": (
                merged["sunrise_azimuth_deg_spa"] - merged["sunrise_azimuth_deg_jpl"]
            ),
            "sunset_azimuth_error_deg": (
                merged["sunset_azimuth_deg_spa"] - merged["sunset_azimuth_deg_jpl"]
            ),
        }
    )


def run_validation(cache_directory: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    config = ReferenceConfig()
    spa = generate_reference_table(config)
    jpl = generate_skyfield_table(cache_directory, config)
    errors = compare_models(spa, jpl)
    return spa, jpl, errors
