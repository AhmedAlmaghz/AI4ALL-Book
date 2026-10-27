#!/usr/bin/env python3
"""Build a complete Arabic reading edition from the 34 chapter manuscripts.

Outputs an accessible, linked HTML reading copy, a reflowable EPUB 3 package,
and an A4 review PDF. This is a manuscript export, not a print-ready
PDF/X file or an approved publication edition.
"""

from __future__ import annotations

import csv
import html
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import markdown
import pymupdf
from lxml import html as lxml_html
from markdown.extensions.toc import slugify as markdown_slugify


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
MANUSCRIPT = ROOT / "manuscript"
MATRIX = ROOT / "docs" / "curriculum-matrix.csv"
ASSETS = ROOT / "assets" / "figures"
FONTS = ROOT / "assets" / "fonts"

PARTS = {
    0: {
        "title": "البوصلة: افهم قبل أن تستخدم",
        "question": "ما هذا الشيء؟ وكيف يعمل؟",
        "outcome": "خريطة ذهنية تساعدك على فهم الذكاء الاصطناعي وحدوده.",
    },
    1: {
        "title": "الأساس: أول مهاراتك",
        "question": "كيف أستخدمه بوعي؟",
        "outcome": "طلبات شخصية وقائمة تحقق للاستخدام الآمن والواعي.",
    },
    2: {
        "title": "الإنتاجية: وفّر وقتك",
        "question": "كيف أوفر وقتًا وأرفع جودة عملي؟",
        "outcome": "سير عمل عملية للكتابة والبحث والعروض والبيانات.",
    },
    3: {
        "title": "الأنظمة: ابنِ مساعدك",
        "question": "كيف أبني نظامًا يعمل من أجلي؟",
        "outcome": "مساعد شخصي وقاعدة معرفة وسير عمل مترابطة.",
    },
    4: {
        "title": "المسارات: الاحتراف في مجالك",
        "question": "كيف أطبق ما تعلمته في مجالي؟",
        "outcome": "تطبيقات عملية للطالب والموظف والباحث والمعلم والمستقل والحياة اليومية.",
    },
    5: {
        "title": "الاحتراف: من ممارس إلى قائد",
        "question": "كيف أقود الاستخدام وأدير مخاطره؟",
        "outcome": "خطة مسؤولة لتطوير المهارات والأنظمة والفرق.",
    },
    6: {
        "title": "الإطلاق: نظامك المتكامل",
        "question": "كيف أستمر وأنمو؟",
        "outcome": "مشروع تطبيقي وخطة استمرار لمدة تسعين يومًا.",
    },
}

FONT_FACE_CSS = r"""
@font-face{font-family:'IBM Plex Sans Arabic';src:url('fonts/IBMPlexSansArabic-Regular.ttf') format('truetype');font-weight:400;font-style:normal;font-display:block}
@font-face{font-family:'IBM Plex Sans Arabic';src:url('fonts/IBMPlexSansArabic-SemiBold.ttf') format('truetype');font-weight:600;font-style:normal;font-display:block}
@font-face{font-family:'IBM Plex Sans Arabic';src:url('fonts/IBMPlexSansArabic-Bold.ttf') format('truetype');font-weight:700;font-style:normal;font-display:block}
@font-face{font-family:'Alexandria';src:url('fonts/Alexandria-Variable.ttf') format('truetype');font-weight:100 900;font-style:normal;font-display:block}
@font-face{font-family:'Inter';src:url('fonts/Inter-Variable.ttf') format('truetype');font-weight:100 900;font-style:normal;font-display:block}
@font-face{font-family:'IBM Plex Mono';src:url('fonts/IBMPlexMono-Regular.ttf') format('truetype');font-weight:400;font-style:normal;font-display:block}
"""

CSS = FONT_FACE_CSS + r"""
:root {
  --navy:#14213D; --navy2:#1E2F55; --teal:#0F766E; --gold:#C6A15B;
  --amber:#B45309; --red:#B91C1C; --green:#15803D; --ink:#1F2937;
  --muted:#526174; --paper:#fff; --tint:#F5F7FA; --border:#D7DEE8;
  --body:'IBM Plex Sans Arabic','Segoe UI',Tahoma,Arial,sans-serif;
  --display:Alexandria,'IBM Plex Sans Arabic','Segoe UI',Tahoma,sans-serif;
  --latin:Inter,'Segoe UI',Arial,sans-serif; --mono:'IBM Plex Mono',Consolas,monospace;
}
* { box-sizing:border-box; }
html { direction:rtl; background:#e9edf2; scroll-behavior:smooth; }
body { margin:0; background:#e9edf2; color:var(--ink); font-family:var(--body); font-size:11.5pt; line-height:1.65; }
a { color:#075E59; text-decoration-thickness:1px; text-underline-offset:2px; overflow-wrap:anywhere; }
a:focus-visible { outline:3px solid #C6A15B; outline-offset:3px; }
header.site-head { max-width:920px; margin:22px auto 0; padding:12px 24px; color:var(--muted); font-size:13px; }
main.book { max-width:920px; margin:0 auto 48px; padding:0 24px 40px; background:white; box-shadow:0 12px 48px #14213d14; }
.cover { min-height:calc(100vh - 50px); display:flex; flex-direction:column; justify-content:center; padding:9% 11%; color:#fff; background:linear-gradient(145deg,#14213D 0%,#1E2F55 68%,#0F766E 150%); border:10px solid #C6A15B; position:relative; overflow:hidden; page:cover; break-after:page; }
.cover:after { content:""; position:absolute; width:340px; height:340px; left:-100px; bottom:-130px; border:1px solid #ffffff40; border-radius:50%; box-shadow:0 0 0 28px #ffffff0b,0 0 0 58px #ffffff0b,0 0 0 90px #ffffff0b; }
.cover-mark { display:inline-block; width:max-content; padding:5px 13px; border:1px solid #C6A15B; border-radius:999px; color:#F4D99D; letter-spacing:.03em; font-size:13px; }
.cover h1 { margin:38px 0 14px; max-width:680px; color:white; font:700 clamp(36px,6vw,64px)/1.3 var(--display); }
.cover .subtitle { max-width:620px; margin:0; color:#E2E8F0; font-size:clamp(19px,2.4vw,27px); line-height:1.55; }
.cover-rule { width:90px; height:4px; margin:32px 0 18px; background:var(--gold); }
.cover-meta { color:#E2E8F0; font-size:15px; }
.cover-status { margin-top:52px; padding:12px 16px; max-width:600px; border-right:3px solid var(--gold); background:#ffffff12; color:#fff; font-size:13px; }
.publication, .how-to-read, .toc, .part-page, .book-colophon, article.chapter { padding:48px 6.5%; }
.publication, .how-to-read, .toc, .book-colophon { break-after:page; }
.publication h2, .how-to-read h2, .toc h2, .book-colophon h2 { color:var(--navy); font:700 28px/1.35 var(--display); }
.publication dl { display:grid; grid-template-columns:minmax(130px, .7fr) 2fr; gap:0; border-top:1px solid var(--border); }
.publication dt,.publication dd { margin:0; padding:12px 8px; border-bottom:1px solid var(--border); }
.publication dt { color:var(--muted); font-weight:600; }
.draft-notice { padding:16px 20px; border-right:4px solid var(--amber); background:#FFFBEB; }
.how-to-read li { margin:.35em 0; }
.toc h2 { margin-top:0; }
.toc-part { margin:24px 0 8px; color:var(--teal); font-weight:700; }
.toc ol { margin:4px 0 18px; padding-right:24px; }
.toc li { margin:4px 0; }
.toc a { color:var(--ink); text-decoration:none; }
.part-page { min-height:590px; display:flex; flex-direction:column; justify-content:center; background:linear-gradient(155deg,#F5F7FA,#fff 70%); border-top:6px solid var(--gold); page:part; break-before:page; break-after:page; }
.part-number { color:#9A7A37; font-size:16px; font-weight:700; letter-spacing:.08em; }
.part-page h1 { margin:10px 0 26px; color:var(--navy); font:700 36px/1.35 var(--display); }
.part-question { margin:0 0 14px; color:var(--teal); font-size:20px; font-weight:700; }
.part-outcome { max-width:650px; color:var(--muted); font-size:17px; }
.part-chapters { margin-top:35px; padding-top:20px; border-top:1px solid var(--border); }
.part-chapters li { margin:4px 0; }
article.chapter { break-before:page; }
article.chapter h1 { margin:0 0 28px; padding-bottom:16px; border-bottom:2px solid var(--gold); color:var(--navy); font:700 32px/1.4 var(--display); string-set: running-chapter content(); }
article.chapter h2 { margin:26px 0 10px; color:var(--navy); font:700 15pt/1.4 var(--display); break-after:avoid-page; }
article.chapter h3 { margin:20px 0 8px; color:var(--teal); font:600 12pt/1.45 var(--display); break-after:avoid-page; }
article.chapter p { margin:0 0 8pt; text-align:justify; orphans:3; widows:3; }
article.chapter ul, article.chapter ol { padding-right:1.55em; padding-left:0; }
article.chapter li { padding-right:2px; margin:.22em 0; }
blockquote { margin:1.2em 0; padding:12px 18px; border-right:4px solid var(--teal); background:#ECFDF5; break-inside:avoid; }
blockquote p:last-child { margin-bottom:0; }
table { width:100%; border-collapse:collapse; margin:14px 0 18px; font-size:9.5pt; break-inside:auto; }
thead { display:table-header-group; }
th,td { border:1px solid var(--border); padding:8px 10px; vertical-align:top; text-align:right; overflow-wrap:anywhere; }
th { color:white; background:var(--navy); font-weight:600; }
tr { break-inside:avoid; }
tbody tr:nth-child(even) { background:#F5F7FA; }
pre { margin:18px 0; padding:16px; overflow:auto; direction:ltr; text-align:left; border:1px solid var(--border); border-radius:8px; background:#F5F7FA; font:13px/1.55 var(--mono); white-space:pre-wrap; overflow-wrap:anywhere; break-inside:avoid; }
code { direction:ltr; unicode-bidi:isolate; font: .9em var(--mono); }
:not(pre)>code { padding:1px 5px; border-radius:4px; background:#EEF2F7; }
hr { height:1px; border:0; margin:28px 0; background:var(--border); }
img { display:block; max-width:100%; height:auto; margin:18px auto; }
figure, p:has(> img) { margin:20px auto 26px; text-align:center; break-inside:avoid; }
figure img, p:has(> img) img { max-height:185mm; object-fit:contain; }
figcaption { margin-top:8px; color:var(--muted); font-size:9.5pt; line-height:1.5; text-align:center; }
figcaption strong { color:var(--navy); }
.book-colophon { background:#F5F7FA; }
.book-colophon h2 { margin-top:0; }
.book-colophon li { margin:.5em 0; }
.sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
@page { size:210mm 297mm; margin:20mm 18mm 22mm 22mm;
  @top-right { content:"من الصفر إلى الاحتراف"; color:#526174; font:9pt 'IBM Plex Sans Arabic',Tahoma,sans-serif; }
  @top-left { content:string(running-chapter); color:#526174; font:8pt 'IBM Plex Sans Arabic',Tahoma,sans-serif; }
  @bottom-center { content:counter(page); color:#526174; font:9pt Inter,Arial,sans-serif; }
}
@page :right { margin-left:22mm; margin-right:18mm; }
@page :left { margin-left:18mm; margin-right:22mm; }
@page cover { size:210mm 297mm; margin:0; @top-right{content:none} @top-left{content:none} @bottom-center{content:none} }
@page part { @top-right{content:none} @top-left{content:none} @bottom-center{content:none} }
@media screen {
  .cover { min-height:920px; }
  .part-page { min-height:820px; }
  article.chapter { padding-top:65px; padding-bottom:75px; }
}
@media print {
  html,body { background:white; }
  header.site-head { display:none; }
  main.book { max-width:none; margin:0; padding:0; box-shadow:none; }
  .cover { min-height:297mm; height:297mm; }
  .publication,.how-to-read,.toc,.part-page,.book-colophon,article.chapter { padding:0; }
  .part-page { min-height:185mm; }
  a { color:#075E59; }
}
"""

EPUB_CSS = CSS.replace("url('fonts/", "url('../fonts/")


def parse_book_yaml(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        values[key] = value
    return values


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    _, raw_meta, body = text.split("---", 2)
    meta: dict[str, str] = {}
    for line in raw_meta.splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            meta[key] = value.strip().strip('"')
    return meta, body.lstrip("\r\n")


def load_matrix() -> list[dict[str, str]]:
    with MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda row: int(row["chapter"]))
    expected = list(range(1, 35))
    actual = [int(row["chapter"]) for row in rows]
    if actual != expected:
        raise ValueError(f"Expected exactly chapters 1–34 in order; received {actual}.")
    return rows


def find_chapter_file(number: int) -> Path:
    matches = list(MANUSCRIPT.glob(f"**/ch{number:02d}.md"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one manuscript file for chapter {number}, got {len(matches)}.")
    return matches[0]


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def remove_editor_notes(text: str) -> str:
    return re.split(r"(?m)^##\s+ملاحظات للمؤلف(?:\s|$).*?$", text, maxsplit=1)[0].rstrip()


def inject_available_figures(body: str, chapter: int) -> str:
    pattern = re.compile(rf"(?m)^\*\*الشكل\s+0?{chapter}-(\d+):\*\*([^\n]*)(?:\n(\*تعليق:.*))?$")
    available = {int(match.group(1)) for match in re.finditer(rf"^fig-{chapter:02d}-(\d+)\.svg$", "\n".join(p.name for p in ASSETS.glob("fig-*.svg")), re.M)}
    if not available:
        return body

    def replace(match: re.Match[str]) -> str:
        figure_no = int(match.group(1))
        if figure_no not in available:
            return match.group(0)
        caption = re.sub(r"\s+", " ", match.group(2).strip()).strip(" .")
        alt = f"الشكل {chapter}-{figure_no}: {caption}".strip()
        comment = match.group(3) or ""
        figure_html = (
            "\n\n<figure>"
            f'<figcaption><strong>الشكل {chapter}-{figure_no}:</strong> {esc(caption)}</figcaption>'
            f'<img src="../assets/figures/fig-{chapter:02d}-{figure_no}.svg" alt="{esc(alt)}" />'
            "</figure>\n\n"
        )
        return figure_html + (comment + "\n" if comment else "")

    return pattern.sub(replace, body)


def normalize_fragment(fragment: str) -> str:
    parent = lxml_html.fragment_fromstring(fragment or "", create_parent="div")
    parts = []
    if parent.text:
        parts.append(html.escape(parent.text))
    for child in parent:
        parts.append(lxml_html.tostring(child, encoding="unicode", method="xml", with_tail=True))
    return "".join(parts)


def markdown_to_xhtml(body: str, chapter: int) -> str:
    prefix = f"chapter-{chapter:02d}-"

    def unique_slug(value: str, separator: str) -> str:
        return prefix + markdown_slugify(value, separator)

    converter = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
        extension_configs={"toc": {"slugify": unique_slug}},
        output_format="xhtml",
    )
    return normalize_fragment(converter.convert(body))


def chapter_content(row: dict[str, str]) -> tuple[dict[str, str], str, int]:
    number = int(row["chapter"])
    source = find_chapter_file(number).read_text(encoding="utf-8")
    meta, body = parse_front_matter(source)
    body = remove_editor_notes(body)
    body = inject_available_figures(body, number)
    count = word_count(body)
    return meta, markdown_to_xhtml(body, number), count


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def title_page(book: dict[str, str], epub: bool = False) -> str:
    title = esc(book.get("title", "من الصفر إلى الاحتراف"))
    subtitle = esc(book.get("subtitle", ""))
    edition = esc(book.get("edition", "0.1-draft"))
    year = esc(book.get("year", "2026"))
    cover_class = "cover"
    return f'''<section class="{cover_class}" id="cover" epub:type="cover">
  <span class="cover-mark">كتاب عملي للقارئ العربي</span>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  <div class="cover-rule"></div>
  <p class="cover-meta">نسخة قراءة تجميعية · <bdi dir="ltr">{edition}</bdi> · <bdi dir="ltr">{year}</bdi></p>
  <p class="cover-status">مسودة للمراجعة، وليست طبعة نشر معتمدة. اسم المؤلف وبيانات النشر قيد الاعتماد.</p>
</section>'''


def publication_page(book: dict[str, str]) -> str:
    edition = esc(book.get("edition", "0.1-draft"))
    year = esc(book.get("year", "2026"))
    return f'''<section class="publication" id="publication-data" epub:type="copyright-page">
  <h2>بيانات النسخة</h2>
  <p class="draft-notice"><strong>نسخة قراءة للمراجعة:</strong> جُمعت من المخطوط الحالي لتسهيل القراءة والتحرير، ولا تمثل اعتمادًا نهائيًا للنص أو بيانات النشر.</p>
  <dl>
    <dt>العنوان</dt><dd>{esc(book.get("title", "من الصفر إلى الاحتراف"))}</dd>
    <dt>العنوان الفرعي</dt><dd>{esc(book.get("subtitle", ""))}</dd>
    <dt>الإصدار</dt><dd><bdi dir="ltr">{edition}</bdi></dd>
    <dt>سنة بيانات المشروع</dt><dd><bdi dir="ltr">{year}</bdi></dd>
    <dt>المؤلف والناشر والرقم الدولي</dt><dd>قيد الاعتماد؛ لم تُثبت في بيانات النشر.</dd>
    <dt>مقاس نسخة المراجعة</dt><dd>A4 — 21 × 29.7 سم</dd>
  </dl>
  <p>تظهر الإحالات والمصادر في مواضعها داخل الفصول. بعض المسائل ما زالت تحتاج مراجعة تحريرية أو تخصصية قبل إصدار طبعة نهائية.</p>
</section>'''


def how_to_read_page() -> str:
    return '''<section class="how-to-read" id="how-to-read" epub:type="preface">
  <h2>كيف تستخدم هذا الكتاب؟</h2>
  <p>هذا مسار تطبيقي من الفهم إلى الاستخدام ثم بناء نظام شخصي ومشروع متكامل. لا تحتاج إلى خبرة برمجية؛ خذ الفكرة من كل فصل، وجرّب نشاطه على مهمة حقيقية من حياتك.</p>
  <ul>
    <li><strong>ابدأ بالمهمة:</strong> اختر عملًا صغيرًا ومتكررًا تريد تحسينه، وحدد ما الذي يجعل النتيجة جيدة.</li>
    <li><strong>جرّب ثم راجع:</strong> تعامل مع مخرجات الأداة كمسودة، وافحص المصادر والأرقام والخصوصية قبل الاعتماد.</li>
    <li><strong>احتفظ بما تعلمته:</strong> دوّن الطلبات وسير العمل التي نجحت، وحدّثها عندما تتغير الأدوات أو احتياجاتك.</li>
    <li><strong>تحرك بالقدر المناسب:</strong> يمكنك قراءة الفصول بالترتيب أو اختيار مسار مجالك من الجزء الرابع، ثم العودة إلى الأساسيات عند الحاجة.</li>
  </ul>
  <p>أسماء الأدوات وواجهاتها تتغير. ركّز على المبادئ، وتحقق من الميزات والأسعار والسياسات الحالية قبل أن تبني عليها قرارًا.</p>
</section>'''


def part_page(part: int, rows: list[dict[str, str]]) -> str:
    info = PARTS[part]
    chapters = "".join(
        f'<li><a href="#chapter-{int(row["chapter"]):02d}">{esc(row["title"])}</a></li>'
        for row in rows
    )
    return f'''<section class="part-page" id="part-{part}" epub:type="part">
  <span class="part-number">الجزء {part}</span>
  <h1>{esc(info["title"])}</h1>
  <p class="part-question">{esc(info["question"])}</p>
  <p class="part-outcome">{esc(info["outcome"])}</p>
  <div class="part-chapters"><strong>فصول هذا الجزء</strong><ol>{chapters}</ol></div>
</section>'''


def toc_html(rows: list[dict[str, str]]) -> str:
    groups: list[str] = []
    for part in range(7):
        part_rows = [row for row in rows if int(row["part"]) == part]
        items = "".join(
            f'<li><a href="#chapter-{int(row["chapter"]):02d}">{esc(row["title"])}</a></li>'
            for row in part_rows
        )
        groups.append(
            f'<section><h3 class="toc-part"><a href="#part-{part}">الجزء {part}: {esc(PARTS[part]["title"])}</a></h3><ol>{items}</ol></section>'
        )
    return '<section class="toc" id="contents" epub:type="toc"><h2>الفهرس</h2>' + "".join(groups) + "</section>"


def colophon_page(book: dict[str, str], total_words: int) -> str:
    return f'''<section class="book-colophon" id="edition-note" epub:type="afterword">
  <h2>عن هذه النسخة</h2>
  <p>تضم هذه النسخة فصول المخطوط الأربعة والثلاثين، مرتبة في سبعة أجزاء. جُمعت ملاحظات المؤلف الداخلية خارج نص القراءة، وأُدرجت الرسوم المتاحة في ملفات المشروع قرب مواضعها.</p>
  <ul>
    <li>حالة النص: مسودة كاملة قيد المراجعة، وليست طبعة نهائية معتمدة.</li>
    <li>حجم متن الفصول بعد استبعاد ملاحظات المؤلف: نحو {total_words:,} كلمة.</li>
    <li>الاسم والناشر والرقم الدولي، والمراجعة التقنية واللغوية واختبار القراء والبروفة الورقية: لم تعتمد بعد.</li>
    <li>صيغة PDF في هذه الحزمة مخصصة للقراءة والمراجعة؛ يلزم إعداد ملف ما قبل الطباعة وفحصه عند اعتماد طبعة ورقية.</li>
  </ul>
  <p>الإصدار <bdi dir="ltr">{esc(book.get("edition", "0.1-draft"))}</bdi> · <bdi dir="ltr">{esc(book.get("year", "2026"))}</bdi></p>
</section>'''


def build_html(book: dict[str, str], rows: list[dict[str, str]]) -> tuple[str, int, dict[int, int]]:
    fragments: list[str] = [title_page(book), publication_page(book), how_to_read_page(), toc_html(rows)]
    total_words = 0
    chapter_words: dict[int, int] = {}
    for part in range(7):
        part_rows = [row for row in rows if int(row["part"]) == part]
        fragments.append(part_page(part, part_rows))
        for row in part_rows:
            number = int(row["chapter"])
            meta, content, count = chapter_content(row)
            total_words += count
            chapter_words[number] = count
            title = meta.get("title", row["title"])
            fragments.append(
                f'<article class="chapter" id="chapter-{number:02d}" data-title="{esc(title)}" epub:type="chapter">{content}</article>'
            )
    fragments.append(colophon_page(book, total_words))
    html_text = f'''<!doctype html>
<html lang="ar" dir="rtl" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="نسخة قراءة تجميعية كاملة لمسودة كتاب من الصفر إلى الاحتراف." />
  <title>{esc(book.get("title", "من الصفر إلى الاحتراف"))} — نسخة قراءة تجميعية</title>
  <link rel="stylesheet" href="book.css" />
</head>
<body>
  <header class="site-head"><span>{esc(book.get("title", "من الصفر إلى الاحتراف"))}</span> · نسخة قراءة تجميعية</header>
  <main class="book">{''.join(fragments)}</main>
</body>
</html>
'''
    return html_text, total_words, chapter_words


def xhtml_document(title: str, body: str, stylesheet: str = "../styles/book.css", extra_head: str = "") -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ar" lang="ar" dir="rtl">
<head><meta charset="utf-8" /><title>{esc(title)}</title><link rel="stylesheet" type="text/css" href="{esc(stylesheet)}" />{extra_head}</head>
<body>{body}</body>
</html>
'''


def build_epub(book: dict[str, str], rows: list[dict[str, str]], out_path: Path, total_words: int) -> int:
    staging = Path(tempfile.mkdtemp(prefix="arabic-book-epub-"))
    try:
        meta_dir = staging / "META-INF"
        epub_dir = staging / "EPUB"
        text_dir = epub_dir / "text"
        styles_dir = epub_dir / "styles"
        images_dir = epub_dir / "images"
        fonts_dir = epub_dir / "fonts"
        for directory in (meta_dir, text_dir, styles_dir, images_dir, fonts_dir):
            directory.mkdir(parents=True, exist_ok=True)
        (staging / "mimetype").write_text("application/epub+zip", encoding="ascii")
        (meta_dir / "container.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            '<rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',
            encoding="utf-8",
        )
        (styles_dir / "book.css").write_text(EPUB_CSS, encoding="utf-8")

        items: list[tuple[str, str, str]] = []
        for font_path in sorted(FONTS.glob("*.ttf")):
            shutil.copy2(font_path, fonts_dir / font_path.name)
            items.append((f"font-{font_path.stem}", f"fonts/{font_path.name}", "font/ttf"))
        spine: list[tuple[str, bool]] = []
        nav_parts: list[str] = []
        landmark_chapters: list[str] = []

        def add_xhtml(item_id: str, filename: str, title: str, body: str, *, linear: bool = True) -> None:
            (text_dir / filename).write_text(xhtml_document(title, body), encoding="utf-8")
            items.append((item_id, f"text/{filename}", "application/xhtml+xml"))
            spine.append((item_id, linear))

        title_text = book.get("title", "من الصفر إلى الاحتراف")
        add_xhtml("cover", "cover.xhtml", title_text, title_page(book))
        add_xhtml("publication", "publication.xhtml", "بيانات النسخة", publication_page(book))
        add_xhtml("how-to-read", "how-to-read.xhtml", "كيف تستخدم هذا الكتاب؟", how_to_read_page())
        epub_toc = toc_html(rows)
        epub_toc = re.sub(r'href="#part-(\d+)"', r'href="part-\1.xhtml"', epub_toc)
        epub_toc = re.sub(r'href="#chapter-(\d+)"', r'href="chapter-\1.xhtml"', epub_toc)
        add_xhtml("contents-page", "contents.xhtml", "الفهرس", epub_toc)
        landmark_chapters.append('<li><a epub:type="toc" href="nav.xhtml">الفهرس</a></li>')
        landmark_chapters.append('<li><a epub:type="bodymatter" href="text/part-0.xhtml">بداية الكتاب</a></li>')

        # EPUB chapters live in text/, so update the figure paths and package the SVGs.
        figure_paths: set[str] = set()
        for part in range(7):
            part_rows = [row for row in rows if int(row["part"]) == part]
            page_body = part_page(part, part_rows)
            page_body = re.sub(r'href="#chapter-(\d+)"', r'href="chapter-\1.xhtml"', page_body)
            add_xhtml(f"part-{part}", f"part-{part}.xhtml", f"الجزء {part}: {PARTS[part]['title']}", page_body)
            nav_items = "".join(
                f'<li><a href="text/chapter-{int(row["chapter"]):02d}.xhtml">{esc(row["title"])}</a></li>'
                for row in part_rows
            )
            nav_parts.append(f'<li><a href="text/part-{part}.xhtml">الجزء {part}: {esc(PARTS[part]["title"])}</a><ol>{nav_items}</ol></li>')
            for row in part_rows:
                number = int(row["chapter"])
                meta, content, _ = chapter_content(row)
                title = meta.get("title", row["title"])
                content = content.replace("../assets/figures/", "../images/")
                for found in re.findall(r'\bsrc="\.\./images/([^"]+\.svg)"', content):
                    figure_paths.add(found)
                body = f'<section epub:type="chapter" id="chapter-{number:02d}">{content}</section>'
                add_xhtml(f"chapter-{number:02d}", f"chapter-{number:02d}.xhtml", title, body)
                if number == 1:
                    landmark_chapters[1] = '<li><a epub:type="bodymatter" href="text/chapter-01.xhtml">بداية الكتاب</a></li>'

        add_xhtml("about", "about.xhtml", "عن هذه النسخة", colophon_page(book, total_words))
        nav_body = (
            '<nav epub:type="toc" id="toc"><h1>الفهرس</h1><ol>' + "".join(nav_parts) + '</ol></nav>'
            '<nav epub:type="landmarks" hidden="hidden"><h2>معالم الكتاب</h2><ol>'
            + "".join(landmark_chapters)
            + '<li><a epub:type="copyright-page" href="text/publication.xhtml">بيانات النسخة</a></li>'
            + '</ol></nav>'
        )
        nav_content = xhtml_document("فهرس الكتاب", nav_body, "styles/book.css").replace(
            '<html xmlns="http://www.w3.org/1999/xhtml"', '<html xmlns="http://www.w3.org/1999/xhtml"'
        )
        (epub_dir / "nav.xhtml").write_text(nav_content, encoding="utf-8")
        items.append(("nav", "nav.xhtml", "application/xhtml+xml"))

        for name in sorted(figure_paths):
            source = ASSETS / name
            if not source.is_file():
                raise FileNotFoundError(f"Chapter refers to a missing illustration: {source}")
            shutil.copy2(source, images_dir / name)
            items.append((f"image-{Path(name).stem}", f"images/{name}", "image/svg+xml"))

        package_items = []
        for item_id, href, media_type in items:
            properties = ' properties="nav"' if item_id == "nav" else ""
            package_items.append(f'<item id="{esc(item_id)}" href="{esc(href)}" media-type="{media_type}"{properties}/>')
        spine_items = "".join(
            f'<itemref idref="{esc(item_id)}"{(" linear=\"no\"" if not linear else "")}/>'
            for item_id, linear in spine
        )
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="ar" prefix="dcterms: http://purl.org/dc/terms/ rendition: http://www.idpf.org/vocab/rendition/# schema: http://schema.org/">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">urn:uuid:8d477e6d-3b38-4fd6-9c68-34d83d2e0e01</dc:identifier>
    <dc:title>{esc(title_text)}</dc:title><dc:language>ar</dc:language>
    <dc:subject>الذكاء الاصطناعي؛ مهارات عملية؛ تعلم ذاتي</dc:subject>
    <dc:description>نسخة قراءة تجميعية لمسودة من 34 فصلًا، غير معتمدة للنشر.</dc:description>
    <meta property="dcterms:modified">{now}</meta>
    <meta property="schema:accessMode">textual</meta>
    <meta property="schema:accessMode">visual</meta>
    <meta property="schema:accessModeSufficient">textual,visual</meta>
    <meta property="schema:accessibilityFeature">alternativeText</meta>
    <meta property="schema:accessibilityFeature">structuralNavigation</meta>
    <meta property="schema:accessibilityFeature">tableOfContents</meta>
    <meta property="schema:accessibilityFeature">readingOrder</meta>
    <meta property="schema:accessibilityHazard">unknown</meta>
    <meta property="schema:accessibilitySummary">النص الكامل متاح مع 67 نصًا بديلًا للرسوم وبنية تنقل؛ لم يُختبر بعد بقارئ شاشة، ولا يُدّعى امتثال كامل لـEPUB Accessibility 1.1.</meta>
    <meta property="rendition:layout">reflowable</meta><meta property="rendition:orientation">auto</meta>
    <meta property="rendition:spread">auto</meta>
  </metadata>
  <manifest>{''.join(package_items)}</manifest>
  <spine page-progression-direction="rtl">{spine_items}</spine>
</package>'''
        (epub_dir / "package.opf").write_text(opf, encoding="utf-8")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        if out_path.exists():
            out_path.unlink()
        with zipfile.ZipFile(out_path, "w") as archive:
            archive.write(staging / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
            for path in sorted(staging.rglob("*")):
                if path.is_file() and path.name != "mimetype":
                    archive.write(path, path.relative_to(staging).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
        return len(figure_paths)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def find_chrome() -> str:
    candidates = [
        shutil.which("chrome"),
        shutil.which("msedge"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise FileNotFoundError("Chrome or Edge is required to produce the review PDF.")


def set_pdf_metadata_and_bookmarks(pdf_path: Path, rows: list[dict[str, str]], book: dict[str, str]) -> tuple[int, tuple[float, float]]:
    doc = pymupdf.open(pdf_path)
    metadata = doc.metadata or {}
    metadata.update({
        "title": book.get("title", "من الصفر إلى الاحتراف") + " — نسخة قراءة تجميعية",
        "author": "",
        "subject": "مسودة مراجعة؛ ليست طبعة نشر معتمدة",
        "keywords": "الذكاء الاصطناعي، مهارات عملية، تعلم ذاتي، نسخة مراجعة",
        "creator": "scripts/export-book.py",
    })
    doc.set_metadata(metadata)
    destinations: dict[str, int] = {}
    for page in doc:
        for link in page.get_links():
            name = link.get("nameddest", "")
            page_index = link.get("page", -1)
            if name and page_index >= 0:
                destinations.setdefault(name, page_index + 1)
    toc: list[list] = []
    for part in range(7):
        part_page = destinations.get(f"part-{part}")
        if part_page:
            toc.append([1, f"الجزء {part}: {PARTS[part]['title']}", part_page])
        part_rows = [row for row in rows if int(row["part"]) == part]
        for row in part_rows:
            number = int(row["chapter"])
            page_number = destinations.get(f"chapter-{number:02d}")
            if page_number:
                toc.append([2, f"الفصل {number}: {row['title']}", page_number])
    chapters_in_toc = sum(1 for row in toc if row[0] == 2)
    if chapters_in_toc != 34:
        doc.close()
        raise ValueError(f"PDF internal links identify {chapters_in_toc} chapters; expected 34.")
    doc.set_toc(toc)
    first = doc[0]
    size_cm = (round(first.rect.width / 72 * 2.54, 2), round(first.rect.height / 72 * 2.54, 2))
    pages = len(doc)
    if doc.can_save_incrementally():
        doc.saveIncr()
    else:
        temp_pdf = pdf_path.with_name(pdf_path.stem + ".metadata.pdf")
        temp_pdf.unlink(missing_ok=True)
        doc.save(temp_pdf, garbage=1, deflate=False)
        doc.close()
        temp_pdf.replace(pdf_path)
        return pages, size_cm
    doc.close()
    return pages, size_cm


def export_pdf(html_path: Path, pdf_path: Path) -> tuple[int, tuple[float, float]]:
    chrome = find_chrome()
    with tempfile.TemporaryDirectory(prefix="arabic-book-chrome-") as profile:
        command = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--allow-file-access-from-files",
            f"--user-data-dir={profile}",
            "--virtual-time-budget=30000",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=900, check=False)
    if not pdf_path.is_file() or pdf_path.stat().st_size < 100_000:
        raise RuntimeError(f"PDF export failed (Chrome exit {result.returncode}).\n{result.stderr[-3000:]}")
    return (0, (0.0, 0.0))


def validate_epub(epub_path: Path) -> tuple[int, int]:
    with zipfile.ZipFile(epub_path) as archive:
        bad_file = archive.testzip()
        if bad_file:
            raise ValueError(f"EPUB ZIP integrity failed at {bad_file}")
        names = archive.namelist()
        if not names or names[0] != "mimetype" or archive.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
            raise ValueError("EPUB mimetype is missing, out of order, or compressed.")
        opf = ET.fromstring(archive.read("EPUB/package.opf"))
        ns = {"opf": "http://www.idpf.org/2007/opf"}
        declared = {item.attrib["href"] for item in opf.findall(".//opf:manifest/opf:item", ns)}
        actual = {name.removeprefix("EPUB/") for name in names if name.startswith("EPUB/")}
        missing = sorted(href for href in declared if href not in actual)
        if missing:
            raise ValueError(f"EPUB manifest references missing files: {missing}")
        for name in names:
            if name.endswith((".xhtml", ".opf", ".xml")):
                root = ET.fromstring(archive.read(name))
                if name.endswith(".xhtml"):
                    base = Path(name).parent
                    ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
                    for element in root.iter():
                        for attr in ("href", "src"):
                            ref = element.attrib.get(attr, "")
                            if not ref or ref.startswith(("https://", "http://", "mailto:")):
                                continue
                            target_path, _, fragment = ref.partition("#")
                            if not target_path:
                                if fragment and fragment not in ids:
                                    raise ValueError(f"EPUB fragment link #{fragment} is missing in {name}.")
                                continue
                            target_name = posixpath.normpath((base / target_path).as_posix())
                            if target_name not in names:
                                raise ValueError(f"EPUB link target is missing: {name} -> {target_name}")
                            if fragment:
                                target_root = ET.fromstring(archive.read(target_name))
                                target_ids = {node.attrib["id"] for node in target_root.iter() if "id" in node.attrib}
                                if fragment not in target_ids:
                                    raise ValueError(f"EPUB fragment target #{fragment} is missing in {target_name}.")
        nav = archive.read("EPUB/nav.xhtml").decode("utf-8")
        chapter_count = len(set(re.findall(r'href="text/chapter-(\d{2})\.xhtml"', nav)))
        image_count = len([name for name in names if name.startswith("EPUB/images/")])
        if chapter_count != 34:
            raise ValueError(f"EPUB navigation includes {chapter_count} chapters; expected 34.")
        return chapter_count, image_count


def render_preview_pages(pdf_path: Path, pages: dict[str, int]) -> None:
    preview_dir = DIST / "preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open(pdf_path)
    for label, page_number in pages.items():
        if 1 <= page_number <= len(document):
            document[page_number - 1].get_pixmap(dpi=105, alpha=False).save(preview_dir / f"{label}.png")
    document.close()


def page_with_destination(pdf_path: Path, marker: str, default: int = 1) -> int:
    with pymupdf.open(pdf_path) as document:
        for page in document:
            for link in page.get_links():
                if link.get("nameddest") == marker and link.get("page", -1) >= 0:
                    return link["page"] + 1
        return default


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    book = parse_book_yaml(ROOT / "book.yaml")
    rows = load_matrix()
    html_text, total_words, chapter_words = build_html(book, rows)
    html_path = DIST / "book-full-draft.html"
    css_path = DIST / "book.css"
    pdf_path = DIST / "book-full-draft.pdf"
    epub_path = DIST / "book-full-draft.epub"
    html_path.write_text(html_text, encoding="utf-8")
    css_path.write_text(CSS, encoding="utf-8")
    dist_fonts = DIST / "fonts"
    dist_fonts.mkdir(parents=True, exist_ok=True)
    for font_path in sorted(FONTS.glob("*.ttf")):
        shutil.copy2(font_path, dist_fonts / font_path.name)

    image_count = build_epub(book, rows, epub_path, total_words)
    epub_chapters, epub_images = validate_epub(epub_path)
    if epub_images != image_count:
        raise ValueError(f"EPUB contains {epub_images} images; expected {image_count}.")

    pdf_path.unlink(missing_ok=True)
    (DIST / "book-full-draft.metadata.pdf").unlink(missing_ok=True)
    export_pdf(html_path, pdf_path)
    page_count, page_size = set_pdf_metadata_and_bookmarks(pdf_path, rows, book)
    with pymupdf.open(pdf_path) as doc:
        if len(doc.get_toc()) < 41:
            raise ValueError(f"PDF outline includes only {len(doc.get_toc())} entries; expected 41.")
        catalog = doc.pdf_catalog()
        if doc.xref_get_key(catalog, "Lang") != ("string", "ar"):
            raise ValueError("PDF catalog language is missing or not Arabic.")
        if doc.xref_get_key(catalog, "StructTreeRoot")[0] == "null":
            raise ValueError("PDF has no structure tree; a tagged PDF is expected.")
        alt_texts = sum(
            1
            for xref in range(1, doc.xref_length())
            if "/Alt" in doc.xref_object(xref, compressed=True)
        )
        if alt_texts < image_count:
            raise ValueError(f"PDF has {alt_texts} alt texts; expected at least {image_count}.")
    preview_pages = {
        "cover": 1,
        "contents": 4,
        "chapter-05": page_with_destination(pdf_path, "chapter-05"),
        "chapter-17": page_with_destination(pdf_path, "chapter-17"),
        "chapter-34": page_with_destination(pdf_path, "chapter-34"),
    }
    render_preview_pages(pdf_path, preview_pages)

    target_pages = book.get("target_pages", "540-580")
    font_count = len(list(FONTS.glob("*.ttf")))
    figure_count = len(list(ASSETS.glob("fig-*.svg")))
    summary = f'''# ملخص التصدير (مولّد آليًا)

- المدخل: {len(rows)} فصلًا من 7 أجزاء.
- كلمات المتن بعد استبعاد ملاحظات المؤلف: {total_words:,}.
- PDF: {page_count} صفحة، مقاس {page_size[0]} × {page_size[1]} سم.
- هدف التخطيط في `book.yaml`: {target_pages} صفحة.
- EPUB: {epub_chapters} فصلًا في التنقل، و{epub_images} رسم SVG، و{font_count} خطًا مضمّنًا.
- الأشكال المتاحة في `assets/figures`: {figure_count}.
- صفحات المعاينة: الغلاف، الفهرس، الفصول 5 و17 و34 في `dist/preview/`.

هذا ملخص آلي؛ التقرير البشري المفصل في `docs/export-report.md`.
'''
    (DIST / "export-summary.md").write_text(summary, encoding="utf-8")

    print(f"Chapters: {len(rows)} (EPUB navigation verified: {epub_chapters})")
    print(f"Chapter words: {total_words:,}")
    print(f"PDF: {pdf_path} — {page_count} pages at {page_size[0]} × {page_size[1]} cm")
    print(f"EPUB: {epub_path} — {epub_images} SVG illustrations")
    print(f"HTML: {html_path}")
    print(f"Preview pages: {preview_pages}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
