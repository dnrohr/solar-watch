import json
from pathlib import Path

import pandas as pd

from solar_watch.p2_analysis import (
    MechanicalAssumptions,
    clearance_checks,
    deflection_summary,
    error_budget,
    full_year_sweep,
)


ROOT = Path(__file__).resolve().parents[1]


def test_full_year_motion_sweep_is_exact_and_complete() -> None:
    table = pd.read_csv(ROOT / "data" / "reference_42p1N_2025.csv")
    sweep = full_year_sweep(table)
    assert len(sweep) == 365 * 48
    assert sweep["date"].nunique() == 365
    assert sweep["sunrise_setting_min"].nunique() == 48
    assert sweep["time_kinematic_error_deg"].abs().max() < 1e-10
    assert sweep["azimuth_mirror_error_deg"].abs().max() < 0.28


def test_clearance_deflection_and_error_allocations_pass() -> None:
    table = pd.read_csv(ROOT / "data" / "reference_42p1N_2025.csv")
    clearances = clearance_checks(table)
    assert clearances["all_pass"]
    assert clearances["minimum_dial_edge_gap_mm"] >= 20
    assert clearances["guard_to_hand_clearance_mm"] >= 8
    assumptions = MechanicalAssumptions()
    deflections = deflection_summary(assumptions)
    assert deflections["shaft_tip_deflection_mm"] < 0.01
    assert deflections["frame_midspan_deflection_mm"] < 0.10
    budget = error_budget(assumptions)
    assert budget["time_rss_min"] < budget["time_target_min"]
    assert budget["azimuth_rss_deg"] < budget["azimuth_target_deg"]


def test_committed_analysis_matches_acceptance_summary() -> None:
    summary = json.loads(
        (ROOT / "artifacts" / "p2" / "mechanical_analysis_revA.json").read_text()
    )
    assert summary["sweep"]["rows"] == 365 * 48
    assert summary["clearance"]["all_pass"]
    assert summary["error_budget"]["physical_acceptance_pending"]
    committed = pd.read_csv(
        ROOT / "data" / "p2_full_year_motion_sweep_42p1N_2025.csv"
    )
    assert len(committed) == 365 * 48
