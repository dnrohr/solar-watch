# Decision 0002: P0 Reference Algorithm and Calendar

Status: Accepted

Date: 2026-09-21

## Context

P1 needs a reproducible full-year table accurate enough to allocate mechanical
error independently. The cam also needs an unambiguous calendar mapping.

## Decision

Use pvlib 0.13.1's NREL SPA implementation as the production P0 model and
validate all 365 days independently with Skyfield 1.53/JPL DE421. Use calendar
year 2025, longitude zero for auditable UTC timestamps, 42.1 degrees north, sea
level, and the specified -0.833-degree ideal event horizon.

## Alternatives considered

- a short trigonometric declination approximation;
- an online sunrise service;
- Skyfield alone without an independent comparison; and
- a leap year or an unexplained 0-to-360-degree seasonal coordinate.

## Consequences

- The complete validation data is committed so normal verification is offline.
- A JPL refresh downloads an ephemeris only into the project cache.
- A non-leap year gives exactly 365 equal date increments.
- The P1 cam represents the 2025 calendar; leap-year drive behavior remains a
  future input-drive decision.
