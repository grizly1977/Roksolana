#!/usr/bin/env python3
"""Generate Roksolana order PDF — English only (Cyrillic not supported by default fonts)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Flowable

CATS = [
    {
        "id": "wool", "name": "WOOL",
        "items": [
            {"p": "Dog Wool Socks",    "s": "L/XL", "q": 50,  "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Dog Wool Socks",    "s": "S/M",  "q": 100, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Rabbit Wool Socks", "s": "L/XL", "q": 50,  "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Rabbit Wool Socks", "s": "S/M",  "q": 100, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Yak Wool Socks",    "s": "L/XL", "q": 75,  "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Yak Wool Socks",    "s": "S/M",  "q": 100, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Alpaca Wool Socks", "s": "L/XL", "q": 100, "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Alpaca Wool Socks", "s": "S/M",  "q": 140, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Bear Wool Socks",   "s": "L/XL", "q": 100, "u": "dz", "n": False, "c": [], "note": "As per previous order"},
            {"p": "Bear Wool Socks",   "s": "S/M",  "q": 100, "u": "dz", "n": False, "c": [], "note": "As per previous order"},
            {"p": "Mink Wool Socks",   "s": "L/XL", "q": 25,  "u": "dz", "n": True,  "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Mink Wool Socks",   "s": "S/M",  "q": 25,  "u": "dz", "n": True,  "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Camel Wool Socks",  "s": "L/XL", "q": 25,  "u": "dz", "n": True,  "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Camel Wool Socks",  "s": "S/M",  "q": 25,  "u": "dz", "n": True,  "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Bison Wool Socks",  "s": "L/XL", "q": 50,  "u": "dz", "n": True,  "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Bison Wool Socks",  "s": "S/M",  "q": 50,  "u": "dz", "n": True,  "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
        ]
    },
    {
        "id": "cotton", "name": "ZHYTOMYR COTTON",
        "items": [
            {"p": "Zhytomyr Cotton", "s": "L/XL", "q": 240, "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Zhytomyr Cotton", "s": "S/M",  "q": 60,  "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#1C2C5F","Pantone 655"),("#3D1A5C","Pantone 2695")]},
        ]
    },
    {
        "id": "diab", "name": "DIABETIC",
        "items": [
            {"p": "Diabetic Mesh",          "s": "OneSize", "q": 50,  "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#FFFFFF","Classic White")]},
            {"p": "Diabetic Cotton",        "s": "S/M",     "q": 200, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Diabetic Cotton",        "s": "M/L",     "q": 400, "u": "dz", "n": False, "c": [("#111111","Black"),("#4880A0","Steel Blue"),("#907050","Brown"),("#F5F5F5","White"),("#D8C8A0","Beige"),("#C0C0C0","Light Grey")]},
            {"p": "Diabetic Cotton",        "s": "L/XL",    "q": 400, "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Diabetic Cotton - Black","s": "S/M",     "q": 50,  "u": "dz", "n": False, "c": [("#111111","Black")]},
            {"p": "Diabetic Cotton - Black","s": "M/L",     "q": 100, "u": "dz", "n": False, "c": [("#111111","Black")]},
            {"p": "Diabetic Cotton - Black","s": "L/XL",    "q": 100, "u": "dz", "n": False, "c": [("#111111","Black")]},
            {"p": "Diabetic Lavender",      "s": "S/M",     "q": 50,  "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Diabetic Lavender",      "s": "M/L",     "q": 100, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Diabetic Lavender",      "s": "L/XL",    "q": 100, "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
        ]
    },
    {
        "id": "tights", "name": "TIGHTS",
        "items": [
            {"p": "Wool Tights",   "s": "M",   "q": 120, "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Wool Tights",   "s": "L",   "q": 180, "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Wool Tights",   "s": "XL",  "q": 250, "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Wool Tights",   "s": "2XL", "q": 250, "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Wool Tights",   "s": "3XL", "q": 250, "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Wool Tights",   "s": "4XL", "q": 250, "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Bamboo Tights", "s": "M",   "q": 30,  "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Bamboo Tights", "s": "L",   "q": 50,  "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Bamboo Tights", "s": "XL",  "q": 80,  "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Bamboo Tights", "s": "2XL", "q": 80,  "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Bamboo Tights", "s": "3XL", "q": 80,  "u": "pcs", "n": True,  "c": [("#111111","Black")]},
            {"p": "Bamboo Tights", "s": "4XL", "q": 80,  "u": "pcs", "n": True,  "c": [("#111111","Black")]},
        ]
    },
]

DARK   = colors.HexColor("#070710")
GOLD   = colors.HexColor("#D4A853")
WHITE  = colors.white
TEXT   = colors.HexColor("#1A1A2E")
TEXT2  = colors.HexColor("#5A5A78")
TEXT3  = colors.HexColor("#9898B0")
BORDER = colors.HexColor("#E4E4EC")
BG     = colors.HexColor("#F4F5F8")

def hex_to_color(h):
    h = h.lstrip("#")
    r, g, b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    return colors.Color(r, g, b)


class SwatchRow(Flowable):
    def __init__(self, color_list, note=None, dia=4.5*mm, gap=1.8*mm):
        super().__init__()
        self.color_list = color_list
        self.note = note
        self.dia = dia
        self.gap = gap
        self.height = dia + 2*mm

    def wrap(self, aW, aH):
        self.width = aW
        return aW, self.height

    def draw(self):
        c = self.canv
        if self.note:
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColor(TEXT2)
            c.drawString(0, self.dia/2 - 2, self.note)
            return
        x = 0
        for (h, _) in self.color_list:
            col = hex_to_color(h)
            c.setFillColor(col)
            c.setStrokeColor(colors.HexColor("#BBBBBB"))
            c.setLineWidth(0.3)
            c.circle(x + self.dia/2, self.dia/2 + 1*mm, self.dia/2, fill=1, stroke=1)
            x += self.dia + self.gap


def build_pdf(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm,
        title="Roksolana - Order August 2026",
        author="Roksolana",
    )
    W = A4[0] - 30*mm
    story = []

    # ── Header ──────────────────────────────────────────────────────────
    brand_style = ParagraphStyle("brand", fontName="Helvetica",      fontSize=7,  textColor=GOLD, letterSpacing=4, leading=10)
    title_style = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, textColor=TEXT, leading=20)
    date_style  = ParagraphStyle("date",  fontName="Helvetica",      fontSize=9,  textColor=TEXT2, leading=12)

    hdr = Table([[Paragraph("ROKSOLANA", brand_style), Paragraph("August 2026", date_style)]],
                colWidths=[W*0.6, W*0.4])
    hdr.setStyle(TableStyle([
        ("ALIGN", (1,0), (1,0), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "BOTTOM"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(hdr)
    story.append(Paragraph("Order - August 2026", title_style))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=4*mm))

    # ── Categories ──────────────────────────────────────────────────────
    col_w = [W*0.38, W*0.10, W*0.12, W*0.40]

    cat_style  = ParagraphStyle("cat",  fontName="Helvetica-Bold", fontSize=9,   textColor=GOLD,  letterSpacing=2, leading=14)
    hdr_style  = ParagraphStyle("hdr",  fontName="Helvetica-Bold", fontSize=7,   textColor=TEXT3, letterSpacing=1, leading=10)
    prod_style = ParagraphStyle("prod", fontName="Helvetica-Bold", fontSize=8.5, textColor=TEXT,  leading=12)
    sz_style   = ParagraphStyle("sz",   fontName="Helvetica-Bold", fontSize=8,   textColor=TEXT2, leading=12)
    qty_style  = ParagraphStyle("qty",  fontName="Helvetica-Bold", fontSize=9,   textColor=TEXT,  leading=12)

    for cat in CATS:
        cat_row = Table([[Paragraph(cat["name"], cat_style), "", "", ""]], colWidths=col_w)
        cat_row.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), DARK),
            ("SPAN",         (0,0), (-1,-1)),
            ("TOPPADDING",   (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0), (-1,-1), 5),
            ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ]))
        story.append(cat_row)

        col_hdr = Table([[
            "",
            Paragraph("SIZE",     hdr_style),
            Paragraph("QTY",      hdr_style),
            Paragraph("COLORS",   hdr_style),
        ]], colWidths=col_w)
        col_hdr.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#F0F0F5")),
            ("TOPPADDING",   (0,0), (-1,-1), 3),
            ("BOTTOMPADDING",(0,0), (-1,-1), 3),
            ("LEFTPADDING",  (0,0), (-1,-1), 6),
            ("LINEBELOW",    (0,0), (-1,-1), 0.5, BORDER),
        ]))
        story.append(col_hdr)

        grouped = {}
        for r in cat["items"]:
            grouped.setdefault(r["p"], []).append(r)

        for pname, rows in grouped.items():
            is_new = rows[0].get("n", False)
            label  = pname + ("  + New" if is_new else "")
            bg     = colors.HexColor("#FDFAF3") if is_new else WHITE

            prod_row = Table([[Paragraph(label, prod_style), "", "", ""]], colWidths=col_w)
            prod_row.setStyle(TableStyle([
                ("BACKGROUND",   (0,0), (-1,-1), bg),
                ("SPAN",         (0,0), (-1,-1)),
                ("TOPPADDING",   (0,0), (-1,-1), 5),
                ("BOTTOMPADDING",(0,0), (-1,-1), 3),
                ("LEFTPADDING",  (0,0), (-1,-1), 6),
                ("LINEBELOW",    (0,0), (-1,-1), 0.3, BORDER),
            ]))
            story.append(prod_row)

            for r in rows:
                qty_para = Paragraph(
                    f"<b>{r['q']}</b> <font size='7' color='#9898B0'>{r['u']}</font>",
                    qty_style
                )
                row_tbl = Table([[
                    "",
                    Paragraph(r["s"], sz_style),
                    qty_para,
                    SwatchRow(r["c"], note=r.get("note")),
                ]], colWidths=col_w)
                row_tbl.setStyle(TableStyle([
                    ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#FFFDF5") if is_new else WHITE),
                    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
                    ("TOPPADDING",   (0,0), (-1,-1), 3),
                    ("BOTTOMPADDING",(0,0), (-1,-1), 3),
                    ("LEFTPADDING",  (0,0), (-1,-1), 6),
                    ("LINEBELOW",    (0,0), (-1,-1), 0.3, BORDER),
                ]))
                story.append(row_tbl)

        story.append(Spacer(1, 4*mm))

    # ── Totals footer ────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=2*mm, spaceAfter=4*mm))

    lbl_style = ParagraphStyle("tl", fontName="Helvetica-Bold", fontSize=7,  textColor=TEXT3, letterSpacing=1, leading=11)
    val_style = ParagraphStyle("tv", fontName="Helvetica-Bold", fontSize=14, textColor=WHITE, leading=18)

    wool_tot  = sum(r["q"] for r in CATS[0]["items"])
    diab_tot  = sum(r["q"] for r in CATS[2]["items"])
    cot_tot   = sum(r["q"] for r in CATS[1]["items"])
    woolT_tot = sum(r["q"] for r in CATS[3]["items"] if r["p"] == "Wool Tights")
    bambT_tot = sum(r["q"] for r in CATS[3]["items"] if r["p"] == "Bamboo Tights")

    cells = []
    for label, val, unit in [
        ("WOOL SOCKS",     wool_tot,  "dz"),
        ("DIABETIC",       diab_tot,  "dz"),
        ("ZHYTOMYR",       cot_tot,   "dz"),
        ("WOOL TIGHTS",    woolT_tot, "pcs"),
        ("BAMBOO TIGHTS",  bambT_tot, "pcs"),
    ]:
        inner = Table([
            [Paragraph(label, lbl_style)],
            [Paragraph(f"{val} <font size='9' color='#D4A853'>{unit}</font>", val_style)],
        ], colWidths=[W/5 - 2*mm])
        inner.setStyle(TableStyle([
            ("LEFTPADDING",  (0,0), (-1,-1), 5),
            ("TOPPADDING",   (0,0), (-1,-1), 3),
            ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ]))
        cells.append(inner)

    tot_tbl = Table([cells], colWidths=[W/5]*5)
    tot_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), DARK),
        ("BOX",          (0,0), (-1,-1), 0.5, GOLD),
        ("LINEAFTER",    (0,0), (-2,-1), 0.3, colors.HexColor("#333355")),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
    ]))
    story.append(tot_tbl)

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(TEXT3)
        canvas.drawRightString(A4[0]-15*mm, 8*mm,
                               f"Roksolana - Order August 2026 - p. {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved -> {path}")

if __name__ == "__main__":
    build_pdf("/home/user/Roksolana/order_preview.pdf")
