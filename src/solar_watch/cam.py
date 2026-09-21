"""Reproducible P1 translating-roller radial cam geometry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from shapely.geometry import Point, Polygon
import trimesh


@dataclass(frozen=True)
class CamSpec:
    name: str
    source_column: str
    datum_value: float
    scale_mm_per_unit: float
    pitch_base_mm: float = 48.0
    roller_radius_mm: float = 8.0
    thickness_mm: float = 8.0
    bearing_bore_mm: float = 22.2
    samples: int = 2880
    revision: str = "A"


DAYLIGHT_CAM = CamSpec(
    name="daylight_42p1N_revA",
    source_column="daylight_min",
    datum_value=545.0,
    scale_mm_per_unit=0.13,
)

AZIMUTH_CAM = CamSpec(
    name="sunrise_azimuth_42p1N_revA",
    source_column="sunrise_azimuth_deg",
    datum_value=55.0,
    scale_mm_per_unit=0.70,
)


def _periodic_value_spline(table: pd.DataFrame, spec: CamSpec) -> CubicSpline:
    values = table[spec.source_column].to_numpy(dtype=float)
    x = np.arange(len(values) + 1, dtype=float)
    y = np.concatenate([values, values[:1]])
    return CubicSpline(x, y, bc_type="periodic")


def periodic_profile(table: pd.DataFrame, spec: CamSpec) -> Callable[[np.ndarray], np.ndarray]:
    spline = _periodic_value_spline(table, spec)
    period = len(table)

    def pitch(day: np.ndarray) -> np.ndarray:
        value = spline(np.mod(day, period))
        return spec.pitch_base_mm + (value - spec.datum_value) * spec.scale_mm_per_unit

    return pitch


def cam_outline(table: pd.DataFrame, spec: CamSpec) -> pd.DataFrame:
    """Return the roller-compensated cam surface and its pitch curve.

    The pitch curve is the path of the center of an 8 mm radius translating
    roller follower.  The printable cam boundary is its inward normal offset.
    Profile dates increase counter-clockwise in cam-fixed coordinates. With a
    fixed follower on the positive-X ray, rotate the marked face clockwise to
    advance the date.
    """

    count = len(table)
    theta = np.linspace(0.0, 2.0 * np.pi, spec.samples, endpoint=False)
    day = theta * count / (2.0 * np.pi)
    spline = _periodic_value_spline(table, spec)
    angle_to_day = count / (2.0 * np.pi)
    pitch = spec.pitch_base_mm + (spline(day) - spec.datum_value) * spec.scale_mm_per_unit
    dr_dtheta = spline(day, 1) * spec.scale_mm_per_unit * angle_to_day
    d2r_dtheta2 = spline(day, 2) * spec.scale_mm_per_unit * angle_to_day**2
    c, s = np.cos(theta), np.sin(theta)
    pitch_x, pitch_y = pitch * c, pitch * s
    tangent_norm = np.sqrt(pitch * pitch + dr_dtheta * dr_dtheta)
    normal_x = (dr_dtheta * s + pitch * c) / tangent_norm
    normal_y = (-dr_dtheta * c + pitch * s) / tangent_norm
    surface_x = pitch_x - spec.roller_radius_mm * normal_x
    surface_y = pitch_y - spec.roller_radius_mm * normal_y
    pressure_angle_deg = np.degrees(np.arctan2(np.abs(dr_dtheta), pitch))
    dx = dr_dtheta * c - pitch * s
    dy = dr_dtheta * s + pitch * c
    ddx = (d2r_dtheta2 - pitch) * c - 2.0 * dr_dtheta * s
    ddy = (d2r_dtheta2 - pitch) * s + 2.0 * dr_dtheta * c
    curvature = (dx * ddy - dy * ddx) / np.power(dx * dx + dy * dy, 1.5)
    pitch_curvature_radius = np.where(curvature > 0.0, 1.0 / curvature, np.inf)
    return pd.DataFrame(
        {
            "day_coordinate": day,
            "cam_angle_deg": np.degrees(theta),
            "pitch_radius_mm": pitch,
            "surface_x_mm": surface_x,
            "surface_y_mm": surface_y,
            "surface_radius_mm": np.hypot(surface_x, surface_y),
            "pressure_angle_deg": pressure_angle_deg,
            "pitch_curvature_radius_mm": pitch_curvature_radius,
        }
    )


def _circle(center: tuple[float, float], diameter: float, resolution: int = 64) -> Polygon:
    return Point(*center).buffer(diameter / 2.0, resolution=resolution)


def cam_polygon(outline: pd.DataFrame, spec: CamSpec, identifier_count: int) -> Polygon:
    polygon = Polygon(outline[["surface_x_mm", "surface_y_mm"]].to_numpy())
    polygon = polygon.difference(_circle((0.0, 0.0), spec.bearing_bore_mm))
    # Jan 1 datum hole lies on the zero-degree ray.  The asymmetric ID holes
    # distinguish daylight (one) from azimuth (two) even after sanding.
    polygon = polygon.difference(_circle((29.0, 0.0), 3.2))
    for index in range(identifier_count):
        polygon = polygon.difference(_circle((-29.0, -3.0 + index * 6.0), 2.4))
    return polygon


def _export_mesh(polygon: Polygon, height: float, path: Path) -> trimesh.Trimesh:
    mesh = trimesh.creation.extrude_polygon(
        polygon,
        height=height,
        engine="earcut",
    )
    mesh.remove_unreferenced_vertices()
    mesh.export(path)
    return mesh


def export_cam(table: pd.DataFrame, spec: CamSpec, output_directory: Path) -> dict[str, object]:
    output_directory.mkdir(parents=True, exist_ok=True)
    outline = cam_outline(table, spec)
    identifier_count = 1 if spec.source_column == "daylight_min" else 2
    polygon = cam_polygon(outline, spec, identifier_count)
    stl_path = output_directory / f"{spec.name}.stl"
    mesh = _export_mesh(polygon, spec.thickness_mm, stl_path)
    csv_path = output_directory / f"{spec.name}_profile.csv"
    outline.to_csv(csv_path, index=False, float_format="%.9f")
    svg_path = output_directory / f"{spec.name}.svg"
    _export_svg(outline, spec, svg_path)
    return {
        "mesh": mesh,
        "outline": outline,
        "stl_path": stl_path,
        "csv_path": csv_path,
        "svg_path": svg_path,
    }


def _export_svg(outline: pd.DataFrame, spec: CamSpec, path: Path) -> None:
    points = outline[["surface_x_mm", "surface_y_mm"]].to_numpy()
    margin = 5.0
    minimum = points.min(axis=0) - margin
    maximum = points.max(axis=0) + margin
    width, height = maximum - minimum
    coords = " ".join(f"{x:.4f},{-y:.4f}" for x, y in points)
    identifier_count = 1 if spec.source_column == "daylight_min" else 2
    id_circles = "\n".join(
        f'    <circle cx="-29" cy="{3.0 - index * 6.0:.1f}" r="1.2" fill="none" stroke="black" stroke-width="0.20"/>'
        for index in range(identifier_count)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.3f}mm" height="{height:.3f}mm" viewBox="0 0 {width:.3f} {height:.3f}">
  <title>{spec.name}; scale 1 SVG unit = 1 mm</title>
  <g transform="translate({-minimum[0]:.4f},{maximum[1]:.4f})">
    <polygon points="{coords}" fill="none" stroke="black" stroke-width="0.20"/>
    <circle cx="0" cy="0" r="{spec.bearing_bore_mm / 2:.3f}" fill="none" stroke="black" stroke-width="0.20"/>
    <circle cx="29" cy="0" r="1.6" fill="none" stroke="red" stroke-width="0.20"/>
{id_circles}
    <line x1="0" y1="0" x2="35" y2="0" stroke="red" stroke-width="0.20"/>
  </g>
  <text x="3" y="{height - 2:.3f}" font-size="3">{spec.name} | Jan 1 datum = red ray</text>
</svg>'''
    path.write_text(svg, encoding="utf-8")


def export_constant_radius_coupon(output_directory: Path) -> trimesh.Trimesh:
    """Export a 60 mm contact-radius runout coupon using the cam bearing bore."""

    output_directory.mkdir(parents=True, exist_ok=True)
    polygon = _circle((0.0, 0.0), 120.0).difference(_circle((0.0, 0.0), 22.2))
    polygon = polygon.difference(_circle((29.0, 0.0), 3.2))
    return _export_mesh(polygon, 8.0, output_directory / "constant_radius_runout_revA.stl")


def export_bearing_fit_coupon(output_directory: Path) -> trimesh.Trimesh:
    """Export five labeled-in-document 608-bearing bore sizes, 21.9-22.3 mm."""

    output_directory.mkdir(parents=True, exist_ok=True)
    polygon = Polygon([(-70, -17), (70, -17), (70, 17), (-70, 17)])
    diameters = [21.9, 22.0, 22.1, 22.2, 22.3]
    centers = np.linspace(-56, 56, len(diameters))
    for x, diameter in zip(centers, diameters, strict=True):
        polygon = polygon.difference(_circle((float(x), 0.0), diameter))
    return _export_mesh(polygon, 8.0, output_directory / "608_bearing_fit_21p9_to_22p3_revA.stl")


def mesh_checks(mesh: trimesh.Trimesh) -> dict[str, object]:
    return {
        "watertight": bool(mesh.is_watertight),
        "winding_consistent": bool(mesh.is_winding_consistent),
        "volume_mm3": float(mesh.volume),
        "bounds_mm": mesh.bounds.tolist(),
    }
