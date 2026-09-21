# Provisional System Architecture

Status: Draft v0.1  
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

### P0: Numerical model

No mechanism. Produces verified tables and error sweeps.

### P1: Fixed-latitude cam bench

- Fixed at 42.1 degrees north
- Manually rotated date input
- One-dimensional daylight and azimuth cams
- Direct measurement scales instead of finished dials

Purpose: measure printed cam accuracy, follower behavior, backlash, and useful
mechanical scale.

### P2: Fixed-latitude display

- Three display dials
- Mirrored azimuth output
- Manual sunrise setting
- Time-summing mechanism

Purpose: validate the complete information architecture and dial readability.

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
| Daylight output | Linear follower displacement | P1 test |
| Azimuth output | Linear follower displacement | P1 test |
| Time indication | 12-hour rotary dial | P2 design |
| Azimuth indication | 360-degree rotary dial | P2 design |

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
