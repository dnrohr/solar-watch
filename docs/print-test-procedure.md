# P1 Print, Calibration, and Test Procedure

## 1. Create the software environment

From a clean checkout in PowerShell:

```powershell
.\scripts\bootstrap.ps1
.\scripts\verify.ps1
```

The scripts create and use `.venv` inside the project. They do not install
system-wide packages. `verify.ps1` runs tests, regenerates all derived files,
and fails if regeneration changes a committed artifact.

To independently refresh JPL data (network required only on the first run):

```powershell
.\.venv\Scripts\solar-watch.exe validate-ephemeris --root . --cache .cache/skyfield
.\scripts\regenerate.ps1
```

## 2. Record the build

Copy `docs/templates/p1-build-record.md` and assign an ID such as
`P1-2026-001`. Record printer, build volume, nozzle, material, layer height,
slicer/version, scaling, temperatures, wall count, infill, and every part
filename/hash. Do not apply slicer XY scaling unless the coupon result justifies
and records it.

## 3. Print coupons first

1. Print `608_bearing_fit_21p9_to_22p3_revA.stl` flat, no support. From left to
   right with the long dimension horizontal, the holes are 21.9 through 22.3 mm.
2. Allow the coupon and bearing to reach room temperature. Select the smallest
   hole into which the bearing seats fully without hammering, cracking, or
   visible ovalization, yet does not rock.
3. If 22.2 mm is not selected, edit the `bearing_bore_mm` default in
   `src/solar_watch/cam.py`, increment the part revision, regenerate, and repeat
   software verification. Do not scale only the bore in the slicer.
4. Print `constant_radius_runout_revA.stl`, install its bearing, shaft, roller,
   rail, indicator, and spring. Rotate it manually through 360 degrees.
5. Record total indicated runout clockwise and counter-clockwise. Investigate
   values above 0.10 mm before committing to full cams.

## 4. Slice and print cams

Recommended starting point for a 0.4 mm nozzle:

- PLA, flat on the marked face or the slicer's smoothest plate-facing side;
- 0.16 or 0.20 mm layers;
- at least four walls/perimeters and five top/bottom layers;
- 30..40% gyroid or grid infill;
- no support;
- no global XY scale compensation;
- seam placed at the Jan 1 ray where it can be identified and measured;
- elephant-foot compensation established by the fit coupon; and
- brim only if needed, kept off the finished contact surface after removal.

Print one cam at a time. Do not place a cam on edge. Let it cool on the plate.
Deburr without rounding the profile. If sanding is necessary, use a rigid block
parallel to the cam axis, preserve the bearing and datum features, and record
the process.

## 5. Assemble the measurement rig

1. Fix the 8 mm shaft perpendicular to a flat baseboard.
2. Fit the cam's 608 bearing and retain it axially with washers/collars without
   side-loading the bearing.
3. Align the MGN12 rail so its centerline intersects the shaft axis within
   ±0.5 mm.
4. Mount the 625 roller with its axis parallel to the cam shaft. Ensure only the
   bearing outer race contacts the cam.
5. Attach the 1..3 N extension spring so it pulls the carriage toward the shaft
   throughout the complete stroke.
6. Align the indicator with carriage motion. Exercise the system several times
   and confirm the follower never lifts or binds.

## 6. Establish datum and calibration

1. Put a 3 mm alignment pin through the Jan 1 datum hole and align the hole with
   the follower centerline. Remove the pin before rotating.
2. Set the date by rotating the marked face clockwise from Jan 1 at
   `0.986301 deg/day`.
3. Zero the indicator at Jan 1 and record its absolute reading if available.
4. Measure the winter and summer extrema. Fit measured displacement `m` to the
   nominal pitch displacement `p` with `p = a*m + b`; retain `a` and `b` in the
   build record. This is the permitted span/zero calibration.
5. Do not change the generated cam profile or manually distort selected dates.

## 7. Annual verification

Use `data/p1_test_points_42p1N_2025.csv`. At each date:

1. Approach clockwise, settle without tapping, and record the indicator.
2. Pass the date, approach counter-clockwise, and record again.
3. Repeat the clockwise approach for repeatability.
4. Convert calibrated displacement with the formulas in
   `docs/p1-cam-package.md` and calculate absolute error against the reference.
5. Record backlash/hysteresis separately from mean absolute calibration error.

Minimum acceptance evidence for each cam:

- all prescribed dates measured;
- no follower lift, binding, or end-of-travel contact;
- runout, clockwise error, counter-clockwise error, repeatability, and surface
  finish recorded;
- azimuth absolute error ≤1 degree; and
- daylight results reported against the one-minute design target, without
  claiming success if the physical data exceed it.

Stop after the P1 report. Do not add a differential, dial artwork, variable
latitude, or P2 integration to solve a P1 measurement problem.
