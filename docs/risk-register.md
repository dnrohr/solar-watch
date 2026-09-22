# Risk Register

Status: P2 Rev A
Date: 2026-09-22

Scores use likelihood and consequence from 1 (low) through 5 (high). Priority is
their product and is provisional until physical tests begin.

| ID | Risk | L | C | Priority | Initial response |
|---|---|---:|---:|---:|---|
| R-001 | Cam and follower errors prevent one-minute indication. | 3 | 5 | 15 | CNC POM cam tolerance is 0.05 mm; run P2 pilot-fit and runout coupons before release, then report results without claiming the target prematurely. |
| R-002 | Backlash causes different answers depending on setting direction. | 3 | 4 | 12 | Spring-preload rack flanks and followers; procedure records bidirectional hysteresis. |
| R-003 | Variable-latitude surface cams bind or lose follower contact. | 3 | 5 | 15 | Analyze surface slopes; use roller followers; prototype the surface module independently. |
| R-004 | One-minute accuracy cannot be read on the chosen dial. | 4 | 3 | 12 | Separate calculated accuracy from readable resolution; use large dials and five-minute markings. |
| R-005 | Frame flexibility overwhelms cam accuracy. | 2 | 4 | 8 | 20x40 perimeter/crossmembers and local 6 mm plates; measure deflection and shaft normality. |
| R-006 | Rack differential adds excessive play or friction. | 3 | 4 | 12 | Use quality-8 module-1 parts, dual linear rails, opposed flank springs, and module-first acceptance. |
| R-007 | Coaxial azimuth hands are difficult to fabricate and align. | 3 | 3 | 9 | Ground 8 mm inner shaft, 14/8.1 mm tube, replaceable bushings, wave-spring preload. |
| R-008 | Astronomical convention differs from published sunrise data. | 1 | 3 | 3 | Mitigated for P1: convention frozen and full year passes NREL SPA vs JPL DE421 validation; retain ideal-horizon warning. |
| R-009 | Atmospheric and terrain effects are mistaken for mechanism error. | 3 | 3 | 9 | State that the display represents a standardized ideal horizon. |
| R-010 | POM cams move after rough machining or clamping. | 3 | 4 | 12 | Stress-relieved stock, rough/stabilize 24 h, finish pilot/profile together, coupon approval before production. |
| R-013 | Incorrect bearing compensation or follower geometry corrupts the cam scale. | 2 | 5 | 10 | Source generates the inward normal offset for a 16 mm roller; automated scale, closure, pressure-angle, and mesh checks run on every verification. |
| R-014 | Vendor silently smooths or resamples the cam profile. | 2 | 5 | 10 | STEP/DXF are geometry masters, CSV is inspection reference, RFQ forbids smoothing and requires 16-station results. |
| R-015 | Bending or parallax at the large hands dominates reading error. | 3 | 3 | 9 | 5052 hands, 1.5-3 mm dial gap, guard clearance, and integrated optical/angle check. |
| R-016 | P1 test bypass leaves follower and preload behavior uncharacterized. | 4 | 4 | 16 | P2 coupon gate and separate cam/time/azimuth module tests are mandatory before integration. |
| R-017 | Remote date-control belt phase error or compliance shifts both annual cam readings. | 3 | 4 | 12 | Use matched 30-tooth HTD-5M pulleys, mark the common zero tooth, set phase with the date coupon, tension at the specified idler, and record bidirectional date-index error before module acceptance. |
| R-011 | Annual automatic drive requires more torque than a clock movement supplies. | 4 | 3 | 12 | Keep early date input manual; characterize torque before choosing a drive. |
| R-012 | Uncontrolled scope shifts the project toward a wristwatch too early. | 3 | 5 | 15 | Treat the 36 by 24 inch demonstrator as the current product and wrist scale as a separate future project. |

## First risk-reduction experiments

1. Machine and inspect the three P2 calibration coupons before releasing production parts.
2. Assemble the fixed-latitude daylight cam module and measure follower repeatability and phase.
3. Assemble the fixed-latitude azimuth cam module and measure follower repeatability and phase.
4. Characterize the remote date-control belt phase and bidirectional error.
5. Measure frame and shaft deflection under the intended preload.
6. Test each reversible output transmission and quantify lost motion before integration.
