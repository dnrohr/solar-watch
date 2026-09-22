# Software and Tooling

Status: Implemented for P0/P1/P2

Date: 2026-09-21

## Required now

The host needs only:

- Python 3.12; and
- Git.

`scripts/bootstrap.ps1` creates `.venv` in the checkout and installs the pinned
free Python dependencies from `requirements-lock.txt`. Nothing is installed
system-wide.

## P0/P1 implementation

| Task | Tool |
|---|---|
| NREL SPA reference | pvlib 0.13.1 |
| Independent ephemeris validation | Skyfield 1.53 + JPL DE421 |
| Arrays/tables/interpolation | NumPy 2.2.6, pandas 2.3.2, SciPy (pvlib dependency) |
| Plots | Matplotlib 3.10.6 |
| Reproducible mesh generation | Shapely 2.1.1, trimesh 4.8.1, mapbox-earcut 1.0.3 |
| Automated verification | pytest 8.4.2 |

## P2 additions

P2 uses CadQuery 2.6.1 and its pinned open-source OCP stack to produce STEP and
STL, plus ezdxf 1.4.2 for machinist-facing DXF files. These install only in the
project-local `.venv`; no system-wide CAD installation is required.

`python -m solar_watch.cli generate-p2 --root .` regenerates the 28 custom
parts, top-level assembly STEP, profiles, layout plot, manifest, and hashes.
`scripts/build_p2_pdfs.py` uses ReportLab from the Codex bundled document
runtime to generate the three release PDFs. Poppler renders every PDF page for
visual QA. A non-Codex user may install the open-source `reportlab`, `pypdf`,
and `pdfplumber` packages in a separate project-local environment if rebuilding
PDFs; the CNC geometry and software verification do not require them.

STEP and DXF writers may vary non-geometric headers between processes. Release
SHA-256 files identify the exact reviewed deliverables. The clean verifier
regenerates P2 in a temporary directory and compares STL/profile bytes, DXF
model-space entities, assembly STEP solid count/volume/bounds, the full motion
sweep, and the analysis JSON. Thus regeneration checks geometry and engineering
content without mistaking volatile interchange metadata for a design change.

The committed STL files are generated directly from the compensated follower
geometry in `src/solar_watch/cam.py`. No desktop CAD installation is required to
reproduce P1.

## Proposed free toolchain

The exact CAD route should be selected after the numerical model and first cam
representation are understood. The current preference is:

| Task | Preferred free option | Notes |
|---|---|---|
| Reference calculation | Python | Already installed |
| Numerical arrays and analysis | NumPy/SciPy | Python packages; install only when the model begins |
| Plots and diagnostic figures | Matplotlib | Python package |
| Parametric solid CAD | FreeCAD | Useful for assemblies, shafts, frames, and drawings |
| Scripted mechanical CAD | CadQuery | Good candidate for reproducible generated solids |
| Direct mesh generation | Python plus a mesh library | Useful for mathematical cam surfaces |
| Slicing | OrcaSlicer or PrusaSlicer | Choose whichever matches the available printer workflow |
| Source control | Git | Already installed |

OpenSCAD remains an alternative for simple parametric parts, but complex smooth
surface cams and assemblies are likely to be easier to manage with CadQuery,
FreeCAD, or direct mesh generation.

## Installation policy

- Do not install software merely because it might become useful.
- Keep the mathematical model independent of a proprietary CAD package.
- Generate derived geometry from version-controlled scripts.
- Record tool versions once they begin affecting output files.
- Prefer file formats that can be regenerated over manually repaired meshes.

## Later phases

A slicer is required to print but is intentionally not selected until the
printer is known. FreeCAD remains a possible later assembly-CAD tool, but P1
does not require it. Any future desktop or system-wide installation must be
discussed before it is required.
