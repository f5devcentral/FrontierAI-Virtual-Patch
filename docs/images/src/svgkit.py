"""Tiny SVG primitives shared by the diagram variants.

Deliberately emits presentation attributes (no <style> block, no CSS classes) because GitHub
sanitises SVG rendered through <img> and strips stylesheets in some paths. Everything here
survives that: attributes, <defs><marker>, <text>.
"""
from html import escape

FONT = "Aptos,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

INK   = "#17181c"
NAVY  = "#111317"
CARD  = "#1c1e24"
CHIP  = "#262931"
EDGE  = "#3a3d47"
RED   = "#e4002b"
GREY  = "#6a7282"
MUTE  = "#9aa1ad"
LINE  = "#dcdade"
BG    = "#ffffff"
SOFT  = "#f6f6f8"
XC    = "#0e41aa"
NGX   = "#00843d"
BIP   = "#61228b"
OK    = "#009639"
AMBER = "#b45a00"


def esc(s):
    return escape(str(s), quote=True)


def rect(x, y, w, h, rx=10, fill=BG, stroke=None, sw=1, extra=""):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    return s + f' {extra}/>'


def text(x, y, s, size=13, fill=INK, weight="400", anchor="start", font=FONT, ls=None, op=None):
    a = f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"'
    if ls is not None:
        a += f' letter-spacing="{ls}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + f'>{esc(s)}</text>'


def kicker(x, y, s, fill=GREY, size=11):
    """Small-caps section label."""
    return text(x, y, s.upper(), size=size, fill=fill, weight="700", ls="1.4")


def line(x1, y1, x2, y2, stroke=LINE, sw=1.5, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')


def path(d, stroke=LINE, sw=1.5, fill="none", dash=None, marker=None, cap="round"):
    a = f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round"'
    if dash:
        a += f' stroke-dasharray="{dash}"'
    if marker:
        a += f' marker-end="url(#{marker})"'
    return a + "/>"


def arrow(x1, y1, x2, y2, stroke=GREY, sw=1.6, marker="ar", dash=None):
    return path(f"M{x1} {y1} L{x2} {y2}", stroke=stroke, sw=sw, dash=dash, marker=marker)


def markers():
    """One marker per colour we point with. `context-stroke` is not reliable in GitHub's
    renderer, so each arrowhead colour is declared explicitly."""
    out = []
    for name, col in (("ar", GREY), ("ar-red", RED), ("ar-ink", INK), ("ar-ok", OK),
                      ("ar-white", "#ffffff"), ("ar-mute", MUTE), ("ar-xc", XC)):
        out.append(
            f'<marker id="{name}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M0 0.8 L9 5 L0 9.2 z" fill="{col}"/></marker>')
    return "<defs>" + "".join(out) + "</defs>"


def svg(w, h, body, bg=BG, title="", desc=""):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" font-family="{FONT}" role="img"'
            + (f' aria-label="{esc(title)}"' if title else "") + ">")
    meta = (f"<title>{esc(title)}</title>" if title else "") + \
           (f"<desc>{esc(desc)}</desc>" if desc else "")
    return (head + meta + markers()
            + rect(0, 0, w, h, rx=0, fill=bg) + body + "</svg>")


def chip(x, y, w, h, label, *, fill=CHIP, stroke=EDGE, fg="#ffffff", size=12.5,
         weight="700", rx=8, sub=None, subfg=MUTE, subsize=10):
    """A labelled pill. With `sub`, the label sits high and the sub-label beneath it."""
    o = [rect(x, y, w, h, rx=rx, fill=fill, stroke=stroke)]
    if sub:
        o.append(text(x + w / 2, y + h / 2 - 2, label, size=size, fill=fg, weight=weight, anchor="middle"))
        o.append(text(x + w / 2, y + h / 2 + 12, sub, size=subsize, fill=subfg, weight="500", anchor="middle"))
    else:
        o.append(text(x + w / 2, y + h / 2 + size * 0.36, label, size=size, fill=fg,
                      weight=weight, anchor="middle"))
    return "".join(o)
