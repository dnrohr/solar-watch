# Open Decisions

Status: Draft v0.1  
Date: 2026-09-21

This is the decision queue for items that materially affect the design. Each
entry includes a recommended default so work can continue while a response is
pending.

## Resolved decisions

- D-001: The first fixed-latitude prototype will use 42.1 degrees north. See
  [decision record 0001](decisions/0001-p1-latitude.md).
- D-003 (P1 portion): use a manual continuous 365-day wheel, advancing clockwise
  by 360/365 degrees per day. Automatic drive and leap-year behavior remain open.
- P0 algorithm and calendar: see [decision record 0002](decisions/0002-p0-reference.md).
- P1 cam/follower geometry: see [decision record 0003](decisions/0003-p1-cam-geometry.md).
- P2 architecture and layout: see [decision record 0004](decisions/0004-p2-architecture.md).
- P2 CNC materials and datums: see [decision record 0005](decisions/0005-p2-cnc-strategy.md).
- P1 physical-test bypass: see [decision record 0006](decisions/0006-p1-test-bypass.md).

## D-002: Time-reference behavior (resolved for P2)

**P2 decision:** manually set sunrise time; calculate sunset by adding
daylight duration

Alternatives considered:

- manually set sunrise and calculate sunset;
- manually set solar noon and calculate both event times symmetrically;
- calculate apparent-solar times around 12:00;
- calculate full civil times using longitude, equation of time, time zone, and
  daylight-saving corrections; or
- manually set both event-time hands, leaving only azimuth calculated.

The recommended option best isolates the latitude/date computation while still
demonstrating a meaningful mechanical time calculation.

## D-003: Date input (automatic-drive remainder)

**Needed before:** an annual automatic drive after P1

**P1 decision:** manual continuous 365-day date input

A continuous wheel allows sub-day testing and avoids the torque and calendar
complexity of an automatic annual drive. An automatic drive can be added after
the required cam torque is measured.

## D-004: Display orientation (resolved for P2)

**P2 decision:** portrait `609 x 900 mm` panel, azimuth dial above two time
dials. Functional scales are designed in P2; decorative artwork remains later.

Landscape and exposed-mechanism layouts remain possible. The mechanism should be
designed as independent modules so the front-panel arrangement does not alter
the mathematics.

## D-005: Maximum depth (resolved for P2)

**P2 decision:** `200 mm` overall target and limit. P3 packaging will reopen the
decision because its surface cams differ.

Allowing generous initial depth reduces the risk of compressing the mechanism
before its necessary cam travel and follower geometry have been measured.

## D-006: Printer constraints (superseded for P2 precision parts)

**P2 decision:** computational and precision transmission parts are specified
for CNC manufacture. P1 print files remain available as test artifacts.

Revision A was generated on the recommended assumption while numerical and
mechanical work proceeded. The one-piece cams need roughly a 135 mm square
footprint before brim. The actual printer, usable build volume, nozzle, material,
and layer height must be recorded before slicing; a smaller bed or different
nozzle may require revision B.

## D-007: Visible mechanism (resolved for P2)

**P2 decision:** expose cams and transmissions behind a removable clear
polycarbonate guard.

The mechanism is central to the object's appeal and makes calibration and fault
finding easier. A concealed mechanism could make the finished object resemble a
more conventional clock but would reduce its explanatory value.

## D-008: Hemisphere labeling

**Needed before:** variable-latitude input design  
**Recommended default:** one signed latitude scale from 60 S through 60 N

This keeps the mathematical convention visible. A separate hemisphere selector
could make the scale larger but introduces another setting that can be wrong.

## Decision-record format

Once resolved, significant decisions move to `docs/decisions/` using a short
record containing:

- context;
- selected approach;
- alternatives considered;
- consequences; and
- date of decision.
