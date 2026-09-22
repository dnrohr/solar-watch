"""Reproducible P2 CNC geometry, drawings inputs, and artifact manifest."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import cadquery as cq
from cadquery import exporters
import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import numpy as np
import pandas as pd

from .cam import AZIMUTH_CAM, DAYLIGHT_CAM, CamSpec, cam_outline
from .p2 import (
    P2_AZIMUTH_SCALE_MM_PER_DEG,
    P2_DAYLIGHT_SCALE_MM_PER_MIN,
    P2Envelope,
    P2Ratios,
)


@dataclass(frozen=True)
class P2CadConfig:
    revision: str = "A"
    cam_thickness_mm: float = 10.0
    cam_pilot_diameter_mm: float = 32.0
    cam_bolt_circle_mm: float = 40.0
    cam_fastener_clearance_mm: float = 5.5
    cam_datum_dowel_mm: float = 4.0
    cam_datum_radius_mm: float = 20.0
    cam_datum_angle_deg: float = 60.0
    shaft_diameter_mm: float = 12.0
    plate_thickness_mm: float = 6.0
    guard_thickness_mm: float = 4.5


PARTS = {
    "P2-101": ("daylight_cam", "POM-C", 1),
    "P2-102": ("sunrise_azimuth_cam", "POM-C", 1),
    "P2-103": ("cam_hub", "6061-T6", 2),
    "P2-104": ("cam_module_plate", "6061-T6", 1),
    "P2-105": ("daylight_span_lever", "6061-T6", 1),
    "P2-106": ("azimuth_span_lever", "6061-T6", 1),
    "P2-107": ("time_carrier_plate", "6061-T6", 1),
    "P2-108": ("time_module_plate", "6061-T6", 1),
    "P2-109": ("azimuth_module_plate", "6061-T6", 1),
    "P2-110": ("sunrise_time_shaft", "303 stainless", 1),
    "P2-111": ("sunset_output_shaft", "303 stainless", 1),
    "P2-112": ("azimuth_inner_shaft", "303 stainless", 1),
    "P2-113": ("azimuth_outer_tube", "303 stainless", 1),
    "P2-114": ("front_layout", "reference", 1),
    "P2-115": ("front_guard", "polycarbonate", 1),
    "P2-116": ("time_dial", "2.5 mm anodized aluminum", 2),
    "P2-117": ("azimuth_dial", "2.5 mm anodized aluminum", 1),
    "P2-118": ("time_hand", "5052-H32", 2),
    "P2-119": ("azimuth_hand", "5052-H32", 2),
    "P2-120": ("cam_runout_coupon", "POM-C", 1),
    "P2-121": ("hub_pilot_fit_coupon", "POM-C", 1),
    "P2-122": ("lever_span_gauge", "6061-T6", 1),
    "P2-123": ("common_cam_date_shaft", "303 stainless", 1),
    "P2-124": ("cam_follower_carriage", "6061-T6", 2),
    "P2-125": ("rack_clamp", "6061-T6", 3),
    "P2-126": ("carrier_output_rack_bracket", "6061-T6", 1),
    "P2-127": ("azimuth_gear_bushing", "303 stainless", 1),
    "P2-128": ("date_control_shaft", "303 stainless", 1),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalize_step(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"(FILE_NAME\([^,]+,)'[^']*'",
        r"\1'2000-01-01T00:00:00'",
        text,
        count=1,
    )
    occurrence = 0

    def normalize_occurrence(match: re.Match[str]) -> str:
        nonlocal occurrence
        occurrence += 1
        return f"NEXT_ASSEMBLY_USAGE_OCCURRENCE('{occurrence}'"

    text = re.sub(
        r"NEXT_ASSEMBLY_USAGE_OCCURRENCE\('\d+'",
        normalize_occurrence,
        text,
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def _normalize_dxf(path: Path) -> None:
    doc = ezdxf.readfile(path)
    doc.header["$TDCREATE"] = 2451544.5
    doc.header["$TDUPDATE"] = 2451544.5
    doc.header["$FINGERPRINTGUID"] = "{00000000-0000-0000-0000-000000000001}"
    doc.header["$VERSIONGUID"] = "{00000000-0000-0000-0000-000000000002}"
    doc.saveas(path)
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"(\$VERSIONGUID\s+2\s+)\{[^}]+\}",
        r"\1{00000000-0000-0000-0000-000000000002}",
        text,
        count=1,
    )
    text = re.sub(
        r"(\d+\.\d+\.\d+ @ )[^\r\n]+",
        r"\g<1>2000-01-01T00:00:00+00:00",
        text,
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def _cam_spec(base: CamSpec, config: P2CadConfig) -> CamSpec:
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
        thickness_mm=config.cam_thickness_mm,
        bearing_bore_mm=config.cam_pilot_diameter_mm,
        samples=base.samples,
        revision=config.revision,
    )


def p2_cam(table: pd.DataFrame, spec: CamSpec, config: P2CadConfig) -> tuple[cq.Workplane, pd.DataFrame]:
    outline = cam_outline(table, spec)
    points = [tuple(row) for row in outline[["surface_x_mm", "surface_y_mm"]].to_numpy()]
    solid = cq.Workplane("XY").polyline(points).close().extrude(config.cam_thickness_mm)
    solid = solid.faces(">Z").workplane().hole(config.cam_pilot_diameter_mm)
    solid = (
        solid.faces(">Z")
        .workplane()
        .polarArray(config.cam_bolt_circle_mm / 2.0, 0.0, 360.0, 3)
        .hole(config.cam_fastener_clearance_mm)
    )
    angle = np.radians(config.cam_datum_angle_deg)
    datum_x = config.cam_datum_radius_mm * np.cos(angle)
    datum_y = config.cam_datum_radius_mm * np.sin(angle)
    solid = solid.faces(">Z").workplane().center(float(datum_x), float(datum_y)).hole(config.cam_datum_dowel_mm)
    return solid, outline


def cam_hub(config: P2CadConfig) -> cq.Workplane:
    hub = cq.Workplane("XY").circle(25.0).extrude(8.0)
    hub = hub.faces(">Z").workplane().circle(16.0).extrude(3.0)
    hub = hub.faces(">Z").workplane(offset=-11.0).hole(config.shaft_diameter_mm)
    hub = (
        hub.faces(">Z")
        .workplane(offset=-11.0)
        .polarArray(config.cam_bolt_circle_mm / 2.0, 0.0, 360.0, 3)
        .hole(5.0)
    )
    angle = np.radians(config.cam_datum_angle_deg)
    hub = (
        hub.faces(">Z")
        .workplane(offset=-11.0)
        .center(
            float(config.cam_datum_radius_mm * np.cos(angle)),
            float(config.cam_datum_radius_mm * np.sin(angle)),
        )
        .hole(config.cam_datum_dowel_mm)
    )
    keyway = (
        cq.Workplane("XY")
        .box(4.0, 3.0, 11.0, centered=(True, True, False))
        .translate((0, 5.5, 0))
    )
    return hub.cut(keyway)


def rectangular_plate(width: float, height: float, thickness: float, holes: list[tuple[float, float, float]]) -> cq.Workplane:
    part = cq.Workplane("XY").box(width, height, thickness, centered=(True, True, False))
    for x, y, diameter in holes:
        part = part.faces(">Z").workplane().center(x, y).hole(diameter)
    return part


def cam_module_plate(config: P2CadConfig) -> cq.Workplane:
    holes = [
        (-80, -75, 28.0), (80, 0, 8.0),
        (-165, -155, 6.6), (165, -155, 6.6),
        (-165, 155, 6.6), (165, 155, 6.6),
        (-20, -87, 5.2), (35, -87, 5.2),
        (-20, -63, 5.2), (35, -63, 5.2),
        (35, 63, 5.2), (110, 63, 5.2),
        (35, 87, 5.2), (110, 87, 5.2),
    ]
    return rectangular_plate(360, 340, config.plate_thickness_mm, holes)


def slotted_lever(length: float = 180.0, thickness: float = 6.0) -> cq.Workplane:
    """Symmetric calibration lever with separate radial input/output slots.

    Crosshead pins run in the two slots on opposite sides of the pivot. Moving
    an output guide by +/-1.5 mm about the 75 mm nominal spacing provides just
    over +/-2 percent exact tangent-intersection ratio adjustment.
    """
    lever = cq.Workplane("XY").rect(22.0, length).extrude(thickness)
    lever = lever.edges("|Z").fillet(10.9)
    lever = lever.faces(">Z").workplane().hole(8.0)
    for y in (-48.5, 48.5):
        lever = (
            lever.faces(">Z")
            .workplane()
            .center(0, y)
            .slot2D(67.0, 6.2, 90)
            .cutThruAll()
        )
    return lever


def time_carrier(config: P2CadConfig) -> cq.Workplane:
    plate = cq.Workplane("XY").box(58, 42, config.plate_thickness_mm, centered=(True, True, False))
    plate = plate.faces(">Z").workplane().hole(8.0)
    for x in (-22.0, 22.0):
        plate = plate.faces(">Z").workplane().center(x, 0).hole(5.2)
    return plate


def time_module_plate(config: P2CadConfig) -> cq.Workplane:
    holes = [
        (-150, -75, 6.6), (150, -75, 6.6),
        (-150, 75, 6.6), (150, 75, 6.6),
        (-139.5, 0, 22.0), (139.5, 0, 22.0),
    ]
    for x in (-105, 105):
        holes.extend([(x, -22, 5.2), (x, 22, 5.2)])
    holes.extend([(0, -38, 6.2), (0, 38, 6.2)])
    return rectangular_plate(320, 180, config.plate_thickness_mm, holes)


def azimuth_module_plate(config: P2CadConfig) -> cq.Workplane:
    holes = [(-80, -55, 6.6), (80, -55, 6.6), (-80, 55, 6.6), (80, 55, 6.6), (0, 0, 22.0)]
    return rectangular_plate(190, 130, config.plate_thickness_mm, holes)


def shaft(length: float, diameter: float, shoulder_diameter: float | None = None) -> cq.Workplane:
    result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length)
    if shoulder_diameter:
        result = result.faces(">Z").workplane().circle(shoulder_diameter / 2.0).extrude(3.0)
    return result


def outer_tube(length: float) -> cq.Workplane:
    return cq.Workplane("XY").circle(7.0).circle(4.05).extrude(length)


def guard(config: P2CadConfig) -> cq.Workplane:
    holes = [(-286.5, -431, 6.6), (286.5, -431, 6.6), (-286.5, 431, 6.6), (286.5, 431, 6.6)]
    return rectangular_plate(585, 875, config.guard_thickness_mm, holes)


def hand(length: float, hub_diameter: float, bore_diameter: float, thickness: float = 1.6) -> cq.Workplane:
    body = cq.Workplane("XY").moveTo(0, -4).lineTo(length - 12, -2).lineTo(length, 0).lineTo(length - 12, 2).lineTo(0, 4).close().extrude(thickness)
    hub = cq.Workplane("XY").circle(hub_diameter / 2).extrude(thickness)
    return body.union(hub).faces(">Z").workplane().hole(bore_diameter)


def cam_runout_coupon(config: P2CadConfig) -> cq.Workplane:
    coupon = cq.Workplane("XY").circle(60).extrude(config.cam_thickness_mm)
    coupon = coupon.faces(">Z").workplane().hole(config.cam_pilot_diameter_mm)
    coupon = coupon.faces(">Z").workplane().polarArray(20, 0, 360, 3).hole(5.5)
    angle = np.radians(config.cam_datum_angle_deg)
    return (
        coupon.faces(">Z")
        .workplane()
        .center(
            float(config.cam_datum_radius_mm * np.cos(angle)),
            float(config.cam_datum_radius_mm * np.sin(angle)),
        )
        .hole(4.0)
    )


def hub_pilot_fit_coupon(config: P2CadConfig) -> cq.Workplane:
    coupon = cq.Workplane("XY").box(170, 52, config.cam_thickness_mm, centered=(True, True, False))
    for x, diameter in zip((-60, -20, 20, 60), (31.98, 32.00, 32.02, 32.04), strict=True):
        coupon = coupon.faces(">Z").workplane().center(x, 0).hole(diameter)
    return coupon


def lever_span_gauge(config: P2CadConfig) -> cq.Workplane:
    gauge = cq.Workplane("XY").box(125, 18, config.plate_thickness_mm, centered=(True, True, False))
    for x in (-50, 50):
        gauge = gauge.faces(">Z").workplane().center(x, 0).hole(5.0)
    return gauge


def keyed_date_shaft(length: float = 160.0) -> cq.Workplane:
    shaft_part = cq.Workplane("XY").circle(6.0).extrude(length)
    keyway = cq.Workplane("XY").box(4.0, 3.0, 70.0, centered=(True, True, False)).translate((0, 5.5, 35.0))
    return shaft_part.cut(keyway)


def follower_carriage(config: P2CadConfig) -> cq.Workplane:
    part = cq.Workplane("XY").box(45, 30, 8, centered=(True, True, False))
    part = part.faces(">Z").workplane().center(15, 0).hole(5.0)
    for x in (-12, 12):
        part = part.faces(">Z").workplane().center(x, 0).hole(4.5)
    return part


def rack_clamp(config: P2CadConfig) -> cq.Workplane:
    part = cq.Workplane("XY").box(50, 20, 8, centered=(True, True, False))
    for x in (-18, 18):
        part = part.faces(">Z").workplane().center(x, 0).hole(4.5)
    return part


def carrier_rack_bracket(config: P2CadConfig) -> cq.Workplane:
    part = cq.Workplane("XY").box(80, 25, 8, centered=(True, True, False))
    for x in (-30, -12, 12, 30):
        part = part.faces(">Z").workplane().center(x, 0).hole(4.5)
    return part


def flanged_bushing() -> cq.Workplane:
    part = cq.Workplane("XY").circle(10).extrude(2)
    part = part.faces(">Z").workplane().circle(7.5).extrude(10)
    return part.faces(">Z").workplane(offset=-12).hole(8.0)


def _dxf_polyline(path: Path, points: list[tuple[float, float]], closed: bool = True) -> None:
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = 4
    doc.modelspace().add_lwpolyline(points, close=closed, dxfattribs={"layer": "CUT"})
    doc.saveas(path)
    _normalize_dxf(path)


def _export_part(part: cq.Workplane, output: Path, stem: str, dxf: bool = True) -> list[Path]:
    step = output / f"{stem}.step"
    stl = output / f"{stem}.stl"
    exporters.export(part, str(step))
    exporters.export(part, str(stl), tolerance=0.02, angularTolerance=0.05)
    _normalize_step(step)
    paths = [step, stl]
    if dxf:
        dxf_path = output / f"{stem}.dxf"
        exporters.export(part.faces(">Z"), str(dxf_path))
        _normalize_dxf(dxf_path)
        paths.append(dxf_path)
    return paths


def _dial_dxf(path: Path, diameter: float, major_degrees: float, minor_degrees: float, labels: str) -> None:
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    radius = diameter / 2.0
    msp.add_circle((0, 0), radius, dxfattribs={"layer": "CUT"})
    steps = int(round(360.0 / minor_degrees))
    for index in range(steps):
        angle = np.radians(index * minor_degrees)
        major = abs((index * minor_degrees / major_degrees) - round(index * minor_degrees / major_degrees)) < 1e-8
        inner = radius - (8.0 if major else 4.0)
        p1 = (inner * np.sin(angle), radius * np.cos(angle))
        p2 = (radius * np.sin(angle), radius * np.cos(angle))
        msp.add_line(p1, p2, dxfattribs={"layer": "ENGRAVE"})
    msp.add_text(labels, height=5.0, dxfattribs={"layer": "ENGRAVE"}).set_placement((0, -10))
    msp.add_circle((0, 0), 4.0, dxfattribs={"layer": "CUT"})
    doc.saveas(path)
    _normalize_dxf(path)


def _front_layout_dxf(path: Path, envelope: P2Envelope) -> None:
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    msp.add_lwpolyline([(0, 0), (envelope.width_mm, 0), (envelope.width_mm, envelope.height_mm), (0, envelope.height_mm)], close=True, dxfattribs={"layer": "ENVELOPE"})
    for center, diameter, name in [((304.5, 665), 360, "AZIMUTH"), ((165, 285), 240, "SUNRISE"), ((444, 285), 240, "SUNSET"), ((304.5, 82), 110, "DATE")]:
        msp.add_circle(center, diameter / 2.0, dxfattribs={"layer": "DIAL"})
        msp.add_text(name, height=8.0, dxfattribs={"layer": "TEXT"}).set_placement((center[0], center[1]))
    doc.saveas(path)
    _normalize_dxf(path)


def _assembly(table: pd.DataFrame, config: P2CadConfig) -> cq.Assembly:
    assembly = cq.Assembly(name="P2-000_SOLAR_WATCH")
    dark = cq.Color(0.12, 0.14, 0.16)
    aluminum = cq.Color(0.72, 0.75, 0.78)
    dial = cq.Color(0.93, 0.91, 0.82)
    guard_color = cq.Color(0.75, 0.9, 1.0, 0.25)
    pom = cq.Color(0.1, 0.1, 0.1)
    # Extrusions and crossmembers are envelope/reference geometry, not custom parts.
    for x in (10, 599):
        assembly.add(cq.Workplane("XY").box(20, 900, 40, centered=(True, True, False)).translate((x, 450, 0)), name=f"frame_vertical_{x}", color=dark)
    for y in (10, 890, 440, 135):
        assembly.add(cq.Workplane("XY").box(589, 20, 40, centered=(True, True, False)).translate((304.5, y, 0)), name=f"frame_horizontal_{y}", color=dark)
    assembly.add(cam_module_plate(config).translate((304.5, 450, 35)), name="P2-104_cam_module_plate", color=aluminum)
    assembly.add(time_module_plate(config).translate((304.5, 285, 90)), name="P2-108_time_module_plate", color=aluminum)
    assembly.add(azimuth_module_plate(config).translate((304.5, 665, 90)), name="P2-109_azimuth_module_plate", color=aluminum)
    for base, z, label in ((DAYLIGHT_CAM, 48, "P2-101_daylight_cam"), (AZIMUTH_CAM, 61, "P2-102_azimuth_cam")):
        cam, _ = p2_cam(table, _cam_spec(base, config), config)
        assembly.add(cam.translate((224.5, 375, z)), name=label, color=pom)
    # Mechanism solids below are envelope/interface representations of listed
    # purchased parts. Custom geometry remains in its numbered component STEP.
    steel = cq.Color(0.42, 0.45, 0.48)
    belt_color = cq.Color(0.18, 0.18, 0.20)
    for x, y, diameter, length, label in (
        (224.5, 375, 12, 120, "date_cam_shaft"),
        (304.5, 82, 8, 120, "date_control_shaft"),
        (165, 285, 8, 130, "sunrise_time_shaft"),
        (444, 285, 8, 130, "sunset_time_shaft"),
        (304.5, 665, 8, 150, "azimuth_inner_shaft"),
    ):
        assembly.add(cq.Workplane("XY").circle(diameter / 2).extrude(length).translate((x, y, 35)), name=label, color=steel)
    for x, y, diameter, label in (
        (304.5, 82, 50, "date_input_pulley"),
        (224.5, 375, 50, "date_cam_pulley"),
        (165, 285, 32, "sunrise_30T_gear"),
        (444, 285, 17, "sunset_15T_gear"),
        (304.5, 665, 82, "azimuth_80T_gear"),
    ):
        assembly.add(cq.Workplane("XY").circle(diameter / 2).extrude(10).translate((x, y, 130 if "date" in label else 104)), name=label, color=steel)
    dx, dy = 224.5 - 304.5, 375 - 82
    belt_length = math.hypot(dx, dy)
    belt_angle = math.degrees(math.atan2(dy, dx))
    for offset in (-25.0, 25.0):
        nx, ny = -dy / belt_length, dx / belt_length
        belt = cq.Workplane("XY").box(belt_length, 2.0, 8.0, centered=(True, True, False))
        belt = belt.rotate((0, 0, 0), (0, 0, 1), belt_angle).translate(((304.5+224.5)/2 + nx*offset, (82+375)/2 + ny*offset, 131))
        assembly.add(belt, name=f"date_belt_span_{offset:+g}", color=belt_color)
    for z, label in ((88, "daylight_span_lever"), (100, "azimuth_span_lever")):
        assembly.add(slotted_lever().translate((384.5, 450, z)), name=label, color=aluminum)
    assembly.add(cq.Workplane("XY").box(105, 10, 8, centered=(True, True, False)).translate((218, 305, 104)), name="sunrise_input_rack", color=steel)
    assembly.add(cq.Workplane("XY").box(120, 10, 8, centered=(True, True, False)).translate((337, 325, 104)), name="daylight_input_rack", color=steel)
    assembly.add(cq.Workplane("XY").box(90, 10, 8, centered=(True, True, False)).translate((395, 285, 116)), name="carrier_output_rack", color=steel)
    for x, y, diameter, label in ((304.5, 665, 360, "azimuth_dial"), (165, 285, 240, "sunrise_dial"), (444, 285, 240, "sunset_dial"), (304.5, 82, 110, "date_dial")):
        assembly.add(cq.Workplane("XY").circle(diameter / 2).extrude(2.5).translate((x, y, 154)), name=label, color=dial)
    assembly.add(hand(105, 20, 8).translate((165, 285, 160)), name="sunrise_time_hand", color=steel)
    assembly.add(hand(105, 20, 8).translate((444, 285, 160)), name="sunset_time_hand", color=steel)
    assembly.add(hand(165, 22, 8).translate((304.5, 665, 160)), name="sunrise_azimuth_hand", color=steel)
    assembly.add(hand(165, 22, 8).rotate((0, 0, 0), (0, 0, 1), 180).translate((304.5, 665, 164)), name="sunset_azimuth_hand", color=cq.Color(0.75, 0.25, 0.18))
    assembly.add(guard(config).translate((304.5, 450, 174)), name="P2-115_guard", color=guard_color)
    return assembly


def _layout_plot(path: Path, envelope: P2Envelope) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 8), gridspec_kw={"width_ratios": [1.0, 0.65]})
    front, side = axes
    front.add_patch(Rectangle((0, 0), envelope.width_mm, envelope.height_mm, fill=False, lw=2, color="#17365d"))
    for center, diameter, label in [((304.5, 665), 360, "Azimuth"), ((165, 285), 240, "Sunrise"), ((444, 285), 240, "Sunset"), ((304.5, 82), 110, "Date")]:
        front.add_patch(Circle(center, diameter / 2, fill=False, lw=1.5, color="#d97706"))
        front.text(center[0], center[1], label, ha="center", va="center", fontsize=9)
    front.add_patch(Rectangle((124.5, 280), 360, 340, facecolor="#708090", alpha=0.18, edgecolor="#405060", label="cam module behind dials"))
    front.set(xlim=(-20, 629), ylim=(-20, 920), aspect="equal", xlabel="X (mm)", ylabel="Y (mm)", title="Front datum layout")
    front.grid(alpha=0.15); front.legend(loc="upper right", fontsize=8)
    bands = [(0, 40, "frame"), (35, 41, "module plates"), (48, 82, "cams / hubs"), (88, 125, "rack modules"), (130, 145, "date belt"), (154, 156.5, "dials"), (160, 166, "hands"), (174, 178.5, "guard")]
    for start, end, label in bands:
        side.add_patch(Rectangle((0, start), 1, end-start, facecolor="#17365d" if label != "guard" else "#7ec8e3", alpha=0.65))
        side.text(1.05, (start+end)/2, f"{label}: Z {start:g}-{end:g}", va="center", fontsize=9)
    side.axhline(200, color="#d97706", ls="--", label="200 mm envelope")
    side.set(xlim=(0, 2.5), ylim=(0, 205), xticks=[], ylabel="Z (mm)", title="Controlled depth stack")
    side.legend(loc="upper right", fontsize=8); side.grid(axis="y", alpha=0.15)
    fig.suptitle("Solar Watch P2 Rev A packaging and dial layout — 42.1 deg N")
    fig.tight_layout()
    fig.savefig(path, dpi=180, metadata={"Software": "solar-watch P2", "Creation Time": None})
    plt.close(fig)


def generate_p2_cad(root: Path) -> dict[str, object]:
    root = root.resolve()
    output = root / "cnc" / "p2"
    output.mkdir(parents=True, exist_ok=True)
    for old in output.iterdir():
        if old.is_file() and (
            old.name.startswith("P2-")
            or old.name in {"manifest.json", "SHA256SUMS.txt"}
        ):
            old.unlink()
    config = P2CadConfig()
    table = pd.read_csv(root / "data" / "reference_42p1N_2025.csv")
    files: list[Path] = []

    for base, part_number in ((DAYLIGHT_CAM, "P2-101"), (AZIMUTH_CAM, "P2-102")):
        spec = _cam_spec(base, config)
        part, outline = p2_cam(table, spec, config)
        stem = f"{part_number}_{spec.name}"
        files.extend(_export_part(part, output, stem))
        profile = output / f"{stem}_profile.csv"
        outline.to_csv(profile, index=False, float_format="%.9f")
        files.append(profile)

    solids = {
        "P2-103_cam_hub": cam_hub(config),
        "P2-104_cam_module_plate": cam_module_plate(config),
        "P2-105_daylight_span_lever": slotted_lever(),
        "P2-106_azimuth_span_lever": slotted_lever(),
        "P2-107_time_carrier_plate": time_carrier(config),
        "P2-108_time_module_plate": time_module_plate(config),
        "P2-109_azimuth_module_plate": azimuth_module_plate(config),
        "P2-110_sunrise_time_shaft": shaft(110, 8, 12),
        "P2-111_sunset_output_shaft": shaft(95, 8, 12),
        "P2-112_azimuth_inner_shaft": shaft(150, 8, 12),
        "P2-113_azimuth_outer_tube": outer_tube(130),
        "P2-115_front_guard": guard(config),
        "P2-118_time_hand": hand(105, 20, 8),
        "P2-119_azimuth_hand": hand(165, 22, 8),
        "P2-120_cam_runout_coupon": cam_runout_coupon(config),
        "P2-121_hub_pilot_fit_coupon": hub_pilot_fit_coupon(config),
        "P2-122_lever_span_gauge": lever_span_gauge(config),
        "P2-123_common_cam_date_shaft": keyed_date_shaft(),
        "P2-124_cam_follower_carriage": follower_carriage(config),
        "P2-125_rack_clamp": rack_clamp(config),
        "P2-126_carrier_output_rack_bracket": carrier_rack_bracket(config),
        "P2-127_azimuth_gear_bushing": flanged_bushing(),
        "P2-128_date_control_shaft": shaft(100, 8, 12),
    }
    for stem, solid in solids.items():
        files.extend(_export_part(solid, output, stem))

    layout = output / "P2-114_front_layout.dxf"
    _front_layout_dxf(layout, P2Envelope())
    files.append(layout)
    time_dial = output / "P2-116_time_dial.dxf"
    _dial_dxf(time_dial, 240, 15, 2.5, "12 HOUR / 5 MIN MINOR")
    files.append(time_dial)
    az_dial = output / "P2-117_azimuth_dial.dxf"
    _dial_dxf(az_dial, 360, 15, 5, "AZIMUTH / 5 DEG MINOR")
    files.append(az_dial)
    assembly_path = output / "P2-000_assembly.step"
    _assembly(table, config).save(str(assembly_path))
    _normalize_step(assembly_path)
    files.append(assembly_path)
    plots = root / "artifacts" / "plots"
    plots.mkdir(parents=True, exist_ok=True)
    layout_plot = plots / "p2_layout_revA.png"
    _layout_plot(layout_plot, P2Envelope())

    ratios = P2Ratios()
    manifest = {
        "generator": "solar-watch P2 CAD rev A",
        "units": "mm",
        "latitude_deg": 42.1,
        "config": asdict(config),
        "envelope": asdict(P2Envelope()),
        "ratios": asdict(ratios),
        "parts": {number: {"name": values[0], "material": values[1], "quantity": values[2]} for number, values in PARTS.items()},
        "files": {path.name: _sha256(path) for path in sorted(files)},
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    files.append(manifest_path)
    sums = output / "SHA256SUMS.txt"
    sums.write_text("".join(f"{_sha256(path)}  {path.name}\n" for path in sorted(files)), encoding="utf-8")
    return manifest
