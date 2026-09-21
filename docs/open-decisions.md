# Open Decisions

Status: Draft v0.1  
Date: 2026-09-21

This is the decision queue for items that materially affect the design. Each
entry includes a recommended default so work can continue while a response is
pending.

## Resolved decisions

- D-001: The first fixed-latitude prototype will use 42.1 degrees north. See
  [decision record 0001](decisions/0001-p1-latitude.md).

## D-002: Time-reference behavior

**Needed before:** detailed P2 time-module design  
**Recommended default:** manually set sunrise time; calculate sunset by adding
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

## D-003: Date input

**Needed before:** P1 physical design  
**Recommended default:** manual continuous date wheel with month and day labels

A continuous wheel allows sub-day testing and avoids the torque and calendar
complexity of an automatic annual drive. An automatic drive can be added after
the required cam torque is measured.

## D-004: Display orientation

**Needed before:** P2 dial artwork  
**Recommended default:** portrait panel, azimuth dial above two time dials

Landscape and exposed-mechanism layouts remain possible. The mechanism should be
designed as independent modules so the front-panel arrangement does not alter
the mathematics.

## D-005: Maximum depth

**Needed before:** P3 surface-cam packaging  
**Recommended default:** 12 inches during prototyping, with a later reduction
target

Allowing generous initial depth reduces the risk of compressing the mechanism
before its necessary cam travel and follower geometry have been measured.

## D-006: Printer constraints

**Needed before:** designing the first printable test cam  
**Recommended default:** parts fit a 220 by 220 by 250 mm build volume and use
0.4 mm nozzle assumptions

The actual printer, nozzle, material, and comfortable print duration will drive
cam segmentation and tolerances.

## D-007: Visible mechanism

**Needed before:** integrated frame design  
**Recommended default:** expose the cams and transmissions behind a clear guard

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
