"""Variant B — the four-act ribbon. Fewer words, bigger type: built for a slide, a LinkedIn
card or a post header rather than for close reading."""
import textwrap
from svgkit import (
    BG, BIP, GREY, INK, LINE, MONO,
    NAVY, NGX, OK, RED, SOFT, XC,
    arrow, kicker, line, path, rect, svg,
    text
)

W, H = 1400, 496
o = []


def mark(x, y, s=28, shield=INK):
    k = s / 24.0
    return (f'<g transform="translate({x},{y}) scale({k})">'
            f'<path d="M12 1.9 4 4.9v6.3c0 5.1 3.3 9 8 10.5 4.7-1.5 8-5.4 8-10.5V4.9L12 1.9Z" '
            f'fill="none" stroke="{shield}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<rect x="6.2" y="10.1" width="11.6" height="4.4" rx="2.2" '
            f'transform="rotate(-38 12 12.3)" fill="{RED}"/>'
            f'<circle cx="12" cy="12.3" r="1.05" fill="#fff"/></g>')


def wrap(s, n):
    return textwrap.wrap(s, n)


# ---------------------------------------------------------------- header
o.append(mark(40, 22, 28))
o.append(f'<text x="79" y="44" font-size="19" font-weight="800" fill="{INK}">'
         f'virtual-patch<tspan fill="{RED}">·</tspan>copilot</text>')
o.append(text(1360, 44, "the exposure window, from weeks to minutes", size=13, fill=GREY,
              anchor="end"))
o.append(line(40, 66, 1360, 66, stroke=LINE, sw=1))

# ---------------------------------------------------------------- four acts
ACTS = [
    (OK, "find", "Find what is really there",
     "Eight agents read your repo, a CVE, the dependency manifests or an OpenAPI spec — then "
     "adversarially refute the findings that do not hold up.",
     ["resolve", "discover", "verify"]),
    (XC, "route", "Pick the control that stops it",
     "Every surviving finding is routed to the strongest available control, or honestly to code "
     "when no band-aid can hold the line.",
     ["triage"]),
    (RED, "mitigate", "Patch it on the proxy you run",
     "One declarative band-aid for every F5 enforcement point, applied behind a human gate and "
     "fired at with the real exploit. If it does not block, it does not ship.",
     ["generate", "probe", "refine"]),
    (BIP, "cure", "Ship the fix, drop the patch",
     "A code-fix pull request for every finding, and a ledger that retires the band-aid once the "
     "cure actually lands.",
     ["remediate"]),
]
AX, AW, AGAP = 40, 300, 40
for i, (col, kick, ttl, body, tags) in enumerate(ACTS):
    x = AX + i * (AW + AGAP)
    y, h = 94, 250
    o.append(rect(x, y, AW, h, rx=14, fill=BG, stroke=LINE))
    o.append(rect(x, y, AW, 4, rx=2, fill=col))
    o.append(f'<circle cx="{x+34}" cy="{y+40}" r="16" fill="{col}"/>')
    o.append(text(x + 34, y + 46, str(i + 1), size=16, weight="800", fill="#fff", anchor="middle"))
    o.append(kicker(x + 60, y + 45, kick, fill=col, size=11.5))
    for j, ln in enumerate(wrap(ttl, 22)):
        o.append(text(x + 22, y + 88 + j * 22, ln, size=17.5, weight="800", fill=INK))
    for j, ln in enumerate(wrap(body, 40)):
        o.append(text(x + 22, y + 138 + j * 17, ln, size=11.5, fill=GREY))
    tx = x + 22
    for t in tags:
        tw = 9 + len(t) * 6.4
        o.append(rect(tx, y + h - 38, tw, 22, rx=11, fill=SOFT, stroke=LINE))
        o.append(text(tx + tw / 2, y + h - 23, t, size=10.5, weight="700", fill=INK,
                      anchor="middle", font=MONO))
        tx += tw + 7
    if i:
        o.append(arrow(x - AGAP + 8, y + 125, x - 9, y + 125, stroke=GREY, sw=2))

# ---------------------------------------------------------------- the enforcement footer
o.append(path("M870 348 L870 386", stroke=RED, sw=1.8, dash="5 4", marker="ar-red"))

o.append(rect(40, 390, 1320, 76, rx=14, fill=NAVY))
o.append(kicker(64, 418, "one band-aid, enforced on the F5 proxy you already run", fill="#ffffff"))
o.append(text(64, 440, "in priority order — the same finding, whichever box fronts your app",
              size=11, fill="#8d95a3"))
PROX = [(XC, "1", "F5 Distributed Cloud", "all 7 controls"),
        (NGX, "2", "F5 WAF for NGINX", "3 forms · live-proven"),
        (BIP, "3", "BIG-IP Advanced WAF", "3 forms · live-proven")]
px, pw, pgap = 604, 240, 12
for i, (col, n, ttl, sub) in enumerate(PROX):
    x = px + i * (pw + pgap)
    o.append(rect(x, 404, pw, 48, rx=10, fill="#22242a", stroke="#3a3d47"))
    o.append(rect(x, 404, 4, 48, rx=2, fill=col))
    o.append(text(x + 16, 423, f"{n} · {ttl}", size=12.5, weight="800", fill="#ffffff"))
    o.append(text(x + 16, 438, sub, size=10, fill="#8d95a3"))

open("../flow-hero.svg", "w").write(svg(
    W, H, "".join(o),
    title="virtual-patch-copilot — find, route, mitigate, cure",
    desc=("Four acts: eight agents find and refute vulnerabilities, route each to the strongest "
          "control, apply a proven band-aid on F5 Distributed Cloud, F5 WAF for NGINX or BIG-IP "
          "Advanced WAF, and ship the code fix that retires it.")))
print("wrote ../flow-hero.svg")
