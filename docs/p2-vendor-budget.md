# P2 Vendor Shortlist and Budgetary Estimate

Status: Current-market review, 2026-09-21
This is a sourcing recommendation and planning estimate, not a quotation. No
files have been uploaded and no vendor has been contacted or authorized.

## Recommended sourcing split

### Precision CNC and inspection

Send the same RFQ to **Xometry**, **Protolabs Network**, and one local ISO 9001
job shop. Xometry publicly offers 6061, stainless, and acetal with specified
tolerances as tight as plus/minus 0.001 inch when called out. Protolabs Network
explicitly lists CNC-machined POM-C and provides instant quotation/DFM review.
The default platform tolerances are looser than the cam profile requirement, so
the 0.05 mm profile, 32 H7/h6 register, stabilization, and inspection report
must be treated as custom quote requirements—not platform defaults.

- Xometry CNC capability: <https://www.xometry.com/capabilities/cnc-machining-service/>
- Protolabs Network POM capability: <https://www.hubs.com/cnc-machining/plastic/pom-delrin/>

Recommendation: release only P2-120 through P2-122 first. Prefer the supplier
that accepts the common-datum setup and returns actual measurements, even if it
is not the lowest bidder. Then keep the cams and hubs with that same supplier.

### Flat guard and hands

**SendCutSend** is the first-choice benchmark for P2-115, P2-118, and P2-119.
Its published materials include 4.5 mm (0.177 inch) CNC-routed polycarbonate and
1.6 mm (0.063 inch) 5052-H32 aluminum. Its published laser/routing tolerance is
plus/minus 0.005 inch, suitable for these non-datum flat parts.

- Materials and thicknesses: <https://sendcutsend.com/materials/>
- Sheet-cutting tolerances: <https://sendcutsend.com/services/sheet-cutting/>

### Functional dials

**Front Panel Express** is the preferred benchmark for P2-116/P2-117 because it
combines CNC panel machining with engraving or UV print and live itemized
pricing. Use 2.5 mm anodized aluminum; its published capacity at that thickness
comfortably includes the 360 mm azimuth dial. Upload the DXF and request only
functional markings—decorative artwork is not part of P2.

- Services and live pricing: <https://www.frontpanelexpress.com/service>
- Aluminum size capability: <https://www.frontpanelexpress.com/downloads/FPE/Aluminum-Datasheet.pdf?v2=>

### Gears, racks, and frame

Use **KHK USA** for the critical module-1 gears: SS1-15 (8 mm bore) for the two
15-tooth elements, SS1-30B (8 mm bore) for sunrise input, SS1-80 with a qualified
bushing for azimuth, and an opposite-hand module-1 miter pair. KHK publishes
JIS grades and backlash; its ground SSG1-15 was listed at USD 40.48 at review.
Use **SDP/SI** or KHK for module-1, 20-degree racks; SDP/SI listed a 500 mm steel
rack at USD 64.64 and a nylon rack at USD 87.96. Cut after receipt and inspection.

- KHK 15-tooth gear: <https://www.khkgears.us/catalog/product/SSG1-15>
- KHK module-1 spur catalog: <https://www.khkgears.us/media/1019/01-spur.pdf>
- KHK module-1 miter catalog: <https://khkgears.net/pdf/2025/miter-gears.pdf>
- SDP/SI steel rack: <https://shop.sdp-si.com/ksrf1-500.html>

Use **80/20 20-2040** or a dimensionally equivalent metric profile for the
frame. The official profile is 20 x 40 mm 6063-T6, clear anodized, with six
slots and published CAD.

- 80/20 20-2040: <https://8020.net/20-2040.html>

## Budgetary cost range for one prototype

| Package | Expected low | Expected high | Basis / main uncertainty |
|---|---:|---:|---|
| Coupon lot P2-120..122 | USD 300 | USD 800 | inspection/setup dominates |
| POM-C cams and two hubs | 900 | 2,200 | 0.05 profile, stabilization, CMM report |
| Aluminum plates/levers/carrier | 700 | 1,800 | setup and anodize |
| Four stainless shafts/tube | 350 | 900 | journals, concentricity, low quantity |
| Guard and four hands | 180 | 450 | routing/laser, deburr, shipping |
| Three functional dials | 550 | 1,200 | engraving/UV print and large diameter |
| Gears, racks, rails, bearings, springs | 750 | 1,600 | gear grade and linear-rail choice |
| Frame and general hardware | 250 | 550 | cut service and fasteners |
| Shipping, inspection, remake reserve | 600 | 1,500 | multi-vendor freight and first article risk |
| **Planning total** | **4,580** | **11,000** | before tax; no assembly labor |

A reasonable authorization budget is **USD 7,500**, with only USD 300-800
released for the coupon gate initially. The low end assumes automated online
quoting and mostly standard inspection; the high end assumes domestic quick-turn
work, formal inspection, and one correction cycle. Consolidating all precision
parts at one inspected shop may cost more initially but reduces datum-transfer
and remake risk.

## Route comparison

| Route | Cam / precision strategy | Expected total | Planning lead time | Tradeoff |
|---|---|---:|---:|---|
| Minimum-cost hybrid | CNC POM-C cams with standard inspection; online-cut guard/hands; commercial-grade racks/gears | USD 4,600-6,500 | 3-6 weeks after coupon approval | Highest dependence on incoming inspection and preload tuning; remake reserve essential |
| Recommended accuracy | Stabilized POM-C cams/hubs in one setup with 16-station CMM report; ground 15T gears; inspected rails; anodized datum plates | USD 7,500-11,000 | 5-10 weeks after coupon approval | Best balance of low cam friction, inspectability, and one-off precision |
| Aluminum-cam alternate | 6061-T6 cams, hard anodized after profile verification, metal rollers | add USD 1,500-3,000 | add 2-4 weeks | More dimensionally stable during machining, but greater inertia/noise and anodize thickness must be compensated; not automatically more accurate |

POM-C remains the release material because its low friction, machinability, and
low moisture uptake suit the lightly loaded follower. POM-H/Delrin is easier to
source but is a controlled substitution because dimensional behavior differs.
Aluminum is a contingency when a supplier will not certify the 0.05 mm POM-C
profile. SLS/MJF nylon, SLA resin, laser-cut stacked cams, and consumer printing
are not precision production alternatives for P2; they are useful only for
fit/mock-up parts and cannot satisfy the profile/runout allocation without new
qualification.

Lead times are planning ranges inferred from the reviewed suppliers' published
instant-quote/stock lead-time model and low-volume prototype practice; actual
lead time begins only after drawing review and coupon acceptance. Shipping,
tax, import duty, and assembly labor are excluded. Before routing live quotes,
confirm delivery country/postal code, quantity, budget ceiling, and required
in-hand date.

## Quote comparison rules

1. Normalize shipping, tax, finish, inspection, and setup before comparing.
2. Reject substitutions from POM-C to POM-H unless thermal/moisture behavior is
   reviewed and Decision 0005 is revised.
3. Reject default-tolerance quotes that do not acknowledge the critical drawing
   notes and interface table.
4. Score dimensional evidence, communication, and remake policy above lead time.
5. Do not release production cams until the coupon report is reviewed.
