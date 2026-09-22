# Decision 0006: Proceed to P2 Without Physical P1 Testing

Status: Accepted by user

Date: 2026-09-21

## Context

The P1 software, reference data, and printable cam package were completed, but
the coupons and cams were not physically manufactured or measured before the
user chose to proceed directly to a CNC-oriented P2 design.

## Decision

Proceed with P2 detailed design while treating all fabrication, runout,
follower preload, friction, hysteresis, structural-deflection, and wear claims
as unverified until P2 module testing. CNC capability may reduce manufacturing
error but does not replace mechanism testing.

## Consequences

- P2 includes module-level inspection and bench-test procedures before final
  display assembly.
- Error budgets identify assumed versus digitally proven contributions.
- The design must retain adjustment margin instead of relying on nominal CAD.
- No document may claim physical achievement of `ACC-003` through `ACC-006`.
