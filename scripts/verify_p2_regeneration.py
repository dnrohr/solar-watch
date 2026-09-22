"""Semantically compare a clean temporary P2 regeneration with the release."""

from __future__ import annotations

import json
import math
from pathlib import Path
import shutil
import tempfile

import cadquery as cq
import ezdxf

from solar_watch.p2_analysis import generate_p2_analysis
from solar_watch.p2_cad import generate_p2_cad


ROOT = Path(__file__).resolve().parents[1]


def _clean_value(value):
    if isinstance(value, float):
        return round(value, 9)
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if hasattr(value, "x") and hasattr(value, "y"):
        return [round(float(value.x), 9), round(float(value.y), 9), round(float(getattr(value, "z", 0.0)), 9)]
    if isinstance(value, (list, tuple)):
        return [_clean_value(item) for item in value]
    return str(value)


def _dxf_signature(path: Path) -> list[tuple[str, str]]:
    ignored = {"handle", "owner", "paperspace"}
    signature = []
    for entity in ezdxf.readfile(path).modelspace():
        attrs = {
            key: _clean_value(value)
            for key, value in entity.dxfattribs().items()
            if key not in ignored
        }
        if entity.dxftype() == "LWPOLYLINE":
            attrs["points"] = [
                [round(float(value), 9) for value in point]
                for point in entity.get_points("xyseb")
            ]
        signature.append((entity.dxftype(), json.dumps(attrs, sort_keys=True)))
    return sorted(signature)


def _step_signature(path: Path) -> tuple[int, float, tuple[float, ...]]:
    shape = cq.importers.importStep(str(path)).val()
    box = shape.BoundingBox()
    bounds = (box.xmin, box.ymin, box.zmin, box.xmax, box.ymax, box.zmax)
    return (
        len(shape.Solids()),
        round(float(shape.Volume()), 5),
        tuple(round(float(value), 5) for value in bounds),
    )


def main() -> None:
    release = ROOT / "cnc" / "p2"
    release_manifest = json.loads((release / "manifest.json").read_text())
    with tempfile.TemporaryDirectory(prefix="solar-watch-p2-verify-") as temp_name:
        temp = Path(temp_name)
        (temp / "data").mkdir(parents=True)
        shutil.copy2(
            ROOT / "data" / "reference_42p1N_2025.csv",
            temp / "data" / "reference_42p1N_2025.csv",
        )
        generated_manifest = generate_p2_cad(temp)
        generate_p2_analysis(temp)
        generated = temp / "cnc" / "p2"

        for key in ("generator", "units", "latitude_deg", "config", "envelope", "ratios", "parts"):
            assert generated_manifest[key] == release_manifest[key], key

        release_names = {path.name for path in release.iterdir() if path.is_file()}
        generated_names = {path.name for path in generated.iterdir() if path.is_file()}
        assert release_names == generated_names

        for path in sorted(release.glob("*.stl")):
            assert path.read_bytes() == (generated / path.name).read_bytes(), path.name
        for path in sorted(release.glob("*.csv")):
            assert path.read_bytes() == (generated / path.name).read_bytes(), path.name
        for path in sorted(release.glob("*.dxf")):
            assert _dxf_signature(path) == _dxf_signature(generated / path.name), path.name

        release_assembly = _step_signature(release / "P2-000_assembly.step")
        generated_assembly = _step_signature(generated / "P2-000_assembly.step")
        assert release_assembly == generated_assembly

        assert (
            ROOT / "data" / "p2_full_year_motion_sweep_42p1N_2025.csv"
        ).read_bytes() == (
            temp / "data" / "p2_full_year_motion_sweep_42p1N_2025.csv"
        ).read_bytes()
        release_analysis = json.loads(
            (ROOT / "artifacts" / "p2" / "mechanical_analysis_revA.json").read_text()
        )
        generated_analysis = json.loads(
            (temp / "artifacts" / "p2" / "mechanical_analysis_revA.json").read_text()
        )
        assert release_analysis == generated_analysis

    print("P2 clean regeneration matches released geometry and analysis")


if __name__ == "__main__":
    main()
