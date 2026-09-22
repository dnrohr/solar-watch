# P2 Mechanical Analysis and Error Budget

Status: Digitally verified Rev A; fabrication evidence pending

## Full-year sweep

The committed analysis evaluates 365 dates at 48 sunrise settings in 15-minute
steps: 17,520 states. The mathematical rack differential reproduces
`(sunrise + daylight) mod 12 hours` with a maximum numerical kinematic error of
2.3e-13 degree. The P0 mirror approximation differs from independently computed
sunset azimuth by at most 0.277 degree. The full table is
`data/p2_full_year_motion_sweep_42p1N_2025.csv`.

| Travel | Minimum | Maximum | Allocated usable travel |
|---|---:|---:|---:|
| Sunrise input rack | 0.000 mm | 92.284 mm at 11:45 | 100 mm |
| Daylight input rack | 0.164 mm | 48.471 mm | 55 mm |
| Carrier output rack | 0.082 mm | 70.378 mm | 78 mm |
| Azimuth rack | 1.176 mm | 46.451 mm | 55 mm |

Each guide receives at least 3 mm end reserve beyond the analyzed range. The
sunrise rack additionally accommodates the untested 11:45-to-12:00 setting
margin up to the 94.248 mm theoretical full turn.

## Cam contact, force, and input torque

At the maximum specified 3 N follower preload, the daylight cam has 18.52-degree
maximum pressure angle, 13.23 mm minimum pitch-curve curvature radius, 1.01 N
maximum tangential follower force, and 65.14 N mm maximum ideal cam torque. The
azimuth cam values are 17.58 degrees, 33.93 mm, 0.96 N, and 64.76 N mm. Both
curvature radii exceed the 8 mm roller radius.

The two worst cam torques plus 40 N mm bearing/collar allowance total about
170 N mm. The date input is designed and acceptance-tested at 250 N mm; a 50 mm
radius handwheel therefore requires no more than 5 N hand force and provides a
1.47 torque factor over the calculated nominal worst case. The sunrise input
design torque is 75 N mm including 3 N working and 2 N preload forces, or 1.88 N
at a 40 mm knob radius. Measure actual torque before installing the dials.

## Deflection

An 8 mm stainless shaft with a 25 mm cantilever under 3 N deflects 0.00041 mm
by Euler-Bernoulli beam theory. A 569 mm 20x40 extrusion span loaded at midspan
with 10 N on its published weak-axis inertia deflects 0.046 mm. These estimates
are below the 0.01 mm shaft and 0.10 mm frame allocations. Joint slip, plate
flatness, and mounting compliance remain physical inspection items.

## Clearance and interference

Automated planar and depth checks establish:

| Check | Result | Requirement |
|---|---:|---:|
| Minimum dial-edge gap | 39.0 mm | at least 20 mm |
| Guard inner face to hand stack | 8.0 mm | at least 8 mm |
| Depth margin to 200 mm envelope | 21.5 mm | at least 20 mm |
| Minimum cam profile-to-pilot radial wall | 24.16 mm | at least 10 mm |
| Time / azimuth hand tip margin | 15 / 15 mm | at least 10 mm |

The assembly STEP and A01-A03 drawings additionally define module zones. The
digital check cannot prove cable, spring, washer, or fastener-head clearance;
the build procedure requires an unguarded slow sweep followed by an 8 mm guard
clearance gauge check.

## Backlash and hysteresis allocation

Commercial gear catalog backlash is not the achieved system lost motion. The
design uses opposed flank springs on all three time racks and axial spring
preload on the miter pair. The error budget assumes residual time-rack lost
motion of 0.020 mm (0.306 minute at the 7.5 mm output radius), azimuth spur lost
motion of 0.020 mm (0.029 degree), and miter lost motion of 0.030 mm at a 10 mm
pitch radius (0.172 degree). These are acceptance limits, not vendor default
claims. Directional tests must measure them after assembly.

## Combined error budget

Independent terms are combined by root-sum-square for planning. This is not a
guarantee because some fabrication errors can be correlated.

| Contribution | Time, min | Azimuth, deg |
|---|---:|---:|
| P0 numerical reference | 0.0022 | 0.00013 |
| 0.05 mm cam profile | 0.382 | 0.072 |
| 0.025 mm hub runout | 0.191 | 0.036 |
| 0.020 mm follower/linkage | 0.153 | 0.029 |
| Preloaded spur/rack residual | 0.306 | 0.029 |
| Preloaded miter residual | not applicable | 0.172 |
| Calibration residual | 0.200 | 0.150 |
| Reading/parallax | 0.500 | 0.500 |
| **Estimated RSS** | **0.768** | **0.557** |
| **Acceptance target** | **1.000** | **1.000** |

Functional time ticks are five minutes apart, 5.236 mm at the rim; a one-minute
interpolation is approximately 1.047 mm. Five azimuth degrees span 15.708 mm;
one degree spans 3.142 mm. Hands require a tip width at most 0.6 mm and a dial
gap of 1.5 to 3 mm to keep the stated reading allocation credible.

## Reproduction

Run `python -m solar_watch.cli analyze-p2 --root .`. The command regenerates the
full sweep, JSON summary, and mechanical verification plot. Automated tests
assert kinematic exactness, travel coverage, clearance, deflection, RSS targets,
and that physical validation remains marked pending.
