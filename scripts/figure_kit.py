#!/usr/bin/env python3
"""Shared drawing kit for the book's SVG figures.

The kit keeps one visual language across all figures: the same palette,
typography, spacing, badges, arrows, and RTL text handling. Figure modules
declare content; this module owns layout.
"""

from __future__ import annotations

import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#14213D"
TEAL = "#0F766E"
GOLD = "#C6A15B"
AMBER = "#B45309"
RED = "#B91C1C"
DARK_RED = "#7F1D1D"
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


def lri(value: str) -> str:
    """Isolate a numeric range or Latin token inside RTL text."""
    return f"\u2066{value}\u2069"


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
    """Emit one <text> element per line.

    Separate elements avoid the bidi breakage that <tspan> can cause when a
    line starts with a digit or a Latin token. In RTL, ``anchor="start"``
    right-aligns at ``x``; ``anchor="middle"`` centers; ``anchor="end"``
    left-aligns at ``x``.
    """
    out: list[str] = []
    for index, line in enumerate(value.split("\n")):
        out.append(
            f'<text x="{x}" y="{y + index * size * line_height}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" opacity="{opacity}" '
            f'direction="rtl" style="direction:rtl;unicode-bidi:isolate">'
            f"{esc(line)}</text>"
        )
    return "".join(out)


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
        marker_id = "arrowMuted"
    elif marker:
        marker_id = marker
    else:
        marker_id = ""
    mark = f' marker-end="url(#{marker_id})"' if marker_id else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"'
        f"{extra}{mark}/>"
    )


def path(
    d: str,
    *,
    stroke: str = TEAL,
    width: float = 3,
    fill: str = "none",
    dash: str | None = None,
    marker: bool | str = False,
    opacity: float = 1.0,
) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    if marker is True:
        marker_id = "arrowTeal"
    elif marker:
        marker_id = marker
    else:
        marker_id = ""
    mark = f' marker-end="url(#{marker_id})"' if marker_id else ""
    return (
        f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
        f'opacity="{opacity}"{extra}{mark}/>'
    )


def circle(cx: float, cy: float, r: float, *, fill: str = GOLD, stroke: str = "none", stroke_width: float = 0) -> str:
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def badge(cx: float, cy: float, label: str, *, fill: str = GOLD, r: float = 22) -> str:
    size = int(r * 0.9) if len(label) <= 2 else int(r * 0.7)
    return circle(cx, cy, r, fill=fill) + text(
        cx, cy + size * 0.36, label, size=size, weight=700, fill=PAPER
    )


def svg(body: str, *, width: int = 1200, height: int = 700, title: str = "") -> str:
    aria = ""
    if title:
        aria = (
            f'<title>{esc(title)}</title>'
            f'<desc>{esc(title)} — رسم تعليمي من كتاب «من الصفر إلى الاحتراف».</desc>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
     viewBox="0 0 {width} {height}" role="img" aria-labelledby="figTitle">
  <defs>
    <marker id="arrowTeal" viewBox="0 0 10 10" refX="8" refY="5"
      markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{TEAL}"/>
    </marker>
    <marker id="arrowGold" viewBox="0 0 10 10" refX="8" refY="5"
      markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{GOLD}"/>
    </marker>
    <marker id="arrowMuted" viewBox="0 0 10 10" refX="8" refY="5"
      markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/>
    </marker>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="{NAVY}" flood-opacity="0.10"/>
    </filter>
  </defs>
  <rect width="{width}" height="{height}" fill="{PAPER}"/>
  {aria}
  {body}
</svg>
'''


def save(name: str, body: str, *, title: str = "", width: int = 1200, height: int = 700) -> None:
    (OUT / name).write_text(svg(body, width=width, height=height, title=title), encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------
def header(parts: list[str], title: str, subtitle: str | None = None) -> None:
    parts.append(text(600, 62, title, size=38, weight=700, fill=NAVY))
    if subtitle:
        parts.append(text(600, 102, subtitle, size=21, fill=MUTED))


def footer(parts: list[str], value: str, y: float) -> None:
    parts.append(text(600, y, value, size=19, fill=MUTED))


def _step(step, index: int) -> tuple[str, str, str, str, str]:
    if len(step) == 4:
        title, body, color, fill = step
        return str(index + 1), title, body, color, fill
    if len(step) == 5:
        return step
    raise ValueError(f"Unsupported step shape: {step!r}")


def sequence(
    name: str,
    title: str,
    subtitle: str,
    steps: list[tuple],
    note: str,
    *,
    h: int = 640,
    y: int = 180,
    card_h: int = 280,
    gap: int = 18,
    margin: int = 36,
    body_size: int | None = None,
    title_size: int = 22,
) -> None:
    """A horizontal RTL sequence of cards with chevrons in the gaps."""
    n = len(steps)
    card_w = (1200 - 2 * margin - gap * (n - 1)) / n
    if body_size is None:
        body_size = 14 if n >= 7 else 15 if n == 6 else 16 if n == 5 else 18
    parts: list[str] = []
    header(parts, title, subtitle)
    xs = [1200 - margin - card_w - i * (card_w + gap) for i in range(n)]
    cy = y + card_h / 2
    for index, step in enumerate(steps):
        num, step_title, body, color, fill = _step(step, index)
        x = xs[index]
        parts.append(rect(x, y, card_w, card_h, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + card_w - 28, y + 28, num, fill=color, r=20))
        parts.append(text(x + card_w / 2, y + 64, step_title, size=title_size, weight=700, fill=color))
        parts.append(rect(x + card_w / 2 - 40, y + 82, 80, 2, fill=color, stroke=color, rx=0))
        parts.append(text(x + card_w / 2, y + 116, body, size=body_size, fill=INK, line_height=1.42))
    for index in range(n - 1):
        ax = xs[index] - gap / 2
        parts.append(path(f"M {ax + 16} {cy - 20} L {ax - 16} {cy} L {ax + 16} {cy + 20}", stroke=TEAL, width=4.5))
    footer(parts, note, y + card_h + 58)
    save(name, "".join(parts), title=title, height=int(y + card_h + 105))


def grid(
    name: str,
    title: str,
    subtitle: str,
    items: list[tuple],
    note: str,
    *,
    cols: int = 3,
    card_w: int = 330,
    card_h: int = 170,
    gap: int = 22,
    y: int = 160,
    h: int | None = None,
    body_size: int = 16,
    title_size: int = 22,
) -> None:
    """A RTL grid: the first item sits in the top-right cell."""
    rows = math.ceil(len(items) / cols)
    total_w = cols * card_w + (cols - 1) * gap
    x0 = (1200 - total_w) / 2
    if h is None:
        h = int(y + rows * (card_h + gap) + 80)
    parts: list[str] = []
    header(parts, title, subtitle)
    for index, item in enumerate(items):
        num, item_title, body, color, fill = _step(item, index)
        row, col = divmod(index, cols)
        x = x0 + (cols - 1 - col) * (card_w + gap)
        yy = y + row * (card_h + gap)
        parts.append(rect(x, yy, card_w, card_h, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + card_w - 26, yy + 26, num, fill=color, r=18))
        parts.append(text(x + card_w / 2, yy + 58, item_title, size=title_size, weight=700, fill=color))
        parts.append(text(x + card_w / 2, yy + 96, body, size=body_size, fill=INK, line_height=1.4))
    footer(parts, note, h - 45)
    save(name, "".join(parts), title=title, height=h)


def cycle(
    name: str,
    title: str,
    subtitle: str,
    nodes: list[tuple],
    note: str,
    *,
    h: int | None = None,
    cx: int = 600,
    cy: int = 430,
    rx: int = 420,
    ry: int = 245,
    card_w: int = 205,
    card_h: int = 100,
    center_title: str | None = None,
    center_sub: str = "",
    body_size: int = 15,
    title_size: int = 20,
) -> None:
    """A clockwise RTL cycle; arrows are drawn behind the cards."""
    n = len(nodes)
    if h is None:
        h = int(cy + ry + card_h / 2 + 70)
    angles = [-90 + i * 360 / n for i in range(n)]
    parts: list[str] = []
    header(parts, title, subtitle)

    for index in range(n):
        start = angles[index] + 18
        end = angles[(index + 1) % n] - 18
        if end <= start:
            end += 360
        a1, a2 = math.radians(start), math.radians(end)
        x1, y1 = cx + rx * math.cos(a1), cy + ry * math.sin(a1)
        x2, y2 = cx + rx * math.cos(a2), cy + ry * math.sin(a2)
        parts.append(path(f"M {x1:.1f} {y1:.1f} A {rx} {ry} 0 0 1 {x2:.1f} {y2:.1f}", stroke=TEAL, width=4, marker="arrowTeal"))

    for index, node in enumerate(nodes):
        num, node_title, body, color, fill = _step(node, index)
        angle = math.radians(angles[index])
        x = cx + rx * math.cos(angle) - card_w / 2
        y = cy + ry * math.sin(angle) - card_h / 2
        parts.append(rect(x, y, card_w, card_h, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + card_w - 24, y + 24, num, fill=color, r=16))
        parts.append(text(x + card_w / 2, y + 44, node_title, size=title_size, weight=700, fill=color))
        parts.append(text(x + card_w / 2, y + 74, body, size=body_size, fill=INK, line_height=1.35))

    parts.append(circle(cx, cy, 105, fill=TIP, stroke=GOLD, stroke_width=2.5))
    if center_title:
        parts.append(text(cx, cy - 8, center_title, size=23, weight=700, fill=AMBER))
        if center_sub:
            parts.append(text(cx, cy + 24, center_sub, size=16, fill=INK, line_height=1.35))
    footer(parts, note, h - 42)
    save(name, "".join(parts), title=title, height=h)


def layers(
    name: str,
    title: str,
    subtitle: str,
    items: list[tuple],
    note: str,
    *,
    h: int | None = None,
    y: int = 150,
    band_h: int = 76,
    gap: int = 10,
    width: int = 1000,
    body_size: int = 15,
    title_size: int = 20,
) -> None:
    """A vertical stack of layers, top to bottom."""
    n = len(items)
    if h is None:
        h = int(y + n * (band_h + gap) + 70)
    x = (1200 - width) / 2
    parts: list[str] = []
    header(parts, title, subtitle)
    for index, item in enumerate(items):
        num, item_title, body, color, fill = _step(item, index)
        yy = y + index * (band_h + gap)
        parts.append(rect(x, yy, width, band_h, fill=fill, stroke=color, stroke_width=2.2, shadow=True))
        parts.append(rect(x, yy, 8, band_h, fill=color, stroke=color, rx=4))
        parts.append(badge(x + 42, yy + band_h / 2, num, fill=color, r=18))
        parts.append(text(x + width / 2, yy + 30, item_title, size=title_size, weight=700, fill=color))
        parts.append(text(x + width / 2, yy + 56, body, size=body_size, fill=INK, line_height=1.3))
    footer(parts, note, h - 42)
    save(name, "".join(parts), title=title, height=h)


def funnel(
    name: str,
    title: str,
    subtitle: str,
    stages: list[tuple],
    note: str,
    *,
    h: int = 720,
    y: int = 150,
    top_w: int = 980,
    bottom_w: int = 420,
    band_h: int = 80,
    gap: int = 10,
    body_size: int = 14,
    title_size: int = 20,
) -> None:
    """A five-stage funnel; widths narrow from top to bottom."""
    n = len(stages)
    parts: list[str] = []
    header(parts, title, subtitle)
    for index, stage in enumerate(stages):
        num, stage_title, body, color, fill = _step(stage, index)
        wt = top_w - (top_w - bottom_w) * index / max(n - 1, 1)
        wb = top_w - (top_w - bottom_w) * (index + 1) / max(n - 1, 1)
        yy = y + index * (band_h + gap)
        points = (
            f"{600 - wt / 2:.1f},{yy} {600 + wt / 2:.1f},{yy} "
            f"{600 + wb / 2:.1f},{yy + band_h} {600 - wb / 2:.1f},{yy + band_h}"
        )
        parts.append(f'<polygon points="{points}" fill="{fill}" stroke="{color}" stroke-width="2.2"/>')
        parts.append(badge(600 + wt / 2 - 28, yy + 24, num, fill=color, r=16))
        parts.append(text(600, yy + 33, stage_title, size=title_size, weight=700, fill=color))
        parts.append(text(600, yy + 56, body, size=body_size, fill=INK, line_height=1.2))
    footer(parts, note, h - 45)
    save(name, "".join(parts), title=title, height=h)


def pyramid(
    name: str,
    title: str,
    subtitle: str,
    levels: list[tuple],
    note: str,
    *,
    h: int = 700,
    y: int = 160,
    top_w: int = 280,
    base_w: int = 900,
    level_h: int = 82,
) -> None:
    """A five-level pyramid, level 1 at the top."""
    n = len(levels)
    parts: list[str] = []
    header(parts, title, subtitle)
    for index, level in enumerate(levels):
        num, level_title, body, color, fill = _step(level, index)
        wt = top_w + (base_w - top_w) * index / n
        wb = top_w + (base_w - top_w) * (index + 1) / n
        yy = y + index * level_h
        points = (
            f"{600 - wt / 2:.1f},{yy} {600 + wt / 2:.1f},{yy} "
            f"{600 + wb / 2:.1f},{yy + level_h} {600 - wb / 2:.1f},{yy + level_h}"
        )
        parts.append(f'<polygon points="{points}" fill="{fill}" stroke="{color}" stroke-width="2.2"/>')
        parts.append(text(600, yy + 30, f"{num}. {level_title}", size=19, weight=700, fill=color))
        parts.append(text(600, yy + 56, body, size=14, fill=INK, line_height=1.25))
    # Confidence axis on the right margin
    parts.append(text(1135, 185, "ثقة أعلى", size=15, weight=700, fill=GREEN, anchor="middle"))
    parts.append(path("M 1135 205 L 1135 560", stroke=MUTED, width=2, dash="6 6", marker="arrowMuted"))
    parts.append(text(1135, 590, "ثقة أقل", size=15, weight=700, fill=MUTED, anchor="middle"))
    footer(parts, note, h - 45)
    save(name, "".join(parts), title=title, height=h)


def tree(
    name: str,
    title: str,
    subtitle: str,
    root: tuple,
    branches: list[tuple],
    note: str,
    *,
    h: int = 720,
    y: int = 170,
    root_w: int = 330,
    root_h: int = 95,
    card_h: int = 175,
    gap: int = 16,
    body_size: int = 14,
    title_size: int = 20,
) -> None:
    """A top-down decision tree with RTL branches."""
    n = len(branches)
    card_w = (1120 - gap * (n - 1)) / n
    x0 = (1200 - (n * card_w + (n - 1) * gap)) / 2
    branch_y = 440
    parts: list[str] = []
    header(parts, title, subtitle)

    # Lines first, so the cards cover their endpoints.
    root_bottom = (600, y + root_h)
    for index in range(n):
        bx = x0 + (n - 1 - index) * (card_w + gap) + card_w / 2
        parts.append(line(root_bottom[0], root_bottom[1], bx, branch_y - 10, stroke=TEAL, width=3, marker="arrowTeal"))

    num, root_title, root_body, color, fill = _step(root, 0)
    parts.append(rect(600 - root_w / 2, y, root_w, root_h, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
    parts.append(text(600, y + 38, root_title, size=25, weight=700, fill=color))
    parts.append(text(600, y + 68, root_body, size=16, fill=INK, line_height=1.3))

    for index, branch in enumerate(branches):
        bnum, btitle, bbody, bcolor, bfill = _step(branch, index)
        bx = x0 + (n - 1 - index) * (card_w + gap)
        parts.append(rect(bx, branch_y, card_w, card_h, fill=bfill, stroke=bcolor, stroke_width=2.3, shadow=True))
        parts.append(badge(bx + card_w - 22, branch_y + 22, bnum, fill=bcolor, r=15))
        parts.append(text(bx + card_w / 2, branch_y + 48, btitle, size=title_size, weight=700, fill=bcolor))
        parts.append(text(bx + card_w / 2, branch_y + 82, bbody, size=body_size, fill=INK, line_height=1.35))
    footer(parts, note, h - 45)
    save(name, "".join(parts), title=title, height=h)


def timeline(
    name: str,
    title: str,
    subtitle: str,
    milestones: list[tuple[str, str, str]],
    note: str,
    *,
    h: int = 680,
) -> None:
    """An RTL timeline with alternating cards above and below the line."""
    n = len(milestones)
    parts: list[str] = []
    header(parts, title, subtitle)
    line_y = 370
    x_start, x_end = 1080, 120
    step = (x_start - x_end) / max(n - 1, 1)
    colors = [NAVY, TEAL, GOLD, AMBER, GREEN, NAVY, TEAL, GOLD]
    parts.append(line(1140, line_y, 80, line_y, stroke=MUTED, width=3, marker=False))
    parts.append(path(f"M 95 {line_y - 10} L 78 {line_y} L 95 {line_y + 10}", stroke=MUTED, width=3))

    for index, (year, item_title, body) in enumerate(milestones):
        x = x_start - index * step
        above = index % 2 == 0
        card_y = 175 if above else 435
        color = colors[index % len(colors)]
        # Connector
        if above:
            parts.append(line(x, line_y - 8, x, card_y + 118, stroke=color, width=2, marker=False))
        else:
            parts.append(line(x, line_y + 8, x, card_y, stroke=color, width=2, marker=False))
        parts.append(rect(x - 115, card_y, 230, 118, fill=TINT, stroke=color, stroke_width=2.2, shadow=True))
        parts.append(text(x, card_y + 34, item_title, size=18, weight=700, fill=color))
        parts.append(text(x, card_y + 64, body, size=14, fill=INK, line_height=1.35))
        # Year pill on the line
        parts.append(rect(x - 48, line_y - 17, 96, 34, fill=PAPER, stroke=color, stroke_width=2, rx=17))
        parts.append(text(x, line_y + 6, year, size=14, weight=700, fill=color))
    footer(parts, note, h - 45)
    save(name, "".join(parts), title=title, height=h)


def t_shape(
    name: str,
    title: str,
    subtitle: str,
    skills: list[str],
    depth_title: str,
    depth_body: str,
    note: str,
    *,
    h: int = 670,
) -> None:
    """A T-shaped skills diagram: broad bar plus deep stem."""
    parts: list[str] = []
    header(parts, title, subtitle)
    bar_x, bar_y, bar_w, bar_h = 150, 185, 900, 125
    parts.append(rect(bar_x, bar_y, bar_w, bar_h, fill=TRY, stroke=NAVY, stroke_width=3, rx=18, shadow=True))
    box_w, box_h, box_gap = 138, 80, 8
    total = len(skills) * box_w + (len(skills) - 1) * box_gap
    box_x0 = bar_x + (bar_w - total) / 2
    for index, skill in enumerate(skills):
        bx = box_x0 + (len(skills) - 1 - index) * (box_w + box_gap)
        parts.append(rect(bx, bar_y + 22, box_w, box_h, fill=PAPER, stroke=BORDER, stroke_width=1.5, rx=10))
        parts.append(text(bx + box_w / 2, bar_y + 68, skill, size=14, weight=600, fill=NAVY))
    parts.append(text(600, 165, "عرض المهارات", size=20, weight=700, fill=TEAL))
    stem_x, stem_y, stem_w, stem_h = 480, 310, 240, 250
    parts.append(rect(stem_x, stem_y, stem_w, stem_h, fill=IDEA, stroke=TEAL, stroke_width=3, rx=18, shadow=True))
    parts.append(text(600, stem_y + 48, depth_title, size=24, weight=700, fill=TEAL))
    parts.append(text(600, stem_y + 88, depth_body, size=15, fill=INK, line_height=1.4))
    parts.append(text(600, 610, "العرض يفتح الأبواب… والعمق يجعلك مرجعًا", size=17, fill=MUTED))
    footer(parts, note, h - 40)
    save(name, "".join(parts), title=title, height=h)


def swimlane(
    name: str,
    title: str,
    subtitle: str,
    stages: list[str],
    roles: list[tuple[str, str, str]],
    cells: dict[tuple[int, int], str],
    note: str,
    *,
    h: int = 690,
) -> None:
    """A RTL swimlane: stages across, roles down."""
    parts: list[str] = []
    header(parts, title, subtitle)
    x0, total_w, role_w = 50, 1100, 150
    stage_w = (total_w - role_w) / len(stages)
    header_y, header_h = 160, 62
    row_y, row_h = header_y + header_h, 85

    # Header background
    parts.append(rect(x0, header_y, total_w, header_h, fill=NAVY, stroke=NAVY, rx=10))
    parts.append(text(x0 + total_w - role_w / 2, header_y + 38, "الدور / المرحلة", size=16, weight=700, fill=PAPER))
    for index, stage in enumerate(stages):
        sx = x0 + total_w - role_w - (index + 1) * stage_w
        parts.append(text(sx + stage_w / 2, header_y + 26, f"{index + 1}. {stage}", size=16, weight=700, fill=PAPER, line_height=1.2))

    for rindex, (role, color, fill) in enumerate(roles):
        ry = row_y + rindex * row_h
        parts.append(rect(x0 + total_w - role_w, ry, role_w, row_h, fill=fill, stroke=color, stroke_width=1.5, rx=0))
        parts.append(text(x0 + total_w - role_w / 2, ry + row_h / 2 + 6, role, size=20, weight=700, fill=color))
        for sindex in range(len(stages)):
            sx = x0 + total_w - role_w - (sindex + 1) * stage_w
            value = cells.get((sindex, rindex), "")
            cell_fill = PAPER if value else TINT
            parts.append(rect(sx, ry, stage_w, row_h, fill=cell_fill, stroke=BORDER, stroke_width=1, rx=0))
            if value:
                parts.append(text(sx + stage_w / 2, ry + 32, value, size=18, fill=INK, line_height=1.3))
    parts.append(rect(x0, header_y, total_w, row_y - header_y + len(roles) * row_h, fill="none", stroke=BORDER, stroke_width=2, rx=10))
    footer(parts, note, h - 40)
    save(name, "".join(parts), title=title, height=h)


def traffic_light(
    name: str,
    title: str,
    subtitle: str,
    levels: list[tuple[str, str, str, str, str]],
    note: str,
    *,
    h: int = 690,
) -> None:
    """A four-light risk signal with explanatory cards."""
    parts: list[str] = []
    header(parts, title, subtitle)
    housing_x, housing_y, housing_w, housing_h = 940, 150, 180, 470
    parts.append(rect(housing_x, housing_y, housing_w, housing_h, fill=NAVY, stroke=NAVY, rx=32, shadow=True))
    for index, (label, color, meaning, action, examples) in enumerate(levels):
        cy = housing_y + 55 + index * 105
        parts.append(circle(1030, cy, 34, fill=color, stroke=PAPER, stroke_width=3))
        card_y = cy - 46
        parts.append(rect(100, card_y, 800, 92, fill=TINT, stroke=color, stroke_width=2, shadow=True))
        parts.append(rect(100, card_y, 8, 92, fill=color, stroke=color, rx=4))
        parts.append(text(870, card_y + 28, label, size=20, weight=700, fill=color, anchor="start"))
        parts.append(text(870, card_y + 52, meaning, size=14, fill=INK, anchor="start"))
        parts.append(text(870, card_y + 74, f"{action} — {examples}", size=13, fill=MUTED, anchor="start"))
    footer(parts, note, h - 42)
    save(name, "".join(parts), title=title, height=h)


def sift_rows(
    name: str,
    title: str,
    subtitle: str,
    rows: list[tuple],
    note: str,
    *,
    h: int = 660,
) -> None:
    """Four wide rows with a large Latin letter on the right and an action
    on the left. Rows may be 4-tuples (no action) or 5-tuples."""
    parts: list[str] = []
    header(parts, title, subtitle)
    colors = [NAVY, TEAL, GOLD, AMBER]
    for index, row in enumerate(rows):
        letter, arabic, question, detail = row[:4]
        action = row[4] if len(row) > 4 else ""
        y = 155 + index * 112
        color = colors[index % len(colors)]
        parts.append(rect(100, y, 1000, 100, fill=TINT, stroke=color, stroke_width=2, shadow=True))
        parts.append(circle(1055, y + 50, 36, fill=color))
        parts.append(text(1055, y + 62, letter, size=30, weight=700, fill=PAPER))
        parts.append(text(990, y + 34, arabic, size=22, weight=700, fill=color, anchor="start"))
        parts.append(text(990, y + 60, question, size=16, fill=INK, anchor="start"))
        parts.append(text(990, y + 84, detail, size=14, fill=MUTED, anchor="start"))
        if action:
            parts.append(line(720, y + 18, 720, y + 82, stroke=BORDER, width=1.5, marker=False))
            parts.append(text(700, y + 38, "المخرج", size=12, weight=700, fill=MUTED, anchor="start"))
            parts.append(text(700, y + 66, action, size=15, weight=600, fill=color, anchor="start"))
    footer(parts, note, h - 42)
    save(name, "".join(parts), title=title, height=h)


def chapter_map(
    name: str,
    title: str,
    subtitle: str,
    items: list[tuple],
    note: str,
    *,
    h: int = 700,
) -> None:
    """A 3x3 one-page chapter map."""
    grid(name, title, subtitle, items, note, cols=3, card_w=330, card_h=140, gap=20, y=160, h=h, body_size=15, title_size=21)


def ladder(
    name: str,
    title: str,
    subtitle: str,
    rungs: list[tuple],
    note: str,
    *,
    h: int = 780,
    top_y: int = 155,
    rung_h: int = 68,
    step: int = 86,
    axis_top: str = "صلاحية وخطر أعلى",
    axis_bottom: str = "صلاحية أقل",
) -> None:
    """A six-rung permission ladder, highest permission at the top."""
    n = len(rungs)
    parts: list[str] = []
    header(parts, title, subtitle)
    card_x, card_w = 90, 980

    # Axis on the right margin, outside the cards.
    axis_x = 1128
    parts.append(path(f"M {axis_x} 640 L {axis_x} 150", stroke=MUTED, width=2, dash="6 6", marker="arrowMuted"))
    parts.append(text(axis_x, 132, axis_top, size=14, weight=700, fill=AMBER, anchor="middle"))
    parts.append(text(axis_x, 668, axis_bottom, size=14, weight=700, fill=MUTED, anchor="middle"))

    for index, rung in enumerate(rungs):
        num, rung_title, example, check, color, fill = rung
        y = top_y + index * step
        parts.append(rect(card_x, y, card_w, rung_h, fill=fill, stroke=color, stroke_width=2.2, shadow=True))
        parts.append(rect(card_x, y, 9, rung_h, fill=color, stroke=color, rx=4))
        parts.append(badge(card_x + card_w - 34, y + rung_h / 2, num, fill=color, r=18))
        parts.append(text(card_x + card_w - 66, y + 28, rung_title, size=20, weight=700, fill=color, anchor="start"))
        parts.append(text(card_x + card_w - 66, y + 52, example, size=14, fill=INK, anchor="start"))
        parts.append(text(card_x + 28, y + 42, check, size=13, fill=MUTED, anchor="end"))
    footer(parts, note, h - 40)
    save(name, "".join(parts), title=title, height=h)


def matrix2x2(
    name: str,
    title: str,
    subtitle: str,
    quadrants: list[tuple],
    note: str,
    *,
    h: int = 760,
    x_top: str = "تأثير أعلى",
    x_bottom: str = "تأثير أقل",
    y_left: str = "اهتمام أقل",
    y_right: str = "اهتمام أعلى",
    y_label: str = "درجة الاهتمام",
    x_label: str = "القدرة على التأثير",
) -> None:
    """A power/interest matrix. Quadrants are ordered: top-right, top-left,
    bottom-right, bottom-left."""
    parts: list[str] = []
    header(parts, title, subtitle)
    card_w, card_h = 420, 190
    left_x, right_x = 170, 610
    top_y, bottom_y = 190, 400

    # Axes first, visible in the 20px gaps between cards.
    parts.append(line(600, 170, 600, 610, stroke=BORDER, width=3, marker=False))
    parts.append(line(150, 390, 1050, 390, stroke=BORDER, width=3, marker=False))
    # Influence axis on the right margin.
    parts.append(path("M 1138 610 L 1138 175", stroke=MUTED, width=2, dash="6 6", marker="arrowMuted"))
    parts.append(text(1138, 158, x_top, size=14, weight=700, fill=AMBER, anchor="middle"))
    parts.append(text(1138, 638, x_bottom, size=14, weight=700, fill=MUTED, anchor="middle"))
    # Interest axis below the cards, increasing to the right.
    parts.append(path("M 170 632 L 1030 632", stroke=MUTED, width=2, dash="6 6", marker="arrowMuted"))
    parts.append(text(170, 660, y_left, size=14, weight=700, fill=MUTED, anchor="middle"))
    parts.append(text(1030, 660, y_right, size=14, weight=700, fill=AMBER, anchor="middle"))
    parts.append(text(600, 692, y_label, size=15, weight=700, fill=NAVY))
    parts.append(text(1138, 700, x_label, size=13, weight=700, fill=NAVY, anchor="middle"))

    positions = [(right_x, top_y), (left_x, top_y), (right_x, bottom_y), (left_x, bottom_y)]
    for index, quadrant in enumerate(quadrants):
        if len(quadrant) == 5:
            q_title, who, how, color, fill = quadrant
            num = str(index + 1)
        else:
            num, q_title, who, how, color, fill = quadrant
        x, y = positions[index]
        parts.append(rect(x, y, card_w, card_h, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(badge(x + card_w - 26, y + 26, num, fill=color, r=17))
        parts.append(text(x + card_w / 2, y + 44, q_title, size=22, weight=700, fill=color))
        parts.append(text(x + card_w / 2, y + 78, who, size=15, fill=INK, line_height=1.4))
        parts.append(text(x + card_w / 2, y + 118, how, size=14, fill=MUTED, line_height=1.4))
    footer(parts, note, h - 38)
    save(name, "".join(parts), title=title, height=h)


def week_plan(
    name: str,
    title: str,
    subtitle: str,
    goal: str,
    output: str,
    days: list[tuple[str, str, str, str, str]],
    note: str,
    *,
    h: int = 720,
) -> None:
    """Seven day cards, right to left, with a weekly goal banner."""
    parts: list[str] = []
    header(parts, title, subtitle)
    parts.append(rect(60, 140, 1080, 62, fill=NAVY, stroke=NAVY, rx=14))
    parts.append(text(1080, 166, f"الهدف الأسبوعي: {goal}", size=17, weight=700, fill=PAPER, anchor="start"))
    parts.append(text(1080, 190, f"المخرج الملموس: {output}", size=14, fill="#E2E8F0", anchor="start"))

    n = len(days)
    margin, gap = 40, 10
    card_w = (1200 - 2 * margin - gap * (n - 1)) / n
    card_h = 360
    for index, (day, focus, task1, task2, color) in enumerate(days):
        x = 1200 - margin - card_w - index * (card_w + gap)
        y = 230
        fill = TINT if index % 2 == 0 else PAPER
        parts.append(rect(x, y, card_w, card_h, fill=fill, stroke=color, stroke_width=2, shadow=True))
        parts.append(rect(x, y, card_w, 46, fill=color, stroke=color, rx=12))
        parts.append(text(x + card_w / 2, y + 31, day, size=18, weight=700, fill=PAPER))
        parts.append(text(x + card_w / 2, y + 82, focus, size=15, weight=700, fill=color))
        parts.append(text(x + card_w / 2, y + 120, task1, size=13, fill=INK, line_height=1.45))
        parts.append(text(x + card_w / 2, y + 190, task2, size=13, fill=MUTED, line_height=1.45))
        parts.append(circle(x + card_w / 2, y + card_h - 26, 7, fill=color))
    footer(parts, note, h - 38)
    save(name, "".join(parts), title=title, height=h)


def doors(
    name: str,
    title: str,
    subtitle: str,
    items: list[tuple],
    note: str,
    *,
    h: int = 660,
) -> None:
    """Five arched doors, one per life domain."""
    n = len(items)
    w, gap = 190, 25
    total = n * w + (n - 1) * gap
    x0 = (1200 - total) / 2
    parts: list[str] = []
    header(parts, title, subtitle)
    parts.append(line(60, 525, 1140, 525, stroke=BORDER, width=4, marker=False))
    for index, item in enumerate(items):
        num, item_title, body, color, fill = _step(item, index)
        x = x0 + (n - 1 - index) * (w + gap)
        y = 200
        d = (
            f"M {x} {y + 320} L {x} {y + 95} "
            f"Q {x} {y} {x + w / 2} {y} Q {x + w} {y} {x + w} {y + 95} "
            f"L {x + w} {y + 320} Z"
        )
        parts.append(path(d, stroke=color, width=2.5, fill=fill))
        parts.append(badge(x + w / 2, y + 52, num, fill=color, r=18))
        parts.append(text(x + w / 2, y + 120, item_title, size=22, weight=700, fill=color))
        parts.append(text(x + w / 2, y + 170, body, size=14, fill=INK, line_height=1.4))
        parts.append(circle(x + w - 32, y + 235, 6, fill=GOLD))
    footer(parts, note, h - 38)
    save(name, "".join(parts), title=title, height=h)
