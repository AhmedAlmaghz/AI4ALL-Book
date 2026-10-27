"""Audit every source URL in docs/fact-check-log.csv.

The audit answers one narrow question: does the URL respond to an automated
request? It does not verify that the source supports the claim. Redirects are
reported but not treated as failures. Sites that block automated clients are
reported separately from genuinely missing pages.

Usage:
    python -X utf8 scripts/audit-source-links.py
    python -X utf8 scripts/audit-source-links.py --fail-on-dead
"""

from __future__ import annotations

import argparse
import csv
import re
import ssl
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "docs" / "fact-check-log.csv"
DEFAULT_OUTPUT = ROOT / "docs" / "source-link-audit.md"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
    "Accept-Language": "ar,en;q=0.8",
}

# URLs that return 403/404 to automated clients but were opened successfully in
# a real browser. Keep this list short, dated, and tied to a manual check.
MANUAL_VERIFIED = {
    "https://www.ftc.gov/business-guidance/advertising-marketing": (
        "2026-10-27",
        "صفحة «Advertising and Marketing» مفتوحة في المتصفح رغم 404 للعميل الآلي.",
    ),
    "https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business": (
        "2026-10-27",
        "دليل CAN-SPAM مفتوح في المتصفح رغم 404 للعميل الآلي.",
    ),
    "https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers": (
        "2026-10-27",
        "أسئلة وأجوبة قاعدة المراجعات مفتوحة في المتصفح رغم 404 للعميل الآلي.",
    ),
}

BLOCKED_STATUSES = {401, 403, 405, 429}
DEAD_STATUSES = {404, 410}


def split_urls(value: str) -> list[str]:
    return [part.strip() for part in re.split(r";\s*", value) if part.strip()]


def collect_urls(csv_path: Path) -> tuple[dict[str, list[str]], int]:
    by_url: dict[str, list[str]] = defaultdict(list)
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    for row in rows:
        for url in split_urls(row.get("source_url", "")):
            by_url[url].append(row["id"])
    return dict(by_url), len(rows)


def check(url: str, timeout: int) -> dict[str, object]:
    started = time.time()
    result: dict[str, object] = {
        "url": url,
        "status": None,
        "final_url": "",
        "error": "",
        "seconds": 0.0,
    }
    request = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response.read(2048)
            result["status"] = response.status
            result["final_url"] = response.geturl()
    except urllib.error.HTTPError as exc:
        result["status"] = exc.code
        result["final_url"] = exc.geturl() or ""
        result["error"] = f"HTTP {exc.code}: {exc.reason}"
    except ssl.SSLError as exc:
        result["error"] = f"SSL: {exc}"
    except Exception as exc:  # noqa: BLE001 - the audit needs the message
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["seconds"] = round(time.time() - started, 1)
    return result


def classify(result: dict[str, object]) -> str:
    status = result["status"]
    url = str(result["url"])
    if status is None:
        return "unreachable"
    if 200 <= int(status) < 300:
        return "ok"
    if int(status) in BLOCKED_STATUSES:
        return "blocked"
    if int(status) in DEAD_STATUSES:
        return "manual" if url in MANUAL_VERIFIED else "dead"
    return "error"


def record_ids(url: str, by_url: dict[str, list[str]]) -> str:
    return "، ".join(by_url.get(url, [])) or "—"


def table(rows: list[dict[str, object]], by_url: dict[str, list[str]], with_error: bool) -> list[str]:
    if not rows:
        return ["لا توجد مدخلات في هذه الفئة.", ""]
    lines = ["| الرابط | السجلات | الحالة | ملاحظة |", "|---|---|---|---|"]
    for result in rows:
        status = result["status"] if result["status"] is not None else "—"
        note = str(result["final_url"] or result["error"] or "—")
        lines.append(
            f"| {result['url']} | {record_ids(str(result['url']), by_url)} | {status} | {note} |"
        )
    if with_error:
        lines.append("")
        lines.append("> «محجوب آليًا» لا يعني أن الرابط ميت؛ تعيد مواقع كثيرة 403 أو 404 لبرامج الزحف.")
    lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--fail-on-dead", action="store_true")
    args = parser.parse_args()

    by_url, record_count = collect_urls(args.csv)
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check, url, args.timeout): url for url in by_url}
        for future in as_completed(futures):
            results.append(future.result())

    for result in results:
        result["kind"] = classify(result)

    results.sort(key=lambda item: (str(item["kind"]), str(item["url"])))
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for result in results:
        groups[str(result["kind"])].append(result)

    redirects = [
        result
        for result in results
        if result["final_url"]
        and str(result["final_url"]).rstrip("/") != str(result["url"]).rstrip("/")
        and result["kind"] in {"ok", "blocked", "manual"}
    ]

    today = date.today().isoformat()
    try:
        csv_label = args.csv.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        csv_label = str(args.csv)
    lines = [
        "# تدقيق روابط المصادر",
        "",
        f"- تاريخ التدقيق: {today}",
        f"- المصدر: `{csv_label}` — {record_count} سجلًا.",
        f"- الروابط الفريدة: {len(results)}",
        "- المنهج: طلب GET آلي بترويسات متصفح، مع متابعة إعادة التوجيه ومهلة "
        f"{args.timeout} ثانية. النتيجة تتحقق من الاستجابة فقط، لا من مطابقة المحتوى للادعاء.",
        "",
        "## 1. الخلاصة",
        "",
        "| الحالة | العدد | المعنى |",
        "|---|---|---|",
        f"| مستجيب | {len(groups['ok'])} | استجابة 2xx. |",
        f"| إعادة توجيه | {len(redirects)} | الرابط يعمل لكنه ينتقل إلى عنوان آخر. |",
        f"| محجوب آليًا | {len(groups['blocked'])} | 401/403/405/429؛ ليس دليل موت. |",
        f"| غير موجود | {len(groups['dead'])} | 404/410 دون تحقق يدوي. |",
        f"| خطأ أو مهلة | {len(groups['unreachable']) + len(groups['error'])} | تعذر إكمال الطلب. |",
        f"| تحقق يدوي | {len(groups['manual'])} | أعاد العميل الآلي 404 لكن الصفحة تعمل في المتصفح. |",
        "",
        "## 2. روابط تحتاج إجراء",
        "",
        "### 2.1 غير موجودة (404/410)",
        "",
    ]
    lines.extend(table(groups["dead"], by_url, with_error=False))
    lines.extend(["### 2.2 محجوبة آليًا (ليست دليل موت)", ""])
    lines.extend(table(groups["blocked"], by_url, with_error=True))
    lines.extend(["### 2.3 أخطاء شبكة أو مهلة", ""])
    lines.extend(table(groups["unreachable"] + groups["error"], by_url, with_error=False))

    lines.extend(
        [
            "## 3. إعادة التوجيه",
            "",
            "| الرابط في السجل | الرابط النهائي | السجلات |",
            "|---|---|---|",
        ]
    )
    for result in redirects:
        lines.append(
            f"| {result['url']} | {result['final_url']} | {record_ids(str(result['url']), by_url)} |"
        )
    if not redirects:
        lines.append("| — | — | — |")
    lines.append("")

    lines.extend(
        [
            "## 4. تحقق يدوي",
            "",
            "| الرابط | تاريخ التحقق | النتيجة |",
            "|---|---|---|",
        ]
    )
    manual_rows = [result for result in results if result["kind"] == "manual"]
    for result in manual_rows:
        verified_on, note = MANUAL_VERIFIED[str(result["url"])]
        lines.append(f"| {result['url']} | {verified_on} | {note} |")
    if not manual_rows:
        lines.append("| — | — | — |")
    lines.append("")

    stale_manual = sorted(set(MANUAL_VERIFIED) - set(by_url))
    if stale_manual:
        lines.extend(
            [
                "## 5. ملاحظات",
                "",
                "مدخلات تحقق يدوي لا تظهر في السجل الحالي:",
                "",
            ]
        )
        lines.extend(f"- {url}" for url in stale_manual)
        lines.append("")

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.output}")
    print(
        f"unique URLs: {len(results)} | ok: {len(groups['ok'])} | "
        f"redirects: {len(redirects)} | blocked: {len(groups['blocked'])} | "
        f"dead: {len(groups['dead'])} | unreachable/error: "
        f"{len(groups['unreachable']) + len(groups['error'])} | manual: {len(groups['manual'])}"
    )
    if groups["dead"]:
        for result in groups["dead"]:
            print(f"DEAD\t{result['url']}")
    return 1 if args.fail_on_dead and groups["dead"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
