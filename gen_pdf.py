#!/usr/bin/env python3
"""Generate Roksolana order PDF preview."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import colorsys, os

# ── Data (mirrors order.html) ──────────────────────────────────────────────
CATS = [
    {
        "id": "wool", "name": "Шерсть",
        "items": [
            {"p": "Dog Wool Socks",    "s": "L/XL", "q": 50,  "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Dog Wool Socks",    "s": "S/M",  "q": 100, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Rabbit Wool Socks", "s": "L/XL", "q": 50,  "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Rabbit Wool Socks", "s": "S/M",  "q": 100, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Yak Wool Socks",    "s": "L/XL", "q": 75,  "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Yak Wool Socks",    "s": "S/M",  "q": 100, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Alpaca Wool Socks", "s": "L/XL", "q": 100, "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Alpaca Wool Socks", "s": "S/M",  "q": 140, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Bear Wool Socks",   "s": "L/XL", "q": 100, "u": "dz", "n": False, "c": [], "note": "По предыдущему заказу"},
            {"p": "Bear Wool Socks",   "s": "S/M",  "q": 100, "u": "dz", "n": False, "c": [], "note": "По предыдущему заказу"},
            {"p": "Mink Wool Socks",   "s": "L/XL", "q": 25,  "u": "dz", "n": True,  "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Mink Wool Socks",   "s": "S/M",  "q": 25,  "u": "dz", "n": True,  "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Camel Wool Socks",  "s": "L/XL", "q": 25,  "u": "dz", "n": True,  "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Camel Wool Socks",  "s": "S/M",  "q": 25,  "u": "dz", "n": True,  "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Bison Wool Socks",  "s": "L/XL", "q": 50,  "u": "dz", "n": True,  "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Bison Wool Socks",  "s": "S/M",  "q": 50,  "u": "dz", "n": True,  "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
        ]
    },
    {
        "id": "cotton", "name": "Житомир",
        "items": [
            {"p": "Zhytomyr Cotton", "s": "L/XL", "q": 240, "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Zhytomyr Cotton", "s": "S/M",  "q": 60,  "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#1C2C5F","Pantone 655"),("#3D1A5C","Pantone 2695")]},
        ]
    },
    {
        "id": "diab", "name": "Диабетические",
        "items": [
            {"p": "Diabetic Mesh",             "s": "OneSize", "q": 50,  "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#FFFFFF","Classic White")]},
            {"p": "Diabetic Cotton",            "s": "S/M",     "q": 200, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Diabetic Cotton",            "s": "M/L",     "q": 400, "u": "dz", "n": False, "c": [("#111111","Чёрный"),("#4880A0","Стальной синий"),("#907050","Коричневый"),("#F5F5F5","Белый"),("#D8C8A0","Бежевый"),("#C0C0C0","Светло-серый")]},
            {"p": "Diabetic Cotton",            "s": "L/XL",    "q": 400, "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
            {"p": "Diabetic Cotton · Чёрный",  "s": "S/M",     "q": 50,  "u": "dz", "n": False, "c": [("#111111","Чёрный")]},
            {"p": "Diabetic Cotton · Чёрный",  "s": "M/L",     "q": 100, "u": "dz", "n": False, "c": [("#111111","Чёрный")]},
            {"p": "Diabetic Cotton · Чёрный",  "s": "L/XL",    "q": 100, "u": "dz", "n": False, "c": [("#111111","Чёрный")]},
            {"p": "Diabetic Lavender",          "s": "S/M",     "q": 50,  "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Diabetic Lavender",          "s": "M/L",     "q": 100, "u": "dz", "n": False, "c": [("#FFFFFF","Classic White"),("#0A0A0A","Jet Black"),("#9E9E9E","Grey Heather"),("#879884","Sage Green"),("#E6E6FA","Soft Lavender"),("#AAF0D1","Mint")]},
            {"p": "Diabetic Lavender",          "s": "L/XL",    "q": 100, "u": "dz", "n": False, "c": [("#231F20","Process Black"),("#1C2C5F","Pantone 655"),("#717073","Pantone 7540"),("#4A5769","Pantone 7546")]},
        ]
    },
    {
        "id": "tights", "name": "Колготки",
        "items": [
            {"p": "Wool Tights",   "s": "M",   "q": 120, "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Wool Tights",   "s": "L",   "q": 180, "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Wool Tights",   "s": "XL",  "q": 250, "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Wool Tights",   "s": "2XL", "q": 250, "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Wool Tights",   "s": "3XL", "q": 250, "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Wool Tights",   "s": "4XL", "q": 250, "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Bamboo Tights", "s": "M",   "q": 30,  "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Bamboo Tights", "s": "L",   "q": 50,  "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Bamboo Tights", "s": "XL",  "q": 80,  "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Bamboo Tights", "s": "2XL", "q": 80,  "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Bamboo Tights", "s": "3XL", "q": 80,  "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
            {"p": "Bamboo Tights", "s": "4XL", "q": 80,  "u": "шт", "n": True,  "c": [("#111111","Чёрный")]},
        ]
    },
]

# ── Colours ────────────────────────────────────────────────────────────────
DARK   = colors.HexColor("#070710")
GOLD   = colors.HexColor("#D4A853")
GOLD2  = colors.HexColor("#F0C870")
BG     = colors.HexColor("#F4F5F8")
WHITE  = colors.white
TEXT   = colors.HexColor("#1A1A2E")
TEXT2  = colors.HexColor("#5A5A78")
TEXT3  = colors.HexColor("#9898B0")
BORDER = colors.HexColor("#E4E4EC")

def hex_to_color(h):
    h = h.lstrip("#")
    r, g, b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    return colors.Color(r, g, b)

# ── Custom flowable: colour swatch row ─────────────────────────────────────
class SwatchRow(Flowable):
    def __init__(self, color_list, note=None, dia=5*mm, gap=2*mm):
        super().__init__()
        self.color_list = color_list   # list of (hex, name)
        self.note = note
        self.dia = dia
        self.gap = gap
        self.width = 0
        self.height = dia + 2*mm

    def wrap(self, aW, aH):
        self.width = aW
        return aW, self.height

    def draw(self):
        c = self.canv
        if self.note:
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColor(TEXT2)
            c.drawString(0, self.dia/2 - 3, self.note)
            return
        x = 0
        for (h, name) in self.color_list:
            col = hex_to_color(h)
            # circle
            c.setFillColor(col)
            c.setStrokeColor(colors.HexColor("#CCCCCC"))
            c.setLineWidth(0.3)
            c.circle(x + self.dia/2, self.dia/2 + 1*mm, self.dia/2, fill=1, stroke=1)
            x += self.dia + self.gap

# ── Build PDF ──────────────────────────────────────────────────────────────
def build_pdf(path):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm,
        title="Roksolana · Заказ Август 2026",
        author="Roksolana",
    )

    W = A4[0] - 30*mm   # usable width

    styles = getSampleStyleSheet()
    story  = []

    # ── Header ──────────────────────────────────────────────────────────
    brand_style = ParagraphStyle("brand", fontName="Helvetica", fontSize=7,
                                 textColor=GOLD, letterSpacing=4, leading=10)
    title_style = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16,
                                 textColor=TEXT, leading=20)
    date_style  = ParagraphStyle("date",  fontName="Helvetica", fontSize=9,
                                 textColor=TEXT2, leading=12)

    hdr_data = [[
        Paragraph("ROKSOLANA", brand_style),
        Paragraph("Август 2026", date_style),
    ]]
    hdr_tbl = Table(hdr_data, colWidths=[W*0.6, W*0.4])
    hdr_tbl.setStyle(TableStyle([
        ("ALIGN",      (0,0), (0,0), "LEFT"),
        ("ALIGN",      (1,0), (1,0), "RIGHT"),
        ("VALIGN",     (0,0), (-1,-1), "BOTTOM"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(hdr_tbl)
    story.append(Paragraph("Заказ · Август 2026", title_style))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=4*mm))

    # ── Per category ────────────────────────────────────────────────────
    cat_style  = ParagraphStyle("cat",  fontName="Helvetica-Bold", fontSize=9,
                                textColor=GOLD, letterSpacing=3, leading=14,
                                backColor=DARK, borderPad=3)
    prod_style = ParagraphStyle("prod", fontName="Helvetica-Bold", fontSize=8.5,
                                textColor=TEXT, leading=12)
    new_style  = ParagraphStyle("new",  fontName="Helvetica-Bold", fontSize=7,
                                textColor=GOLD)
    sz_style   = ParagraphStyle("sz",   fontName="Helvetica-Bold", fontSize=8,
                                textColor=TEXT2)
    qty_style  = ParagraphStyle("qty",  fontName="Helvetica-Bold", fontSize=9,
                                textColor=TEXT)
    unit_style = ParagraphStyle("unit", fontName="Helvetica", fontSize=7,
                                textColor=TEXT3)

    col_w = [W*0.38, W*0.10, W*0.12, W*0.40]  # product, size, qty, swatches

    for cat in CATS:
        # Category header row
        cat_para = Paragraph(cat["name"].upper(), cat_style)
        cat_row  = Table([[cat_para, "", "", ""]], colWidths=col_w)
        cat_row.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,-1), DARK),
            ("SPAN",        (0,0), (-1,-1)),
            ("TEXTCOLOR",   (0,0), (-1,-1), GOLD),
            ("TOPPADDING",  (0,0), (-1,-1), 4),
            ("BOTTOMPADDING",(0,0), (-1,-1), 4),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(cat_row)

        # Group by product name
        seen = {}
        for r in cat["items"]:
            seen.setdefault(r["p"], []).append(r)

        for pname, rows in seen.items():
            is_new = rows[0].get("n", False)

            # Product name header
            prod_text = pname
            if is_new:
                prod_text += "  ✦ Новинка"
            prod_row = Table(
                [[Paragraph(prod_text, prod_style), "", "", ""]],
                colWidths=col_w
            )
            bg = colors.HexColor("#FDFAF3") if is_new else WHITE
            prod_row.setStyle(TableStyle([
                ("BACKGROUND",  (0,0), (-1,-1), bg),
                ("SPAN",        (0,0), (-1,-1)),
                ("TOPPADDING",  (0,0), (-1,-1), 5),
                ("BOTTOMPADDING",(0,0), (-1,-1), 3),
                ("LEFTPADDING", (0,0), (-1,-1), 6),
                ("LINEBELOW",   (0,0), (-1,-1), 0.3, BORDER),
            ]))
            story.append(prod_row)

            for r in rows:
                note = r.get("note")
                swatches = SwatchRow(r["c"], note=note, dia=4.5*mm, gap=1.8*mm)

                qty_para = Paragraph(
                    f"<b>{r['q']}</b> <font size='7' color='#9898B0'>{r['u']}</font>",
                    ParagraphStyle("q2", fontName="Helvetica-Bold", fontSize=9, textColor=TEXT, leading=12)
                )

                row_data = [[
                    "",
                    Paragraph(r["s"], sz_style),
                    qty_para,
                    swatches,
                ]]
                row_tbl = Table(row_data, colWidths=col_w)
                row_bg = colors.HexColor("#FFFDF5") if is_new else WHITE
                row_tbl.setStyle(TableStyle([
                    ("BACKGROUND",   (0,0), (-1,-1), row_bg),
                    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
                    ("TOPPADDING",   (0,0), (-1,-1), 3),
                    ("BOTTOMPADDING",(0,0), (-1,-1), 3),
                    ("LEFTPADDING",  (0,0), (-1,-1), 6),
                    ("LINEBELOW",    (0,0), (-1,-1), 0.3, BORDER),
                ]))
                story.append(row_tbl)

        story.append(Spacer(1, 4*mm))

    # ── Footer totals ────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=2*mm, spaceAfter=4*mm))
    totals_label = ParagraphStyle("tl", fontName="Helvetica-Bold", fontSize=8,
                                  textColor=TEXT2, letterSpacing=2, leading=12)
    totals_val   = ParagraphStyle("tv", fontName="Helvetica-Bold", fontSize=14,
                                  textColor=TEXT, leading=18)

    wool_tot   = sum(r["q"] for r in CATS[0]["items"])
    diab_tot   = sum(r["q"] for r in CATS[2]["items"])
    cotton_tot = sum(r["q"] for r in CATS[1]["items"])
    woolT_tot  = sum(r["q"] for r in CATS[3]["items"] if r["p"] == "Wool Tights")
    bambT_tot  = sum(r["q"] for r in CATS[3]["items"] if r["p"] == "Bamboo Tights")

    def tot_cell(label, val, unit):
        return [Paragraph(label.upper(), totals_label),
                Paragraph(f"{val} <font size='9' color='#9898B0'>{unit}</font>", totals_val)]

    tot_data = [
        [tot_cell("Шерсть",            wool_tot,   "dz"),
         tot_cell("Диабетические",     diab_tot,   "dz"),
         tot_cell("Житомир",           cotton_tot, "dz"),
         tot_cell("Колготки шерсть",   woolT_tot,  "шт"),
         tot_cell("Колготки бамбук",   bambT_tot,  "шт")],
    ]

    # Flatten: each cell is a list of 2 paragraphs → put in nested table
    flat = []
    for cell_pair in tot_data[0]:
        inner = Table([[cell_pair[0]], [cell_pair[1]]], colWidths=[W/5 - 3*mm])
        inner.setStyle(TableStyle([
            ("LEFTPADDING",  (0,0), (-1,-1), 4),
            ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ("TOPPADDING",   (0,0), (-1,-1), 2),
            ("BOTTOMPADDING",(0,0), (-1,-1), 2),
        ]))
        flat.append(inner)

    tot_tbl = Table([flat], colWidths=[W/5]*5)
    tot_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), DARK),
        ("BOX",          (0,0), (-1,-1), 0.5, GOLD),
        ("LINEAFTER",    (0,0), (-2,-1), 0.3, colors.HexColor("#333355")),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("TEXTCOLOR",    (0,0), (-1,-1), WHITE),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [DARK]),
    ]))
    story.append(tot_tbl)

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(TEXT3)
        canvas.drawRightString(A4[0] - 15*mm, 8*mm,
                               f"Roksolana · Заказ Август 2026 · стр. {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved → {path}")

if __name__ == "__main__":
    build_pdf("/home/user/Roksolana/order_preview.pdf")
