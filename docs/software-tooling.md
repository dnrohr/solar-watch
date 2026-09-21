# Software and Tooling

Status: Draft v0.1  
Date: 2026-09-21

## Required now

No additional software installation is required for the specification phase.
The development computer already has:

- Python 3.12
- Git

A plain text editor is sufficient to review the current Markdown documents.

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

## Expected near-term installation

The first likely additions are Python packages installed into a project-local
virtual environment. No installation is needed until work starts on the
reference model. A slicer and CAD application are not required until a physical
test part is ready.

FreeCAD is the leading desktop-CAD recommendation for this project, but that
choice is not yet binding. The printer model, build volume, and the user's
preferred CAD interaction style should be known first.
