"""Render each flow-*.svg in docs/images/ to a PNG beside it.

The SVGs are the source of truth and are what the README and DESIGN.md embed — GitHub scales
them crisply at any width. The PNGs exist for everywhere that does not take SVG: PowerPoint and
Keynote, LinkedIn and other social cards, Substack and most email clients, and anything headed
for print.

    python3 docs/images/src/render_png.py            # 2x — good for a full-bleed slide
    python3 docs/images/src/render_png.py --scale 3  # 3x — print, or a poster crop

Rendered through headless Chromium, which is already a dependency of `shoot_screenshots.py`:

    pip install playwright && playwright install chromium

Re-run this after regenerating any SVG, or the PNG silently goes stale. The diagrams carry an
explicit white background rect, so the PNGs are opaque white rather than transparent — which is
what you want on a slide, and the reason the SVGs render correctly against a dark GitHub theme.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

SIZE = re.compile(r'\bwidth="(\d+)"\s+height="(\d+)"')


def natural_size(svg: pathlib.Path) -> tuple[int, int]:
    """Read width/height off the root <svg>. They are always emitted by svgkit."""
    head = svg.read_text()[:600]
    m = SIZE.search(head)
    if not m:
        raise ValueError(f"{svg.name}: no width/height on the root <svg>")
    return int(m.group(1)), int(m.group(2))


def main() -> int:
    images = pathlib.Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scale", type=float, default=2.0,
                    help="pixel multiplier over the SVG's natural size (default: 2)")
    ap.add_argument("--dir", default=str(images), help="directory holding the SVGs")
    args = ap.parse_args()
    d = pathlib.Path(args.dir)

    svgs = sorted(d.glob("flow-*.svg"))
    if not svgs:
        print(f"no flow-*.svg under {d}", file=sys.stderr)
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright is not installed — pip install playwright && playwright install chromium",
              file=sys.stderr)
        return 2

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for svg in svgs:
            w, h = natural_size(svg)
            page = browser.new_page(viewport={"width": w, "height": h},
                                    device_scale_factor=args.scale)
            # The SVG is INLINED, not referenced as an <img src>. set_content gives the page an
            # about:blank origin, from which Chromium refuses to load a file:// subresource — that
            # renders a broken-image icon on a blank canvas, which looks like a bad diagram rather
            # than a blocked fetch. Inlining also means nothing has to load at all.
            page.set_content(
                '<style>html,body{margin:0;padding:0;overflow:hidden}'
                'svg{display:block}</style>' + svg.read_text())
            out = svg.with_suffix(".png")
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h})
            page.close()
            print(f"wrote {out}  ({int(w * args.scale)}x{int(h * args.scale)})")
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
