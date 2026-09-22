# P2 Interface Control Document

Status: Released for quotation, Rev A
All dimensions are millimetres. CAD is master for profile geometry; this file
is master for functional interfaces and acceptance.

## Coordinate system

Front view uses X right, Y up, and Z toward the viewer. The overall origin is
the lower-left corner of the 609 by 900 envelope. Cam-fixed profile angle zero
is the positive-X January 1 ray. The 4 mm indexing dowel is at radius 20 and 60
degrees counter-clockwise from that ray to avoid the three M5 clamp screws.
Positive cam profile angles are counter-clockwise; the installed date knob
advances clockwise.

## Controlled interfaces

| ID | Interface | Nominal | Fit / tolerance | Verification |
|---|---|---:|---|---|
| I-01 | Cam-to-hub pilot | 32 diameter | H7 cam / h6 hub | bore gauge, micrometer |
| I-02 | Cam clamp circle | 3 x M5 on 40 PCD | true position 0.10 to I-01 | CMM or pins |
| I-03 | January 1 datum | 4 reamed at radius 20, 60 deg CCW from profile zero | H7, position 0.05 to I-01 | CMM or height gauge |
| I-04 | Hub-to-date shaft | 12 diameter keyed | H7 bore, commercial key | plug gauge |
| I-05 | Cam face stack | 10 each | plus/minus 0.03; parallel 0.05 | micrometer |
| I-06 | Roller follower | 16 OD x 5 bore | commercial sealed bearing | certificate / measure |
| I-07 | Time rack/pinion | module 1, 20 degree PA | quality 8 or better | supplier certificate |
| I-08 | Sunrise pinion | 30 tooth | 15 pitch radius | roll test |
| I-09 | Differential/output pinions | 15 tooth | 7.5 pitch radius | roll test |
| I-10 | Azimuth pinion | 80 tooth | 40 pitch radius | roll test |
| I-11 | Azimuth coaxial shafts | 8 shaft, 14/8.1 tube | 0.05 diametral running clearance | gauges |
| I-12 | Module plate mounting | M6 clearance | 6.6 diameter | plug gauge |
| I-13 | Front guard | 585 x 875 x 4.5 | plus/minus 0.5 outline | tape / caliper |
| I-14 | Overall envelope | 609 x 900 x 200 maximum | must not exceed | assembled measurement |
| I-15 | Date belt transmission | HTD-5M, 30T:30T, 760 length, 15 width | 1:1; 10-20 N static tension | tension gauge / phase sweep |

## Datum scheme for custom parts

- Cams: datum A is the 32 mm pilot axis; B is the rear face; C is the January 1
  dowel hole. The generated profile is basic relative to A and C.
- Hubs: A is the 12 mm shaft bore axis; B is the rear flange face; C is the hub
  dowel hole. Pilot runout is 0.025 total indicated relative to A.
- Module plates: A is the rear mounting face, B the lower long edge, and C the
  left short edge. Bearing and shaft locations are basic from B/C.
- Levers: A is the pivot bore; B is one broad face; C is the roller-slot center
  plane. Pivot-to-slot setting is adjustable and locked by two jam nuts.
- Shafts: A is the bearing journal axis; B is the front shoulder. Display hub
  runout is 0.025 total indicated relative to A.

## General drawing notes

1. ISO 2768-mK applies unless specifically toleranced.
2. Deburr and break sharp edges 0.2 to 0.5; never roll or hand-blend cam profiles.
3. Aluminum is 6061-T6, clear anodized 8 to 12 micrometres after machining;
   mask bearing fits and electrical bonding points.
4. Cams are stress-relieved, machinable POM-C/acetal, black or natural. Machine
   both faces in one setup after roughing and allow 24 hours before finishing.
5. Shafts are 303 stainless, ground journals Ra 0.8 micrometre or better.
6. Polycarbonate guard edges are polished only after all holes are complete.
7. Supplier shall return dimensional inspection results for I-01 through I-05
   and shaft runout. No material substitution without written approval.
8. STEP controls 3D form. DXF controls flat profiles. PDF drawing notes control
   tolerances, finishes, and inspection.

## Assembly stack along Z

The frame rear plane is Z0. Module plates mount at Z35. The cam stack occupies
Z48 through Z82 including hubs, spacers, and followers. Rack modules occupy
Z88 through Z125. The date belt occupies Z130 through Z145. Dial faces lie at
Z154 through Z156.5, hands at Z160 to Z166, and the guard
inner face at Z174. The guard outer face at Z178.5 leaves at least 21.5 mm to
the 200 mm maximum envelope for fasteners and stand-off variation.

## Module placement in front coordinates

| Module / axis | X | Y | Interface |
|---|---:|---:|---|
| Cam module plate center | 304.5 | 450 | P2-104, 360 x 340 |
| Common cam/date shaft | 224.5 | 375 | local (-80,-75) on P2-104 |
| Date control shaft | 304.5 | 82 | 1:1 HTD link to cam shaft |
| Time module plate center | 304.5 | 285 | P2-108, 320 x 180 |
| Sunrise shaft | 165 | 285 | local X -139.5 on P2-108 |
| Sunset shaft | 444 | 285 | local X +139.5 on P2-108 |
| Azimuth module / coaxial shaft | 304.5 | 665 | P2-109 center |

The cam plate overlaps dial projections only in X/Y; its Z35-to-Z82 mechanism
zone is behind the Z154 dial plane. Belt, spring, and fastener-head clearance is
confirmed by the mandatory unguarded physical sweep.

## Adjustment provisions

| Adjustment | Range | Locking method | Witness mark |
|---|---:|---|---|
| Date phase | plus/minus 3 degrees | split hub collar | shaft/hub line |
| Daylight span | plus/minus 2 percent | slotted lever, two jam nuts | lever scale |
| Sunset zero | plus/minus 15 degrees | split output collar | collar/shaft line |
| Azimuth span | plus/minus 2 percent | slotted lever, two jam nuts | lever scale |
| Sunrise azimuth zero | plus/minus 5 degrees | split pinion collar | collar/shaft line |
| Sunset azimuth zero | plus/minus 5 degrees | split hand hub | hub/tube line |
