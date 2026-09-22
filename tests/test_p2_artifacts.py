import hashlib
import json
from pathlib import Path

import ezdxf
import pandas as pd
import trimesh

from solar_watch.cam import AZIMUTH_CAM, DAYLIGHT_CAM, CamSpec, cam_outline
from solar_watch.p2 import P2_AZIMUTH_SCALE_MM_PER_DEG, P2_DAYLIGHT_SCALE_MM_PER_MIN

ROOT = Path(__file__).resolve().parents[1]
P2 = ROOT / "cnc" / "p2"


def test_p2_manifest_and_hashes_are_complete() -> None:
    manifest = json.loads((P2 / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["latitude_deg"] == 42.1
    assert len(manifest["parts"]) == 28
    assert manifest["envelope"]["width_mm"] <= 24 * 25.4
    assert manifest["envelope"]["height_mm"] <= 36 * 25.4
    for name, expected in manifest["files"].items():
        assert hashlib.sha256((P2 / name).read_bytes()).hexdigest() == expected
    for line in (P2 / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", maxsplit=1)
        assert hashlib.sha256((P2 / name).read_bytes()).hexdigest() == expected


def test_all_p2_preview_meshes_are_watertight_and_metric_scale() -> None:
    paths = sorted(P2.glob("*.stl"))
    assert len(paths) == 25
    for path in paths:
        mesh = trimesh.load_mesh(path, process=True)
        assert mesh.is_watertight, path.name
        assert mesh.is_winding_consistent, path.name
        assert mesh.volume > 0, path.name
        assert (mesh.bounds[1] - mesh.bounds[0]).max() <= 900, path.name


def test_cam_profiles_retain_safety_metrics_and_full_year() -> None:
    paths = sorted(P2.glob("P2-10[12]*profile.csv"))
    assert len(paths) == 2
    for path in paths:
        profile = pd.read_csv(path)
        assert len(profile) == 2880
        assert profile["day_coordinate"].min() == 0
        assert profile["day_coordinate"].max() < 365
        assert profile["pressure_angle_deg"].max() < 30
        assert profile["pitch_curvature_radius_mm"].min() > 8


def test_committed_p2_cam_profiles_equal_source_geometry() -> None:
    table = pd.read_csv(ROOT / "data" / "reference_42p1N_2025.csv")
    for base, pattern in (
        (DAYLIGHT_CAM, "P2-101*profile.csv"),
        (AZIMUTH_CAM, "P2-102*profile.csv"),
    ):
        scale = (
            P2_DAYLIGHT_SCALE_MM_PER_MIN
            if base.source_column == "daylight_min"
            else P2_AZIMUTH_SCALE_MM_PER_DEG
        )
        spec = CamSpec(
            name=base.name,
            source_column=base.source_column,
            datum_value=base.datum_value,
            scale_mm_per_unit=scale,
            pitch_base_mm=base.pitch_base_mm,
            roller_radius_mm=base.roller_radius_mm,
            thickness_mm=10.0,
            bearing_bore_mm=32.0,
            samples=base.samples,
        )
        generated = cam_outline(table, spec)
        committed = pd.read_csv(next(P2.glob(pattern)))
        columns = [
            "day_coordinate", "cam_angle_deg", "pitch_radius_mm",
            "surface_x_mm", "surface_y_mm", "surface_radius_mm",
            "pressure_angle_deg", "pitch_curvature_radius_mm",
        ]
        assert (committed[columns] - generated[columns]).abs().max().max() < 5e-9


def test_functional_dials_have_required_tick_entities() -> None:
    time_entities = list(ezdxf.readfile(P2 / "P2-116_time_dial.dxf").modelspace())
    az_entities = list(ezdxf.readfile(P2 / "P2-117_azimuth_dial.dxf").modelspace())
    assert sum(entity.dxftype() == "LINE" for entity in time_entities) == 144
    assert sum(entity.dxftype() == "LINE" for entity in az_entities) == 72
    assert any(entity.dxftype() == "CIRCLE" for entity in time_entities)
    assert any(entity.dxftype() == "CIRCLE" for entity in az_entities)


def test_every_custom_part_has_manufacturing_geometry() -> None:
    for number in range(101, 129):
        part = f"P2-{number}"
        if number == 114:
            assert list(P2.glob(f"{part}*.dxf"))
        elif number in (116, 117):
            assert list(P2.glob(f"{part}*.dxf"))
        else:
            assert list(P2.glob(f"{part}*.step")), part
            assert list(P2.glob(f"{part}*.dxf")), part
