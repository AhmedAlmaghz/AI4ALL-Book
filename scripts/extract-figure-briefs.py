#!/usr/bin/env python3
"""Extract a compact brief for every figure declared in the manuscript.

The brief keeps the real caption, the nearest section heading, the author's
comment, the following table or paragraphs, and the visual-plan line. It is a
working document for illustration, not a publication artifact.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
OUT = ROOT / "docs" / "figure-briefs.md"


def chapter_files() -> list[Path]:
    return sorted(MANUSCRIPT.glob("**/ch*.md"))


def nearest_heading(lines: list[str], index: int) -> str:
    for cursor in range(index - 1, -1, -1):
        if lines[cursor].startswith("## "):
            return lines[cursor].strip("# ").strip()
        if lines[cursor].startswith("# "):
            return lines[cursor].strip("# ").strip()
    return "—"


def context_after(lines: list[str], index: int, limit: int = 16) -> list[str]:
    context: list[str] = []
    for line in lines[index + 1:]:
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            break
        if re.match(r"^\*\*الشكل\s+\d+-\d+:", stripped):
            break
        if stripped:
            context.append(stripped)
        if len(context) >= limit:
            break
    return context


def extract(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    chapter = int(re.search(r"ch(\d+)", path.stem).group(1))
    declared = {
        match.group(1): match.group(2).strip()
        for match in re.finditer(r'^  - "شكل (\d+-\d+):([^"]+)"', text, re.M)
    }

    blocks: list[str] = []
    seen: set[str] = set()
    for index, line in enumerate(lines):
        match = re.match(
            rf"^\*\*الشكل\s+0?{chapter}-(\d+):\*\*\s*(.+?)\s*$", line
        )
        if not match:
            continue
        figure_id = f"{chapter}-{match.group(1)}"
        if figure_id in seen:
            continue
        seen.add(figure_id)
        caption = match.group(2).strip()
        heading = nearest_heading(lines, index)
        context = context_after(lines, index)
        plan = ""
        plan_match = re.search(
            rf"^\s*-\s*شكل\s+0?{chapter}-{match.group(1)}:\s*(.+)$", text, re.M
        )
        if plan_match:
            plan = plan_match.group(1).strip()

        declared_caption = declared.get(figure_id, "—")
        mismatch = ""
        if declared_caption != "—" and declared_caption != caption:
            mismatch = f"\n- **تنبيه:** الوصف في بيانات الفصل يخالف التعليق: «{declared_caption}»"

        blocks.append(
            "\n".join(
                [
                    f"## شكل {figure_id} — {caption}",
                    "",
                    f"- **القسم:** {heading}",
                    f"- **خطة المخطط:** {plan or '—'}{mismatch}",
                    "",
                    "**السياق:**",
                    "",
                    *[f"> {item}" for item in context[:12]],
                    "",
                ]
            )
        )
    return blocks


def main() -> None:
    chunks = [
        "# موجزات الأشكال",
        "",
        "ملف عمل لتصميم الرسوم. يُستخرج آليًا من المخطوطة؛ التعليق الحقيقي في المتن هو المرجع.",
        "",
    ]
    total = 0
    for path in chapter_files():
        blocks = extract(path)
        if blocks:
            total += len(blocks)
            chunks.append(f"\n# {path.stem}\n")
            chunks.extend(blocks)
    OUT.write_text("\n".join(chunks), encoding="utf-8")
    print(f"wrote {OUT} ({total} figures)")


if __name__ == "__main__":
    main()
