# P1 Fixed-Latitude Cam Package

Status: Digitally validated, awaiting physical print results

Latitude: `42.1 deg N`

Part revision: A

## Scope

P1 contains two independent radial plate cams driven by a manually positioned
annual shaft:

1. daylight duration; and
2. sunrise azimuth.

It deliberately contains no variable-latitude surface, time differential,
finished dial, mirrored sunset mechanism, or integrated P2 frame.

## Follower model

Both profiles are generated for a translating radial roller follower:

- roller: 625 bearing, `16 mm` outside diameter (`8 mm` radius), `5 mm` bore;
- follower centerline: passes through the cam axis;
- translation: an MGN12H carriage on a radial 150 mm rail, or an equivalent
  low-play guide;
- preload: extension spring pulling the carriage toward the cam, nominally
  `1..3 N` over the full stroke;
- measurement: `0.01 mm` digital indicator parallel to the rail;
- prescribed setting direction: rotate the marked cam face clockwise to move
  forward through the year.

The generated contact surface is the inward normal offset of the desired
roller-center pitch curve. It is not a raw polar plot. Maximum pressure angles
are `18.42 deg` (daylight) and `17.62 deg` (azimuth), comfortably below the
provisional 30-degree P1 limit.

## Scale and geometry

| Parameter | Daylight cam | Sunrise-azimuth cam |
|---|---:|---:|
| Conversion datum | 545 min | 55 deg |
| Pitch radius at datum | 48.0 mm | 48.0 mm |
| Scale | 0.13 mm/min | 0.70 mm/deg |
| 2025 input range | 546.252..915.290 min | 56.685..121.536 deg |
| Follower travel | 47.975 mm | 45.395 mm |
| Cam surface radius | 40.163..88.138 mm | 41.179..86.575 mm |
| Maximum pressure angle | 18.42 deg | 17.61 deg |
| Thickness | 8.0 mm | 8.0 mm |
| Nominal 608 bearing bore | 22.2 mm | 22.2 mm |

The conversion from measured roller-center pitch radius `r` is:

```text
daylight_minutes = 545 + (r_mm - 48) / 0.13
sunrise_azimuth_degrees = 55 + (r_mm - 48) / 0.70
```

A `0.01 mm` indicator increment corresponds to `0.077 min` or `0.014 deg`.
Those are instrument increments, not finished-part accuracy claims. With a
finished profile error of `±0.13 mm`, the equivalent errors are `±1.0 min` and
`±0.19 deg`. At `±0.20 mm`, they are `±1.54 min` and `±0.29 deg`. P1 exists to
measure which tolerance is repeatable with the user's printer and finishing
process.

## Date coordinate and datums

- The central `22.2 mm` bore accepts a 608 bearing; the 8 mm steel shaft runs in
  that replaceable bearing, never directly in a printed precision hole.
- The `3.2 mm` hole on the positive-X ray is the Jan 1 angular datum.
- With the Jan 1 hole pointing at the follower, the cam is at Jan 1. Rotate the
  marked face clockwise by `360/365 = 0.986301 deg` per day to advance the date.
- One small ID hole opposite the datum identifies the daylight cam; two identify
  the azimuth cam. Filenames also carry latitude and revision.
- The SVG red ray is the inspection datum and is not decorative dial artwork.

Use a shaft collar and washer for axial retention. Do not clamp through or
finish away the Jan 1 datum hole.

## Adjustment provisions

P1 uses an adjustable measurement chain instead of baking calibration error
into the cam:

- **Bearing fit:** print the five-size 608 coupon first and select the bore that
  gives a seated, removable bearing without visible distortion. Revision A
  printables use 22.2 mm; change `bearing_bore_mm` and regenerate if the coupon
  selects another size.
- **Runout:** the constant-radius coupon isolates bearing/bore/shaft runout from
  the astronomical profile.
- **Zero:** translate or zero the indicator at the Jan 1 datum. The indicator
  mount must retain at least ±5 mm of coarse adjustment.
- **Span:** use the two seasonal extrema to fit an affine measured-displacement
  calibration. Record both the nominal conversion and measured slope; do not
  edit the STL by hand.
- **Phase:** loosen the manual date pointer or shaft collar, align Jan 1's datum
  hole to the follower centerline, and retighten. No cam reprint is needed.
- **Preload:** move the spring anchor among baseboard holes or use a turnbuckle;
  target reliable contact with the smallest force that avoids lift-off.

## Tolerances

| Feature | Revision A target | Verification |
|---|---:|---|
| Finished contact profile | ±0.13 mm desired; ±0.20 mm initial limit | indicator versus reference dates |
| Constant-radius total indicated runout | ≤0.10 mm desired | runout coupon, full revolution |
| Bidirectional hysteresis | ≤0.08 mm desired | same date from both directions |
| Cam flatness | ≤0.30 mm over part | surface plate/straightedge and feeler gauge |
| Bearing fit | coupon-selected, no visible ovalization | hand fit and runout test |
| Follower-to-axis alignment | ±0.5 mm lateral | ruler/square inspection |

The one-minute integrated time target is not claimed until physical P1 results
show a repeatable `±0.13 mm` or better daylight profile. Azimuth has substantial
margin against its one-degree requirement.

## Segmentation and printer envelope

Revision A is intentionally one piece. The minimum rotated rectangles are about
`128.3 x 135.1 mm` (daylight) and `127.8 x 132.5 mm` (azimuth), and the largest
radius is under 89 mm. Both fit the repository's provisional 220 mm square bed
with ample room and avoid joint runout, phase error, and extra fasteners.

If the available bed is smaller than 150 mm after brim allowance, do not slice
the STL arbitrarily. A future segmented variant should use at least two dowel
datums per joint, radial fasteners outside the 608 bearing, and a printed joint
coupon; its assembled surface must be requalified with the same runout and
profile tests. No segmented file is included because it would reduce accuracy
without helping the assumed printer.

## Generated deliverables

`printables/p1/` contains:

- both watertight STL cams;
- matching 1:1 SVG inspection profiles;
- dense profile CSV files;
- a constant-radius runout STL;
- a 608-bearing fit STL with 21.9, 22.0, 22.1, 22.2, and 22.3 mm holes from
  left to right when the long edge is horizontal;
- `manifest.json` with generator inputs and mesh checks; and
- `SHA256SUMS.txt` for file-integrity checks.

All are regenerated by `scripts/regenerate.ps1`; the source of truth is Python,
not the mesh.
