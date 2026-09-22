# P2 Manufacturing, Assembly, Calibration, and Test Procedure

Status: Release candidate, Rev A
This procedure is mandatory evidence for physical acceptance. A clean software
verification does not replace it.

## 1. Incoming file and material control

1. Confirm the quotation references Rev A, millimetres, the PDF drawings, STEP
   models, DXFs, and the matching `SHA256SUMS.txt`.
2. Reject a quote that proposes machining from STL.
3. Obtain material certifications for POM-C, 6061-T6, and 303 stainless.
4. Require the machinist to identify any conflict between PDF notes and CAD
   before cutting. PDF controls tolerances/finish; STEP/DXF controls form.

## 2. Coupon gate before production cams

1. Machine P2-121 from the same POM-C stock and process intended for the cams.
2. Measure all four marked bores: 31.98, 32.00, 32.02, and 32.04 nominal.
3. Fit the first P2-103 hub. Select the process offset that produces free hand
   assembly with no detectable rocking; record the actual bore and hub diameter.
4. Machine P2-120 and mount it on that hub with the production screws and dowel.
5. Indicate the 120 mm diameter while rotating the date shaft. Total indicated
   runout must be 0.05 mm or less. If it fails, isolate shaft, hub-pilot, and
   profile contributions before authorizing production cams.
6. Inspect P2-122 hole-center distance. It must be 100.00 plus/minus 0.03. Use it
   to validate the setup used for lever slot and pivot locations.

## 3. Custom-part inspection

1. Verify manifest hashes and count every part against the BOM.
2. Inspect controlled interfaces I-01 through I-14 from the ICD.
3. On each cam, record thickness at four quadrants, pilot size, datum-hole
   position, face parallelism, and profile deviation at 16 specified dates.
4. Indicate each shaft journal and hand seat. Total indicated runout must not
   exceed 0.025 mm.
5. Roll-test purchased racks/gears over their full used travel. Reject tight
   spots, burrs, visible tooth damage, or backlash above 0.10 mm at the pitch
   line before spring preload.

## 4. Cam module assembly

1. Install bearings and the 12 mm date shaft without cams. Confirm free rotation
   and no more than 0.025 mm radial shaft runout at each hub position.
2. Install P2-128, the two 30-tooth pulleys, 760 mm belt, and idler. Set static
   belt tension to 10-20 N and verify 1:1 phase over two control revolutions.
3. Install hubs, dowels, and cams with both January 1 rays aligned. Tighten M5
   cam screws progressively to 3 N m; POM must not dish or gap from the hub.
4. Install each 16 mm track roller and set 1 to 3 N follower preload. Sweep one
   full revolution by hand. Contact must be continuous and torque smooth.
5. Record roller-center displacement at the 16 dates in
   `data/p1_test_points_42p1N_2025.csv`. Correct for the P2 hub datum only; do
   not alter the generated profile.

Acceptance: daylight displacement error at most 0.10 mm, azimuth displacement
error at most 0.20 mm, repeatability 0.05 mm, and clockwise/counter-clockwise
hysteresis 0.10 mm or less. Date control-to-cam phase hysteresis shall be no more
than 0.20 degree. These module limits reserve error for transmissions.

## 5. Time module assembly and calibration

1. Install both opposed racks, rails, 15-tooth differential pinion, carrier,
   30-tooth sunrise pinion, and 15-tooth output pinion dry.
2. Align pitch lines within 0.05 mm and install 1 to 2 N anti-backlash springs.
3. Use P2-122 to set the daylight lever nominal ratio to 1.000000. Leave jam
   nuts finger-tight.
4. With daylight follower at its 545-minute datum, set the sunset phase collar
   to the same indicated time as sunrise plus 9 h 05 min modulo 12 hours.
5. At winter and summer daylight extrema, adjust lever span equally about the
   datum until both errors have equal magnitude and opposite sign. Lock nuts,
   apply witness lacquer, and repeat.
6. Exercise sunrise in 15-minute steps through 12 hours at both daylight
   extrema. Compare sunset to `(sunrise + daylight) mod 720 minutes`.

Acceptance: maximum sunset indication error 1.0 minute, repeatability 0.5 minute,
and direction-dependent hysteresis 0.5 minute.

## 6. Azimuth module assembly and calibration

1. Install the 80-tooth pinion, coaxial shaft/tube, 1:1 miter reverser, wave
   washers, and hands. Preload without perceptible axial play or binding.
2. Set the azimuth lever nominal ratio to 1.000000 using P2-122.
3. At the spring-equinox reference, set the sunrise hand to the reference table
   and set sunset equal and opposite about north-south.
4. At both solstices, trim lever span for equal and opposite sunrise errors.
5. Sweep all 16 test dates in both directions, reading both hands.

Acceptance: each hand within 1.0 degree of the reference, repeatability 0.5
degree, hysteresis 0.5 degree, and mirror error 1.0 degree.

## 7. Frame, dial, and guard assembly

1. Square the extrusion frame so diagonal lengths differ by no more than 1 mm.
2. Mount module plates at the ICD Z stations. Verify shafts are normal to the
   dial plane within 0.1 degree.
3. Install functional dials at the P2-114 centers. Verify every hand clears its
   dial by 1.5 to 3 mm and adjacent hands by at least 1 mm.
4. Install the guard. Confirm at least 8 mm clearance to every moving part and
   that routine zero/span fasteners remain reachable after removing only the
   guard—not another calibrated module.
5. Measure the completed assembly. It must not exceed 609 x 900 x 200.

## 8. Integrated acceptance sweep

Test the 16 prescribed dates with sunrise settings of 04:00, 06:00, 08:00, and
10:00. Approach every setting clockwise first, then counter-clockwise. Record:

- measured daylight follower displacement;
- sunrise and sunset time indication;
- sunrise and sunset azimuth indication;
- setting direction, ambient temperature, and anomalies.

Pass only when all 64 states meet the time and azimuth acceptance limits and no
follower loses contact. Photograph the mechanism at both solstices and archive
the completed build record, raw data, deviations, and disposition.

## 9. Stop conditions

Stop and investigate rather than re-machining a generated profile when runout
exceeds the coupon limit, the follower unloads, a rack binds, the guard is
contacted, calibration requires more than the documented adjustment range, or
results depend on approach direction beyond the hysteresis limit.
