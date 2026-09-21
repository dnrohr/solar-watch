# P0 Numerical Reference and Validation

Status: Complete for P1

Reference year: 2025 (365 days)

Latitude: `+42.1 deg`

Longitude used for timestamps: `0 deg` (UTC; it does not affect daylight duration)

## Frozen convention

The reference event is the topocentric solar-center crossing of `-0.833 deg`
at an ideal, unobstructed sea-level horizon. Azimuth is clockwise from true
north. The reference year is deliberately non-leap so the P1 date cam has 365
equal daily increments. A future annual drive must address leap years; that is
not part of P1.

The production calculation in `src/solar_watch/model.py` uses pvlib 0.13.1's
Python implementation of the NREL Solar Position Algorithm (SPA). SPA supplies
the initial event estimate; a vectorized root refinement then locates the
topocentric geometric-elevation crossing at exactly `-0.833 deg`. An automated
test checks every sunrise and sunset to within `0.000001 deg` of that altitude.

NREL describes SPA as a high-accuracy solar position algorithm with a reported
solar-position uncertainty of about `±0.0003 deg`:

- [NREL SPA technical report](https://www.nrel.gov/docs/fy08osti/34302.pdf)
- [pvlib SPA implementation](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.solarposition.spa_python.html)

## Independent validation

`src/solar_watch/validation.py` independently computes every event in 2025
with Skyfield 1.53 and the JPL DE421 planetary ephemeris. Skyfield's documented
sunrise definition is a solar center `0.8333 deg` below the horizon; the script
explicitly requests `-0.833 deg` to match this project:

- [Skyfield almanac documentation](https://rhodesmill.org/skyfield/almanac.html)

The committed JPL-derived table makes the 365-day comparison available offline.
It can be refreshed with `solar-watch validate-ephemeris`; the first refresh
downloads `de421.bsp` into `.cache/skyfield`, not into a system location.

| Quantity | Maximum absolute difference | Requirement |
|---|---:|---:|
| Sunrise event time | 0.002153 min (0.129 s) | 0.1 min |
| Sunset event time | 0.002144 min (0.129 s) | 0.1 min |
| Daylight duration | 0.000564 min (0.034 s) | derived diagnostic |
| Sunrise azimuth | 0.000121 deg | 0.1 deg |
| Sunset azimuth | 0.000094 deg | 0.1 deg |

The model passes `ACC-001` and `ACC-002` for the P1 latitude and reference year.
The full `-60..+60 deg` domain is boundary-tested but not claimed as a completed
P3 validation sweep.

## Outputs

- `data/reference_42p1N_2025.csv`: the production full-year table.
- `data/skyfield_de421_42p1N_2025.csv`: independent full-year events.
- `data/validation_errors_42p1N_2025.csv`: row-by-row differences.
- `artifacts/plots/p0_reference_42p1N_2025.png`: annual functions.
- `artifacts/plots/p0_validation_errors_42p1N_2025.png`: error sweep.

The reference table retains timestamps and unrounded values. Cam generation
uses those values directly; display rounding is never fed back into geometry.

## Symmetry finding

Using the event-specific solar positions, actual sunset azimuth differs from
`360 deg - sunrise azimuth` by at most `0.277 deg` in 2025. That is below the
one-degree P1/P2 azimuth allocation, so mirrored sunset indication remains a
valid later architecture choice. P1 nevertheless generates only the requested
sunrise-azimuth cam and does not implement the P2 mirror mechanism.
