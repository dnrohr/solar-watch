# Risk Register

Status: Draft v0.1  
Date: 2026-09-21

Scores use likelihood and consequence from 1 (low) through 5 (high). Priority is
their product and is provisional until physical tests begin.

| ID | Risk | L | C | Priority | Initial response |
|---|---|---:|---:|---:|---|
| R-001 | Printed cam and follower errors prevent one-minute indication. | 4 | 5 | 20 | Build a large fixed-latitude test cam first; maximize output travel; measure rather than assume. |
| R-002 | Backlash causes different answers depending on setting direction. | 4 | 4 | 16 | Preload transmissions; specify an approach direction; test hysteresis separately. |
| R-003 | Variable-latitude surface cams bind or lose follower contact. | 3 | 5 | 15 | Analyze surface slopes; use roller followers; prototype the surface module independently. |
| R-004 | One-minute accuracy cannot be read on the chosen dial. | 4 | 3 | 12 | Separate calculated accuracy from readable resolution; use large dials and five-minute markings. |
| R-005 | Frame flexibility overwhelms cam accuracy. | 3 | 4 | 12 | Use a stiff backplane and short supported shafts; measure deflection under follower load. |
| R-006 | Time differential adds excessive play or friction. | 3 | 4 | 12 | Prototype a simple cable/belt summer before a compact geared differential. |
| R-007 | Coaxial azimuth hands are difficult to fabricate and align. | 3 | 3 | 9 | Permit separate axes during development; use metal tube/shaft stock in the integrated version. |
| R-008 | Astronomical convention differs from published sunrise data. | 3 | 3 | 9 | Freeze conventions and validation source before cam generation. |
| R-009 | Atmospheric and terrain effects are mistaken for mechanism error. | 3 | 3 | 9 | State that the display represents a standardized ideal horizon. |
| R-010 | Large cams exceed printer build volume or warp after assembly. | 3 | 4 | 12 | Segment cams with datum-controlled joints; print a small joint coupon before full parts. |
| R-011 | Annual automatic drive requires more torque than a clock movement supplies. | 4 | 3 | 12 | Keep early date input manual; characterize torque before choosing a drive. |
| R-012 | Uncontrolled scope shifts the project toward a wristwatch too early. | 3 | 5 | 15 | Treat the 36 by 24 inch demonstrator as the current product and wrist scale as a separate future project. |

## First risk-reduction experiments

1. Print a constant-slope calibration cam and measure follower repeatability.
2. Print one fixed-latitude annual azimuth cam.
3. Print one fixed-latitude annual daylight-duration cam at several output scales.
4. Compare roller and sliding followers.
5. Measure frame and shaft deflection under the intended preload.
6. Test a reversible output transmission and quantify lost motion.
