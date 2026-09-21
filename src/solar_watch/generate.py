"""Generate all version-controlled P0 and P1 derived artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .cam import (
    AZIMUTH_CAM,
    DAYLIGHT_CAM,
    export_bearing_fit_coupon,
    export_cam,
    export_constant_radius_coupon,
    mesh_checks,
)
from .model import ReferenceConfig, generate_reference_table
from .validation import compare_models, generate_skyfield_table


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _save_figure(fig: plt.Figure, path: Path) -> None:
    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
        metadata={"Software": "solar-watch 0.1.0", "Creation Time": None},
    )
    plt.close(fig)


def _reference_plot(table: pd.DataFrame, path: Path) -> None:
    dates = pd.to_datetime(table["date"])
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    axes[0].plot(dates, table["daylight_min"] / 60.0, color="#e28f00", lw=2)
    axes[0].set_ylabel("daylight duration (hours)")
    axes[0].grid(alpha=0.25)
    axes[1].plot(dates, table["sunrise_azimuth_deg"], label="sunrise", color="#1464a0")
    axes[1].plot(dates, table["sunset_azimuth_deg"], label="sunset", color="#b14d33")
    axes[1].set_ylabel("azimuth clockwise from north (deg)")
    axes[1].legend()
    axes[1].grid(alpha=0.25)
    fig.suptitle("Solar Watch P0 reference — 42.1° N, ideal horizon, 2025")
    _save_figure(fig, path)


def _validation_plot(errors: pd.DataFrame, path: Path) -> None:
    dates = pd.to_datetime(errors["date"])
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    axes[0].plot(dates, errors["sunrise_error_min"], label="sunrise")
    axes[0].plot(dates, errors["sunset_error_min"], label="sunset")
    axes[0].axhline(0.1, color="red", ls="--", lw=1, label="±0.1 min limit")
    axes[0].axhline(-0.1, color="red", ls="--", lw=1)
    axes[0].set_ylabel("SPA − JPL event time (min)")
    axes[0].legend(ncol=3)
    axes[0].grid(alpha=0.25)
    axes[1].plot(dates, errors["sunrise_azimuth_error_deg"], label="sunrise")
    axes[1].plot(dates, errors["sunset_azimuth_error_deg"], label="sunset")
    axes[1].axhline(0.1, color="red", ls="--", lw=1, label="±0.1° limit")
    axes[1].axhline(-0.1, color="red", ls="--", lw=1)
    axes[1].set_ylabel("SPA − JPL azimuth (deg)")
    axes[1].legend(ncol=3)
    axes[1].grid(alpha=0.25)
    fig.suptitle("Independent validation — NREL SPA vs Skyfield/JPL DE421")
    _save_figure(fig, path)


def _cam_plot(results: list[tuple[object, dict[str, object]]], path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for axis, (spec, result) in zip(axes, results, strict=True):
        outline = result["outline"]
        axis.plot(outline["surface_x_mm"], outline["surface_y_mm"], color="#333333")
        bore = plt.Circle((0, 0), spec.bearing_bore_mm / 2, fill=False, color="#777777")
        axis.add_patch(bore)
        axis.plot([0, 35], [0, 0], color="red", lw=1, label="Jan 1 datum")
        axis.set_aspect("equal")
        axis.set_title(spec.name.replace("_", " "))
        axis.set_xlabel("mm")
        axis.set_ylabel("mm")
        axis.grid(alpha=0.2)
        axis.legend()
    fig.suptitle("P1 roller-compensated printable cam surfaces")
    _save_figure(fig, path)


def refresh_ephemeris(root: Path, cache: Path) -> Path:
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    table = generate_skyfield_table(cache, ReferenceConfig())
    path = data_dir / "skyfield_de421_42p1N_2025.csv"
    table.to_csv(path, index=False, float_format="%.9f")
    return path


def generate_all(root: Path) -> dict[str, object]:
    root = root.resolve()
    data_dir = root / "data"
    plots_dir = root / "artifacts" / "plots"
    printable_dir = root / "printables" / "p1"
    for directory in (data_dir, plots_dir, printable_dir):
        directory.mkdir(parents=True, exist_ok=True)

    config = ReferenceConfig()
    reference = generate_reference_table(config)
    reference_path = data_dir / "reference_42p1N_2025.csv"
    reference.to_csv(reference_path, index=False, float_format="%.9f")
    prescribed_dates = [
        "2025-01-01", "2025-02-01", "2025-03-01", "2025-03-20",
        "2025-04-01", "2025-05-01", "2025-06-01", "2025-06-21",
        "2025-07-01", "2025-08-01", "2025-09-01", "2025-09-22",
        "2025-10-01", "2025-11-01", "2025-12-01", "2025-12-21",
    ]
    test_points = reference[reference["date"].isin(prescribed_dates)].copy()
    test_points["daylight_pitch_radius_mm"] = DAYLIGHT_CAM.pitch_base_mm + (
        test_points[DAYLIGHT_CAM.source_column] - DAYLIGHT_CAM.datum_value
    ) * DAYLIGHT_CAM.scale_mm_per_unit
    test_points["azimuth_pitch_radius_mm"] = AZIMUTH_CAM.pitch_base_mm + (
        test_points[AZIMUTH_CAM.source_column] - AZIMUTH_CAM.datum_value
    ) * AZIMUTH_CAM.scale_mm_per_unit
    test_points_path = data_dir / "p1_test_points_42p1N_2025.csv"
    test_points[
        [
            "date", "day_of_year", "cam_angle_deg", "daylight_min",
            "daylight_pitch_radius_mm", "sunrise_azimuth_deg",
            "azimuth_pitch_radius_mm",
        ]
    ].to_csv(test_points_path, index=False, float_format="%.9f")

    ephemeris_path = data_dir / "skyfield_de421_42p1N_2025.csv"
    if not ephemeris_path.exists():
        raise FileNotFoundError(
            f"{ephemeris_path} missing; run validate-ephemeris once with network access"
        )
    ephemeris = pd.read_csv(ephemeris_path)
    errors = compare_models(reference, ephemeris)
    error_path = data_dir / "validation_errors_42p1N_2025.csv"
    errors.to_csv(error_path, index=False, float_format="%.9f")

    _reference_plot(reference, plots_dir / "p0_reference_42p1N_2025.png")
    _validation_plot(errors, plots_dir / "p0_validation_errors_42p1N_2025.png")

    cam_results = [
        (DAYLIGHT_CAM, export_cam(reference, DAYLIGHT_CAM, printable_dir)),
        (AZIMUTH_CAM, export_cam(reference, AZIMUTH_CAM, printable_dir)),
    ]
    _cam_plot(cam_results, plots_dir / "p1_cam_profiles_42p1N.png")
    runout_mesh = export_constant_radius_coupon(printable_dir)
    fit_mesh = export_bearing_fit_coupon(printable_dir)

    numerical = errors.select_dtypes(include=[np.number]).abs().max().to_dict()
    mesh_summary = {
        spec.name: mesh_checks(result["mesh"]) for spec, result in cam_results
    }
    mesh_summary["constant_radius_runout_revA"] = mesh_checks(runout_mesh)
    mesh_summary["608_bearing_fit_21p9_to_22p3_revA"] = mesh_checks(fit_mesh)
    manifest = {
        "generator": "solar-watch 0.1.0",
        "reference": {
            "latitude_deg": config.latitude_deg,
            "longitude_deg": config.longitude_deg,
            "year": config.year,
            "event_altitude_deg": -0.833,
            "algorithm": "pvlib 0.13.1 NREL SPA",
            "validation": "Skyfield 1.53 with JPL DE421",
            "maximum_absolute_errors": numerical,
        },
        "cams": {
            spec.name: {
                "source_column": spec.source_column,
                "datum_value": spec.datum_value,
                "scale_mm_per_unit": spec.scale_mm_per_unit,
                "pitch_base_mm": spec.pitch_base_mm,
                "roller_radius_mm": spec.roller_radius_mm,
                "thickness_mm": spec.thickness_mm,
                "bearing_bore_mm": spec.bearing_bore_mm,
                "profile_samples": spec.samples,
                "pressure_angle_max_deg": float(result["outline"]["pressure_angle_deg"].max()),
                "pitch_curvature_radius_min_mm": float(
                    result["outline"]["pitch_curvature_radius_mm"].min()
                ),
                "surface_radius_range_mm": [
                    float(result["outline"]["surface_radius_mm"].min()),
                    float(result["outline"]["surface_radius_mm"].max()),
                ],
            }
            for spec, result in cam_results
        },
        "meshes": mesh_summary,
    }
    manifest_path = printable_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    hashes = {}
    for path in sorted(
        [reference_path, ephemeris_path, error_path, test_points_path]
        + list(plots_dir.glob("*.png"))
        + list(printable_dir.glob("*.*"))
    ):
        if path.name != "SHA256SUMS.txt":
            hashes[path.relative_to(root).as_posix()] = _sha256(path)
    sums_path = printable_dir / "SHA256SUMS.txt"
    sums_path.write_text(
        "".join(f"{digest}  {name}\n" for name, digest in hashes.items()),
        encoding="utf-8",
    )
    return manifest
