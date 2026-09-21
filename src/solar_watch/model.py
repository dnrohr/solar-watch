"""Authoritative P0 solar-event calculations.

The production reference uses pvlib's Python implementation of the NREL Solar
Position Algorithm (SPA).  Event time is the topocentric solar-center crossing
of -0.8333 degrees used by SPA; this differs from the project convention of
-0.833 degrees by far less than the allocated 0.1 minute / 0.1 degree.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import math

import numpy as np
import pandas as pd
from pvlib import solarposition


SUPPORTED_LATITUDE_DEG = (-60.0, 60.0)
REFERENCE_ALTITUDE_DEG = -0.833
SPA_EVENT_ALTITUDE_DEG = -0.8333


@dataclass(frozen=True)
class ReferenceConfig:
    latitude_deg: float = 42.1
    longitude_deg: float = 0.0
    year: int = 2025

    def validate(self) -> None:
        low, high = SUPPORTED_LATITUDE_DEG
        if not low <= self.latitude_deg <= high:
            raise ValueError(
                f"latitude {self.latitude_deg} outside supported [{low}, {high}] deg"
            )
        if not 1 <= self.year <= 9998:
            raise ValueError("year must permit generation of this and the following year")


def _daily_index(year: int) -> pd.DatetimeIndex:
    return pd.date_range(
        f"{year}-01-01",
        f"{year + 1}-01-01",
        inclusive="left",
        freq="D",
        tz="UTC",
    )


def _refine_event_times(
    estimates: pd.DatetimeIndex,
    latitude_deg: float,
    longitude_deg: float,
    rising: bool,
) -> pd.DatetimeIndex:
    """Refine SPA's -0.8333-degree estimates to exactly -0.833 degrees."""

    low = estimates - pd.Timedelta(minutes=2)
    high = estimates + pd.Timedelta(minutes=2)
    for _ in range(20):
        middle_ns = (low.asi8 + high.asi8) // 2
        middle = pd.DatetimeIndex(middle_ns, tz="UTC")
        elevation = solarposition.spa_python(
            middle,
            latitude_deg,
            longitude_deg,
            altitude=0.0,
            pressure=0.0,
            delta_t=None,
        )["elevation"].to_numpy()
        below = elevation < REFERENCE_ALTITUDE_DEG
        if rising:
            low = pd.DatetimeIndex(np.where(below, middle.asi8, low.asi8), tz="UTC")
            high = pd.DatetimeIndex(np.where(below, high.asi8, middle.asi8), tz="UTC")
        else:
            low = pd.DatetimeIndex(np.where(below, low.asi8, middle.asi8), tz="UTC")
            high = pd.DatetimeIndex(np.where(below, middle.asi8, high.asi8), tz="UTC")
    return pd.DatetimeIndex((low.asi8 + high.asi8) // 2, tz="UTC")


def generate_reference_table(config: ReferenceConfig = ReferenceConfig()) -> pd.DataFrame:
    """Return one row per date using NREL SPA at an ideal sea-level horizon.

    Longitude is retained to make event timestamps auditable, but daylight
    duration and event azimuths are independent of the arbitrary longitude used
    for this fixed-latitude cam.
    """

    config.validate()
    days = _daily_index(config.year)
    events = solarposition.sun_rise_set_transit_spa(
        days,
        latitude=config.latitude_deg,
        longitude=config.longitude_deg,
        delta_t=None,
    )
    if events[["sunrise", "sunset"]].isna().any().any():
        raise ValueError("sunrise or sunset does not exist inside the supported domain")

    sunrise = _refine_event_times(
        pd.DatetimeIndex(events["sunrise"]),
        config.latitude_deg,
        config.longitude_deg,
        rising=True,
    )
    sunset = _refine_event_times(
        pd.DatetimeIndex(events["sunset"]),
        config.latitude_deg,
        config.longitude_deg,
        rising=False,
    )
    sunrise_pos = solarposition.spa_python(
        sunrise,
        config.latitude_deg,
        config.longitude_deg,
        altitude=0.0,
        pressure=0.0,
        delta_t=None,
    )
    sunset_pos = solarposition.spa_python(
        sunset,
        config.latitude_deg,
        config.longitude_deg,
        altitude=0.0,
        pressure=0.0,
        delta_t=None,
    )

    daylight_min = (sunset - sunrise).total_seconds() / 60.0
    sunrise_min_utc = (
        sunrise.hour * 60
        + sunrise.minute
        + sunrise.second / 60.0
        + sunrise.microsecond / 60_000_000.0
    )
    sunset_min_utc = (
        sunset.hour * 60
        + sunset.minute
        + sunset.second / 60.0
        + sunset.microsecond / 60_000_000.0
    )
    sunrise_az = sunrise_pos["azimuth"].to_numpy()
    sunset_az = sunset_pos["azimuth"].to_numpy()

    table = pd.DataFrame(
        {
            "date": days.date.astype(str),
            "day_of_year": days.dayofyear,
            "cam_angle_deg": np.arange(len(days), dtype=float) * 360.0 / len(days),
            "sunrise_utc": sunrise.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "sunset_utc": sunset.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "sunrise_min_utc": sunrise_min_utc,
            "sunset_min_utc": sunset_min_utc,
            "daylight_min": daylight_min,
            "sunrise_azimuth_deg": sunrise_az,
            "sunset_azimuth_deg": sunset_az,
            "azimuth_mirror_error_deg": sunset_az - (360.0 - sunrise_az),
        }
    )
    return table


def analytical_event_geometry(
    latitude_deg: float, declination_deg: float, altitude_deg: float = REFERENCE_ALTITUDE_DEG
) -> tuple[float, float]:
    """Return daylight minutes and sunrise azimuth from the frozen equations.

    This function is a transparent unit-testable statement of the relationships
    in ``docs/conventions.md``.  The annual reference table uses SPA because
    declination changes slightly between sunrise and sunset.
    """

    if not SUPPORTED_LATITUDE_DEG[0] <= latitude_deg <= SUPPORTED_LATITUDE_DEG[1]:
        raise ValueError("latitude outside supported domain")
    phi = math.radians(latitude_deg)
    delta = math.radians(declination_deg)
    h0 = math.radians(altitude_deg)
    hour_arg = (math.sin(h0) - math.sin(phi) * math.sin(delta)) / (
        math.cos(phi) * math.cos(delta)
    )
    if not -1.0 <= hour_arg <= 1.0:
        raise ValueError("no sunrise/sunset for supplied geometry")
    h0_deg = math.degrees(math.acos(hour_arg))
    daylight_min = 8.0 * h0_deg
    az_arg = (math.sin(delta) - math.sin(phi) * math.sin(h0)) / (
        math.cos(phi) * math.cos(h0)
    )
    sunrise_azimuth_deg = math.degrees(math.acos(max(-1.0, min(1.0, az_arg))))
    return daylight_min, sunrise_azimuth_deg


def validate_calendar_date(value: date, year: int) -> None:
    if value.year != year:
        raise ValueError(f"date {value.isoformat()} is outside reference year {year}")
