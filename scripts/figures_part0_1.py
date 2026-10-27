#!/usr/bin/env python3
"""Figures for Part 0 (chapters 1–4) and the shared chapters 6 and 10."""

from __future__ import annotations

import figure_kit as kit
from figure_kit import (
    AMBER,
    BORDER,
    DARK_RED,
    EXERCISE,
    GOLD,
    GREEN,
    IDEA,
    INK,
    MUTED,
    NAVY,
    PAPER,
    RED,
    TEAL,
    TINT,
    TIP,
    TRY,
    WARNING,
    badge,
    circle,
    footer,
    header,
    line,
    lri,
    path,
    rect,
    save,
    text,
)


# ---------------------------------------------------------------------------
# 1-1 — families of AI (overlapping circles)
# ---------------------------------------------------------------------------
def figure_01_1() -> None:
    parts: list[str] = []
    header(parts, "عائلات الذكاء الاصطناعي", "دوائر متداخلة… ليست بديلًا عن بعضها")
    # Overlapping families: AI ⊃ ML ⊃ DL ⊃ generative/LLM
    parts.append(
        f'<circle cx="410" cy="400" r="255" fill="{TRY}" fill-opacity="0.55" '
        f'stroke="{NAVY}" stroke-width="3"/>'
    )
    parts.append(
        f'<circle cx="585" cy="400" r="190" fill="{IDEA}" fill-opacity="0.65" '
        f'stroke="{TEAL}" stroke-width="3"/>'
    )
    parts.append(
        f'<circle cx="750" cy="400" r="128" fill="{TIP}" fill-opacity="0.75" '
        f'stroke="{GOLD}" stroke-width="3"/>'
    )
    parts.append(
        f'<circle cx="805" cy="400" r="66" fill="{EXERCISE}" fill-opacity="0.85" '
        f'stroke="{GREEN}" stroke-width="2.5"/>'
    )

    # Labels outside the circles, with short leader lines.
    parts.append(text(235, 148, "الذكاء الاصطناعي", size=26, weight=700, fill=NAVY))
    parts.append(line(280, 162, 345, 285, stroke=NAVY, width=2, marker=False))
    parts.append(text(585, 148, "تعلم الآلة", size=25, weight=700, fill=TEAL))
    parts.append(line(585, 162, 585, 250, stroke=TEAL, width=2, marker=False))
    parts.append(text(930, 210, "التعلم العميق", size=24, weight=700, fill=AMBER))
    parts.append(line(895, 224, 820, 320, stroke=GOLD, width=2, marker=False))
    parts.append(text(1115, 392, "توليدي", size=21, weight=700, fill=GREEN, anchor="start"))
    parts.append(text(1115, 420, "ونماذج لغوية", size=17, fill=GREEN, anchor="start"))
    parts.append(line(990, 400, 872, 400, stroke=GREEN, width=2, marker=False))

    # Concrete examples sit below the outer circle, clear of the footer.
    parts.append(text(300, 672, "أنظمة خبيرة، روبوتات، ألعاب", size=15, fill=MUTED))
    parts.append(text(560, 672, "تصنيف، تنبؤ، توصية", size=15, fill=MUTED))
    parts.append(text(790, 672, "شبكات عصبية، صور، صوت", size=15, fill=MUTED))
    parts.append(text(805, 480, "نص، صورة، كود", size=14, fill=GREEN))

    footer(parts, "كل نموذج توليدي يستخدم تعلم الآلة، لكن ليس كل تعلم آلي توليديًا.", 722)
    save("fig-01-1.svg", "".join(parts), title="عائلات الذكاء الاصطناعي", height=760)


# ---------------------------------------------------------------------------
# 1-2 — a short timeline
# ---------------------------------------------------------------------------
def figure_01_2() -> None:
    milestones = [
        ("1950", "اختبار تورينج", "هل تستطيع الآلة التفكير؟"),
        ("1956", "مؤتمر دارتموث", "يولد مصطلح «الذكاء الاصطناعي»."),
        ("1970s–80s", "الأنظمة الخبيرة", "قواعد ناجحة في مجالات ضيقة."),
        ("1990s–2000s", "التعلم الآلي", "تحول من القواعد إلى الأمثلة."),
        ("2012", "قفزة التعلم العميق", "الشبكات العصبية تثبت قوتها."),
        ("2017", "المحوّل", "أساس النماذج اللغوية الحديثة."),
        ("2022", "واجهة المحادثة", "الاستخدام بلغة طبيعية للجميع."),
        ("2023–26", "تعدد الوسائط", "وكلاء وتنظيم وعمل يومي."),
    ]
    kit.timeline(
        "fig-01-2.svg",
        "خط زمني مختصر",
        "محطات في رحلة طويلة… لا أعياد ميلاد للأدوات",
        milestones,
        "التواريخ إشارات للتحولات الكبرى؛ ما يهمك هو ما تغيّر في العمل والحياة.",
        h=680,
    )


# ---------------------------------------------------------------------------
# 2-1 — the data-learning cycle
# ---------------------------------------------------------------------------
def figure_02_1() -> None:
    kit.cycle(
        "fig-02-1.svg",
        "دورة التعلم من البيانات",
        "من البيانات الخام إلى نموذج يُقيَّم… ثم يعود",
        [
            ("جمع البيانات", "أمثلة كافية ومناسبة.", NAVY, TRY),
            ("تنظيف وتجهيز", "تكرار، قيم ناقصة، وحدات.", TEAL, IDEA),
            ("تدريب النموذج", "استخراج أنماط من الأمثلة.", GOLD, TIP),
            ("تقييم", "هل يعمم على بيانات جديدة؟", AMBER, WARNING),
            ("تحسين أو نشر", "عدّل البيانات أو النموذج.", GREEN, EXERCISE),
        ],
        "الدورة لا تنتهي عند التنبؤ؛ التقييم يعيدك إلى البيانات أو النموذج.",
        cy=420,
        ry=235,
        card_w=220,
        card_h=108,
        center_title="دورة التعلم",
        center_sub="بيانات ← نموذج ← تقييم",
        h=780,
    )


# ---------------------------------------------------------------------------
# 2-2 — three kinds of learning
# ---------------------------------------------------------------------------
def figure_02_2() -> None:
    kit.grid(
        "fig-02-2.svg",
        "ثلاثة أنواع من التعلم",
        "النوع يحدد البيانات والهدف، لا مستوى الذكاء",
        [
            ("بالإشراف", "بيانات موسومة.\nالهدف: تصنيف أو تنبؤ.\nمثال: بريد مزعج.", NAVY, TRY),
            ("بدون إشراف", "بيانات بلا وسوم.\nالهدف: اكتشاف أنماط.\nمثال: تقسيم عملاء.", TEAL, IDEA),
            ("بالتعزيز", "مكافأة وعقاب.\nالهدف: سياسة أفضل.\nمثال: لعبة أو روبوت.", GOLD, TIP),
        ],
        "النوع يحدد نوع البيانات والهدف؛ ولا يعني أن أحدها «أذكى» من الآخر.",
        cols=3,
        card_w=350,
        card_h=280,
        y=180,
        h=640,
        body_size=18,
        title_size=25,
    )


# ---------------------------------------------------------------------------
# 3-1 — from text to probability
# ---------------------------------------------------------------------------
def figure_03_1() -> None:
    parts: list[str] = []
    header(parts, "من النص إلى الاحتمال", "النموذج لا يقرأ معناك؛ يحسب ما يلي")
    cards = [
        ("النص", "«ذهبت إلى…»", NAVY, TRY),
        ("التقطيع", "كلمات أو رموز", TEAL, IDEA),
        ("التمثيل", "أرقام ومعانٍ", GOLD, TIP),
        ("الاحتمالات", "ما الكلمة التالية؟", AMBER, WARNING),
    ]
    w, gap = 250, 20
    x0 = (1200 - (4 * w + 3 * gap)) / 2
    xs = [x0 + (3 - i) * (w + gap) for i in range(4)]
    for index, (title, body, color, fill) in enumerate(cards):
        x = xs[index]
        parts.append(rect(x, 160, w, 125, fill=fill, stroke=color, stroke_width=2.5, shadow=True))
        parts.append(text(x + w / 2, 198, title, size=23, weight=700, fill=color))
        parts.append(text(x + w / 2, 238, body, size=16, fill=INK))
    for index in range(3):
        ax = xs[index] - gap / 2
        parts.append(path(f"M {ax + 7} 222 L {ax - 7} 232 L {ax + 7} 242", stroke=TEAL, width=3))

    # Probability panel
    parts.append(rect(120, 330, 960, 260, fill=TINT, stroke=BORDER, rx=20))
    parts.append(text(600, 372, "الكلمة التالية: احتمالات توضيحية", size=22, weight=700, fill=NAVY))
    rows = [("المساء", 42, TEAL), ("الصباح", 27, GOLD), ("الطريق", 15, AMBER), ("كلمة أخرى", 16, MUTED)]
    for index, (label, value, color) in enumerate(rows):
        y = 415 + index * 42
        # Track ends at 900 so the RTL label at 1055 never sits on a bar.
        parts.append(text(1055, y + 18, label, size=17, weight=600, fill=INK, anchor="start"))
        parts.append(rect(260, y, 640, 26, fill=BORDER, stroke=BORDER, rx=13))
        width = 640 * value / 100
        parts.append(rect(900 - width, y, width, 26, fill=color, stroke=color, rx=13))
        parts.append(text(235, y + 18, f"{value}%", size=16, weight=700, fill=color, anchor="end"))
    footer(parts, "الأرقام توضيحية، وليست ناتج نموذج حقيقي. النموذج يحسب احتمال ما يلي، لا حقيقة ما تقصده.", 650)
    save("fig-03-1.svg", "".join(parts), title="من النص إلى الاحتمال", height=700)


# ---------------------------------------------------------------------------
# 3-2 — the context window
# ---------------------------------------------------------------------------
def figure_03_2() -> None:
    parts: list[str] = []
    header(parts, "نافذة السياق", "ما يدخل… وما يُقطع حين يطول النص")
    parts.append(text(1080, 150, "بداية المحادثة", size=16, weight=600, fill=TEAL, anchor="start"))
    parts.append(text(120, 150, "الآن", size=16, weight=600, fill=AMBER, anchor="end"))
    parts.append(line(1080, 162, 130, 162, stroke=MUTED, width=2, marker="arrowMuted"))

    parts.append(rect(100, 190, 1000, 250, fill=TINT, stroke=NAVY, stroke_width=2.5, rx=20))
    tokens = ["بداية", "سياق", "هدف", "جمهور", "مصدر", "قيد", "سؤال", "مثال", "تفصيل", "ملاحظة", "نسخة", "قديمة"]
    x = 1040
    for index, token in enumerate(tokens):
        inside = index < 8
        fill = IDEA if inside else WARNING
        stroke = TEAL if inside else RED
        dash = None if inside else "5 4"
        parts.append(rect(x - 72, 240, 72, 72, fill=fill, stroke=stroke, stroke_width=2, rx=10, dash=dash, opacity=1 if inside else 0.55))
        parts.append(text(x - 36, 282, token, size=12, fill=INK if inside else MUTED))
        x -= 80

    # The boundary between what fits and what is cut.
    parts.append(line(400, 220, 400, 420, stroke=RED, width=2.5, dash="8 6", marker=False))
    parts.append(text(400, 468, "حدّ النافذة", size=15, weight=700, fill=RED))
    parts.append(path("M 416 218 L 1110 218", stroke=TEAL, width=2, marker=False))
    parts.append(path("M 1100 208 L 1110 218 L 1100 228", stroke=TEAL, width=2))
    parts.append(text(760, 208, "ما يصل إلى النموذج", size=15, weight=700, fill=TEAL))
    parts.append(path("M 390 498 L 110 498", stroke=RED, width=2, marker=False))
    parts.append(path("M 120 488 L 110 498 L 120 508", stroke=RED, width=2))
    parts.append(text(250, 526, "ما يُقطع أو يُفقد", size=15, weight=700, fill=RED))

    footer(parts, "لخّص، أو قسّم المهمة، أو ضع الأهم في البداية. النافذة ليست ذاكرة دائمة.", 590)
    save("fig-03-2.svg", "".join(parts), title="نافذة السياق", height=640)


# ---------------------------------------------------------------------------
# 4-1 — six functions of tools
# ---------------------------------------------------------------------------
def figure_04_1() -> None:
    kit.grid(
        "fig-04-1.svg",
        "الوظائف الست للأدوات",
        "ضع الأداة حيث تستخدمها فعلًا، لا حيث تصف نفسها",
        [
            ("الكتابة", "صياغة، تلخيص،\nتحرير، ترجمة.", NAVY, TRY),
            ("البحث", "مصادر، مقارنة،\nتحقق، تلخيص.", TEAL, IDEA),
            ("التحليل", "بيانات، أنماط،\nتفسير، رسم.", GOLD, TIP),
            ("الصور", "توليد، تحرير،\nوصف، فحص.", AMBER, WARNING),
            ("الصوت والفيديو", "تفريغ، ترجمة،\nتلخيص، بحث.", GREEN, EXERCISE),
            ("الأتمتة والوكلاء", "خطوات، أدوات،\nتنفيذ، توقف.", NAVY, TRY),
        ],
        "الأدوات الحديثة تتداخل؛ أداة واحدة قد تخدم أكثر من وظيفة.",
        cols=3,
        card_w=330,
        card_h=180,
        y=170,
        h=650,
        body_size=17,
    )


# ---------------------------------------------------------------------------
# 4-2 — tool-selection tree
# ---------------------------------------------------------------------------
def figure_04_2() -> None:
    kit.tree(
        "fig-04-2.svg",
        "شجرة اختيار الأداة",
        "ابدأ من نوع المادة، لا من اسم الأداة",
        ("ما نوع المادة؟", "حدد المهمة أولًا.", NAVY, TRY),
        [
            ("نص", "محادثة، تلخيص،\nتحرير، بحث.", TEAL, IDEA),
            ("صورة", "توليد، تحرير،\nتحليل، وصف.", GOLD, TIP),
            ("صوت وفيديو", "تفريغ، ترجمة،\nتلخيص، مقاطع.", AMBER, WARNING),
            ("بيانات وإجراء", "جدول، رسم،\nأتمتة، وكيل.", GREEN, EXERCISE),
        ],
        "إذا تعددت الإجابات، فالمهمة تحتاج سلسلة أدوات لا أداة واحدة.",
        h=720,
        card_h=180,
    )


# ---------------------------------------------------------------------------
# 6-1 — anatomy of a request
# ---------------------------------------------------------------------------
def figure_06_1() -> None:
    kit.layers(
        "fig-06-1.svg",
        "تشريح الطلب",
        "سبعة مكونات… بقدر ما تستحقه المهمة",
        [
            ("الدور", "انظر كمراجع نقدي، لا ككاتب ترويجي.", NAVY, TRY),
            ("الهدف", "لاتخاذ قرار بشأن حملة الشهر القادم.", TEAL, IDEA),
            ("السياق", "مدير تسويق، الجمهور: إدارة عليا.", GOLD, TIP),
            ("المهمة", "استخرج أكبر ثلاث فئات للشكاوى.", AMBER, WARNING),
            ("المدخلات", "ملف الشكاوى المرفق (120 شكوى).", GREEN, EXERCISE),
            ("الصيغة", "جدول من 4 أعمدة، 300 كلمة، عربية مبسطة.", NAVY, TRY),
            ("القيود والمعيار", "لا تخترع أرقامًا، واذكر عدد الشكاوى.", TEAL, IDEA),
        ],
        "ليس كل طلب يحتاج المكونات السبعة؛ المهمة الأهم تستحق تفصيلًا أكثر.",
        y=145,
        band_h=62,
        gap=8,
        h=720,
        body_size=14,
        title_size=19,
    )


# ---------------------------------------------------------------------------
# 6-2 — request evaluation loop
# ---------------------------------------------------------------------------
def figure_06_2() -> None:
    kit.cycle(
        "fig-06-2.svg",
        "حلقة تقييم الطلب",
        "جرّب… قارن… عدّل مكوّنًا واحدًا",
        [
            ("اكتب الطلب", "سبعة مكونات بحسب المهمة.", NAVY, TRY),
            ("جرّب", "نفّذ على حالة حقيقية.", TEAL, IDEA),
            ("قارن بالمعيار", "هل حقق ما وعدت به؟", GOLD, TIP),
            ("عدّل", "غيّر مكونًا واحدًا فقط.", AMBER, WARNING),
        ],
        "لا تغيّر كل شيء في مرة واحدة؛ وإلا لن تعرف ما الذي أحدث الفرق.",
        cy=400,
        ry=220,
        card_w=240,
        card_h=120,
        center_title="حلقة التقييم",
        center_sub="طلب ← نتيجة ← قرار",
        h=760,
        body_size=16,
        title_size=22,
    )


# ---------------------------------------------------------------------------
# 10-1 — six red lines
# ---------------------------------------------------------------------------
def figure_10_1() -> None:
    kit.grid(
        "fig-10-1.svg",
        "الخطوط الحمراء الستة",
        "ما لا تفعله… حتى لو كان سهلًا",
        [
            ("الملكية", "لا تلصق ما لا تملك\nحق مشاركته.", RED, WARNING),
            ("الحقيقة", "لا تنشر ما لم\nتتحقق منه.", AMBER, WARNING),
            ("القرار", "لا تترك قرارًا يؤثر\nعلى إنسان لآلة وحدها.", RED, WARNING),
            ("الهوية", "لا تنتحل صوت أحد\nأو صورته دون إذن.", AMBER, WARNING),
            ("الشفافية", "لا تخفِ أن المحتوى\nمولّد حين يكون الإخفاء مضللًا.", RED, WARNING),
            ("الصلاحية", "لا تمنح صلاحية أكبر\nمما تحتاجه المهمة.", AMBER, WARNING),
        ],
        "الخطوط ليست منفصلة؛ قد يجتمع خطان في موقف واحد. المهم أن تعرف أي خط تجاوزت.",
        cols=3,
        card_w=340,
        card_h=190,
        y=170,
        h=650,
        body_size=16,
    )


# ---------------------------------------------------------------------------
# 10-2 — risk traffic light
# ---------------------------------------------------------------------------
def figure_10_2() -> None:
    kit.traffic_light(
        "fig-10-2.svg",
        "إشارة المرور للمخاطر",
        "أربعة ألوان… أربعة قرارات",
        [
            ("أخضر", GREEN, "خطر منخفض، بيانات عامة، خطأ قابل للتصحيح.", "استخدم مع تحقق عادي", "تلخيص مقال منشور"),
            ("أصفر", GOLD, "خطر متوسط، بيانات داخلية أو قرار محدود.", "استخدم بضوابط ومراجعة بشرية", "بريد عمل، خطة درس"),
            ("أحمر", RED, "خطر مرتفع، بيانات حساسة أو أثر على حقوق.", "توقف، أو استخدم بيئة معتمدة", "عقود، بيانات طلاب"),
            ("أحمر داكن", DARK_RED, "خطر حرج، ضرر محتمل على سلامة أو حق.", "لا تفعل، وصعّد لمختص", "تشخيص طبي، قرار قانوني"),
        ],
        "إذا لم تعرف اللون، فاعتبره أصفر على الأقل؛ وإذا كان هناك احتمال ضرر على شخص، فاعتبره أحمر.",
        h=690,
    )


def build_all() -> None:
    figure_01_1()
    figure_01_2()
    figure_02_1()
    figure_02_2()
    figure_03_1()
    figure_03_2()
    figure_04_1()
    figure_04_2()
    figure_06_1()
    figure_06_2()
    figure_10_1()
    figure_10_2()
