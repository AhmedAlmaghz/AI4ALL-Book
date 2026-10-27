#!/usr/bin/env python3
"""فحص اتساق المخطوطة ومصفوفة الفصول.

الاستخدام:
    python scripts/check-manuscript.py

يعمل من جذر المشروع أو من أي مجلد داخل المشروع.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATRIX = ROOT / "docs" / "curriculum-matrix.csv"
MANUSCRIPT = ROOT / "manuscript"
FACT_LOG = ROOT / "docs" / "fact-check-log.csv"
SCREENSHOT_LOG = ROOT / "docs" / "screenshot-register.csv"

REQUIRED_SECTIONS = [
    "المشهد",
    "لماذا يهمك",
    "الفكرة الكبرى",
    "جرّب الآن",
    "قارن وقرر",
    "أخطاء ونصائح",
    "تمرين التحدي",
    "الخلاصة البصرية",
    "قائمة التحقق",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, parts[2]


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def check_matrix(rows: list[dict[str, str]]) -> list[str]:
    issues: list[str] = []
    if len(rows) != 34:
        issues.append(f"عدد صفوف المصفوفة {len(rows)} بدل 34.")
    chapters = [row.get("chapter", "").strip() for row in rows]
    if len(set(chapters)) != len(chapters):
        issues.append("توجد أرقام فصول مكررة في المصفوفة.")
    expected_chapters = {str(number) for number in range(1, 35)}
    if set(chapters) != expected_chapters:
        missing = sorted(expected_chapters - set(chapters), key=int)
        unexpected = sorted(set(chapters) - expected_chapters)
        if missing:
            issues.append(f"أرقام الفصول المفقودة من المصفوفة: {', '.join(missing)}.")
        if unexpected:
            issues.append(f"أرقام فصول غير متوقعة في المصفوفة: {', '.join(unexpected)}.")
    for row in rows:
        if not row.get("title") or not row.get("outcome"):
            issues.append(f"الفصل {row.get('chapter')}: عنوان أو مخرج ناقص.")
        try:
            target = int(row.get("words", "0"))
            if target < 2000 or target > 4500:
                issues.append(f"الفصل {row.get('chapter')}: عدد الكلمات المستهدف غير منطقي ({target}).")
        except ValueError:
            issues.append(f"الفصل {row.get('chapter')}: عدد الكلمات غير رقمي.")
    return issues


def check_chapters(rows: list[dict[str, str]]) -> tuple[list[str], list[dict[str, object]]]:
    issues: list[str] = []
    report: list[dict[str, object]] = []
    by_number = {row["chapter"]: row for row in rows}
    seen: set[str] = set()

    for path in sorted(MANUSCRIPT.rglob("ch*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)
        number = meta.get("chapter", "")
        title = meta.get("title", "")
        status = meta.get("status", "")
        words = word_count(body)

        if not number:
            issues.append(f"{path.name}: لا يوجد رقم فصل في البيانات الوصفية.")
            continue
        if number not in by_number:
            issues.append(f"{path.name}: رقم الفصل {number} غير موجود في المصفوفة.")
            continue
        if number in seen:
            issues.append(f"الفصل {number}: توجد أكثر من مخطوطة تحمل رقم الفصل نفسه.")
        seen.add(number)

        expected = by_number[number]
        if title and title != expected["title"]:
            issues.append(
                f"الفصل {number}: العنوان في الملف «{title}» لا يطابق المصفوفة «{expected['title']}»."
            )
        if status and status != expected["status"]:
            issues.append(
                f"الفصل {number}: الحالة في الملف «{status}» لا تطابق المصفوفة «{expected['status']}»."
            )

        for section in REQUIRED_SECTIONS:
            if section not in body:
                issues.append(f"الفصل {number}: القسم «{section}» مفقود.")

        target = int(expected.get("words", "0") or 0)
        ratio = round(words / target, 2) if target else 0
        report.append(
            {
                "chapter": int(number),
                "title": title,
                "status": status,
                "words": words,
                "target": target,
                "ratio": ratio,
                "file": str(path.relative_to(ROOT)),
            }
        )

    found = {item["chapter"] for item in report}
    for row in rows:
        number = int(row["chapter"])
        if number not in found and row["status"] in {"draft", "pilot", "review", "done"}:
            issues.append(f"الفصل {number}: حالته «{row['status']}» لكن لا يوجد ملف مخطوطة.")

    return issues, report


def check_logs() -> list[str]:
    issues: list[str] = []
    if not FACT_LOG.exists():
        return ["سجل التحقق غير موجود."]
    facts = read_csv(FACT_LOG)
    ids = [row.get("id", "") for row in facts]
    if any(not value.strip() for value in ids):
        issues.append("توجد سجلات تحقق بلا معرف.")
    if len(set(ids)) != len(ids):
        issues.append("توجد معرفات مكررة في سجل التحقق.")
    for row in facts:
        status = row.get("status", "").strip()
        if status not in {"pending", "verified", "partial", "rejected", "example", "editorial"}:
            issues.append(f"{row.get('id')}: حالة تحقق غير معروفة «{row.get('status')}».")
        if status in {"verified", "partial"} and not row.get("source_url", "").strip():
            issues.append(f"{row.get('id')}: الحالة «{status}» بلا رابط مصدر.")
        if status == "editorial" and not row.get("notes", "").strip():
            issues.append(f"{row.get('id')}: الادعاء التحريري بلا توضيح لأساسه أو حدوده.")
        if status == "pending" and not row.get("notes", "").strip():
            issues.append(f"{row.get('id')}: الادعاء المعلّق بلا خطوة تالية موثقة.")

    if SCREENSHOT_LOG.exists():
        shots = read_csv(SCREENSHOT_LOG)
        shot_ids = [row.get("id", "") for row in shots]
        if any(not value.strip() for value in shot_ids):
            issues.append("توجد سجلات بصرية بلا معرف.")
        if len(set(shot_ids)) != len(shot_ids):
            issues.append("توجد معرفات مكررة في سجل اللقطات.")
        valid_shot_statuses = {"placeholder", "simulation", "captured", "optional"}
        for row in shots:
            status = row.get("status", "").strip()
            if status not in valid_shot_statuses:
                issues.append(f"{row.get('id')}: حالة بصرية غير معروفة «{status}».")
            if status in {"simulation", "captured"}:
                required = ("tool", "date", "caption", "license", "alt_text")
                missing = [field for field in required if not row.get(field, "").strip()]
                if missing:
                    issues.append(
                        f"{row.get('id')}: سجل {status} ينقصه: {', '.join(missing)}."
                    )
            if status == "captured" and not row.get("version", "").strip():
                issues.append(f"{row.get('id')}: اللقطة الفعلية بلا رقم إصدار أو بيان عدم انطباقه.")
    return issues


def main() -> int:
    if not MATRIX.exists():
        print(f"لم يُعثر على المصفوفة: {MATRIX}")
        return 1

    rows = read_csv(MATRIX)
    fact_rows = read_csv(FACT_LOG) if FACT_LOG.exists() else []
    issues = check_matrix(rows)
    chapter_issues, report = check_chapters(rows)
    issues.extend(chapter_issues)
    issues.extend(check_logs())

    print("=" * 68)
    print("فحص المخطوطة — من الصفر إلى الاحتراف")
    print("=" * 68)
    print(f"الفصول في المصفوفة: {len(rows)}")
    print(f"ملفات المخطوطة: {len(report)}")
    fact_counts = Counter(row.get("status", "").strip() for row in fact_rows)
    if fact_counts:
        print(
            "سجل الادعاءات: "
            + ", ".join(
                f"{status}={fact_counts[status]}"
                for status in ("verified", "partial", "editorial", "example", "pending", "rejected")
                if fact_counts[status]
            )
        )
    print()

    print(f"{'الفصل':<6} {'الحالة':<9} {'الكلمات':<8} {'الهدف':<7} {'النسبة':<7} العنوان")
    print("-" * 68)
    for item in sorted(report, key=lambda value: value["chapter"]):
        print(
            f"{item['chapter']:<6} {item['status']:<9} {item['words']:<8} "
            f"{item['target']:<7} {item['ratio']:<7} {item['title']}"
        )

    total_words = sum(int(item["words"]) for item in report)
    total_target = sum(int(item["target"]) for item in report)
    print("-" * 68)
    print(f"إجمالي كلمات المسودات: {total_words:,}")
    print(f"إجمالي المستهدف للفصول المكتوبة: {total_target:,}")
    print()

    if issues:
        print(f"المشكلات ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("النتيجة: لا مشكلات بنيوية أو تعارضات في حالة السجلات.")
    if fact_counts["pending"] or fact_counts["partial"]:
        print(
            "تنبيه: وجود سجلات pending أو partial يعني أن دقة المحتوى غير مكتملة؛ "
            "نجاح فحص الاتساق لا يغلق بوابة التحقق الواقعي."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
