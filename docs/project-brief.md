# Project Brief

Status: Draft v0.1  
Date: 2026-09-21

## Purpose

Create a visually understandable mechanical astronomical display, built
primarily from 3D-printed parts, that represents:

1. local sunrise time;
2. local sunset time;
3. sunrise azimuth; and
4. sunset azimuth.

The finished demonstrator should make the relationship between season,
latitude, daylight duration, and sunrise direction visible through physical
motion. The intended scale is a wall-mounted or tabletop mechanism with a
maximum frontal envelope of approximately 36 by 24 inches.

## Product idea

The display has three solar dials:

- a sunrise-time dial;
- a sunset-time dial; and
- a 360-degree compass dial carrying separate sunrise and sunset hands.

An optional conventional clock movement may provide current local time as a
fourth display. That clock is not part of the astronomical computation in the
initial prototypes.

The preferred final mechanism accepts date and latitude. A manually established
time reference may be used to avoid mechanically calculating longitude, civil
time zone, daylight-saving rules, and the equation of time in the first version.

## Development principle

Software will be used to calculate and validate the astronomical functions and
to generate printable cam geometry. The finished display may remain entirely
mechanical in operation. Using software during design is not considered an
electronic implementation of the final mechanism.

The development sequence is:

1. verified numerical reference model;
2. fixed-latitude cam and follower test;
3. full dial and summing-mechanism test;
4. variable-latitude surface cams;
5. integrated demonstrator; and
6. refinement for repeatable fabrication.

## Initial success criteria

The project is successful when an integrated demonstrator:

- operates across latitudes from 60 degrees south through 60 degrees north;
- indicates standardized astronomical sunrise and sunset azimuth within one
  degree of the reference model;
- indicates standardized sunrise and sunset time within one minute of the
  reference model as a design target;
- makes five-minute time differences and five-degree angle differences readily
  visible to a user;
- can be fabricated with commonly available 3D printers and inexpensive metal
  shafts, bearings, fasteners, and springs; and
- can be calibrated without reprinting the entire mechanism.

The distinction between calculation accuracy, mechanical indication accuracy,
repeatability, and human readability is intentional. Each will be measured
separately.

## Out of scope for the first prototypes

- Wristwatch-scale packaging
- Automatic longitude detection
- Automatic daylight-saving rules
- GPS or phone connectivity
- Actual terrain or building-horizon modeling
- Guaranteed agreement with visually observed sunrise in unusual atmospheric
  conditions
- Polar-day and polar-night behavior beyond 60 degrees latitude
- Decorative finishing suitable for a production object
