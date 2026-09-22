# Requirements

Status: Draft v0.2
Date: 2026-09-21

The words **shall**, **should**, and **may** distinguish required behavior,
preferred behavior, and optional behavior. Requirements labeled `TBD` are not
approved until their associated open decision is resolved.

## Functional requirements

| ID | Requirement | Verification |
|---|---|---|
| FUN-001 | The system shall indicate sunrise time. | Inspection and reference comparison |
| FUN-002 | The system shall indicate sunset time. | Inspection and reference comparison |
| FUN-003 | The system shall indicate sunrise azimuth on a 360-degree compass scale. | Inspection and reference comparison |
| FUN-004 | The system shall indicate sunset azimuth on the same compass scale. | Inspection and reference comparison |
| FUN-005 | The final demonstrator shall accept latitude from 60 degrees south through 60 degrees north. | Full-range test |
| FUN-006 | The system shall accept a seasonal or calendar-date input. | Inspection and annual sweep |
| FUN-007 | The sunset-azimuth indication may be mechanically mirrored from the sunrise-azimuth indication. | Analysis and comparison |
| FUN-008 | The initial system shall permit manual positioning of the date input. | Demonstration |
| FUN-009 | The first cam prototype shall use one fixed latitude. | Design inspection |
| FUN-010 | An independent conventional movement may indicate current local time. | Optional inspection |

## Astronomical requirements

| ID | Requirement | Verification |
|---|---|---|
| AST-001 | Reference sunrise and sunset shall use an apparent solar-center altitude of -0.833 degrees unless subsequently revised. | Model inspection |
| AST-002 | Azimuth shall be measured clockwise from true north. | Model and dial inspection |
| AST-003 | Latitude shall be positive north and negative south. | Model tests |
| AST-004 | The reference model shall distinguish calendar date from solar declination. | Model inspection |
| AST-005 | The model shall report when an input is outside the supported domain rather than silently extrapolating. | Automated boundary test |
| AST-006 | Ideal-horizon sunrise and sunset azimuths may be treated as mirror images if the introduced error remains below the azimuth error allocation. | Numerical sweep |

## Accuracy requirements

| ID | Requirement | Verification |
|---|---|---|
| ACC-001 | The numerical reference model shall differ from the selected validation ephemeris by no more than 0.1 minute in event time within the supported domain. | Automated comparison |
| ACC-002 | The numerical reference model shall differ from the selected validation ephemeris by no more than 0.1 degree in azimuth within the supported domain. | Automated comparison |
| ACC-003 | The integrated mechanism should indicate event time within one minute of the reference model. | Calibrated grid test |
| ACC-004 | The integrated mechanism shall indicate event azimuth within one degree of the reference model. | Calibrated grid test |
| ACC-005 | Repeat measurements made after approaching a setting from the prescribed direction should agree within one minute and one degree. | Repeatability test |
| ACC-006 | Backlash and hysteresis shall be measured separately from absolute calibration error. | Bidirectional test |
| ACC-007 | The time dials should provide markings at intervals of no more than five minutes. | Inspection |
| ACC-008 | The azimuth dial should provide markings at intervals of no more than five degrees. | Inspection |

`ACC-003` is initially a design target rather than a release claim. It will be
reclassified after the first physical cam tests establish the achievable error
budget for printed parts.

## Mechanical requirements

| ID | Requirement | Verification |
|---|---|---|
| MEC-001 | The integrated display shall fit within a 36 by 24 inch frontal envelope. | Measurement |
| MEC-002 | The P2 mechanism shall not exceed 200 mm overall depth. P3 shall revisit this limit. | CAD envelope and measurement |
| MEC-003 | Major printed assemblies shall be segmentable for the available printer build volume. | CAD inspection |
| MEC-004 | Cam followers shall be positively preloaded by a spring, gravity, or equivalent method. | Inspection |
| MEC-005 | Output indications shall provide an accessible zero or calibration adjustment. | Inspection |
| MEC-006 | Rotating load-bearing elements should use replaceable metal shafts and bearings or bushings. | BOM and inspection |
| MEC-007 | Failure or removal of the optional local-time clock shall not disable the solar computation. | Demonstration |
| MEC-008 | User-adjustable mechanisms shall include end stops where motion outside the supported domain could cause damage. | Inspection and boundary test |
| MEC-009 | The date and latitude controls shall display their current settings. | Inspection |

## Fabrication requirements

| ID | Requirement | Verification |
|---|---|---|
| FAB-001 | P1 prototype parts shall remain manufacturable using consumer 3D printing. P2 precision computational parts may use CNC manufacture under Decision 0005. | File and drawing inspection |
| FAB-002 | Purchased components should be commonly available metric hardware where practical. | BOM review |
| FAB-003 | Parts that determine calibration shall include identifying marks and revision identifiers. | Inspection |
| FAB-004 | Printed cam surfaces shall permit finishing without changing their datum references. | Process trial |
| FAB-005 | The design shall not require printed shafts running directly in printed structural holes for precision outputs. | CAD inspection |

## Service and documentation requirements

| ID | Requirement | Verification |
|---|---|---|
| DOC-001 | Each physical build shall have a unique identifier. | Build record inspection |
| DOC-002 | Each physical build shall record material, printer, slicer settings, and part revisions. | Build record inspection |
| DOC-003 | Reference data and printable cam geometry shall be reproducible from version-controlled source files. | Clean regeneration test |
| DOC-004 | Assembly and calibration shall be possible without modifying source CAD. | Procedure trial |
| DOC-005 | Major design decisions shall record context, alternatives, and rationale. | Decision-log review |

## P2 fixed-latitude requirements

| ID | Requirement | Verification |
|---|---|---|
| P2-001 | One manual date input shall phase both fixed-latitude cams through one 365-day cycle. | Annual motion sweep |
| P2-002 | The sunrise-time input shall directly establish the sunrise indication without altering astronomical cam outputs. | Kinematic analysis and test |
| P2-003 | The sunset indication shall equal sunrise time plus daylight duration modulo 12 hours. | Full-year and input-grid sweep |
| P2-004 | Sunrise and sunset azimuth hands shall be concentric and equal/opposite about the north-south meridian. | Kinematic sweep |
| P2-005 | Daylight, time-summing, and azimuth modules shall be independently inspectable and calibratable. | Drawing and procedure inspection |
| P2-006 | The functional azimuth dial shall be at least 360 mm diameter and the time dials at least 240 mm diameter. | Drawing inspection |
| P2-007 | P2 shall provide independent zero, span, and date-phase adjustments without modifying source CAD. | Adjustment-range analysis |
| P2-008 | Custom CNC parts shall define datums, material, finish, critical tolerances, and inspection requirements on drawings. | Drawing review |
| P2-009 | The design shall distinguish digitally verified performance from fabrication-dependent acceptance evidence. | Verification matrix review |
| P2-010 | No single module shall require removal of another calibrated module for routine adjustment or inspection. | Assembly/service review |
