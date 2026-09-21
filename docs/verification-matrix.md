# P0/P1 Verification Matrix

| Requirement / deliverable | Evidence | Status |
|---|---|---|
| AST-001..004 conventions | `model.py`, `conventions.md`, P0 report | Pass by inspection/tests |
| AST-005 domain reporting | latitude and calendar boundary tests | Pass |
| AST-006 azimuth symmetry | 365-day mirror-error column; max 0.277 deg | Pass for P1 allocation |
| ACC-001 event time ≤0.1 min | NREL SPA vs JPL DE421 full-year test; max 0.002153 min | Pass |
| ACC-002 azimuth ≤0.1 deg | same full-year test; max 0.000121 deg | Pass |
| ACC-003 one-minute mechanism | physical P1 measurements | Pending physical test; design target only |
| ACC-004 one-degree mechanism | physical P1 measurements | Pending physical test |
| ACC-005/006 repeatability/hysteresis | bidirectional print/test procedure | Pending physical test |
| MEC-003 segmentation | one-piece ~135 mm footprint; documented revision path | Pass for assumed 220 mm bed; printer confirmation pending |
| MEC-004 positive preload | 1..3 N spring follower assumption and BOM | Pass by design; physical inspection pending |
| MEC-005 accessible adjustment | indicator zero, affine span, shaft phase adjustments | Pass by design; physical inspection pending |
| MEC-006/FAB-005 replaceable bearing/shaft | 608 bearing and 8 mm metal shaft | Pass by design; physical inspection pending |
| FAB-001 consumer printing | watertight STL, ≤135 mm bounding boxes, no support | Digitally pass; physical print pending |
| FAB-003 identification | filenames, datum/ID hole patterns, revision, manifest | Pass |
| FAB-004 finish preserves datums | separate center bearing and internal datum hole; procedure | Pass by design |
| DOC-001/002 build traceability | build-record template | Pass for package; build record pending print |
| DOC-003 reproducibility | generator, pinned environment, offline verify script | Pass |
| DOC-004 calibration without CAD edits | coupon/zero/span/phase procedure | Pass by design |
| DOC-005 decision records | decisions 0001..0003 | Pass |

Software passing does not convert pending physical acceptance items into claims.
The package is ready for the user to print and test; P1 physical validation is
the next gate.
