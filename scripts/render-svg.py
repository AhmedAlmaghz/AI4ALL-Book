#!/usr/bin/env python3
"""Render SVG figures to PNG with headless Chrome, without leaving Chrome running."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]
PROFILE = Path.home() / "AppData" / "Local" / "Temp" / "opencode-chrome-figures"


def chrome() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    raise SystemExit("Chrome or Edge was not found.")


def render(svg: Path, png: Path, width: int, height: int) -> bool:
    png.unlink(missing_ok=True)
    args = [
        str(chrome()),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        "--force-device-scale-factor=1",
        f"--user-data-dir={PROFILE}",
        f"--window-size={width},{height}",
        f"--screenshot={png}",
        f"file:///{svg.as_posix()}",
    ]
    process = subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    deadline = time.time() + 20
    try:
        while time.time() < deadline:
            if png.exists() and png.stat().st_size > 0:
                time.sleep(0.4)
                return True
            if process.poll() is not None:
                return png.exists() and png.stat().st_size > 0
            time.sleep(0.2)
        return False
    finally:
        if process.poll() is None:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: render-svg.py <svg> [<svg> ...]")
        return 2
    failed = 0
    for raw in sys.argv[1:]:
        svg = (ROOT / raw).resolve() if not Path(raw).is_absolute() else Path(raw)
        if not svg.exists():
            print("missing", svg)
            failed += 1
            continue
        # Read the SVG's declared size so the viewport matches the artwork.
        head = svg.read_text(encoding="utf-8")[:600]
        width, height = 1200, 800
        for token in ("width", "height"):
            marker = f'{token}="'
            index = head.find(marker)
            if index != -1:
                value = head[index + len(marker):].split('"', 1)[0]
                if value.isdigit():
                    if token == "width":
                        width = int(value)
                    else:
                        height = int(value)
        png = svg.with_name("_" + svg.stem + ".png")
        ok = render(svg, png, width, height)
        print(("ok  " if ok else "FAIL") + f" {png.name} {width}x{height}")
        if not ok:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
