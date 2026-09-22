# P0/P1/P2 Verification Matrix

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
| P2-001 shared manual date | keyed common shaft, cam hub/dowel interfaces | Pass by CAD; physical sweep pending |
| P2-002 manual sunrise input | 30-tooth input pinion and direct sunrise hand | Pass by design; physical pending |
| P2-003 sunset arithmetic | full-year x 48 sunrise-setting software sweep | Pass digitally; physical pending |
| P2-004 mirrored azimuth | full-year linkage/mirror test, 1:1 reverser | Pass digitally; physical pending |
| P2-005 module calibration | three removable plates and module procedures | Pass by design inspection |
| P2-006 dial sizes | 240 mm time and 360 mm azimuth DXFs | Pass digitally |
| P2-007 zero/span/phase | ICD adjustment table and range analysis | Pass by design; physical pending |
| P2-008 CNC definition | STEP/DXF/PDF, datum scheme, material/finish/inspection | Pass package inspection |
| P2-009 evidence boundary | design basis, procedure, matrix | Pass |
| P2-010 serviceability | guard-only access and independent plates | Pass by layout; physical review pending |
| P2 travel and kinematics | 17,520-state full-year sweep | Pass digitally; max time arithmetic error 2.3e-13 deg |
| P2 pressure/force/torque | generated cam-load and input-torque summary | Pass analysis; physical torque pending |
| P2 clearance/interference | dial, cam wall, hand, guard, and depth checks | Pass modeled checks; fastener/spring sweep pending |
| P2 deflection | shaft and weak-axis frame beam estimates | Pass allocation; assembled measurement pending |
| P2 error budget | numerical/cam/runout/linkage/backlash/calibration/readability RSS | Pass allocation at 0.768 min / 0.557 deg; physical pending |

Software passing does not convert pending physical acceptance items into claims.
P1 physical validation was deliberately bypassed by Decision 0006. The P2
package is ready for quotation, then coupon manufacture and module-first test.
