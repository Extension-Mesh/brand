from pathlib import Path

from fontTools.ttLib import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLTTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "build/ExtensionMesh-Brand-Guide-v0.1.pdf"
TMP = ROOT / "build/fonts"
LOGO_DIR = ROOT / "build/raster"

W, H = 960, 540
M = 42

NAVY = HexColor("#0F1B2E")
TEAL = HexColor("#00AFC1")
WARM = HexColor("#F7F7F4")
WHITE = HexColor("#FFFFFF")
SLATE = HexColor("#667286")
MIST = HexColor("#E9EDF0")
LINE = HexColor("#D9DEE5")
PALE_TEAL = HexColor("#E4F8FA")
SOFT_NAVY = HexColor("#1B2A40")


def convert_font(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return
    font = TTFont(str(source))
    font.flavor = None
    font.save(str(target))


def register_fonts() -> None:
    font_sources = {
        "Geologica": Path(
            ROOT
            / "node_modules/@fontsource/geologica/files/"
            "geologica-latin-500-normal.woff"
        ),
        "Plex": Path(
            ROOT
            / "node_modules/@fontsource/ibm-plex-sans/files/"
            "ibm-plex-sans-latin-400-normal.woff"
        ),
        "Plex-Semi": Path(
            ROOT
            / "node_modules/@fontsource/ibm-plex-sans/files/"
            "ibm-plex-sans-latin-600-normal.woff"
        ),
        "Plex-Mono": Path(
            ROOT
            / "node_modules/@fontsource/ibm-plex-mono/files/"
            "ibm-plex-mono-latin-500-normal.woff"
        ),
    }
    for name, source in font_sources.items():
        target = TMP / f"{name}.ttf"
        convert_font(source, target)
        pdfmetrics.registerFont(RLTTFont(name, str(target)))
    pdfmetrics.registerFontFamily(
        "Plex",
        normal="Plex",
        bold="Plex-Semi",
        italic="Plex",
        boldItalic="Plex-Semi",
    )


def para(
    c: canvas.Canvas,
    text: str,
    x: float,
    y_top: float,
    width: float,
    *,
    font: str = "Plex",
    size: float = 12,
    leading: float | None = None,
    color=NAVY,
    align=TA_LEFT,
) -> float:
    style = ParagraphStyle(
        "p",
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.45,
        textColor=color,
        alignment=align,
        spaceAfter=0,
        spaceBefore=0,
    )
    p = Paragraph(text, style)
    _, h = p.wrap(width, H)
    p.drawOn(c, x, y_top - h)
    return h


def label(c: canvas.Canvas, text: str, x: float, y: float, color=TEAL) -> None:
    c.setFillColor(color)
    c.setFont("Plex-Mono", 8.5)
    c.drawString(x, y, text.upper())


def page_header(c: canvas.Canvas, number: int, section: str, title: str) -> None:
    c.setFillColor(WARM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    label(c, f"{number:02d}  {section}", M, H - 37)
    c.setFillColor(SLATE)
    c.setFont("Plex-Mono", 8.5)
    c.drawRightString(W - M, H - 37, "EXTENSIONMESH  /  BRAND FOUNDATIONS V0.1")
    c.setFillColor(NAVY)
    c.setFont("Geologica", 27)
    c.drawString(M, H - 77, title)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(M, H - 94, W - M, H - 94)


def footer(c: canvas.Canvas, number: int) -> None:
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(M, 30, W - M, 30)
    c.setFillColor(SLATE)
    c.setFont("Plex", 7.8)
    c.drawString(M, 16, "Open extension distribution.")
    c.setFont("Plex-Mono", 7.8)
    c.drawRightString(W - M, 16, f"{number:02d}")


def card(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill=WHITE) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 14, fill=1, stroke=1)


def dot(c: canvas.Canvas, x: float, y: float, r: float = 3) -> None:
    c.setFillColor(TEAL)
    c.circle(x, y, r, fill=1, stroke=0)


def draw_logo(c: canvas.Canvas, reversed_logo: bool, x: float, y: float, w: float) -> None:
    name = (
        "extensionmesh-logo-horizontal-reversed-1600.png"
        if reversed_logo
        else "extensionmesh-logo-horizontal-1600.png"
    )
    img = ImageReader(str(LOGO_DIR / name))
    c.drawImage(img, x, y, width=w, height=w * 219 / 1600, mask="auto")


def draw_mark(c: canvas.Canvas, reversed_mark: bool, x: float, y: float, size: float) -> None:
    name = (
        "extensionmesh-mark-reversed-512.png"
        if reversed_mark
        else "extensionmesh-mark-color-512.png"
    )
    img = ImageReader(str(LOGO_DIR / name))
    c.drawImage(img, x, y, width=size, height=size, mask="auto")


def page_cover(c: canvas.Canvas) -> None:
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(SOFT_NAVY)
    c.roundRect(650, -70, 380, 380, 110, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.roundRect(810, 300, 118, 118, 34, fill=1, stroke=0)
    draw_logo(c, True, M, H - 92, 315)
    label(c, "Brand foundations  /  v0.1", M, H - 132, HexColor("#9BE9EF"))
    c.setFillColor(WARM)
    c.setFont("Geologica", 45)
    c.drawString(M, 264, "Open extension")
    c.drawString(M, 211, "distribution.")
    para(
        c,
        "A practical identity system for an open project: clear enough for "
        "documentation, distinctive enough for a public ecosystem.",
        M,
        166,
        470,
        size=14,
        leading=21,
        color=HexColor("#B9C3D0"),
    )
    c.setFillColor(HexColor("#9BE9EF"))
    c.setFont("Plex-Mono", 8.5)
    c.drawString(M, 38, "CONNECTED MODULES  /  JULY 2026")
    c.showPage()


def page_brand_core(c: canvas.Canvas) -> None:
    page_header(c, 2, "Brand core", "What ExtensionMesh stands for")
    para(
        c,
        "<b>ExtensionMesh is an open project for practical extension "
        "distribution through independent registries.</b>",
        M,
        H - 126,
        480,
        font="Plex",
        size=17,
        leading=25,
    )
    para(
        c,
        "The first implementation connects independent registries with "
        "Shopware. Future connectors should be presented as concrete "
        "implementations, not as proof of a universal protocol.",
        M,
        H - 205,
        480,
        size=11.5,
        leading=18,
        color=SLATE,
    )
    label(c, "Public claim", M, 226)
    c.setFont("Geologica", 26)
    c.setFillColor(NAVY)
    c.drawString(M, 184, "Open extension distribution.")

    principles = [
        ("Open by default", "Public, accessible and designed for participation."),
        ("Practical first", "Explain what works today before describing the future."),
        ("Neutral voice", "No enemy narrative, no rebellion language, no sales pitch."),
        ("Connector-ready", "Grow through specific integrations with explicit scope."),
    ]
    positions = [(570, 308), (756, 308), (570, 142), (756, 142)]
    for (title, text), (x, y) in zip(principles, positions):
        card(c, x, y, 166, 142)
        dot(c, x + 18, y + 116)
        c.setFont("Plex-Semi", 11)
        c.setFillColor(NAVY)
        c.drawString(x + 31, y + 112, title)
        para(c, text, x + 18, y + 88, 130, size=9.2, leading=14, color=SLATE)
    footer(c, 2)
    c.showPage()


def page_logo(c: canvas.Canvas) -> None:
    page_header(c, 3, "Logo system", "One mark, one calm wordmark")
    card(c, M, 265, 547, 150)
    label(c, "Primary on light", M + 22, 390, NAVY)
    draw_logo(c, False, M + 22, 308, 460)

    c.setFillColor(NAVY)
    c.roundRect(610, 265, 308, 150, 14, fill=1, stroke=0)
    label(c, "Primary on dark", 632, 390, HexColor("#9BE9EF"))
    draw_logo(c, True, 632, 313, 258)

    label(c, "Construction rules", M, 232)
    rules = [
        "The symbol carries the distinctive behavior.",
        "The M remains conventional and unmodified.",
        "The name is always written as one word.",
        "Clear space equals one terminal module.",
    ]
    for i, text in enumerate(rules):
        y = 199 - i * 31
        dot(c, M + 3, y + 3, 2.5)
        c.setFillColor(NAVY)
        c.setFont("Plex", 10.2)
        c.drawString(M + 16, y, text)

    label(c, "Small-size behavior", 533, 232)
    sizes = [(64, 533, 143), (32, 640, 159), (16, 725, 167)]
    for size, x, y in sizes:
        draw_mark(c, False, x, y, size)
        c.setFillColor(SLATE)
        c.setFont("Plex-Mono", 8)
        c.drawCentredString(x + size / 2, 126, f"{size} px")
    para(
        c,
        "Use the monochrome mark below 48 px when the accent no longer reads cleanly.",
        800,
        203,
        118,
        size=8.5,
        leading=12.5,
        color=SLATE,
    )
    footer(c, 3)
    c.showPage()


def page_color(c: canvas.Canvas) -> None:
    page_header(c, 4, "Color", "A restrained palette with one active accent")
    swatches = [
        ("Mesh Navy", "#0F1B2E", "Primary text, dark surfaces", NAVY),
        ("Signal Teal", "#00AFC1", "Accent, state, connection", TEAL),
        ("Warm White", "#F7F7F4", "Default canvas", WARM),
        ("Surface", "#FFFFFF", "Cards and raised areas", WHITE),
        ("Slate", "#667286", "Secondary copy", SLATE),
        ("Mist", "#E9EDF0", "Quiet backgrounds", MIST),
    ]
    for idx, (name, code, use, color) in enumerate(swatches):
        row, col = divmod(idx, 3)
        x = M + col * 296
        y = 285 - row * 150
        c.setFillColor(color)
        c.setStrokeColor(LINE)
        c.roundRect(x, y + 52, 264, 76, 12, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Plex-Semi", 10)
        c.drawString(x, y + 31, name)
        c.setFont("Plex-Mono", 8.5)
        c.drawRightString(x + 264, y + 31, code)
        c.setFillColor(SLATE)
        c.setFont("Plex", 8.8)
        c.drawString(x, y + 10, use)

    c.setFillColor(NAVY)
    c.roundRect(M, 65, 876, 54, 12, fill=1, stroke=0)
    c.setFillColor(WARM)
    c.setFont("Plex", 9.2)
    c.drawString(M + 18, 96, "Contrast")
    c.setFont("Plex-Mono", 8.2)
    c.drawString(M + 93, 96, "Navy / Warm 16.08:1")
    c.drawString(M + 255, 96, "Teal / Navy 6.50:1")
    c.drawString(M + 413, 96, "Slate / Warm 4.53:1")
    c.setFillColor(HexColor("#9BE9EF"))
    c.drawString(M + 590, 96, "Do not use teal for body text on light.")
    footer(c, 4)
    c.showPage()


def page_type(c: canvas.Canvas) -> None:
    page_header(c, 5, "Typography", "Character where it matters, neutrality where it helps")
    card(c, M, 268, 530, 148)
    label(c, "Display  /  Geologica Medium", M + 20, 391, NAVY)
    c.setFillColor(NAVY)
    c.setFont("Geologica", 36)
    c.drawString(M + 20, 335, "Connected systems")
    c.setFont("Geologica", 19)
    c.drawString(M + 22, 299, "Headlines, key statements, campaign moments")

    card(c, 590, 268, 328, 148)
    label(c, "Interface  /  IBM Plex Sans", 610, 391, NAVY)
    para(
        c,
        "Readable documentation and interfaces need a calm workhorse. "
        "Use regular for copy and semibold for navigation or controls.",
        610,
        359,
        270,
        size=11,
        leading=17,
    )

    card(c, M, 87, 385, 151)
    label(c, "Technical  /  IBM Plex Mono Medium", M + 20, 213, NAVY)
    c.setFillColor(NAVY)
    c.setFont("Plex-Mono", 10.5)
    c.drawString(M + 20, 174, "registry.connect(source)")
    c.setFillColor(TEAL)
    c.drawString(M + 20, 148, "STATUS  CONNECTED")
    c.setFillColor(SLATE)
    c.setFont("Plex", 8.8)
    c.drawString(M + 20, 117, "Labels, versions, status, code and metadata only.")

    label(c, "Recommended scale", 470, 223)
    scale = [
        ("Display", "56 / 64", "Geologica 500"),
        ("H1", "40 / 48", "Geologica 500"),
        ("H2", "28 / 36", "Geologica 500"),
        ("Body", "16 / 26", "Plex Sans 400"),
        ("Label", "13 / 18", "Plex Mono 500"),
    ]
    for i, (role, size, font) in enumerate(scale):
        y = 197 - i * 27
        c.setFillColor(NAVY)
        c.setFont("Plex-Semi", 8.8)
        c.drawString(470, y, role)
        c.setFont("Plex-Mono", 8.3)
        c.drawString(570, y, size)
        c.setFillColor(SLATE)
        c.drawString(654, y, font)
    footer(c, 5)
    c.showPage()


def page_layout(c: canvas.Canvas) -> None:
    page_header(c, 6, "Layout language", "Modular, spacious and visibly connected")
    left_x, left_y, left_w, left_h = M, 91, 547, 326
    card(c, left_x, left_y, left_w, left_h)
    label(c, "Example composition", left_x + 20, left_y + left_h - 29, NAVY)
    for i in range(1, 12):
        x = left_x + 20 + i * 42
        c.setStrokeColor(HexColor("#EEF1F4"))
        c.line(x, left_y + 20, x, left_y + left_h - 50)
    c.setFillColor(NAVY)
    c.roundRect(left_x + 20, left_y + 154, 314, 93, 18, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.roundRect(left_x + 41, left_y + 210, 18, 18, 6, fill=1, stroke=0)
    c.setFillColor(WARM)
    c.setFont("Geologica", 20)
    c.drawString(left_x + 72, left_y + 205, "A clear primary idea")
    c.setFillColor(HexColor("#B9C3D0"))
    c.setFont("Plex", 8.5)
    c.drawString(left_x + 72, left_y + 182, "Support it with one quiet explanatory layer.")
    c.setStrokeColor(LINE)
    c.roundRect(left_x + 20, left_y + 42, 150, 84, 14, fill=0, stroke=1)
    c.roundRect(left_x + 187, left_y + 42, 150, 84, 14, fill=0, stroke=1)
    c.roundRect(left_x + 354, left_y + 42, 150, 84, 14, fill=0, stroke=1)
    for x in (left_x + 36, left_x + 203, left_x + 370):
        dot(c, x, left_y + 101, 3)
        c.setFillColor(NAVY)
        c.setFont("Plex-Semi", 8.5)
        c.drawString(x + 12, left_y + 98, "Module")
        c.setFillColor(SLATE)
        c.setFont("Plex", 7.5)
        c.drawString(x, left_y + 70, "One role per surface.")

    rules = [
        ("8 pt grid", "Use multiples of eight for structure and rhythm."),
        ("Open space", "Prefer fewer, larger regions over dense dashboards."),
        ("Soft geometry", "16-24 px radii, thin borders, almost no shadow."),
        ("One accent", "Teal marks state or connection, never decoration."),
        ("Visible joints", "Lines and nodes may connect modules sparingly."),
    ]
    x = 625
    label(c, "System rules", x, 395)
    for i, (title, text) in enumerate(rules):
        y = 352 - i * 62
        dot(c, x + 3, y + 7, 2.5)
        c.setFillColor(NAVY)
        c.setFont("Plex-Semi", 9.5)
        c.drawString(x + 16, y + 4, title)
        c.setFillColor(SLATE)
        c.setFont("Plex", 8.5)
        c.drawString(x + 16, y - 15, text)
    footer(c, 6)
    c.showPage()


def page_voice(c: canvas.Canvas) -> None:
    page_header(c, 7, "Voice and language", "Clear technical language without ideology")
    columns = [
        (
            "Sound like",
            [
                "Direct and factual",
                "Open and collaborative",
                "Technically precise",
                "Confident without hype",
            ],
        ),
        (
            "Prefer",
            [
                "registry and connector",
                "extension distribution",
                "open project",
                "first implementation",
            ],
        ),
        (
            "Avoid",
            [
                "enemy or rebellion framing",
                "universal protocol claims",
                "marketplace killer language",
                "sales-led promises",
            ],
        ),
    ]
    for idx, (head, items) in enumerate(columns):
        x = M + idx * 296
        card(c, x, 260, 264, 153)
        label(c, head, x + 18, 387, NAVY)
        for i, item in enumerate(items):
            y = 354 - i * 27
            dot(c, x + 21, y + 3, 2.2)
            c.setFillColor(SLATE)
            c.setFont("Plex", 9.2)
            c.drawString(x + 33, y, item)

    label(c, "Approved message stack", M, 226)
    messages = [
        ("Claim", "Open extension distribution."),
        (
            "Short",
            "An open project for practical extension distribution through independent registries.",
        ),
        (
            "Implementation",
            "The first implementation connects independent registries with Shopware.",
        ),
    ]
    for i, (kind, text) in enumerate(messages):
        y = 185 - i * 49
        c.setFillColor(PALE_TEAL if i == 0 else WHITE)
        c.setStrokeColor(LINE)
        c.roundRect(M, y - 16, 876, 38, 10, fill=1, stroke=1)
        c.setFillColor(TEAL if i == 0 else SLATE)
        c.setFont("Plex-Mono", 8)
        c.drawString(M + 14, y - 1, kind.upper())
        c.setFillColor(NAVY)
        c.setFont("Plex-Semi" if i == 0 else "Plex", 9.5)
        c.drawString(M + 130, y - 1, text)
    footer(c, 7)
    c.showPage()


def page_applications(c: canvas.Canvas) -> None:
    page_header(c, 8, "Applications", "One system across web, docs and GitHub")
    # Website mockup
    c.setFillColor(NAVY)
    c.roundRect(M, 91, 518, 326, 16, fill=1, stroke=0)
    draw_logo(c, True, M + 20, 382, 200)
    c.setFillColor(HexColor("#24344A"))
    c.roundRect(M + 369, 380, 58, 18, 9, fill=1, stroke=0)
    c.roundRect(M + 438, 380, 57, 18, 9, fill=1, stroke=0)
    label(c, "Website hero", M + 24, 347, HexColor("#9BE9EF"))
    c.setFillColor(WARM)
    c.setFont("Geologica", 28)
    c.drawString(M + 24, 297, "Open extension")
    c.drawString(M + 24, 262, "distribution.")
    para(
        c,
        "Run a registry, publish extensions and connect them through "
        "dedicated integrations.",
        M + 24,
        233,
        330,
        size=10,
        leading=15,
        color=HexColor("#B9C3D0"),
    )
    c.setFillColor(TEAL)
    c.roundRect(M + 24, 143, 122, 34, 11, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Plex-Semi", 8.5)
    c.drawCentredString(M + 85, 155, "View documentation")
    c.setStrokeColor(HexColor("#52657C"))
    c.roundRect(M + 156, 143, 108, 34, 11, fill=0, stroke=1)
    c.setFillColor(WARM)
    c.drawCentredString(M + 210, 155, "Explore GitHub")

    # Docs and release examples
    card(c, 586, 249, 332, 168)
    label(c, "Documentation", 606, 391, NAVY)
    draw_logo(c, False, 606, 350, 144)
    c.setFillColor(MIST)
    c.roundRect(606, 278, 84, 52, 9, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Plex-Semi", 8.2)
    c.drawString(705, 316, "Connect a registry")
    c.setFillColor(SLATE)
    c.setFont("Plex", 7.5)
    c.drawString(705, 298, "Installation  /  Configuration  /  API")
    c.setStrokeColor(LINE)
    c.line(705, 284, 886, 284)

    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.roundRect(586, 91, 332, 140, 16, fill=1, stroke=1)
    label(c, "GitHub release card", 606, 205, NAVY)
    c.setFillColor(PALE_TEAL)
    c.roundRect(606, 151, 48, 30, 10, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Plex-Mono", 8)
    c.drawCentredString(630, 162, "V0.2")
    c.setFillColor(NAVY)
    c.setFont("Plex-Semi", 10)
    c.drawString(670, 170, "Connector improvements")
    c.setFillColor(SLATE)
    c.setFont("Plex", 8)
    c.drawString(670, 151, "Clear changes, migration notes and scope.")
    c.setFont("Plex-Mono", 7.5)
    c.drawString(606, 118, "OPEN SOURCE  /  RELEASED  /  DOCUMENTED")
    footer(c, 8)
    c.showPage()


def page_tokens(c: canvas.Canvas) -> None:
    page_header(c, 9, "Implementation", "Tokens first, components second")
    c.setFillColor(NAVY)
    c.roundRect(M, 108, 520, 310, 16, fill=1, stroke=0)
    label(c, "CSS foundation", M + 22, 390, HexColor("#9BE9EF"))
    code = [
        ":root {",
        "  --em-navy: #0F1B2E;",
        "  --em-teal: #00AFC1;",
        "  --em-warm: #F7F7F4;",
        "  --em-slate: #667286;",
        "  --em-mist: #E9EDF0;",
        "",
        "  --em-font-display: \"Geologica\";",
        "  --em-font-ui: \"IBM Plex Sans\";",
        "  --em-font-mono: \"IBM Plex Mono\";",
        "",
        "  --em-grid: 8px;",
        "  --em-radius: 16px;",
        "}",
    ]
    c.setFont("Plex-Mono", 9)
    for i, line in enumerate(code):
        c.setFillColor(TEAL if "--em-" in line else HexColor("#D8E0EA"))
        c.drawString(M + 22, 360 - i * 18, line)

    label(c, "Build order", 608, 395)
    steps = [
        ("01", "Foundations", "Fonts, colors, spacing and surfaces"),
        ("02", "Primitives", "Button, link, badge, card and code block"),
        ("03", "Navigation", "Website header and documentation shell"),
        ("04", "Patterns", "Hero, release card and connector overview"),
        ("05", "Templates", "Website, docs and repository assets"),
    ]
    for i, (num, title, text) in enumerate(steps):
        y = 350 - i * 59
        c.setFillColor(PALE_TEAL)
        c.roundRect(608, y - 4, 35, 35, 10, fill=1, stroke=0)
        c.setFillColor(TEAL)
        c.setFont("Plex-Mono", 8)
        c.drawCentredString(625.5, y + 8, num)
        c.setFillColor(NAVY)
        c.setFont("Plex-Semi", 9.5)
        c.drawString(658, y + 13, title)
        c.setFillColor(SLATE)
        c.setFont("Plex", 8.2)
        c.drawString(658, y - 4, text)

    c.setFillColor(NAVY)
    c.setFont("Geologica", 16)
    c.drawString(608, 76, "Next concrete artifact: website foundation.")
    footer(c, 9)
    c.showPage()


def build() -> None:
    register_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setTitle("ExtensionMesh Brand Foundations v0.1")
    c.setAuthor("ExtensionMesh")
    page_cover(c)
    page_brand_core(c)
    page_logo(c)
    page_color(c)
    page_type(c)
    page_layout(c)
    page_voice(c)
    page_applications(c)
    page_tokens(c)
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
