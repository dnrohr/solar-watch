"""Mechanical analysis and full-year digital verification for P2."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .cam import AZIMUTH_CAM, DAYLIGHT_CAM, CamSpec, cam_outline
from .p2 import (
    AZIMUTH_OUTPUT_PITCH_RADIUS_MM,
    P2_AZIMUTH_SCALE_MM_PER_DEG,
    P2_DAYLIGHT_SCALE_MM_PER_MIN,
    P2Envelope,
    TIME_INPUT_PITCH_RADIUS_MM,
    TIME_OUTPUT_PITCH_RADIUS_MM,
    azimuth_follower_from_degrees,
    daylight_follower_from_minutes,
    mirrored_sunset_azimuth_deg,
    recovered_sunrise_azimuth_deg,
    recovered_sunset_angle_deg,
    sunset_minutes,
    time_dial_angle_deg,
    time_summer_rack_positions,
)


@dataclass(frozen=True)
class MechanicalAssumptions:
    cam_preload_max_n: float = 3.0
    rack_preload_n: float = 2.0
    shaft_diameter_mm: float = 8.0
    shaft_cantilever_mm: float = 25.0
    stainless_modulus_n_per_mm2: float = 193_000.0
    frame_span_mm: float = 569.0
    frame_weak_axis_i_mm4: float = 12_133.0
    aluminum_modulus_n_per_mm2: float = 69_000.0
    frame_point_load_n: float = 10.0
    residual_rack_lost_motion_mm: float = 0.020
    residual_miter_lost_motion_mm: float = 0.030
    miter_pitch_radius_mm: float = 10.0


def p2_cam_spec(base: CamSpec) -> CamSpec:
    scale = (
        P2_DAYLIGHT_SCALE_MM_PER_MIN
        if base.source_column == "daylight_min"
        else P2_AZIMUTH_SCALE_MM_PER_DEG
    )
    return CamSpec(
        name=base.name.replace("revA", "p2_revA"),
        source_column=base.source_column,
        datum_value=base.datum_value,
        scale_mm_per_unit=scale,
        pitch_base_mm=base.pitch_base_mm,
        roller_radius_mm=base.roller_radius_mm,
        thickness_mm=10.0,
        bearing_bore_mm=32.0,
        samples=base.samples,
    )


def cam_load_summary(table: pd.DataFrame, base: CamSpec, assumptions: MechanicalAssumptions) -> dict[str, float]:
    outline = cam_outline(table, p2_cam_spec(base))
    angle = np.radians(outline["cam_angle_deg"].to_numpy())
    pitch = outline["pitch_radius_mm"].to_numpy()
    dr_dtheta = np.gradient(pitch, angle, edge_order=2)
    torque = assumptions.cam_preload_max_n * np.abs(dr_dtheta)
    tangent_force = assumptions.cam_preload_max_n * np.tan(
        np.radians(outline["pressure_angle_deg"].to_numpy())
    )
    return {
        "pitch_radius_min_mm": float(pitch.min()),
        "pitch_radius_max_mm": float(pitch.max()),
        "surface_radius_min_mm": float(outline["surface_radius_mm"].min()),
        "surface_radius_max_mm": float(outline["surface_radius_mm"].max()),
        "pressure_angle_max_deg": float(outline["pressure_angle_deg"].max()),
        "pitch_curvature_radius_min_mm": float(outline["pitch_curvature_radius_mm"].min()),
        "cam_torque_max_nmm": float(torque.max()),
        "follower_tangent_force_max_n": float(tangent_force.max()),
    }


def deflection_summary(assumptions: MechanicalAssumptions) -> dict[str, float]:
    diameter = assumptions.shaft_diameter_mm
    inertia = math.pi * diameter**4 / 64.0
    shaft = (
        assumptions.cam_preload_max_n
        * assumptions.shaft_cantilever_mm**3
        / (3.0 * assumptions.stainless_modulus_n_per_mm2 * inertia)
    )
    frame = (
        assumptions.frame_point_load_n
        * assumptions.frame_span_mm**3
        / (
            48.0
            * assumptions.aluminum_modulus_n_per_mm2
            * assumptions.frame_weak_axis_i_mm4
        )
    )
    return {"shaft_tip_deflection_mm": shaft, "frame_midspan_deflection_mm": frame}


def force_and_torque_summary(
    daylight_cam: dict[str, float],
    azimuth_cam: dict[str, float],
    assumptions: MechanicalAssumptions,
) -> dict[str, float]:
    date_nominal = (
        daylight_cam["cam_torque_max_nmm"]
        + azimuth_cam["cam_torque_max_nmm"]
        + 40.0
    )
    date_design = 250.0
    sunrise_design = (
        assumptions.cam_preload_max_n + assumptions.rack_preload_n
    ) * TIME_INPUT_PITCH_RADIUS_MM
    return {
        "date_nominal_worst_case_nmm": date_nominal,
        "date_design_torque_nmm": date_design,
        "date_hand_force_at_50mm_radius_n": date_design / 50.0,
        "sunrise_input_design_torque_nmm": sunrise_design,
        "sunrise_hand_force_at_40mm_radius_n": sunrise_design / 40.0,
        "maximum_rack_force_n": assumptions.cam_preload_max_n + assumptions.rack_preload_n,
        "safety_factor_on_date_torque": date_design / date_nominal,
    }


def error_budget(assumptions: MechanicalAssumptions) -> dict[str, object]:
    time_terms = {
        "numerical_reference_min": 0.0022,
        "cam_profile_0p05mm_min": 0.05 / P2_DAYLIGHT_SCALE_MM_PER_MIN,
        "hub_runout_0p025mm_min": 0.025 / P2_DAYLIGHT_SCALE_MM_PER_MIN,
        "follower_0p02mm_min": 0.02 / P2_DAYLIGHT_SCALE_MM_PER_MIN,
        "preloaded_rack_lost_motion_min": math.degrees(
            assumptions.residual_rack_lost_motion_mm / TIME_OUTPUT_PITCH_RADIUS_MM
        ) / 0.5,
        "calibration_residual_min": 0.20,
        "readability_min": 0.50,
    }
    az_terms = {
        "numerical_reference_deg": 0.00013,
        "cam_profile_0p05mm_deg": 0.05 / P2_AZIMUTH_SCALE_MM_PER_DEG,
        "hub_runout_0p025mm_deg": 0.025 / P2_AZIMUTH_SCALE_MM_PER_DEG,
        "follower_0p02mm_deg": 0.02 / P2_AZIMUTH_SCALE_MM_PER_DEG,
        "spur_lost_motion_deg": math.degrees(
            assumptions.residual_rack_lost_motion_mm / AZIMUTH_OUTPUT_PITCH_RADIUS_MM
        ),
        "miter_lost_motion_deg": math.degrees(
            assumptions.residual_miter_lost_motion_mm / assumptions.miter_pitch_radius_mm
        ),
        "calibration_residual_deg": 0.15,
        "readability_deg": 0.50,
    }
    time_rss = math.sqrt(sum(value**2 for value in time_terms.values()))
    az_rss = math.sqrt(sum(value**2 for value in az_terms.values()))
    return {
        "time_terms": time_terms,
        "time_rss_min": time_rss,
        "time_target_min": 1.0,
        "azimuth_terms": az_terms,
        "azimuth_rss_deg": az_rss,
        "azimuth_target_deg": 1.0,
        "physical_acceptance_pending": True,
    }


def clearance_checks(table: pd.DataFrame) -> dict[str, object]:
    envelope = P2Envelope()
    dials = [
        (304.5, 665.0, 180.0, "azimuth"),
        (165.0, 285.0, 120.0, "sunrise"),
        (444.0, 285.0, 120.0, "sunset"),
        (304.5, 82.0, 55.0, "date"),
    ]
    dial_inside = all(
        radius <= x <= envelope.width_mm - radius
        and radius <= y <= envelope.height_mm - radius
        for x, y, radius, _ in dials
    )
    gaps: dict[str, float] = {}
    for index, first in enumerate(dials):
        for second in dials[index + 1:]:
            distance = math.hypot(first[0] - second[0], first[1] - second[1])
            gaps[f"{first[3]}_to_{second[3]}_mm"] = distance - first[2] - second[2]
    cam_clearances = {}
    for base in (DAYLIGHT_CAM, AZIMUTH_CAM):
        outline = cam_outline(table, p2_cam_spec(base))
        cam_clearances[base.source_column] = float(
            outline["surface_radius_mm"].min() - 16.0
        )
    results = {
        "dials_inside_envelope": dial_inside,
        "minimum_dial_edge_gap_mm": min(gaps.values()),
        "dial_edge_gaps_mm": gaps,
        "guard_to_hand_clearance_mm": 174.0 - 166.0,
        "depth_margin_mm": envelope.depth_mm - 178.5,
        "cam_profile_to_pilot_radial_clearance_mm": cam_clearances,
        "time_hand_tip_margin_mm": 120.0 - 105.0,
        "azimuth_hand_tip_margin_mm": 180.0 - 165.0,
    }
    results["all_pass"] = bool(
        dial_inside
        and min(gaps.values()) >= 20.0
        and results["guard_to_hand_clearance_mm"] >= 8.0
        and results["depth_margin_mm"] >= 20.0
        and min(cam_clearances.values()) >= 10.0
    )
    return results


def full_year_sweep(table: pd.DataFrame) -> pd.DataFrame:
    rows = []
    daylight = table["daylight_min"].to_numpy(dtype=float)
    daylight_follower = daylight_follower_from_minutes(daylight)
    sunrise_azimuth = table["sunrise_azimuth_deg"].to_numpy(dtype=float)
    az_follower = azimuth_follower_from_degrees(sunrise_azimuth)
    recovered_az = recovered_sunrise_azimuth_deg(az_follower)
    mirror = mirrored_sunset_azimuth_deg(recovered_az)
    for sunrise in np.arange(0.0, 720.0, 15.0):
        sunrise_rack, daylight_rack, carrier = time_summer_rack_positions(
            sunrise, daylight_follower
        )
        actual_sunset = recovered_sunset_angle_deg(
            carrier, phase_deg=0.5 * DAYLIGHT_CAM.datum_value
        )
        expected_sunset = time_dial_angle_deg(sunset_minutes(sunrise, daylight))
        time_error = (actual_sunset - expected_sunset + 180.0) % 360.0 - 180.0
        az_error = (mirror - table["sunset_azimuth_deg"].to_numpy() + 180.0) % 360.0 - 180.0
        for index in range(len(table)):
            rows.append(
                {
                    "date": table.iloc[index]["date"],
                    "sunrise_setting_min": sunrise,
                    "daylight_min": daylight[index],
                    "sunrise_rack_mm": float(sunrise_rack),
                    "daylight_rack_mm": daylight_rack[index],
                    "carrier_output_rack_mm": carrier[index],
                    "expected_sunset_angle_deg": expected_sunset[index],
                    "actual_sunset_angle_deg": actual_sunset[index],
                    "time_kinematic_error_deg": time_error[index],
                    "sunrise_azimuth_deg": recovered_az[index],
                    "sunset_azimuth_deg": mirror[index],
                    "azimuth_mirror_error_deg": az_error[index],
                }
            )
    return pd.DataFrame(rows)


def generate_p2_analysis(root: Path) -> dict[str, object]:
    root = root.resolve()
    table = pd.read_csv(root / "data" / "reference_42p1N_2025.csv")
    assumptions = MechanicalAssumptions()
    sweep = full_year_sweep(table)
    data_path = root / "data" / "p2_full_year_motion_sweep_42p1N_2025.csv"
    sweep.to_csv(data_path, index=False, float_format="%.9f")
    daylight_load = cam_load_summary(table, DAYLIGHT_CAM, assumptions)
    azimuth_load = cam_load_summary(table, AZIMUTH_CAM, assumptions)
    summary = {
        "assumptions": asdict(assumptions),
        "daylight_cam": daylight_load,
        "azimuth_cam": azimuth_load,
        "force_and_torque": force_and_torque_summary(
            daylight_load, azimuth_load, assumptions
        ),
        "travel": {
            "sunrise_rack_mm": [float(sweep["sunrise_rack_mm"].min()), float(sweep["sunrise_rack_mm"].max())],
            "daylight_rack_mm": [float(sweep["daylight_rack_mm"].min()), float(sweep["daylight_rack_mm"].max())],
            "carrier_output_rack_mm": [float(sweep["carrier_output_rack_mm"].min()), float(sweep["carrier_output_rack_mm"].max())],
            "azimuth_rack_mm": [float(azimuth_follower_from_degrees(table["sunrise_azimuth_deg"]).min()), float(azimuth_follower_from_degrees(table["sunrise_azimuth_deg"]).max())],
        },
        "deflection": deflection_summary(assumptions),
        "error_budget": error_budget(assumptions),
        "clearance": clearance_checks(table),
        "sweep": {
            "rows": len(sweep),
            "date_count": int(sweep["date"].nunique()),
            "sunrise_setting_count": int(sweep["sunrise_setting_min"].nunique()),
            "maximum_time_kinematic_error_deg": float(sweep["time_kinematic_error_deg"].abs().max()),
            "maximum_azimuth_mirror_error_deg": float(sweep["azimuth_mirror_error_deg"].abs().max()),
        },
    }
    analysis_dir = root / "artifacts" / "p2"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    summary_path = analysis_dir / "mechanical_analysis_revA.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    dates = pd.to_datetime(table["date"])
    axes[0, 0].plot(dates, daylight_follower_from_minutes(table["daylight_min"]), color="#d97706")
    axes[0, 0].set_title("Daylight rack travel")
    axes[0, 0].set_ylabel("mm from datum")
    axes[0, 1].plot(dates, azimuth_follower_from_degrees(table["sunrise_azimuth_deg"]), color="#17365d")
    axes[0, 1].set_title("Azimuth rack travel")
    axes[0, 1].set_ylabel("mm from datum")
    budget = summary["error_budget"]
    axes[1, 0].bar(["RSS", "target"], [budget["time_rss_min"], budget["time_target_min"]], color=["#17365d", "#d97706"])
    axes[1, 0].set_title("Time error allocation")
    axes[1, 0].set_ylabel("minutes")
    axes[1, 1].bar(["RSS", "target"], [budget["azimuth_rss_deg"], budget["azimuth_target_deg"]], color=["#17365d", "#d97706"])
    axes[1, 1].set_title("Azimuth error allocation")
    axes[1, 1].set_ylabel("degrees")
    for axis in axes.flat:
        axis.grid(alpha=0.2)
    fig.suptitle("Solar Watch P2 digital mechanical verification — 42.1 deg N")
    fig.tight_layout()
    fig.savefig(analysis_dir / "p2_mechanical_verification_revA.png", dpi=180, metadata={"Software": "solar-watch P2", "Creation Time": None})
    plt.close(fig)
    return summary
