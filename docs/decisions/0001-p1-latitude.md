# Decision 0001: P1 Latitude

Status: Accepted  
Date: 2026-09-21

## Context

The first physical cam prototype needs a single fixed latitude. This permits the
cam profile, follower, mechanical scale, and fabrication process to be validated
before variable-latitude surface cams are introduced.

## Decision

P1 shall use a latitude of 42.1 degrees north.

## Alternatives considered

- A rounded mid-latitude default such as 40 degrees north
- A different fixed latitude selected only for convenient calculation
- Proceeding directly to a variable-latitude surface

## Consequences

- All P1 reference tables and cam profiles will be generated for `phi = +42.1
  degrees`.
- P1 parts and test reports must identify the latitude explicitly.
- Results at 42.1 degrees north validate the fixed-latitude implementation but do
  not by themselves validate the full -60 through +60 degree requirement.
- The variable-latitude P3 mechanism remains unchanged in scope.
