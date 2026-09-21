# Mathematical and Display Conventions

Status: Draft v0.1  
Date: 2026-09-21

This document prevents sign, time, and coordinate conventions from drifting
between the numerical model, CAD generator, mechanism, and dial artwork.

## Supported domain

- Latitude: `-60 deg <= phi <= +60 deg`
- Date: one complete Gregorian calendar year
- Horizon: ideal, unobstructed astronomical horizon
- Observer elevation: initially zero metres

## Coordinates

- Latitude `phi` is positive north and negative south.
- Azimuth is measured clockwise from true north.
- North is 0 degrees.
- East is 90 degrees.
- South is 180 degrees.
- West is 270 degrees.
- Angles are calculated internally in radians and presented in degrees.

## Sunrise and sunset

Initial reference events occur when the apparent altitude of the Sun's center is
`h0 = -0.833 degrees`. This conventional value approximates atmospheric
refraction and the apparent solar radius near the horizon.

The physical mechanism represents a standardized astronomical result, not the
moment at which the Sun becomes visible over local terrain, buildings, or a
variable atmosphere.

## Time

Three time systems must not be conflated:

1. **Apparent solar time:** the Sun crosses the local meridian at 12:00.
2. **Mean solar time:** corrected for the equation of time.
3. **Civil time:** includes longitude within a time zone, UTC offset, and
   potentially daylight-saving rules.

The initial mechanical architecture uses a manually established event-time
reference and mechanically adds calculated daylight duration. This avoids
claiming that latitude and date alone determine civil sunrise and sunset.

Times in software shall be stored as minutes from the relevant midnight or as an
explicit timestamp. Display formatting shall not be used as an internal unit.

## Primary quantities

- `delta`: solar declination
- `H0`: sunrise/sunset hour-angle magnitude
- `D`: daylight duration
- `Ar`: sunrise azimuth
- `As`: sunset azimuth
- `Tr`: sunrise time indication
- `Ts`: sunset time indication

The initial analytical relationships are:

```text
cos(H0) = (sin(h0) - sin(phi) sin(delta))
          / (cos(phi) cos(delta))

D = 8 H0_deg minutes

cos(Ar) = (sin(delta) - sin(phi) sin(h0))
          / (cos(phi) cos(h0))

As = 360 deg - Ar

Ts = Tr + D
```

The production reference model may evaluate declination separately at each
event. If so, the difference from perfect azimuth symmetry shall be quantified
before the mirrored-hand architecture is approved.

## Calendar coordinate

The user-facing seasonal input should be calendar dates, not an unexplained
0-to-360-degree year angle. Internally, a date shaft may rotate once per selected
reference year. Leap-year handling is deferred until the annual drive is
specified.

## Rounding

- Calculations shall retain full available precision.
- Cam-generation values shall not be rounded to dial resolution.
- Reported time values may be rounded to the nearest minute.
- Reported azimuth values may be rounded to the nearest tenth of a degree during
  testing.
- Mechanical measurements shall record instrument resolution and uncertainty.
