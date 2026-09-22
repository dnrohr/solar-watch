# P2 Bill of Materials

Status: Quotation BOM, Rev A
Currency and supplier are intentionally open until the manufacturing package is
reviewed. Quantities include one assembly unless a spare is stated.

## Custom CNC and cut parts

| Item | Qty | Description | Material / process | Master files |
|---|---:|---|---|---|
| P2-101 | 1 | Daylight-duration cam | 10 mm POM-C, 3-axis profile finish | STEP, DXF, CSV, PDF |
| P2-102 | 1 | Sunrise-azimuth cam | 10 mm POM-C, 3-axis profile finish | STEP, DXF, CSV, PDF |
| P2-103 | 2 | Cam hub | 6061-T6, turn/mill, clear anodize | STEP, DXF, PDF |
| P2-104 | 1 | Cam module plate | 6 mm 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-105 | 1 | Daylight span lever | 6 mm 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-106 | 1 | Azimuth span lever | 6 mm 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-107 | 1 | Time carrier plate | 6 mm 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-108 | 1 | Time module plate | 6 mm 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-109 | 1 | Azimuth module plate | 6 mm 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-110 | 1 | Sunrise time shaft | 303 stainless, turn/grind | STEP, PDF |
| P2-111 | 1 | Sunset output shaft | 303 stainless, turn/grind | STEP, PDF |
| P2-112 | 1 | Azimuth inner shaft | 303 stainless, turn/grind | STEP, PDF |
| P2-113 | 1 | Azimuth outer tube | 303 stainless, turn/grind | STEP, PDF |
| P2-115 | 1 | Removable guard | 4.5 mm clear polycarbonate, route | STEP, DXF, PDF |
| P2-116 | 2 | Functional time dial | 2.5 mm engraved/printed anodized aluminum | DXF, PDF |
| P2-117 | 1 | Functional azimuth dial | same as P2-116 | DXF, PDF |
| P2-118 | 2 | Time hand | 1.6 mm 5052-H32, laser/waterjet | STEP, DXF, PDF |
| P2-119 | 2 | Azimuth hand | 1.6 mm 5052-H32, laser/waterjet | STEP, DXF, PDF |
| P2-120 | 1 | Constant-radius cam runout coupon | 10 mm POM-C | STEP, DXF, PDF |
| P2-121 | 1 | 32 mm hub pilot fit coupon | 10 mm POM-C | STEP, DXF, PDF |
| P2-122 | 1 | 100 mm lever span gauge | 6 mm 6061-T6 | STEP, DXF, PDF |
| P2-123 | 1 | Keyed common cam/date shaft | 303 stainless, turn/mill/grind | STEP, DXF, PDF |
| P2-124 | 2 | Cam follower carriage | 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-125 | 3 | Rack clamp | 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-126 | 1 | Carrier output-rack bracket | 6061-T6, mill, clear anodize | STEP, DXF, PDF |
| P2-127 | 1 | Azimuth gear reducer bushing | 303 stainless, turn/grind | STEP, DXF, PDF |
| P2-128 | 1 | Date control shaft | 303 stainless, turn/grind | STEP, DXF, PDF |

P2-114 is a reference layout, not a separately manufactured part. Do not quote
STL files for production; they are inspection/preview derivatives only.

## Motion and bearing components

| Ref | Qty | Minimum specification | Notes |
|---|---:|---|---|
| B01 | 2 + 1 spare | Track roller, 16 OD x 5 bore x approximately 7 wide, sealed | cam followers |
| B02 | 8 | Flanged bearing, 8 ID, radial play C2 or standard | display shafts |
| B03 | 2 | Flanged bushing, 14 ID, dry-running polymer | outer azimuth tube |
| G01 | 3 | Module 1 rack, 20 degree PA, quality 8+, 120 mm usable teeth | two inputs plus carrier output |
| G02 | 1 | Module 1, 30 tooth spur pinion, 8 mm bore | sunrise input |
| G03 | 2 + 1 spare | Module 1, 15 tooth spur pinion, 8 mm bore | differential/output |
| G04 | 1 | Module 1, 80 tooth spur gear, 8 mm bore | sunrise azimuth |
| G05 | 1 set | 1:1 miter gears, 20 degree PA, 8 mm bores | azimuth reversal |
| L01 | 4 | 100 to 120 mm miniature profile rails with two carriages each | opposed racks/carrier |
| S01 | 2 | Extension spring, 1 to 2 N installed load, stainless | rack anti-backlash |
| S02 | 2 | Extension spring, 1 to 3 N over follower travel | cam preload |
| W01 | 4 | Wave spring washer for 8/14 mm coaxial stack | axial preload |
| D01 | 1 | HTD-5M timing belt, 15 wide, 760 pitch length | date input, 1:1 |
| D02 | 2 | HTD-5M pulley, 30 tooth, 15 belt width; 12 and 8 mm bores | cam shaft / control shaft |
| D03 | 1 | Smooth-back timing-belt idler with slotted mount | set belt tension, 10-20 N static |

Purchased gears may use imperial bores only if replaceable bushings preserve the
specified shaft journals and phase adjustments. Supplier part numbers are left
open for the vendor-selection stage.

## Shaft and bearing schedule

| Shaft | Journal / length | Supports | Mounted elements | Axial retention |
|---|---|---|---|---|
| P2-123 common cam/date | 12 h6 x 160, 4 mm keyway over 70 | two 12 mm flanged bearings, 110 span | two P2-103 hubs, D02 pulley | two 12 mm split collars |
| P2-128 date control | 8 h6 x 100 | two 8 mm flanged bearings, 55 span | date knob/hand, D02 pulley | shoulder plus 8 mm collar |
| P2-110 sunrise time | 8 h6 x 110 | two 8 mm flanged bearings, 65 span | G02 pinion, sunrise hand, input knob | shoulder plus 8 mm collar |
| P2-111 sunset output | 8 h6 x 95 | two 8 mm flanged bearings, 55 span | G03 output pinion, sunset hand | shoulder plus 8 mm collar |
| P2-112 azimuth inner | 8 h6 x 150 | two 8 mm flanged bearings, 90 span | G04 gear/bushing, sunrise hand | shoulder plus 8 mm collar |
| P2-113 azimuth tube | 14 h8 / 8.10 ID x 130 | two 14 mm bushings, 75 span | G05 driven miter, sunset hand | two wave washers and 14 mm collar |

## Fastener torque schedule

| Joint | Fastener | Dry assembly torque | Retention |
|---|---|---:|---|
| POM cam to hub | M5 class 8.8 with washer | 3 N m maximum | removable threadlocker |
| Aluminum module plates to T-slot | M6 class 8.8 | 8 N m | prevailing nut / T-nut |
| Rack clamps | M4 class 8.8 | 2.5 N m | removable threadlocker |
| Follower shoulder screws | M5 shoulder screw | 4 N m at thread | prevailing nut |
| Guard standoffs | M6, nylon washer | 3 N m | prevailing nut |

Verify that the POM remains flat after torque. Split collars and gear set screws
use their supplier torque, never the generic table.

## Frame and general hardware

| Ref | Qty | Specification |
|---|---:|---|
| F01 | 2 | 20 x 40 T-slot extrusion, 900 long |
| F02 | 4 | 20 x 40 T-slot extrusion, 569 long; two perimeter, two crossmembers |
| F03 | 8 | 20-series right-angle corner brackets with M5 fasteners |
| F04 | 12 | M6 adjustable standoffs, 35 to 55 long |
| H01 | 50 | M5 socket head screws, mixed 12/16/20 lengths, class 8.8 |
| H02 | 30 | M6 socket head screws and T-nuts, class 8.8 |
| H03 | 8 | M5 shoulder screws sized for B01 rollers |
| H04 | 8 | Split shaft collars, 8 mm bore; two with phase slots |
| H05 | 2 | Split shaft collars, 12 mm bore, keyed/date phase clamp |
| H06 | 12 | M5 all-metal prevailing torque jam nuts |
| H07 | 1 lot | 0.1/0.2/0.5 mm stainless shim washers |
| H08 | 1 lot | Medium-strength removable threadlocker and witness lacquer |

## Required inspection equipment (not consumed)

- 0 to 150 mm digital caliper, 0.01 mm display;
- 0 to 25 mm micrometer;
- dial indicator reading 0.01 mm with magnetic or rigid stand;
- 32 mm bore gauge or certified plug/ring masters;
- 4, 5, 6, 8, and 12 mm gauge pins or verified equivalents;
- 0 to 5 N spring scale;
- machinist square and surface plate or verified flat reference;
- protractor or optical angle encoder resolving 0.1 degree;
- printed test record from the included template.
