"""Re-capture the console and report screenshots used by README.md and docs/DEMO.md.

Run this whenever the shared UI chrome changes — the header, the step nav, the hero band.
Those screenshots are pictures of the product, so a header change silently makes every one
of them wrong, and they are the first thing a README reader sees. That is exactly how the
F5 logo survived its own removal for a while in 0.3.0.

    pip install -e ".[console]" && pip install playwright && playwright install chromium
    python3 demo/build_demo_out.py
    VPCOPILOT_OUT=demo/out vpcopilot console          # leave it running on :8787
    python3 docs/images/src/shoot_screenshots.py      # optionally --console-url / --out

Capture settings match the committed images: 1200 logical px wide at deviceScaleFactor 2, so
the PNGs land at 2400px. Trailing rows of flat page background are trimmed, because a
full-page capture pads a short step out to the full viewport height.

Not captured here: `4-mitigate.png`, `apply-your-own-waf.png` and `report-bigip-nginx.png` are
hand-framed crops of individual panels — several need a live BIG-IP or NGINX box to show
anything real, so they stay manual.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

WIDTH, SCALE, VIEWPORT_H = 1200, 2, 900

# (console step id, output file). The step id is the `#step-<id>` button in the nav.
CONSOLE_SHOTS = [("scan", "1-scan.png"), ("review", "2-review.png"),
                 ("simulate", "3-simulate.png"), ("retire", "6-retire.png")]
REPORT_SHOT = ("report.png", 860)   # a crop of the top of report.html, not the whole page


def trim_flat_bottom(path: pathlib.Path, pad: int = 32) -> None:
    """Drop trailing rows that are entirely the page background colour."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    w, h = im.size
    bg = im.getpixel((4, h - 4))
    y = h - 1
    while y > 0:
        colours = im.crop((0, y, w, y + 1)).getcolors(maxcolors=8)
        if colours is None or colours[0][1] != bg:
            break
        y -= 1
    new_h = min(h, y + 1 + pad)
    if new_h < h:
        im.crop((0, 0, w, new_h)).save(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--console-url", default="http://127.0.0.1:8787/",
                    help="a running console with VPCOPILOT_OUT pointed at the demo dataset")
    ap.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parents[1]),
                    help="directory to write the PNGs into (default: docs/images)")
    args = ap.parse_args()
    out = pathlib.Path(args.out)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright is not installed — pip install playwright && playwright install chromium",
              file=sys.stderr)
        return 2

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": VIEWPORT_H},
                                device_scale_factor=SCALE)
        page.goto(args.console_url, wait_until="networkidle")
        page.wait_for_timeout(1500)

        for step, name in CONSOLE_SHOTS:
            # A bare hash change is a same-document navigation and does NOT re-run the router,
            # so the step has to be switched by clicking its nav button. Assert afterwards:
            # capturing the wrong step looks plausible and is easy to miss in review.
            page.click(f"#step-{step}")
            page.wait_for_timeout(2500)
            active = page.eval_on_selector("section.active", "e => e.id")
            if active != step:
                print(f"expected section {step!r}, got {active!r}", file=sys.stderr)
                return 1
            path = out / name
            page.screenshot(path=str(path), full_page=True)
            trim_flat_bottom(path)
            print(f"wrote {path}")

        # The report is rebuilt from the run dir on every open, so the console's own link is
        # the freshest source for it.
        name, clip_h = REPORT_SHOT
        page.goto(args.console_url.rstrip("/") + "/report.html", wait_until="networkidle")
        page.wait_for_timeout(1200)
        path = out / name
        page.screenshot(path=str(path),
                        clip={"x": 0, "y": 0, "width": WIDTH, "height": clip_h})
        print(f"wrote {path}")
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
