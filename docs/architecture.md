# Provisional System Architecture

Status: P2 Rev A
Date: 2026-09-21

## Functional decomposition

```text
Calendar input ─┬─> solar-geometry function ─> sunrise azimuth ─> sunrise hand
                │                                      └───────> mirrored sunset hand
Latitude input ─┘

Calendar input ─┬─> daylight function ─> daylight-duration displacement ─┐
Latitude input ─┘                                                         │
                                                                          v
Manual sunrise-time input ─────────────────────────────────────────> time summer
                                                                          │
                                                                          v
                                                                  sunset-time hand
```

The local-time clock, if installed, is an independent module.

## Computational degrees of freedom

The ideal-horizon mechanism needs to generate only two independent astronomical
outputs:

1. sunrise azimuth; and
2. daylight duration.

Sunset azimuth is obtained by reflection around the north-south meridian.
Sunset time is obtained by adding daylight duration to an established sunrise
time. This reduction is central to keeping the printed mechanism achievable.

## Proposed final modules

### A. Input module

- Manually positioned annual date shaft
- Latitude carriage covering -60 through +60 degrees
- Manually positioned sunrise-time shaft
- Setting scales and positive locks

### B. Astronomical cam module

- One two-input cam surface for daylight duration
- One two-input cam surface for sunrise azimuth
- Shared latitude carriage
- Spring-preloaded roller followers
- Replaceable and individually adjustable output couplings

The leading candidate is a pair of cylindrical surface cams. Circumferential
position represents date, axial follower position represents latitude, and cam
radius or groove displacement represents the result.

### C. Time module

- Converts daylight-cam displacement into angular time displacement
- Adds that displacement to the manually established sunrise indication
- Drives the sunset-time hand
- Provides independent zero and span calibration

The first implementation may use a linear cable or belt summer. A printed bevel
or planetary differential should be introduced only after required ranges and
torques have been measured.

### D. Azimuth module

- Converts azimuth-cam displacement into sunrise-hand rotation
- Produces equal and opposite sunset-hand movement
- Provides independent zero and span calibration

The sunrise and sunset hands may be coaxial if a sufficiently stiff concentric
shaft can be fabricated. Separate nearby axes are an acceptable prototype
fallback.

### E. Display and frame

- Sunrise-time dial
- Sunset-time dial
- Combined 360-degree azimuth dial
- Date and latitude setting scales
- Structural backplane
- Protective guards over pinch points and exposed cams
- Optional independent local-time clock

## Prototype sequence

### P0: Numerical model — digitally complete

No mechanism. Produces verified tables and error sweeps. NREL SPA is validated
for every 2025 day at 42.1 degrees north against Skyfield/JPL DE421.

### P1: Fixed-latitude cam bench — print package complete, physical test pending

- Fixed at 42.1 degrees north
- Manually rotated date input
- One-dimensional daylight and azimuth cams
- Direct measurement scales instead of finished dials

Purpose: measure printed cam accuracy, follower behavior, backlash, and useful
mechanical scale.

### P2: Fixed-latitude display — digitally complete, physical build pending

- Three display dials
- Mirrored azimuth output
- Manual sunrise setting
- Time-summing mechanism

Purpose: validate the complete information architecture and dial readability.

P2 detailed design freezes a 609 x 900 x 200 mm portrait assembly. Two 10 mm
POM-C radial cams share a keyed 12 mm manual date shaft. The daylight output and
manual sunrise setting enter an opposed-rack translating-pinion summer; its
carrier position is one half the linear sum and a 7.5 mm output pitch radius
restores the full angular sum. The sunrise azimuth output drives an 80-tooth
pinion and a preloaded 1:1 miter reverser drives the concentric sunset hand.
Independent zero, span, and phase adjustments are accessible behind the guard.

See `p2-design-basis.md`, `p2-interface-control.md`, and Decision 0004.

### P3: Variable-latitude cam bench

- Two surface cams
- Shared latitude carriage
- Temporary direct scales

Purpose: isolate and validate the main two-variable mechanism.

### P4: Integrated demonstrator

- Variable latitude
- Three solar dials
- Finished controls and calibration features
- Optional independent local-time movement

## Interfaces requiring measurement before detailed design

| Interface | Provisional representation | Must be established by |
|---|---|---|
| Date input | 360 degrees per selected reference year | P0/P1 design |
| Latitude input | Linear carriage position | P3 design |
| Daylight output | 0.1308997 mm/min, 16 mm roller | P2 CAD; physical acceptance pending |
| Azimuth output | 0.6981317 mm/degree, 16 mm roller | P2 CAD; physical acceptance pending |
| Time indication | 240 mm 12-hour dial, 5-minute divisions | P2 DXF |
| Azimuth indication | 360 mm combined dial, 5-degree divisions | P2 DXF |

## Design rules

- Every precision output receives zero adjustment.
- Span adjustment is preferred where cam scale or linkage ratio may vary.
- Followers remain preloaded through their complete operating domain.
- Printed holes do not serve directly as precision bearings.
- Modules can be tested separately before installation in the frame.
- Cam geometry is generated from source data and is never edited manually as an
  unexplained mesh.
- Generated files record the model version and input parameters used to create
  them.
