import hashlib
import json
from pathlib import Path

import pandas as pd
import trimesh

from solar_watch.model import generate_reference_table


ROOT = Path(__file__).resolve().parents[1]


def test_committed_reference_is_current() -> None:
    committed = pd.read_csv(ROOT / "data" / "reference_42p1N_2025.csv")
    generated = generate_reference_table()
    assert committed["date"].tolist() == generated["date"].tolist()
    numeric = generated.select_dtypes("number").columns
    assert (committed[numeric] - generated[numeric]).abs().max().max() < 5e-9


def test_all_printable_meshes_are_watertight_and_fit_assumed_bed() -> None:
    for path in sorted((ROOT / "printables" / "p1").glob("*.stl")):
        # STL duplicates triangle vertices by design; processing welds identical
        # coordinates before topology checks, as slicers do on import.
        mesh = trimesh.load_mesh(path, process=True)
        assert mesh.is_watertight, path.name
        assert mesh.is_winding_consistent, path.name
        size = mesh.bounds[1] - mesh.bounds[0]
        assert size[0] <= 220.0 and size[1] <= 220.0 and size[2] <= 250.0, path.name


def test_manifest_records_required_cam_safety_metrics() -> None:
    manifest = json.loads((ROOT / "printables" / "p1" / "manifest.json").read_text())
    assert len(manifest["cams"]) == 2
    for cam in manifest["cams"].values():
        assert cam["pressure_angle_max_deg"] < 30.0
        assert cam["pitch_curvature_radius_min_mm"] > 8.0
        assert cam["surface_radius_range_mm"][0] > 35.0
        assert cam["surface_radius_range_mm"][1] < 92.0
    for mesh in manifest["meshes"].values():
        assert mesh["watertight"]
        assert mesh["winding_consistent"]


def test_test_plan_covers_year_and_seasonal_extrema() -> None:
    points = pd.read_csv(ROOT / "data" / "p1_test_points_42p1N_2025.csv")
    assert len(points) == 16
    assert "2025-01-01" in points["date"].tolist()
    assert "2025-06-21" in points["date"].tolist()
    assert "2025-12-21" in points["date"].tolist()


def test_generated_file_hashes_match() -> None:
    sums = ROOT / "printables" / "p1" / "SHA256SUMS.txt"
    for line in sums.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", maxsplit=1)
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected, relative
