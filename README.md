# Solar Watch

The repository contains the digitally validated P0 solar reference, the P1
fixed-latitude cam bench, and the Rev-A CNC-ready P2 fixed-latitude display for
42.1 degrees north. P2 is ready for quotation and physical coupon/module tests;
its fabrication-dependent accuracy is not yet claimed.

## P2 release package

- `output/pdf/solar_watch_p2_design_dossier_revA.pdf` — design basis,
  validation evidence, interfaces, verification matrix, and risks;
- `output/pdf/solar_watch_p2_custom_part_drawings_revA.pdf` — 28 controlled
  custom-part sheets;
- `output/pdf/solar_watch_p2_procurement_test_revA.pdf` — BOM, RFQ, assembly,
  calibration, and acceptance procedure;
- `cnc/p2/` — STEP, DXF, STL preview, cam profile CSV, assembly STEP, manifest,
  and SHA-256 list;
- `src/solar_watch/p2.py` and `src/solar_watch/p2_cad.py` — kinematic and CAD
  sources.

Run `scripts/bootstrap.ps1`, then `scripts/regenerate.ps1` and
`scripts/verify.ps1`. PDF generation additionally uses the free ReportLab
runtime documented in `docs/software-tooling.md`.

Solar Watch is a large-format mechanical astronomical display. Its
three solar indications show:

- sunrise time;
- sunset time; and
- sunrise and sunset azimuth on one 360-degree dial.

The target demonstrator occupies no more than a 36 by 24 inch frontal area and
accepts latitude and date as astronomical inputs. A conventional clock movement
may later provide local time independently.

The P0 numerical reference, P1 cam package, and P2 CNC design are complete in
software for 42.1 degrees north. Decision 0006 records the user's choice to
bypass P1 fabrication. The next action is to quote and machine the P2 coupons,
then release production parts only after those coupons pass.

## Start here

- [Project brief](docs/project-brief.md)
- [Requirements](docs/requirements.md)
- [Conventions](docs/conventions.md)
- [Provisional architecture](docs/architecture.md)
- [Risk register](docs/risk-register.md)
- [Software and tooling](docs/software-tooling.md)
- [Open decisions](docs/open-decisions.md)
- [P0 numerical validation](docs/p0-validation.md)
- [P1 cam package](docs/p1-cam-package.md)
- [P1 bill of materials](docs/bom.md)
- [Print and test procedure](docs/print-test-procedure.md)
- [P2 design basis](docs/p2-design-basis.md)
- [P2 interface control](docs/p2-interface-control.md)
- [P2 mechanical analysis](docs/p2-mechanical-analysis.md)
- [P2 bill of materials](docs/p2-bom.md)
- [P2 RFQ](docs/p2-rfq.md)
- [P2 vendor shortlist and budget](docs/p2-vendor-budget.md)
- [P2 manufacture and test](docs/p2-manufacturing-test.md)

## Reproduce and verify P0/P1/P2

The toolchain is free and project-local. From PowerShell with Python 3.12:

```powershell
.\scripts\bootstrap.ps1
.\scripts\verify.ps1
```

Generated reference data lives in `data/`, diagnostic plots in
`artifacts/plots/`, print-ready P1 files in `printables/p1/`, and CNC P2 files in
`cnc/p2/`.
Normal verification is offline; refreshing the independent JPL DE421 fixture is
an explicit separate command documented in the P0 report.

Documents marked **Provisional** contain assumptions that may change after the
first design review.
