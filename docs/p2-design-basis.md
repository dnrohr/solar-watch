# P2 Fixed-Latitude Design Basis

Status: Released for quotation, Rev A
Latitude: 42.1 degrees north
Units: millimetres unless noted

## Scope and evidence boundary

P2 is a full-size, manually set, fixed-latitude astronomical display. One date
input drives the P0-validated daylight-duration and sunrise-azimuth cams. The
operator separately sets sunrise time. The mechanism displays sunrise time,
mechanically calculates sunset time, and displays mirrored sunrise and sunset
azimuths. The package intentionally stops before variable latitude, automatic
civil-time correction, decorative dial artwork, or the P3/P4 mechanisms.

The solar model, cam profiles, linkage equations, nominal clearances, and CAD
envelopes are digitally verified. Cutting accuracy, bearing fits, friction,
preload, backlash, stiffness, and achieved indication error remain physical
acceptance items. Decision 0006 records the deliberate P1 test bypass.

## Display and frame

The controlled external envelope is 609 wide by 900 high by 200 deep. A
20-series metric T-slot perimeter supports three removable 6 mm 6061-T6 module
plates and a 4.5 mm clear polycarbonate guard. The front layout uses these
dial centers from the lower-left corner:

| Display | Center X | Center Y | Diameter | Minor division |
|---|---:|---:|---:|---:|
| Sunrise azimuth / sunset azimuth | 304.5 | 665 | 360 | 5 degrees |
| Sunrise time | 165 | 285 | 240 | 5 minutes |
| Sunset time | 444 | 285 | 240 | 5 minutes |
| Date setting | 304.5 | 82 | 110 | monthly reference |

The five-minute time spacing is 5.236 mm on the dial rim. Five azimuth degrees
occupies 15.708 mm. The functional scales are engraved or UV printed on 2.5 mm
anodized aluminum; decorative artwork remains outside P2.

## Cam stack and date datum

Both cams retain the P1 translating 16 mm roller geometry and validated scales:

| Cam | Datum | Follower scale | Pitch radius | Surface radius range |
|---|---:|---:|---:|---:|
| Daylight duration | 545 min | 0.1308997 mm/min | 48 mm nominal | generated manifest |
| Sunrise azimuth | 55 degrees | 0.6981317 mm/degree | 48 mm nominal | generated manifest |

Each 10 mm POM-C cam pilots on a 32 H7/h6 metal hub register, clamps with three
M5 screws on a 40 mm bolt circle, and has a 4 mm indexing dowel at radius 20,
60 degrees counter-clockwise from the January 1 profile ray. The pair shares a
12 mm keyed date shaft. A split-clamp shaft collar gives
continuous date phase adjustment of at least plus/minus 3 degrees after the
dowel-defined nominal phase is established. Rotate the date control clockwise
to advance the calendar while the followers remain on the positive-X datum ray.

The visible date control at (304.5, 82) drives the common cam shaft at
(224.5, 375) through two 30-tooth HTD-5M pulleys and one 760 mm, 15 mm-wide
belt. Equal tooth counts preserve 1:1 date phase. A smooth-back idler on a slot
sets 10 to 20 N static belt tension and provides assembly tolerance. The date
phase collar is downstream of the belt so belt indexing does not alter the cam
datum. The belt is always approached clockwise during setting; bidirectional
phase hysteresis is measured separately.

Cam faces are finish-machined together to 10.00 plus/minus 0.03 thickness.
Profile tolerance is 0.05 relative to datum A (hub pilot); face parallelism and
shaft-axis perpendicularity are 0.05. The follower surface is Ra 1.6 micrometre
or better, with edges broken 0.2 maximum. Do not polish across the datum pilot.

## Daylight-to-sunset mechanism

The sunrise knob drives a 15 mm pitch-radius pinion and the sunrise hand. Its
rack travel is 94.248 mm for one 12-hour revolution. The P2 daylight cam directly
encodes the required rack scale, so the daylight calibration lever is nominally
1:1; its annual rack range is approximately 48.31 mm.

Two opposed module-1 input racks constrain a freely rotating module-1, 15-tooth
planet pinion carrier to their arithmetic mean. Carrier translation therefore
equals one half of the summed rack positions. A third rack attached to the
carrier drives a fixed-axis module-1, 15-tooth output pinion; its 7.5 mm pitch
radius converts carrier translation back to the full angular sum. The sunset
phase clamp removes the constant 545-minute cam datum. Nominal
kinematics are:

```text
x_sunrise = 15 rad(0.5 degrees/minute times sunrise_minutes)
x_daylight = 0.1308997 times (daylight_minutes - 545)
x_carrier = (x_sunrise + x_daylight) / 2
sunset_angle = x_carrier / 7.5 + phase
```

The racks are spring-biased against opposite tooth flanks by a 1 to 2 N
extension spring. Rack guides use dry-running polymer bushings; oil is not
permitted near POM cams. Carrier end stops provide 3 mm reserve beyond the
calculated motion. The sunset zero collar provides plus/minus 15 degrees and
the daylight lever slot provides plus/minus 2 percent span adjustment.

## Azimuth mechanism

The P2 azimuth cam directly encodes 0.6981317 mm/degree. Its follower drives a
rack through a nominal 1:1 adjustable calibration lever. The rack turns a
module-1 pinion with 40 mm pitch radius (80 teeth),
so one true azimuth degree produces one output degree. A preloaded 1:1 miter
gear pair reverses the sunset output around the north-south meridian. The
sunrise hand mounts on an 8 mm inner shaft and the sunset hand on a 14 mm OD by
8.1 mm ID outer tube. Two opposed spring washers remove axial clearance.

The sunrise zero collar allows plus/minus 5 degrees; the lever slot allows
plus/minus 2 percent span. The sunset hand has an independent zero clamp so the
two hands can be made symmetric at the equinox without disturbing the cam.

Both calibration levers use exact tangent-intersection geometry. A
center-pivoted 180 mm lever has separate radial slots on each side. Input and
output crosshead pins move on parallel guides at nominal offsets of minus and
plus 75 mm, so their displacement ratio equals the ratio of guide offsets.
Shifting the output guide from 73.5 to 76.5 mm provides 0.98:1 through 1.02:1
span without trigonometric scale error. Spring-biased slot rollers remove play;
the calibrated guide is clamped by two bolts and jam nuts.

## Followers, preload, and bearings

Both cams use sealed 16 mm OD by 5 mm bore track rollers, 7 mm nominal width,
on shoulder screws. Each follower has 1 to 3 N positive preload throughout its
travel and a mechanical retainer that prevents a disengaged roller from
contacting the adjacent cam. All rotating display shafts run in replaceable
flanged ball bearings or oil-impregnated bronze bushings located by machined
module plates. Printed holes are not precision bearings.

## Mechanical analysis and error allocation

The automated full-year sweep, pressure-angle loads, input torque, shaft/frame
deflection, travel, interference clearances, backlash allocations, readability,
and root-sum-square error budget are controlled by
`p2-mechanical-analysis.md`. Estimated RSS is 0.768 minute and 0.557 degree
against one-minute and one-degree targets. These are design estimates; physical
module and integrated sweeps are required before the targets can be claimed.

## Adjustment order

1. Inspect the hub pilot and shaft runout coupons.
2. Set date phase at January 1 with both cam dowels installed.
3. Set daylight and azimuth follower preload to 1 to 3 N.
4. Set daylight lever span using the minimum and maximum reference dates.
5. Set sunset zero at the 545-minute daylight datum.
6. Set azimuth lever span at the two solstice reference points.
7. Set sunrise azimuth zero, then set the reversed sunset hand for symmetry.
8. Lock all jam nuts, witness-mark clamps, and repeat the full sweep.
