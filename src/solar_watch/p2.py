"""P2 fixed-latitude mechanism ratios and deterministic kinematic model."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .cam import AZIMUTH_CAM, DAYLIGHT_CAM


TIME_DEG_PER_MIN = 0.5
TIME_INPUT_PITCH_RADIUS_MM = 15.0
TIME_OUTPUT_PITCH_RADIUS_MM = 7.5
AZIMUTH_OUTPUT_PITCH_RADIUS_MM = 40.0
P2_DAYLIGHT_SCALE_MM_PER_MIN = (
    TIME_INPUT_PITCH_RADIUS_MM * math.radians(TIME_DEG_PER_MIN)
)
P2_AZIMUTH_SCALE_MM_PER_DEG = AZIMUTH_OUTPUT_PITCH_RADIUS_MM * math.radians(1.0)


@dataclass(frozen=True)
class P2Envelope:
    width_mm: float = 609.0
    height_mm: float = 900.0
    depth_mm: float = 200.0
    azimuth_dial_diameter_mm: float = 360.0
    time_dial_diameter_mm: float = 240.0


@dataclass(frozen=True)
class P2Ratios:
    daylight_span_ratio: float = 1.0
    azimuth_span_ratio: float = 1.0


def time_dial_angle_deg(minutes: np.ndarray | float) -> np.ndarray:
    """Return 12-hour dial angle clockwise from midnight/noon."""

    return np.mod(np.asarray(minutes, dtype=float) * TIME_DEG_PER_MIN, 360.0)


def sunset_minutes(sunrise_minutes: np.ndarray | float, daylight_minutes: np.ndarray | float) -> np.ndarray:
    """Return sunset on a repeating 12-hour dial in minutes."""

    return np.mod(
        np.asarray(sunrise_minutes, dtype=float) + np.asarray(daylight_minutes, dtype=float),
        720.0,
    )


def time_summer_rack_positions(
    sunrise_minutes: np.ndarray | float,
    daylight_follower_mm: np.ndarray | float,
    ratios: P2Ratios = P2Ratios(),
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return sunrise rack, daylight rack, and differential-carrier positions.

    Opposed racks constrain the free pinion center to their arithmetic mean.
    A 7.5 mm output pinion converts that carrier position back to the sum of
    sunrise and daylight angles.
    """

    sunrise_angle_rad = np.radians(time_dial_angle_deg(sunrise_minutes))
    sunrise_rack = TIME_INPUT_PITCH_RADIUS_MM * sunrise_angle_rad
    daylight_rack = np.asarray(daylight_follower_mm, dtype=float) * ratios.daylight_span_ratio
    carrier = 0.5 * (sunrise_rack + daylight_rack)
    return sunrise_rack, daylight_rack, carrier


def recovered_sunset_angle_deg(carrier_mm: np.ndarray | float, phase_deg: float = 0.0) -> np.ndarray:
    angle = np.degrees(np.asarray(carrier_mm, dtype=float) / TIME_OUTPUT_PITCH_RADIUS_MM)
    return np.mod(angle + phase_deg, 360.0)


def daylight_follower_from_minutes(daylight_minutes: np.ndarray | float) -> np.ndarray:
    """Return the P1/P2 nominal follower pitch displacement relative to datum."""

    return (
        np.asarray(daylight_minutes, dtype=float) - DAYLIGHT_CAM.datum_value
    ) * P2_DAYLIGHT_SCALE_MM_PER_MIN


def azimuth_follower_from_degrees(azimuth_deg: np.ndarray | float) -> np.ndarray:
    return (
        np.asarray(azimuth_deg, dtype=float) - AZIMUTH_CAM.datum_value
    ) * P2_AZIMUTH_SCALE_MM_PER_DEG


def recovered_sunrise_azimuth_deg(
    follower_mm: np.ndarray | float,
    ratios: P2Ratios = P2Ratios(),
    phase_deg: float = AZIMUTH_CAM.datum_value,
) -> np.ndarray:
    rack_mm = np.asarray(follower_mm, dtype=float) * ratios.azimuth_span_ratio
    return np.mod(np.degrees(rack_mm / AZIMUTH_OUTPUT_PITCH_RADIUS_MM) + phase_deg, 360.0)


def mirrored_sunset_azimuth_deg(sunrise_azimuth_deg: np.ndarray | float) -> np.ndarray:
    return np.mod(360.0 - np.asarray(sunrise_azimuth_deg, dtype=float), 360.0)


def dial_tick_spacing_mm(diameter_mm: float, increment_deg: float) -> float:
    return math.pi * diameter_mm * increment_deg / 360.0
