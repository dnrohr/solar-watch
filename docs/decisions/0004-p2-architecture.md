# Decision 0004: P2 Fixed-Latitude Architecture

Status: Accepted for detailed design

Date: 2026-09-21

## Context

P2 must convert the two validated fixed-latitude cam outputs into three readable
displays while keeping backlash, calibration, and service interfaces explicit.
The user has chosen to proceed directly to P2 and prioritize accurate CNC parts.

## Decision

P2 will use a portrait `609 x 900 mm` frontal envelope and no more than `200 mm`
overall depth. The functional layout is a `360 mm` azimuth dial above two
`240 mm` time dials. The mechanism remains visible behind a removable clear
guard.

A shared manual date shaft carries both fixed-latitude cams. The shaft is
supported in replaceable bearings; each CNC acetal cam bolts to a keyed metal
hub so profile parts can be inspected, replaced, or re-phased independently.

The time module uses a linear rack differential:

- a `15 mm` pitch-radius sunrise input converts sunrise-shaft rotation to rack
  travel;
- the P2 daylight cam directly encodes the required `0.1308997 mm/min` rack
  scale and drives the opposed input rack through a nominal `1:1` calibration
  lever;
- the differential pinion carrier moves by half the sum of the rack inputs; and
- a third rack fixed to the carrier drives a `7.5 mm` pitch-radius output pinion
  and restores the full angular sum on the sunset shaft.

The P2 azimuth cam directly encodes `0.6981317 mm/degree` and drives a nominal
`40 mm` pitch-radius pinion through a `1:1` calibration lever. A preloaded 1:1 bevel reverser couples the
sunrise inner shaft to the concentric sunset tube, producing equal and opposite
hand motion.

The structural system uses a metric T-slot perimeter frame with local CNC 6061
module plates. Precision is established locally by dowels, bearings, and module
plates rather than by a single full-size machined backplane.

## Alternatives considered

- A bevel or planetary rotary differential for time summation was more compact
  but introduced custom gear geometry, less transparent ratios, and additional
  backlash.
- Moving the entire cam module with the sunrise setting produced a direct sum
  but imposed unnecessary mass and date-shaft coupling.
- Separate azimuth axes simplified fabrication but failed to exercise the
  combined compass display intended for P2.
- A full `609 x 900 mm` aluminum backplate was stiff but expensive to machine
  and ship; local datum plates provide the required precision more economically.

## Consequences

- The time sum is visible, measurable, and independently testable in linear
  coordinates before dial installation.
- Zero, span, and phase remain separate adjustments.
- Rack preload and bevel preload are required to control reversal error.
- Functional dial scales are in scope, but decorative artwork remains deferred.
- The P2 architecture is fixed-latitude and does not pre-design P3 surfaces.
