# Decision 0005: P2 CNC Materials and Datum Strategy

Status: Accepted for detailed design

Date: 2026-09-21

## Context

The P1 profiles were generated for consumer printing, including printer-fit
bearing bores. P2 parts are intended for accurate CNC manufacture and possible
reuse in a fixed-latitude display. Manufacturing drawings must distinguish
functional contour accuracy from ordinary overall size tolerance.

## Decision

- Cam profiles: black or natural POM-C/acetal, nominally `10 mm` thick.
- Cam hubs, local module plates, bearing blocks, and critical levers: 6061-T6
  aluminum unless a purchased component is selected.
- Shafts and dowels: ground stainless or hardened steel stock.
- Guards: clear polycarbonate; nonprecision functional dial panels may use
  aluminum composite panel or engraved acrylic after the geometry is frozen.
- Cam-to-hub location: precision pilot plus one asymmetric indexing dowel; bolts provide
  clamp load but do not define phase.
- Cam contour: basic geometry from the controlled DXF/STEP, profile tolerance
  `0.05 mm` relative to the hub pilot datum, with no uncontrolled edge break on
  the follower surface.
- Cam faces: parallel within `0.05 mm`; contact edge perpendicular to datum face
  within `0.05 mm` over thickness; target machined finish `Ra 1.6 micrometre` or
  better on the follower surface.
- Critical bores and dowel holes receive explicit limits on drawings; vendor
  general tolerances apply only where no specific tolerance is shown.

## Alternatives considered

- SLA offered smooth surfaces but introduced cure shrinkage, long-term resin
  behavior, and support-orientation sensitivity.
- SLS and MJF offered durable nylon but their normal dimensional tolerance and
  grainy surface were poorly matched to the one-minute cam target.
- Aluminum cams offered stiffness and stable machining but increased rotating
  mass, follower wear, price, and noise without improving the reference data.
- Direct bearing bores in the cam made the profile disposable with the bearing
  fit and provided no robust phase interface for P2 reuse.

## Consequences

- P1 print-fit coupons do not set P2 CNC bore dimensions.
- The cam hub becomes a separate controlled part.
- Quote packages must request contour inspection, not merely a generic overall
  tolerance.
- Physical conformance and wear remain pending until parts are manufactured.
