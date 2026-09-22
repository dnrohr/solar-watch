"""Build the three controlled P2 PDF deliverables with ReportLab."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = colors.HexColor("#17365D")
ORANGE = colors.HexColor("#D97706")
LIGHT = colors.HexColor("#EAF0F6")
INK = colors.HexColor("#202830")


def _fonts() -> tuple[str, str]:
    candidates = [
        (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")),
        (Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")),
    ]
    for regular, bold in candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("SWRegular", regular))
            pdfmetrics.registerFont(TTFont("SWBold", bold))
            return "SWRegular", "SWBold"
    return "Helvetica", "Helvetica-Bold"


REGULAR, BOLD = _fonts()


def _styles():
    base = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=base["BodyText"], fontName=REGULAR, fontSize=8.5, leading=11, textColor=INK, spaceAfter=4)
    h1 = ParagraphStyle("h1", parent=base["Heading1"], fontName=BOLD, fontSize=17, leading=20, textColor=BLUE, spaceBefore=7, spaceAfter=8)
    h2 = ParagraphStyle("h2", parent=base["Heading2"], fontName=BOLD, fontSize=12, leading=14, textColor=BLUE, spaceBefore=8, spaceAfter=5)
    h3 = ParagraphStyle("h3", parent=base["Heading3"], fontName=BOLD, fontSize=9.5, leading=12, textColor=ORANGE, spaceBefore=6, spaceAfter=3)
    small = ParagraphStyle("small", parent=body, fontSize=7, leading=8.5)
    code = ParagraphStyle("code", parent=body, fontName="Courier", fontSize=7, leading=9, leftIndent=8, backColor=colors.HexColor("#F3F5F7"), borderPadding=5)
    return body, h1, h2, h3, small, code


BODY, H1, H2, H3, SMALL, CODE = _styles()


def _footer(canvas, doc, label: str):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#AAB4BE"))
    canvas.line(16 * mm, 13 * mm, doc.pagesize[0] - 16 * mm, 13 * mm)
    canvas.setFont(REGULAR, 7)
    canvas.setFillColor(colors.HexColor("#52616F"))
    canvas.drawString(16 * mm, 8 * mm, f"Solar Watch | {label} | Rev A | 42.1 deg N")
    canvas.drawRightString(doc.pagesize[0] - 16 * mm, 8 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _header_block(title: str, subtitle: str):
    return [
        Spacer(1, 3 * mm),
        Paragraph(title, ParagraphStyle("title", parent=H1, fontSize=24, leading=28, alignment=TA_LEFT, textColor=BLUE)),
        Paragraph(subtitle, ParagraphStyle("sub", parent=BODY, fontSize=11, leading=14, textColor=ORANGE)),
        Spacer(1, 3 * mm),
        Table([["REV", "A", "LATITUDE", "42.1 deg N", "RELEASE", "FOR QUOTATION / PHYSICAL TEST PENDING"]], colWidths=[12*mm, 10*mm, 20*mm, 25*mm, 18*mm, 83*mm], style=[("BACKGROUND", (0,0), (-1,-1), LIGHT), ("FONTNAME", (0,0), (-1,-1), BOLD), ("FONTSIZE", (0,0), (-1,-1), 6.5), ("GRID", (0,0), (-1,-1), 0.35, BLUE), ("VALIGN", (0,0), (-1,-1), "MIDDLE")]),
        Spacer(1, 5 * mm),
    ]


def _clean(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def _markdown_story(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    story = []
    paragraph = []
    code = []
    in_code = False

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            story.append(Paragraph(_clean(" ".join(line.strip() for line in paragraph)), BODY))
            paragraph = []

    def flush_code():
        nonlocal code
        if code:
            story.append(Paragraph("<br/>".join(_clean(line).replace(" ", "&nbsp;") for line in code), CODE))
            code = []

    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            flush_paragraph()
            if in_code:
                flush_code()
            in_code = not in_code
            index += 1
            continue
        if in_code:
            code.append(line)
            index += 1
            continue
        if line.startswith("# "):
            flush_paragraph(); story.append(Paragraph(_clean(line[2:]), H1))
        elif line.startswith("## "):
            flush_paragraph(); story.append(Paragraph(_clean(line[3:]), H2))
        elif line.startswith("### "):
            flush_paragraph(); story.append(Paragraph(_clean(line[4:]), H3))
        elif line.startswith("|") and index + 1 < len(lines) and set(lines[index + 1].replace("|", "").replace("-", "").replace(":", "").strip()) == set():
            flush_paragraph()
            rows = []
            while index < len(lines) and lines[index].startswith("|"):
                if "---" not in lines[index]:
                    rows.append([Paragraph(_clean(cell.strip()), SMALL) for cell in lines[index].strip("|").split("|")])
                index += 1
            table = Table(rows, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), BLUE), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("FONTNAME", (0,0), (-1,0), BOLD), ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#9AA8B5")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 3), ("RIGHTPADDING", (0,0), (-1,-1), 3), ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2)]))
            story.extend([table, Spacer(1, 3 * mm)])
            continue
        elif re.match(r"^\d+\. ", line):
            flush_paragraph(); story.append(Paragraph(_clean(line), ParagraphStyle("numbered", parent=BODY, leftIndent=10, firstLineIndent=-10)))
        elif line.startswith("- "):
            flush_paragraph(); story.append(Paragraph("&#8226; " + _clean(line[2:]), ParagraphStyle("bullet", parent=BODY, leftIndent=10, firstLineIndent=-8)))
        elif not line.strip():
            flush_paragraph()
        else:
            paragraph.append(line)
        index += 1
    flush_paragraph(); flush_code()
    return story


def build_design_dossier(path: Path):
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=16*mm, leftMargin=16*mm, topMargin=13*mm, bottomMargin=18*mm, title="Solar Watch P2 Design Dossier", author="Solar Watch project", invariant=1)
    story = _header_block("Solar Watch P2 Design Dossier", "CNC-ready fixed-latitude astronomical display")
    story += [Paragraph("Release statement", H2), Paragraph("This release completes the digital P2 design and quotation package. Numerical results and kinematics are verified. Fabrication-dependent accuracy remains explicitly pending until the coupon, module, and integrated tests are completed.", BODY)]
    story += [Spacer(1, 4*mm), Image(str(ROOT / "artifacts" / "plots" / "p2_layout_revA.png"), width=170*mm, height=113.3*mm)]
    for name in ("p0-validation.md", "p2-design-basis.md", "p2-interface-control.md", "p2-mechanical-analysis.md", "verification-matrix.md", "risk-register.md"):
        story.append(PageBreak())
        story.extend(_markdown_story(ROOT / "docs" / name))
        if name == "p0-validation.md":
            for image in ("p0_reference_42p1N_2025.png", "p0_validation_errors_42p1N_2025.png"):
                story.extend([Spacer(1, 3*mm), Image(str(ROOT / "artifacts" / "plots" / image), width=175*mm, height=122.5*mm)])
        if name == "p2-mechanical-analysis.md":
            story.extend([
                Spacer(1, 3*mm),
                Image(
                    str(ROOT / "artifacts" / "p2" / "p2_mechanical_verification_revA.png"),
                    width=175*mm,
                    height=127.3*mm,
                ),
            ])
    doc.build(story, onFirstPage=lambda c,d: _footer(c,d,"P2 DESIGN DOSSIER"), onLaterPages=lambda c,d: _footer(c,d,"P2 DESIGN DOSSIER"))


DRAWINGS = {
    "P2-101": ("DAYLIGHT-DURATION CAM", "POM-C", "10.00 +/-0.03 THK; 32 H7 PILOT; 3x 5.5 THRU ON 40 PCD; 4 H7 DATUM AT R20 / 60 DEG; PROFILE 0.05 TO A|C; Ra1.6"),
    "P2-102": ("SUNRISE-AZIMUTH CAM", "POM-C", "10.00 +/-0.03 THK; 32 H7 PILOT; 3x 5.5 THRU ON 40 PCD; 4 H7 DATUM AT R20 / 60 DEG; PROFILE 0.05 TO A|C; Ra1.6"),
    "P2-103": ("CAM HUB", "6061-T6", "FLANGE OD50 x 8; PILOT 32 h6 x 3; SHAFT BORE 12 H7 KEYED; 3x M5 ON 40 PCD; PILOT TIR 0.025 TO BORE"),
    "P2-104": ("CAM MODULE PLATE", "6061-T6", "360 x 340 x 6; DATE BORE 28 AT (-80,-75); LEVER PIVOT 8 H7 AT (80,0); 4x FRAME 6.6 AT (+/-165,+/-155); GUIDE HOLES PER DXF"),
    "P2-105": ("DAYLIGHT SPAN LEVER", "6061-T6", "180 x 22 x 6; CENTER PIVOT 8 H7; 2x RADIAL 6.2 x 67 SLOTS; NOMINAL GUIDE SPACING +/-75"),
    "P2-106": ("AZIMUTH SPAN LEVER", "6061-T6", "180 x 22 x 6; CENTER PIVOT 8 H7; 2x RADIAL 6.2 x 67 SLOTS; NOMINAL GUIDE SPACING +/-75"),
    "P2-107": ("TIME CARRIER PLATE", "6061-T6", "58 x 42 x 6; PLANET SHAFT BORE 8 H7; 2x 5.2 THRU AT X +/-22"),
    "P2-108": ("TIME MODULE PLATE", "6061-T6", "320 x 180 x 6; SHAFT BORES 22 AT X +/-139.5; 4x FRAME 6.6 AT (+/-150,+/-75); RAIL/STOP HOLES PER DXF"),
    "P2-109": ("AZIMUTH MODULE PLATE", "6061-T6", "190 x 130 x 6; CENTER BORE 22 H7; 4x FRAME 6.6 AT (+/-80,+/-55)"),
    "P2-110": ("SUNRISE TIME SHAFT", "303 SS", "OD8 h6 x 110; OD12 SHOULDER x 3; JOURNAL Ra0.8; TIR 0.025"),
    "P2-111": ("SUNSET OUTPUT SHAFT", "303 SS", "OD8 h6 x 95; OD12 SHOULDER x 3; JOURNAL Ra0.8; TIR 0.025"),
    "P2-112": ("AZIMUTH INNER SHAFT", "303 SS", "OD8 h6 x 150; OD12 SHOULDER x 3; JOURNAL Ra0.8; TIR 0.025"),
    "P2-113": ("AZIMUTH OUTER TUBE", "303 SS", "OD14 h8; ID8.10 +0.03/-0.00; LENGTH130; CONCENTRIC 0.025 TIR"),
    "P2-114": ("FRONT LAYOUT", "REFERENCE", "ENVELOPE 609 x 900; DIAL CENTERS: AZ (304.5,665), SUNRISE (165,285), SUNSET (444,285), DATE (304.5,82)"),
    "P2-115": ("FRONT GUARD", "CLEAR POLYCARBONATE", "585 x 875 x 4.5; 4x 6.6 AT (+/-286.5,+/-431); EDGE POLISH AFTER MACHINING"),
    "P2-116": ("TIME DIAL", "ANODIZED ALUMINUM", "OD240; ID8; THK2.5; 5-MIN MINOR TICKS (2.5 DEG); 30-MIN MAJOR TICKS; ARTWORK FUNCTIONAL ONLY"),
    "P2-117": ("AZIMUTH DIAL", "ANODIZED ALUMINUM", "OD360; ID8; THK2.5; 5-DEG MINOR TICKS; 15-DEG MAJOR TICKS; NORTH AT +Y"),
    "P2-118": ("TIME HAND", "5052-H32", "LENGTH105; HUB OD20; BORE8 H7; THK1.6; BALANCE AFTER FINISH"),
    "P2-119": ("AZIMUTH HAND", "5052-H32", "LENGTH165; HUB OD22; BORE8 H7; THK1.6; BALANCE AFTER FINISH"),
    "P2-120": ("CAM RUNOUT COUPON", "POM-C", "OD120 x 10; PRODUCTION 32 PILOT / M5 PCD / 4 DATUM; OD TIR <=0.05 ON PRODUCTION HUB"),
    "P2-121": ("HUB PILOT FIT COUPON", "POM-C", "170 x 52 x 10; BORES 31.98 / 32.00 / 32.02 / 32.04 LEFT TO RIGHT; SAME SETUP AS CAMS"),
    "P2-122": ("LEVER SPAN GAUGE", "6061-T6", "125 x 18 x 6; 2x 5 H7; CENTER DISTANCE 100.00 +/-0.03"),
    "P2-123": ("COMMON CAM / DATE SHAFT", "303 SS", "OD12 h6 x 160; 4 WIDE x 2 DEEP KEYWAY OVER 70; JOURNAL Ra0.8; TIR 0.025"),
    "P2-124": ("CAM FOLLOWER CARRIAGE", "6061-T6", "45 x 30 x 8; ROLLER BORE 5 H7 AT X15; 2x M4 CLEARANCE AT X +/-12"),
    "P2-125": ("RACK CLAMP", "6061-T6", "50 x 20 x 8; 2x M4 CLEARANCE AT X +/-18; MATCH-DRILL TO COMMERCIAL RACK"),
    "P2-126": ("CARRIER OUTPUT-RACK BRACKET", "6061-T6", "80 x 25 x 8; 4x M4 CLEARANCE AT X +/-12,+/-30; MOUNTS THIRD RACK"),
    "P2-127": ("AZIMUTH GEAR BUSHING", "303 SS", "FLANGE OD20 x 2; BODY OD15 h6 x 10; BORE8 H7; CONCENTRIC 0.025 TIR"),
    "P2-128": ("DATE CONTROL SHAFT", "303 SS", "OD8 h6 x 100; OD12 SHOULDER x 3; HTD PULLEY + DATE KNOB; JOURNAL Ra0.8; TIR 0.025"),
}


def _drawing_page(canvas, doc, part: str, title: str, material: str, notes: str, page_no: int, total: int):
    w, h = landscape(A4)
    canvas.saveState()
    canvas.setStrokeColor(BLUE); canvas.setLineWidth(0.8)
    canvas.rect(10*mm, 10*mm, w-20*mm, h-20*mm)
    canvas.setFont(BOLD, 14); canvas.setFillColor(BLUE)
    canvas.drawString(16*mm, h-22*mm, f"{part}  {title}")
    canvas.setFont(REGULAR, 8); canvas.setFillColor(INK)
    canvas.drawRightString(w-16*mm, h-21*mm, f"SHEET {page_no} OF {total} | REV A | mm")
    cx, cy = w*0.42, h*0.55
    canvas.setStrokeColor(colors.HexColor("#52616F")); canvas.setLineWidth(1.2)
    if part in ("P2-101", "P2-102", "P2-120", "P2-116", "P2-117"):
        r = 48*mm if part == "P2-117" else 38*mm
        canvas.circle(cx, cy, r); canvas.circle(cx, cy, 8*mm)
        canvas.line(cx-r-8*mm, cy, cx+r+8*mm, cy); canvas.line(cx, cy-r-8*mm, cx, cy+r+8*mm)
    elif part in ("P2-110", "P2-111", "P2-112", "P2-113"):
        canvas.rect(cx-65*mm, cy-5*mm, 130*mm, 10*mm); canvas.line(cx-70*mm, cy, cx+70*mm, cy)
    else:
        canvas.roundRect(cx-65*mm, cy-35*mm, 130*mm, 70*mm, 3*mm)
        canvas.circle(cx-35*mm, cy, 4*mm); canvas.circle(cx+35*mm, cy, 4*mm)
    canvas.setFont(BOLD, 8); canvas.drawString(16*mm, 51*mm, "CONTROLLED CHARACTERISTICS")
    canvas.setFont(REGULAR, 7.5)
    text = canvas.beginText(16*mm, 45*mm); text.setLeading(10)
    for chunk in notes.split("; "):
        text.textLine(chunk)
    canvas.drawText(text)
    data = [["PART", part, "MATERIAL", material, "QTY", str(json.loads((ROOT/'cnc/p2/manifest.json').read_text())["parts"][part]["quantity"])], ["DATUMS", "SEE ICD", "GENERAL", "ISO 2768-mK", "STATUS", "FOR QUOTATION"], ["CAD", "STEP/DXF MASTER", "PROFILE", "NO STL MACHINING", "FINISH", "SEE ICD"]]
    table = Table(data, colWidths=[13*mm, 36*mm, 18*mm, 36*mm, 15*mm, 48*mm], rowHeights=8*mm)
    table.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.4, BLUE), ("BACKGROUND", (0,0), (-1,-1), LIGHT), ("FONTNAME", (0,0), (-1,-1), REGULAR), ("FONTNAME", (0,0), (0,-1), BOLD), ("FONTNAME", (2,0), (2,-1), BOLD), ("FONTNAME", (4,0), (4,-1), BOLD), ("FONTSIZE", (0,0), (-1,-1), 6.5), ("VALIGN", (0,0), (-1,-1), "MIDDLE")]))
    table.wrapOn(canvas, w, h); table.drawOn(canvas, w-176*mm, 16*mm)
    canvas.setFont(REGULAR, 6.5); canvas.drawString(16*mm, 14*mm, "CAD defines basic geometry. PDF notes and P2 Interface Control Document define tolerances and inspection.")
    canvas.restoreState(); canvas.showPage()


def _assembly_drawing_page(canvas, title: str, sheet: int, total: int, kind: str):
    w, h = landscape(A4)
    canvas.saveState()
    canvas.setStrokeColor(BLUE); canvas.setLineWidth(0.8)
    canvas.rect(10*mm, 10*mm, w-20*mm, h-20*mm)
    canvas.setFont(BOLD, 14); canvas.setFillColor(BLUE)
    canvas.drawString(16*mm, h-22*mm, title)
    canvas.setFont(REGULAR, 8); canvas.setFillColor(INK)
    canvas.drawRightString(w-16*mm, h-21*mm, f"SHEET {sheet} OF {total} | REV A | mm")
    if kind == "general":
        scale = 0.16
        ox, oy = 28*mm, 24*mm
        canvas.rect(ox, oy, 609*scale*mm, 900*scale*mm)
        for x, y, diameter, label in ((304.5,665,360,"AZ"),(165,285,240,"SUNRISE"),(444,285,240,"SUNSET"),(304.5,82,110,"DATE")):
            canvas.circle(ox+x*scale*mm, oy+y*scale*mm, diameter/2*scale*mm)
            canvas.setFont(REGULAR, 6); canvas.drawCentredString(ox+x*scale*mm, oy+y*scale*mm, label)
        canvas.setFont(BOLD, 8); canvas.drawString(150*mm, 155*mm, "OVERALL ENVELOPE")
        for line_no, text in enumerate(("609 W x 900 H x 200 D MAX", "DIALS: 360 AZ / 240 TIME", "GUARD INNER FACE Z174", "MIN HAND/GUARD CLEARANCE 8")):
            canvas.setFont(REGULAR, 8); canvas.drawString(150*mm, (145-line_no*10)*mm, text)
    elif kind == "exploded":
        layers = [("20x40 FRAME",25),("MODULE PLATES",48),("CAM STACK",75),("RACK / GEAR MODULES",105),("DIALS",140),("HANDS",160),("CLEAR GUARD",180)]
        for idx, (label, z) in enumerate(layers):
            x = (28 + idx*32)*mm; y = (35 + idx*13)*mm
            canvas.setFillColor(colors.Color(0.15,0.3,0.5,alpha=0.12+idx*0.04)); canvas.setStrokeColor(BLUE)
            canvas.rect(x, y, 58*mm, 90*mm, fill=1)
            canvas.setFillColor(INK); canvas.setFont(BOLD, 6.5); canvas.drawCentredString(x+29*mm, y+45*mm, label)
            canvas.setFont(REGULAR, 6); canvas.drawCentredString(x+29*mm, y+38*mm, f"Z {z}")
            if idx < len(layers)-1:
                canvas.line(x+58*mm, y+45*mm, x+68*mm, y+58*mm)
        canvas.setFont(REGULAR, 8); canvas.drawString(20*mm, 20*mm, "Assembly order: square frame -> datum plates -> shafts/cams -> racks/gears -> dials -> hands -> guard. Service removal is the reverse; calibrated modules remain installed.")
    else:
        boxes = [
            (18,145,44,18,"DATE INPUT"),(75,145,45,18,"2 CAMS"),(135,160,45,18,"DAYLIGHT"),(135,125,45,18,"AZIMUTH"),
            (195,160,48,18,"3-RACK SUMMER"),(195,125,48,18,"80T + MITER"),(255,160,25,18,"SUNSET"),(255,125,25,18,"AZ HANDS"),
            (18,85,52,18,"SUNRISE KNOB"),(90,85,42,18,"30T / RACK"),
        ]
        for x,y,bw,bh,label in boxes:
            canvas.setFillColor(LIGHT); canvas.setStrokeColor(BLUE); canvas.rect(x*mm,y*mm,bw*mm,bh*mm,fill=1)
            canvas.setFillColor(INK); canvas.setFont(BOLD,6.5); canvas.drawCentredString((x+bw/2)*mm,(y+6)*mm,label)
        arrows = [((62,154),(75,154)),((120,154),(135,169)),((120,145),(135,134)),((180,169),(195,169)),((243,169),(255,169)),((180,134),(195,134)),((243,134),(255,134)),((70,94),(90,94)),((132,94),(195,169))]
        canvas.setStrokeColor(ORANGE); canvas.setFillColor(ORANGE)
        for (x1,y1),(x2,y2) in arrows:
            canvas.line(x1*mm,y1*mm,x2*mm,y2*mm); canvas.circle(x2*mm,y2*mm,1.1*mm,fill=1)
        canvas.setFillColor(INK); canvas.setFont(REGULAR,8)
        notes = ("TIME: x_carrier=(x_sunrise+x_daylight)/2; 7.5 mm output radius restores full sum.", "AZIMUTH: 40 mm pitch radius gives 1 deg output per 0.6981317 mm; 1:1 miter reverses sunset.", "All three modules expose independent zero/span/phase adjustments after guard removal.")
        for i,text in enumerate(notes): canvas.drawString(18*mm,(58-i*10)*mm,text)
    data = [["DRAWING", title, "STATUS", "FOR QUOTATION"], ["DATUM", "LOWER-LEFT FRONT / Z REAR", "MASTER", "P2 ICD + STEP/DXF"]]
    table = Table(data, colWidths=[18*mm,70*mm,18*mm,70*mm], rowHeights=8*mm)
    table.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.4,BLUE),("BACKGROUND",(0,0),(-1,-1),LIGHT),("FONTNAME",(0,0),(-1,-1),REGULAR),("FONTNAME",(0,0),(0,-1),BOLD),("FONTNAME",(2,0),(2,-1),BOLD),("FONTSIZE",(0,0),(-1,-1),6.5)]))
    table.wrapOn(canvas,w,h); table.drawOn(canvas,w-188*mm,16*mm)
    canvas.restoreState(); canvas.showPage()


def _drawing_index_page(canvas, total: int):
    w, h = landscape(A4)
    canvas.saveState(); canvas.setStrokeColor(BLUE); canvas.setLineWidth(0.8)
    canvas.rect(10*mm, 10*mm, w-20*mm, h-20*mm)
    canvas.setFont(BOLD, 14); canvas.setFillColor(BLUE)
    canvas.drawString(16*mm, h-22*mm, "P2-A00 DRAWING INDEX")
    canvas.setFont(REGULAR, 8); canvas.setFillColor(INK)
    canvas.drawRightString(w-16*mm, h-21*mm, f"SHEET 1 OF {total} | REV A | mm")
    entries = [
        ("P2-A01", "GENERAL ARRANGEMENT"),
        ("P2-A02", "EXPLODED MODULE STACK"),
        ("P2-A03", "KINEMATIC / INTERFACE DIAGRAM"),
    ] + [(part, values[0]) for part, values in DRAWINGS.items()]
    midpoint = (len(entries) + 1) // 2
    columns = (entries[:midpoint], entries[midpoint:])
    for col, items in enumerate(columns):
        x = (18 + col*138)*mm
        y = h - 35*mm
        for part, title in items:
            canvas.setFont(BOLD, 7); canvas.drawString(x, y, part)
            canvas.setFont(REGULAR, 7); canvas.drawString(x+24*mm, y, title)
            canvas.setStrokeColor(colors.HexColor("#D4DCE4")); canvas.line(x, y-1.5*mm, x+125*mm, y-1.5*mm)
            y -= 8.5*mm
    canvas.setFont(REGULAR, 7); canvas.setFillColor(INK)
    canvas.drawString(16*mm, 15*mm, "Every numbered custom part has STEP/DXF geometry; STL is preview-only. PDF notes and the ICD control tolerances and inspection.")
    canvas.restoreState(); canvas.showPage()


def build_drawings(path: Path):
    from reportlab.pdfgen.canvas import Canvas
    canvas = Canvas(str(path), pagesize=landscape(A4), pageCompression=1, invariant=1)
    canvas.setTitle("Solar Watch P2 Assembly and Custom Part Drawings")
    total = len(DRAWINGS) + 4
    _drawing_index_page(canvas, total)
    _assembly_drawing_page(canvas, "P2-A01 GENERAL ARRANGEMENT", 2, total, "general")
    _assembly_drawing_page(canvas, "P2-A02 EXPLODED MODULE STACK", 3, total, "exploded")
    _assembly_drawing_page(canvas, "P2-A03 KINEMATIC / INTERFACE DIAGRAM", 4, total, "interface")
    for index, (part, values) in enumerate(DRAWINGS.items(), start=5):
        _drawing_page(canvas, None, part, *values, index, total)
    canvas.save()


def build_procurement(path: Path):
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=16*mm, leftMargin=16*mm, topMargin=13*mm, bottomMargin=18*mm, title="Solar Watch P2 Procurement and Test Pack", author="Solar Watch project", invariant=1)
    story = _header_block("P2 Procurement & Test Pack", "Quotation BOM, RFQ instructions, assembly, calibration, and acceptance")
    story += [Paragraph("Release gate", H2), Paragraph("Authorize coupon manufacture first. Release the production cams only after P2-120 through P2-122 pass. Do not accept machining from STL and do not treat software verification as physical acceptance.", BODY)]
    for name in ("p2-bom.md", "p2-rfq.md", "p2-vendor-budget.md", "p2-manufacturing-test.md"):
        story.append(PageBreak()); story.extend(_markdown_story(ROOT / "docs" / name))
    doc.build(story, onFirstPage=lambda c,d: _footer(c,d,"P2 PROCUREMENT & TEST"), onLaterPages=lambda c,d: _footer(c,d,"P2 PROCUREMENT & TEST"))


def main():
    build_design_dossier(OUT / "solar_watch_p2_design_dossier_revA.pdf")
    build_drawings(OUT / "solar_watch_p2_custom_part_drawings_revA.pdf")
    build_procurement(OUT / "solar_watch_p2_procurement_test_revA.pdf")
    pdfs = sorted(OUT.glob("solar_watch_p2_*_revA.pdf"))
    (OUT / "SHA256SUMS.txt").write_text(
        "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in pdfs),
        encoding="utf-8",
    )
    print("\n".join(str(path) for path in pdfs))


if __name__ == "__main__":
    sys.exit(main())
