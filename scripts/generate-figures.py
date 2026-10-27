#!/usr/bin/env python3
"""Generate the book's SVG figures from a single visual system.

Outputs go to assets/figures/. The SVGs are vector, RTL, and use the
design-system palette. Arabic text is shaped by the renderer (Chrome,
Inkscape, or a browser-based PDF export).
"""

from __future__ import annotations

import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# Design system palette
NAVY = "#14213D"
TEAL = "#0F766E"
GOLD = "#C6A15B"
AMBER = "#B45309"
RED = "#B91C1C"
GREEN = "#15803D"
INK = "#1F2937"
MUTED = "#64748B"
PAPER = "#FFFFFF"
TINT = "#F8FAFC"
BORDER = "#E2E8F0"
STORY = "#FBF7EF"
IDEA = "#ECFDF5"
TRY = "#EEF2FF"
TIP = "#FFFBEB"
WARNING = "#FEF2F2"
EXERCISE = "#F0FDF4"

FONT = "'IBM Plex Sans Arabic','Segoe UI',Tahoma,Arial,sans-serif"


def esc(value: str) -> str:
    return escape(value)


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 24,
    fill: str = INK,
    weight: int = 400,
    anchor: str = "middle",
    line_height: float = 1.45,
    opacity: float = 1.0,
) -> str:
    """Emit RTL text.

    In RTL, SVG's logical ``start`` is the right edge. Use
    ``anchor="start"`` to right-align a block at ``x``; ``anchor="end"``
    aligns its left edge and will overflow rightward.
    """
    lines = value.split("\n")
    if len(lines) == 1:
        content = esc(value)
    else:
        spans = []
        for index, line in enumerate(lines):
            dy = 0 if index == 0 else size * line_height
            spans.append(
                f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>'
            )
        content = "".join(spans)
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
        f'opacity="{opacity}" direction="rtl" '
        f'style="direction:rtl;unicode-bidi:isolate">'
        + content
        + "</text>"
    )


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str = PAPER,
    stroke: str = BORDER,
    stroke_width: float = 2,
    rx: float = 14,
    dash: str | None = None,
    opacity: float = 1.0,
    shadow: bool = False,
) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    filt = ' filter="url(#softShadow)"' if shadow else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'opacity="{opacity}"{extra}{filt}/>'
    )


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    stroke: str = MUTED,
    width: float = 2.5,
    dash: str | None = None,
    marker: bool | str = True,
    opacity: float = 1.0,
) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    if marker is True:
        marker = "arrow"
    mark = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"'
        f'{extra}{mark}/>'
    )


def path(
    d: str,
    *,
    fill: str = "none",
    stroke: str = MUTED,
    width: float = 2.5,
    marker: bool | str = True,
    dash: str | None = None,
    opacity: float = 1.0,
) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    if marker is True:
        marker = "arrow"
    mark = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
        f'opacity="{opacity}"{extra}{mark}/>'
    )


def circle(
    cx: float,
    cy: float,
    r: float,
    *,
    fill: str = NAVY,
    stroke: str = "none",
    stroke_width: float = 2,
    opacity: float = 1.0,
) -> str:
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}"/>'
    )


def badge(cx: float, cy: float, label: str, *, fill: str = GOLD, r: float = 22) -> str:
    return (
        circle(cx, cy, r, fill=fill)
        + text(cx, cy + 8, label, size=22, fill=PAPER, weight=700)
    )


def svg(body: str, *, width: int = 1200, height: int = 700, title: str = "") -> str:
    aria = f'<title>{esc(title)}</title>' if title else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/>
    </marker>
    <marker id="arrowTeal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{TEAL}"/>
    </marker>
    <marker id="arrowGold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{GOLD}"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{RED}"/>
    </marker>
    <marker id="arrowTeal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{TEAL}"/>
    </marker>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="{NAVY}" flood-opacity="0.10"/>
    </filter>
  </defs>
  {aria}
  <rect width="{width}" height="{height}" fill="{PAPER}"/>
  {body}
</svg>
'''


def save(name: str, body: str, *, title: str = "", width: int = 1200, height: int = 700) -> None:
    (OUT / name).write_text(svg(body, width=width, height=height, title=title), encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------------------
# Figure 5-1: the six conversation steps (snake path with a return arrow)
# ---------------------------------------------------------------------------
def figure_5_1() -> None:
    w, h = 1200, 720
    parts: list[str] = []
    parts.append(text(600, 64, "خطوات المحادثة الست", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 106, "من النتيجة إلى المراجعة… ثم تعود لتحديث السياق", size=21, fill=MUTED))

    cards = [
        ("1", "النتيجة", "ماذا أريد أن أملك\nفي النهاية؟"),
        ("2", "السياق", "من أنا، ولمن النتيجة،\nوما الخلفية؟"),
        ("3", "الدور", "من أي زاوية\nتنظر؟"),
        ("4", "المهمة", "ما الفعل المطلوب\nبدقة؟"),
        ("5", "الصيغة", "بأي شكل وطول\nولغة؟"),
        ("6", "المراجعة", "ما الذي يحتاج\nتحققًا أو تحسينًا؟"),
    ]
    # RTL snake: 1 right, 2 middle, 3 left; 4 left, 5 middle, 6 right.
    positions = [(760, 190), (440, 190), (120, 190), (120, 430), (440, 430), (760, 430)]
    colors = [NAVY, TEAL, NAVY, TEAL, NAVY, TEAL]
    fills = [TRY, IDEA, TRY, IDEA, TRY, IDEA]

    for (num, title, sub), (x, y), color, fill in zip(cards, positions, colors, fills):
        parts.append(rect(x, y, 280, 180, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + 250, y + 34, num, fill=color, r=20))
        parts.append(text(x + 140, y + 62, title, size=29, weight=700, fill=color))
        parts.append(text(x + 140, y + 112, sub, size=19, fill=INK, line_height=1.5))

    # Horizontal arrows on the top row (right to left)
    parts.append(line(748, 280, 732, 280, stroke=TEAL, width=4))
    parts.append(line(428, 280, 412, 280, stroke=TEAL, width=4))
    # Down arrow from 3 to 4
    parts.append(path("M 260 378 C 260 410 260 410 260 420", stroke=TEAL, width=4))
    # Horizontal arrows on the bottom row (left to right)
    parts.append(line(412, 520, 428, 520, stroke=TEAL, width=4))
    parts.append(line(732, 520, 748, 520, stroke=TEAL, width=4))
    # Return arrow from 6 to 1, routed outside the cards along the right margin
    # and over the top row, so it never crosses card content.
    parts.append(
        path(
            "M 1045 520 L 1085 520 Q 1105 520 1105 500 "
            "L 1105 175 Q 1105 155 1085 155 L 925 155 "
            "Q 905 155 905 175 L 905 185",
            stroke=GOLD,
            width=4,
            dash="8 8",
        )
    )
    parts.append(text(1005, 143, "راجع وحدّث", size=19, fill=AMBER, weight=600))

    parts.append(text(600, 660, "الخطوات ليست خطًا مستقيمًا: يمكنك العودة إلى أي خطوة خلال الحوار.", size=20, fill=MUTED))
    save("fig-05-1.svg", "".join(parts), title="خطوات المحادثة الست", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 7-1: the four context layers
# ---------------------------------------------------------------------------
def figure_7_1() -> None:
    w, h = 1200, 760
    parts: list[str] = []
    parts.append(text(600, 64, "طبقات السياق الأربع", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 106, "من العام إلى الخاص… وداخل إطار من الحدود", size=21, fill=MUTED))

    # Boundary frame
    parts.append(rect(80, 160, 1040, 480, fill=WARNING, stroke=RED, stroke_width=3, rx=20, dash="12 8", opacity=0.55))
    parts.append(rect(930, 142, 150, 38, fill=PAPER, stroke=RED, stroke_width=2.5, rx=19))
    parts.append(text(1005, 169, "الحدود", size=22, weight=700, fill=RED))
    parts.append(text(1090, 207, "ما لا يُقال، وما لا يُرسل، وما لا يُنشر", size=18, fill=RED, anchor="start"))

    # Progression arrow on the left margin
    parts.append(text(120, 138, "من العام", size=18, fill=MUTED, weight=600))
    parts.append(path("M 120 176 L 120 624", stroke=MUTED, width=3))
    parts.append(text(120, 668, "إلى الخاص", size=18, fill=MUTED, weight=600))

    layers = [
        ("1", "الهوية", "من أنا؟ تخصصي، لغتي، جمهوري، أسلوبي.", NAVY, TRY),
        ("2", "المشروع", "ما المشروع؟ أهدافه، مصادره، مقياس نجاحه.", TEAL, IDEA),
        ("3", "المهمة الحالية", "ما المطلوب الآن؟ الصيغة، الطول، الموعد.", GOLD, TIP),
    ]
    y = 240
    for num, title, desc, color, fill in layers:
        parts.append(rect(190, y, 880, 105, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(rect(190, y, 14, 105, fill=color, stroke=color, rx=7))
        parts.append(badge(240, y + 52, num, fill=color, r=19))
        parts.append(text(1040, y + 45, title, size=28, weight=700, fill=color, anchor="start"))
        parts.append(text(1040, y + 81, desc, size=19, fill=INK, anchor="start"))
        y += 125

    parts.append(text(600, 715, "كلما اقتربت الطبقة من المهمة، صار السياق أدق… والحدود تمنع الانحراف.", size=20, fill=MUTED))
    save("fig-07-1.svg", "".join(parts), title="طبقات السياق الأربع", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 7-2: context vs memory vs knowledge base
# ---------------------------------------------------------------------------
def figure_7_2() -> None:
    w, h = 1200, 700
    parts: list[str] = []
    parts.append(text(600, 64, "السياق… الذاكرة… قاعدة المعرفة", size=36, weight=700, fill=NAVY))
    parts.append(text(600, 106, "ثلاثة أشياء يخلط بينها كثيرون", size=21, fill=MUTED))

    columns = [
        ("السياق", "ما تعطيه الآن", "أنت، في الطلب", "حزمة السياق\nأو النص المرفق", TEAL, IDEA),
        ("الذاكرة", "ما تحتفظ به بين المحادثات", "الأداة وإعداداتك", "«تذكر أنني\nأفضل العربية»", NAVY, TRY),
        ("قاعدة المعرفة", "مصادر خارجية يبحث فيها النظام", "أنت أو مؤسستك", "ملفات مشروع،\nويكي، مستندات", GOLD, TIP),
    ]
    x = 70
    for title, what, who, example, color, fill in columns:
        parts.append(rect(x, 170, 340, 430, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(circle(x + 170, 240, 44, fill=color))
        parts.append(text(x + 170, 252, "◆", size=30, fill=PAPER))
        parts.append(text(x + 170, 320, title, size=29, weight=700, fill=color))
        parts.append(text(x + 170, 365, what, size=19, fill=INK))
        parts.append(rect(x + 35, 395, 270, 2, fill=color, stroke=color, rx=0))
        parts.append(text(x + 170, 435, "من يتحكم؟", size=16, fill=MUTED, weight=600))
        parts.append(text(x + 170, 466, who, size=20, fill=INK, weight=600))
        parts.append(text(x + 170, 525, "مثال", size=16, fill=MUTED, weight=600))
        parts.append(text(x + 170, 558, example, size=19, fill=INK))
        x += 370

    parts.append(text(600, 660, "القاعدة: المؤقت في السياق، والمتكرر في الذاكرة، والمؤسسي في قاعدة المعرفة.", size=20, fill=MUTED))
    save("fig-07-2.svg", "".join(parts), title="السياق مقابل الذاكرة وقاعدة المعرفة", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 8-1: the five-step verification protocol
# ---------------------------------------------------------------------------
def figure_8_1() -> None:
    w, h = 1200, 820
    parts: list[str] = []
    parts.append(text(600, 62, "بروتوكول التحقق الخمسي", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "من الادعاء إلى قرار موثق", size=21, fill=MUTED))

    rows = [
        ("1", "استخرج", "ما الادعاءات القابلة للتحقق؟", "قائمة ادعاءات", NAVY, TRY),
        ("2", "صنّف", "ما مستوى المخاطرة؟", "منخفض / متوسط / مرتفع", TEAL, IDEA),
        ("3", "ابحث", "ما المصدر الأولي؟", "رابط أو مرجع أصلي", GOLD, TIP),
        ("4", "قارن", "هل المصدر يدعم الادعاء؟", "دعم كامل / جزئي / معارض / غير موجود", AMBER, WARNING),
        ("5", "وثّق", "ماذا قررت؟", "تقرير تحقق", GREEN, EXERCISE),
    ]
    y = 160
    for num, title, question, output, color, fill in rows:
        parts.append(rect(70, y, 1060, 112, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(rect(70, y, 9, 112, fill=color, stroke=color, rx=4))
        parts.append(badge(1075, y + 56, num, fill=color, r=28))
        parts.append(text(1015, y + 42, title, size=27, weight=700, fill=color, anchor="start"))
        parts.append(text(1015, y + 78, question, size=18, fill=INK, anchor="start"))
        parts.append(line(540, y + 20, 540, y + 92, stroke=BORDER, width=2, marker=False))
        parts.append(text(500, y + 34, "المخرج", size=14, fill=MUTED, weight=600, anchor="start"))
        parts.append(text(500, y + 68, output, size=18, fill=INK, weight=600, anchor="start"))
        y += 122

    parts.append(text(600, 800, "الخطوات ليست طويلة، لكنها تحتاج عادة. مع التمرين تصبح سريعة.", size=19, fill=MUTED))
    save("fig-08-1.svg", "".join(parts), title="بروتوكول التحقق الخمسي", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 8-2: the source pyramid
# ---------------------------------------------------------------------------
def figure_8_2() -> None:
    w, h = 1200, 760
    parts: list[str] = []
    parts.append(text(600, 62, "هرم المصادر", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "ترتيب أولي للثقة… لا حكم نهائي", size=21, fill=MUTED))

    bands = [
        (320, 440, NAVY, PAPER, ["1 · دراسة محكمة", "أو بيانات رسمية أولية"]),
        (440, 560, TEAL, PAPER, ["2 · تقرير مؤسسة معروفة", "أو جهة رسمية"]),
        (560, 680, GOLD, INK, ["3 · كتاب أو مقالة تخصصية"]),
        (680, 800, AMBER, PAPER, ["4 · صحافة مهنية"]),
        (800, 920, MUTED, PAPER, ["5 · مدونات ومنتديات", "وشبكات اجتماعية"]),
    ]
    y = 170
    for top_w, bottom_w, fill, ink, lines in bands:
        pts = (
            f"{600 - top_w / 2},{y} {600 + top_w / 2},{y} "
            f"{600 + bottom_w / 2},{y + 95} {600 - bottom_w / 2},{y + 95}"
        )
        parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{fill}" stroke-width="2.5"/>')
        if len(lines) == 2:
            parts.append(text(600, y + 40, lines[0], size=20, weight=700, fill=ink))
            parts.append(text(600, y + 68, lines[1], size=18, fill=ink))
        else:
            parts.append(text(600, y + 56, lines[0], size=20, weight=700, fill=ink))
        y += 95

    # Confidence arrow on the left
    parts.append(path("M 85 625 L 85 180", stroke=MUTED, width=3, marker=True))
    parts.append(text(85, 160, "ثقة أعلى", size=16, fill=MUTED, weight=600))
    parts.append(text(85, 660, "ثقة أقل", size=16, fill=MUTED, weight=600))

    parts.append(text(600, 720, "الهرم ترتيب أولي، لا حكم نهائي: دراسة قد تكون ضعيفة المنهج، ومصدر رسمي قد يكون متحيزًا.", size=18, fill=MUTED))
    save("fig-08-2.svg", "".join(parts), title="هرم المصادر", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 9-1: the improvement loop
# ---------------------------------------------------------------------------
def figure_9_1() -> None:
    w, h = 1200, 780
    parts: list[str] = []
    parts.append(text(600, 62, "حلقة التحسين", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "قيّم… غيّر… قارن… ثم توقف", size=21, fill=MUTED))

    cards = [
        (465, 150, "1", "قيّم", "أين يقصّر النص\nوفق المعيار؟", NAVY, TRY),
        (115, 330, "2", "غيّر", "ما التغيير الواحد\nالذي سأجرّبه؟", TEAL, IDEA),
        (465, 510, "3", "قارن", "هل تحسّن المعيار؟\nأُبقي أم أتراجع؟", GOLD, TIP),
        (815, 330, "4", "توقف", "هل تحقق الهدف\nأو انتهى الوقت؟", GREEN, EXERCISE),
    ]
    for x, y, num, title, body, color, fill in cards:
        parts.append(rect(x, y, 270, 140, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + 235, y + 30, num, fill=color, r=18))
        parts.append(text(x + 135, y + 62, title, size=26, weight=700, fill=color))
        parts.append(text(x + 135, y + 102, body, size=17, fill=INK))

    # Counter-clockwise loop, matching RTL reading order
    parts.append(path("M 450 240 Q 330 250 285 315", stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(path("M 285 470 Q 350 520 440 550", stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(path("M 750 560 Q 850 530 915 480", stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(path("M 915 315 Q 850 250 760 235", stroke=TEAL, width=4, marker="arrowTeal"))

    parts.append(circle(600, 400, 105, fill=TIP, stroke=GOLD, stroke_width=2.5, opacity=1))
    parts.append(text(600, 382, "تغيير واحد", size=24, weight=700, fill=AMBER))
    parts.append(text(600, 414, "لكل جولة", size=20, fill=INK))
    parts.append(text(600, 444, "وقس الفرق", size=18, fill=MUTED))

    parts.append(text(600, 730, "الحلقة ليست دورانًا بلا نهاية. لكل جولة سؤال واحد، وتغيير واحد، ومقارنة واحدة.", size=19, fill=MUTED))
    save("fig-09-1.svg", "".join(parts), title="حلقة التحسين", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 9-2: the three editing rounds
# ---------------------------------------------------------------------------
def figure_9_2() -> None:
    w, h = 1200, 740
    parts: list[str] = []
    parts.append(text(600, 62, "الجولات الثلاث", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "البنية… ثم المحتوى… ثم اللغة", size=21, fill=MUTED))

    cards = [
        (810, "1", "البنية", "هل يجيب النص\nعلى الموجز؟",
         "هل الترتيب منطقي؟\nهل هناك جزء ناقص\nأو زائد؟",
         "إعادة ترتيب، حذف قسم،\nإضافة توصية.", NAVY, TRY),
        (435, "2", "المحتوى", "هل كل ادعاء\nمدعوم؟",
         "هل الأمثلة محددة؟\nهل هناك تعميمات؟",
         "رقم موثق، مثال خاص\nبدل العام.", TEAL, IDEA),
        (60, "3", "اللغة", "هل النص واضح\nومقنع؟",
         "هل الجمل طويلة؟\nهل النبرة مناسبة؟",
         "حذف الحشو، تقصير الجمل،\nضبط النبرة.", GOLD, TIP),
    ]
    for x, num, title, focus, question, examples, color, fill in cards:
        parts.append(rect(x, 160, 330, 490, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + 165, 205, num, fill=color, r=24))
        parts.append(text(x + 165, 260, title, size=27, weight=700, fill=color))
        parts.append(rect(x + 40, 285, 250, 2, fill=color, stroke=color, rx=0))
        parts.append(text(x + 165, 315, "التركيز", size=14, fill=MUTED, weight=600))
        parts.append(text(x + 165, 345, focus, size=18, fill=INK))
        parts.append(text(x + 165, 415, "السؤال", size=14, fill=MUTED, weight=600))
        parts.append(text(x + 165, 445, question, size=18, fill=INK))
        parts.append(text(x + 165, 545, "أمثلة التغيير", size=14, fill=MUTED, weight=600))
        parts.append(text(x + 165, 575, examples, size=18, fill=INK))

    parts.append(line(805, 405, 775, 405, stroke=MUTED, width=3))
    parts.append(line(430, 405, 400, 405, stroke=MUTED, width=3))

    parts.append(text(600, 700, "لا تنتقل إلى الجولة التالية قبل أن تستقر الحالية. وغيّر شيئًا واحدًا في كل مرة.", size=19, fill=MUTED))
    save("fig-09-2.svg", "".join(parts), title="الجولات الثلاث", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 31-1: the five-step risk path
# ---------------------------------------------------------------------------
def figure_31_1() -> None:
    w, h = 1200, 600
    parts: list[str] = []
    parts.append(text(600, 62, "مسار المخاطرة الخمس", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "سمِّ… قيّم… اضبط… عيّن مالكًا… سجّل وراجع", size=21, fill=MUTED))

    cards = [
        ("1", "سمِّ", "بسبب [سبب]،\nقد يحدث [حدث]،\nفيؤدي إلى [أثر].", NAVY, TRY),
        ("2", "قيّم", "احتمال × أثر\nيحددان مستوى المخاطرة.", TEAL, IDEA),
        ("3", "اضبط", "منع، تقليل،\nنقل، أو قبول.", GOLD, TIP),
        ("4", "عيّن مالكًا", "شخص واحد مسؤول،\nلا لجنة غامضة.", AMBER, WARNING),
        ("5", "سجّل وراجع", "سجل المخاطر،\nومراجعة دورية.", GREEN, EXERCISE),
    ]
    xs = [950, 725, 500, 275, 50]
    for (num, title, body, color, fill), x in zip(cards, xs):
        parts.append(rect(x, 170, 200, 300, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + 100, 210, num, fill=color, r=24))
        parts.append(text(x + 100, 262, title, size=23, weight=700, fill=color))
        parts.append(rect(x + 34, 284, 132, 2, fill=color, stroke=color, rx=0))
        parts.append(text(x + 100, 320, body, size=17, fill=INK))

    # Small chevrons in the 25px gaps, pointing left
    for x in (935, 710, 485, 260):
        parts.append(path(f"M {x} 310 L {x - 10} 320 L {x} 330", stroke=TEAL, width=3, marker=False))

    parts.append(text(600, 540, "الأداة قد تكون السبب المباشر، لكن المسؤولية تبقى لمن اختارها وحدد صلاحياتها.", size=19, fill=MUTED))
    save("fig-31-1.svg", "".join(parts), title="مسار المخاطرة الخمس", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 31-2: the three lines of defense
# ---------------------------------------------------------------------------
def figure_31_2() -> None:
    w, h = 1200, 720
    parts: list[str] = []
    parts.append(text(600, 62, "خطوط الدفاع الثلاثة", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "من التنفيذ اليومي إلى المراجعة المستقلة", size=21, fill=MUTED))

    parts.append(rect(70, 150, 1060, 490, fill=WARNING, stroke=RED, stroke_width=3, rx=28))
    parts.append(rect(180, 230, 840, 350, fill=IDEA, stroke=TEAL, stroke_width=3, rx=24))
    parts.append(rect(290, 310, 620, 210, fill=TRY, stroke=NAVY, stroke_width=3, rx=20))

    # Badges sit on the left edge of each ring; labels are centered so they
    # never collide with the badges or with the ring borders.
    parts.append(badge(95, 150, "3", fill=RED, r=22))
    parts.append(text(600, 190, "المراجعة", size=24, weight=700, fill=RED))
    parts.append(text(600, 218, "قيادة أو جهة مستقلة تسأل: هل الضوابط تعمل؟", size=17, fill=INK))

    parts.append(badge(205, 230, "2", fill=TEAL, r=22))
    parts.append(text(600, 268, "المراقبة", size=24, weight=700, fill=TEAL))
    parts.append(text(600, 296, "شخص أو وظيفة تفحص السجلات والمؤشرات.", size=17, fill=INK))

    parts.append(badge(315, 310, "1", fill=NAVY, r=22))
    parts.append(text(600, 348, "التنفيذ", size=24, weight=700, fill=NAVY))
    parts.append(text(600, 376, "الفريق يطبق الضوابط يوميًا.", size=17, fill=INK))

    parts.append(text(600, 440, "العمل اليومي", size=30, weight=700, fill=NAVY))
    parts.append(text(600, 475, "الأداة + الفريق + الضوابط", size=19, fill=INK))

    parts.append(text(600, 690, "لا تجعل المنفذ هو المراجع الوحيد. من يريد أن ينجح العمل قد لا يرى الخطر.", size=19, fill=MUTED))
    save("fig-31-2.svg", "".join(parts), title="خطوط الدفاع الثلاثة", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 33-1: the integrated project map
# ---------------------------------------------------------------------------
def figure_33_1() -> None:
    w, h = 1200, 700
    parts: list[str] = []
    parts.append(text(600, 62, "خريطة المشروع المتكامل", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "ست محطات من المشكلة إلى العرض", size=21, fill=MUTED))

    cards = [
        (780, 190, "1", "اختر", "مشكلة متكررة\nومؤلمة.", NAVY, TRY),
        (450, 190, "2", "حدد النطاق", "ما داخل المشروع\nوما خارجه؟", TEAL, IDEA),
        (120, 190, "3", "ابنِ", "نسخة صغيرة\nتعمل.", NAVY, TRY),
        (120, 450, "4", "اختبر", "حالة حقيقية،\nوشخص جديد.", TEAL, IDEA),
        (450, 450, "5", "وثّق", "دليل من صفحة،\nومالك.", NAVY, TRY),
        (780, 450, "6", "اعرض", "سبع شرائح\nتبدأ بالإنسان.", TEAL, IDEA),
    ]
    for x, y, num, title, body, color, fill in cards:
        parts.append(rect(x, y, 300, 150, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + 265, y + 32, num, fill=color, r=20))
        parts.append(text(x + 150, y + 60, title, size=26, weight=700, fill=color))
        parts.append(text(x + 150, y + 108, body, size=18, fill=INK))

    # Top row: right to left
    parts.append(line(775, 265, 755, 265, stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(line(445, 265, 425, 265, stroke=TEAL, width=4, marker="arrowTeal"))
    # Down from 3 to 4
    parts.append(path("M 270 345 L 270 440", stroke=TEAL, width=4, marker="arrowTeal"))
    # Bottom row: left to right
    parts.append(line(425, 525, 445, 525, stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(line(755, 525, 775, 525, stroke=TEAL, width=4, marker="arrowTeal"))

    parts.append(text(600, 660, "المشروع الناجح ليس أكبر مشروع؛ هو أصغر مشروع يثبت القيمة.", size=20, fill=MUTED))
    save("fig-33-1.svg", "".join(parts), title="خريطة المشروع المتكامل", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 33-2: the seven-slide presentation arc
# ---------------------------------------------------------------------------
def figure_33_2() -> None:
    w, h = 1200, 540
    parts: list[str] = []
    parts.append(text(600, 62, "قوس العرض السبعة", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "من الموقف إلى الخطوة التالية", size=21, fill=MUTED))

    slides = [
        (1020, 280, "1", "الموقف", "20 ث"),
        (855, 250, "2", "المشكلة", "30 ث"),
        (690, 225, "3", "الدليل", "30 ث"),
        (525, 215, "4", "الحل", "40 ث"),
        (360, 225, "5", "النتيجة", "30 ث"),
        (195, 250, "6", "الحدود", "20 ث"),
        (30, 280, "7", "الخطوة", "20 ث"),
    ]
    colors = [NAVY, TEAL, GOLD, AMBER, GREEN, NAVY, TEAL]
    fills = [TRY, IDEA, TIP, WARNING, EXERCISE, TRY, IDEA]

    # Draw the connecting line first, through the card centers, so the cards
    # cover it and it appears only in the gaps. This avoids crossing titles.
    centers = " ".join(f"{x + 75},{y + 52}" for x, y, *_ in slides)
    points = centers.split()
    polyline = "M " + " L ".join(points)
    parts.append(path(polyline, stroke=GOLD, width=2, dash="6 6", marker=False, opacity=0.55))

    for (x, y, num, title, duration), color, fill in zip(slides, colors, fills):
        parts.append(rect(x, y, 150, 105, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + 75, y + 22, num, fill=color, r=16))
        parts.append(text(x + 75, y + 58, title, size=20, weight=700, fill=color))
        parts.append(text(x + 75, y + 86, duration, size=15, fill=MUTED))

    parts.append(text(600, 490, "لا تبدأ بالتقنية. ابدأ بالإنسان: من يتأثر؟ وما الألم؟", size=20, fill=MUTED))
    save("fig-33-2.svg", "".join(parts), title="قوس العرض السبعة", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 34-1: the ninety-day arc
# ---------------------------------------------------------------------------
def figure_34_1() -> None:
    w, h = 1200, 600
    parts: list[str] = []
    parts.append(text(600, 62, "قوس التسعين يومًا", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "ثبّت… وسّع… علّم", size=21, fill=MUTED))

    phases = [
        (820, "1", "ثبّت", "\u20661–30\u2069", "نظام واحد، عادة واحدة", "استخدام أسبوعي منتظم", NAVY, TRY),
        (440, "2", "وسّع", "\u206631–60\u2069", "حالة استخدام ثانية", "نتيجة أفضل أو وقت أقل", TEAL, IDEA),
        (60, "3", "علّم", "\u206661–90\u2069", "وثّق، درّب، راجع", "نظام يعيش بدونك", GOLD, TIP),
    ]
    for x, num, title, days, goal, output, color, fill in phases:
        parts.append(rect(x, 190, 320, 210, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + 285, 225, num, fill=color, r=22))
        parts.append(text(x + 160, 245, title, size=30, weight=700, fill=color))
        parts.append(rect(x + 110, 268, 100, 32, fill=color, stroke=color, rx=16))
        parts.append(text(x + 160, 290, days, size=17, weight=700, fill=PAPER))
        parts.append(text(x + 160, 340, goal, size=19, weight=600, fill=INK))
        parts.append(text(x + 160, 372, output, size=17, fill=MUTED))

    # Timeline: time flows right to left
    parts.append(line(1120, 455, 80, 455, stroke=MUTED, width=3))
    for x, color in ((980, NAVY), (600, TEAL), (220, GOLD)):
        parts.append(line(x, 400, x, 445, stroke=color, width=2, marker=False))
        parts.append(circle(x, 455, 10, fill=color))
    parts.append(text(980, 490, "الشهر الأول", size=16, fill=MUTED))
    parts.append(text(600, 490, "الشهر الثاني", size=16, fill=MUTED))
    parts.append(text(220, 490, "الشهر الثالث", size=16, fill=MUTED))

    parts.append(text(600, 550, "الشهر الأول ليس للنتائج الكبيرة؛ هو لإثبات أنك تستطيع التكرار.", size=20, fill=MUTED))
    save("fig-34-1.svg", "".join(parts), title="قوس التسعين يومًا", width=w, height=h)


# ---------------------------------------------------------------------------
# Figure 34-2: the five-moment week
# ---------------------------------------------------------------------------
def figure_34_2() -> None:
    w, h = 1200, 800
    parts: list[str] = []
    parts.append(text(600, 62, "حلقة الأسبوع الخمس", size=38, weight=700, fill=NAVY))
    parts.append(text(600, 102, "خمس لحظات صغيرة… أفضل من يوم كامل", size=21, fill=MUTED))

    cards = [
        (490, 135, "1", "التخطيط", "الأحد، 15 د", "ما المهمة الواحدة؟", NAVY, TRY),
        (728, 308, "2", "التنفيذ", "3 جلسات، 20 د", "هل فعلتها؟ ما العائق؟", TEAL, IDEA),
        (637, 587, "3", "الملاحظة", "يوميًا، دقيقتان", "ما الذي نجح؟", GOLD, TIP),
        (343, 587, "4", "المراجعة", "الخميس، 10 د", "هل تحرك المقياس؟", AMBER, WARNING),
        (252, 308, "5", "التعلم", "الجمعة، 20 د", "ما الذي سأتعلمه؟", GREEN, EXERCISE),
    ]
    for x, y, num, title, when, question, color, fill in cards:
        parts.append(rect(x, y, 220, 120, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + 190, y + 22, num, fill=color, r=16))
        parts.append(text(x + 110, y + 38, title, size=23, weight=700, fill=color))
        parts.append(text(x + 110, y + 68, when, size=15, fill=MUTED))
        parts.append(text(x + 110, y + 96, question, size=16, fill=INK))

    # Clockwise week loop
    parts.append(path("M 710 205 Q 800 235 830 295", stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(path("M 838 435 Q 820 525 760 575", stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(line(630, 647, 575, 647, stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(path("M 440 575 Q 380 525 362 435", stroke=TEAL, width=4, marker="arrowTeal"))
    parts.append(path("M 370 355 Q 420 265 480 210", stroke=TEAL, width=4, marker="arrowTeal"))

    parts.append(circle(600, 445, 105, fill=TIP, stroke=GOLD, stroke_width=2.5))
    parts.append(text(600, 425, "خمس لحظات", size=24, weight=700, fill=AMBER))
    parts.append(text(600, 457, "صغيرة", size=20, fill=INK))
    parts.append(text(600, 487, "أفضل من يوم كامل", size=17, fill=MUTED))

    parts.append(text(600, 765, "الخطة التي لا تُراجع أسبوعيًا تصبح أمنية.", size=20, fill=MUTED))
    save("fig-34-2.svg", "".join(parts), title="حلقة الأسبوع الخمس", width=w, height=h)


def build_all() -> None:
    """Build every figure in the book (67 SVGs)."""
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from figures_part0_1 import build_all as build_part0_1
    from figures_part2_3 import build_all as build_part2_3
    from figures_part4_5 import build_all as build_part4_5

    build_part0_1()
    build_part2_3()
    build_part4_5()
    figure_5_1()
    figure_7_1()
    figure_7_2()
    figure_8_1()
    figure_8_2()
    figure_9_1()
    figure_9_2()
    figure_31_1()
    figure_31_2()
    figure_33_1()
    figure_33_2()
    figure_34_1()
    figure_34_2()


if __name__ == "__main__":
    build_all()
