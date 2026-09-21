# Solar Watch

Solar Watch is a large-format, 3D-printable mechanical astronomical display. Its
three solar indications show:

- sunrise time;
- sunset time; and
- sunrise and sunset azimuth on one 360-degree dial.

The target demonstrator occupies no more than a 36 by 24 inch frontal area and
accepts latitude and date as astronomical inputs. A conventional clock movement
may later provide local time independently.

The P0 numerical reference and P1 fixed-latitude cam package are complete in
software for 42.1 degrees north. The next project action is to print and measure
the P1 coupons and cams before any variable-latitude or P2 work begins.

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

## Reproduce and verify P0/P1

The toolchain is free and project-local. From PowerShell with Python 3.12:

```powershell
.\scripts\bootstrap.ps1
.\scripts\verify.ps1
```

Generated reference data lives in `data/`, diagnostic plots in
`artifacts/plots/`, and print-ready STL/SVG/profile files in `printables/p1/`.
Normal verification is offline; refreshing the independent JPL DE421 fixture is
an explicit separate command documented in the P0 report.

Documents marked **Provisional** contain assumptions that may change after the
first design review.
