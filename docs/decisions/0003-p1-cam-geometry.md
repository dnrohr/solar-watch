# Decision 0003: P1 Cam and Follower Geometry

Status: Accepted provisionally for first print

Date: 2026-09-21

## Context

P1 must maximize measurable motion while fitting a consumer printer and must
separate surface error, runout, hysteresis, and calibration.

## Decision

Use one-piece 8 mm plate cams with a translating 16 mm roller follower on a
radial linear rail. Encode daylight at 0.13 mm/min and sunrise azimuth at
0.70 mm/degree from a 48 mm pitch-radius datum. Locate each cam on a replaceable
608 bearing. Provide a bearing-fit coupon, constant-radius runout coupon, Jan 1
datum, distinct physical ID-hole patterns, and affine zero/span calibration.

## Alternatives considered

- sliding followers, which add friction and finish sensitivity;
- 22 mm 608 bearings as rollers, which increase offset and envelope;
- smaller scales, which reduce measurable resolution;
- larger or segmented cams, which add joint/runout error; and
- manually edited CAD profiles.

## Consequences

- One minute of daylight is 0.13 mm and one degree is 0.70 mm.
- The cams fit the provisional 220 mm printer and do not need segmentation.
- The daylight one-minute target remains a physical test target, not a claim.
- A printer selecting a non-22.2 mm fit coupon requires regeneration and a new
  part revision, never local mesh editing.
