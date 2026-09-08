"""Variant A — the hero pipeline. Left-to-right: input -> agents -> the F5 proxy -> your app,
with the lifecycle strip underneath."""
from svgkit import (
    BG, BIP, CARD, GREY, INK, LINE,
    MONO, MUTE, NGX, OK, RED, SOFT,
    XC, arrow, chip, kicker, line, path,
    rect, svg, text
)

W, H = 1600, 676
o = []


def mark(x, y, s=30, shield=INK):
    k = s / 24.0
    return (f'<g transform="translate({x},{y}) scale({k})">'
            f'<path d="M12 1.9 4 4.9v6.3c0 5.1 3.3 9 8 10.5 4.7-1.5 8-5.4 8-10.5V4.9L12 1.9Z" '
            f'fill="none" stroke="{shield}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<rect x="6.2" y="10.1" width="11.6" height="4.4" rx="2.2" '
            f'transform="rotate(-38 12 12.3)" fill="{RED}"/>'
            f'<circle cx="12" cy="12.3" r="1.05" fill="#fff"/></g>')


# ---------------------------------------------------------------- header
o.append(mark(40, 24, 30))
o.append(f'<text x="82" y="48" font-size="21" font-weight="800" fill="{INK}">'
         f'virtual-patch<tspan fill="{RED}">·</tspan>copilot</text>')
o.append(text(1560, 40, "Find the vulnerability. Mitigate it live on the F5 proxy you already run.",
              size=13, fill=GREY, anchor="end"))
o.append(text(1560, 59, "Ship the code fix. Retire the band-aid.", size=13, fill=GREY, anchor="end"))
o.append(line(40, 80, 1560, 80, stroke=LINE, sw=1))

# ---------------------------------------------------------------- col 1 : scan input
o.append(kicker(40, 118, "scan input"))
for i, (a, b) in enumerate([("source repo", "any language"),
                            ("CVE / advisory id", "resolved via OSV.dev"),
                            ("dependency manifests", "lockfiles, pom.xml"),
                            ("OpenAPI spec", "+ spec-vs-code drift")]):
    y = 134 + i * 42
    o.append(rect(40, y, 200, 36, rx=9, fill=SOFT, stroke=LINE))
    o.append(text(52, y + 16, a, size=12, weight="700", fill=INK))
    o.append(text(52, y + 29, b, size=9.5, fill=GREY))
o.append(text(40, 320, "read-only · a scan makes no cloud or repo writes", size=10, fill=GREY,
              weight="600"))

o.append(kicker(40, 372, "guardrails"))
for i, g in enumerate(["dry-run is the default",
                       "every apply snapshots first",
                       "protected load balancers refuse mutation",
                       "any failure rolls back automatically",
                       "a human gate on every live change"]):
    y = 392 + i * 19
    o.append(f'<circle cx="45" cy="{y - 4}" r="2.5" fill="{RED}"/>')
    o.append(text(56, y, g, size=10.5, fill=GREY))

o.append(arrow(248, 214, 292, 214, stroke=GREY, sw=1.8))

# ---------------------------------------------------------------- col 2 : the agents
CX, CW = 300, 700
o.append(rect(CX, 100, CW, 370, rx=14, fill=CARD))
o.append(kicker(322, 130, "the copilot · 8 agents", fill=MUTE))
o.append(text(978, 130, "one loop, one finding at a time", size=10.5, fill="#6f7684", anchor="end"))

XS, CWID = [322, 490, 658, 826], 152
o.append(text(322, 160, "find — is it real, and what stops it?", size=10.5, fill="#7c8493",
              weight="600"))
for (lbl, sub), x in zip([("resolve", "advisory → exploit"), ("discover", "source → findings"),
                          ("verify", "refute the weak ones"), ("triage", "pick the control")], XS, strict=True):
    o.append(chip(x, 168, CWID, 56, lbl, sub=sub, size=13.5))
for x in XS[:-1]:
    o.append(arrow(x + CWID + 3, 196, x + 164, 196, stroke="#5c6373", sw=1.5, marker="ar-mute"))

o.append(text(650, 240, "each verified finding → the band-aid now, the code fix next", size=10.5,
              fill="#7c8493", weight="600", anchor="middle"))
o.append(path("M902 224 L902 248 L398 248 L398 270", stroke="#5c6373", sw=1.5, marker="ar-mute"))
o.append(path("M902 248 L902 270", stroke="#5c6373", sw=1.5, marker="ar-mute"))

for (lbl, sub), x in zip([("generate", "write the policy"), ("probe", "derive the exploit"),
                          ("refine", "fix what didn't block"), ("remediate", "write the code fix")],
                         XS, strict=True):
    o.append(chip(x, 270, CWID, 56, lbl, sub=sub, size=13.5))
for x in XS[:2]:
    o.append(arrow(x + CWID + 3, 298, x + 164, 298, stroke="#5c6373", sw=1.5, marker="ar-mute"))
o.append(line(810, 272, 810, 324, stroke="#3a3d47", sw=1, dash="3 3"))
o.append(text(818, 262, "the cure", size=9.5, fill="#6f7684", weight="700"))
o.append(text(322, 262, "the band-aid — proven, not assumed", size=9.5, fill="#6f7684",
              weight="700"))

o.append(path("M734 326 L734 348 L398 348 L398 328", stroke=RED, sw=1.5, dash="4 4",
              marker="ar-red"))
o.append(text(566, 366, "the policy didn't block → diagnose and retry until it does",
              size=10.5, fill="#c8556c", weight="600", anchor="middle"))
o.append(line(322, 386, 978, 386, stroke="#2e313a", sw=1))
o.append(text(322, 408, "a deterministic linter rejects a self-defeating policy before any live "
                        "round-trip", size=10.5, fill="#7c8493"))
o.append(text(322, 430, "model-independent — Claude, OpenAI, Gemini or local Ollama, chosen per "
                        "agent in config/agents.yaml", size=10.5, fill="#7c8493"))
o.append(text(322, 452, "one declarative band-aid, emitted for every enforcement point below",
              size=10.5, fill="#7c8493"))

o.append(arrow(1008, 294, 1062, 294, stroke=RED, sw=2, marker="ar-red"))
o.append(text(1035, 281, "band-aid", size=10, fill=RED, weight="700", anchor="middle"))

# ---------------------------------------------------------------- col 3 : enforcement
EX, EW = 1070, 490
o.append(kicker(EX, 118, "enforce · the F5 proxy you already run"))
o.append(text(EX + EW, 118, "in priority order", size=10.5, fill=GREY, anchor="end", weight="600"))
POINTS = [
    (XC, "F5 Distributed Cloud", "SaaS edge · the default target · all 7 controls",
     [("service_policy · waf · waf_data_guard · api_schema", "mono"),
      ("malicious_user · bot_defense · rate_limit", "mono")]),
    (NGX, "F5 WAF for NGINX (App Protect)", "your own box · 3 forms, every one live-proven",
     [("service_policy · waf_data_guard · api_schema", "mono"),
      ("waf, rate_limit, malicious_user, bot_defense — declined, each with its reason", "note")]),
    (BIP, "BIG-IP Advanced WAF", "your own appliance · 3 forms, every one live-proven",
     [("service_policy · waf_data_guard · api_schema", "mono"),
      ("waf, rate_limit, malicious_user, bot_defense — declined, each with its reason", "note")]),
]
for i, (col, ttl, sub, lines) in enumerate(POINTS):
    y = 140 + i * 104
    o.append(rect(EX, y, EW, 96, rx=12, fill=BG, stroke=LINE))
    o.append(rect(EX, y, 5, 96, rx=2.5, fill=col))
    o.append(f'<circle cx="{EX+32}" cy="{y+30}" r="13" fill="{col}"/>')
    o.append(text(EX + 32, y + 35, str(i + 1), size=13.5, weight="800", fill="#fff", anchor="middle"))
    o.append(text(EX + 56, y + 28, ttl, size=14.5, weight="800", fill=INK))
    o.append(text(EX + 56, y + 47, sub, size=11, fill=GREY))
    for j, (s, kind) in enumerate(lines):
        yy = y + 68 + j * 15
        if kind == "mono":
            o.append(text(EX + 56, yy, s, size=9.5, fill=col, font=MONO, weight="600"))
        else:
            o.append(text(EX + 56, yy, s, size=9.5, fill=GREY))

o.append(arrow(EX + EW / 2, 444, EX + EW / 2, 460, stroke=GREY, sw=1.6))
o.append(rect(EX, 464, EW, 48, rx=12, fill=SOFT, stroke=LINE))
o.append(text(EX + EW / 2, 486, "your application · the origin", size=13.5, weight="800",
              fill=INK, anchor="middle"))
o.append(text(EX + EW / 2, 502, "untouched — the attack is stopped in front of it", size=10,
              fill=GREY, anchor="middle"))

# ---------------------------------------------------------------- lifecycle strip
o.append(rect(40, 534, 1520, 112, rx=14, fill=SOFT, stroke=LINE))
o.append(kicker(64, 562, "after the apply — the band-aid is temporary by construction"))
o.append(text(64, 582, "every mutating step is appended to an audit trail and exports as a",
              size=10.5, fill=GREY))
o.append(text(64, 597, "SHA-256-manifested evidence bundle for a change board.", size=10.5,
              fill=GREY))

STEPS = [(OK, "found", "verified, not guessed"),
         (RED, "mitigated", "live band-aid, proven"),
         (XC, "remediated", "the code-fix PR merges"),
         (BIP, "reconciled", "exploit re-fired at the origin"),
         (GREY, "retired", "the band-aid is detached")]
sx, sw_, gap = 480, 196, 22
for i, (col, lbl, sub) in enumerate(STEPS):
    x = sx + i * (sw_ + gap)
    o.append(rect(x, 566, sw_, 52, rx=10, fill=BG, stroke=LINE))
    o.append(rect(x, 566, 4, 52, rx=2, fill=col))
    o.append(text(x + 14, 586, lbl, size=12.5, weight="800", fill=INK))
    o.append(text(x + 14, 603, sub, size=9, fill=GREY))
    if i:
        o.append(arrow(x - gap + 3, 592, x - 5, 592, stroke=GREY, sw=1.4))

open("../flow-pipeline.svg", "w").write(svg(
    W, H, "".join(o),
    title="virtual-patch-copilot — from a finding to a live F5 band-aid to the code fix",
    desc=("Scan inputs feed eight agents. The agents find and verify a vulnerability, pick the "
          "strongest control, write the band-aid policy and prove it blocks the real exploit. "
          "The band-aid applies to F5 Distributed Cloud, F5 WAF for NGINX, or BIG-IP Advanced WAF "
          "in front of the untouched origin, and is retired once the code-fix PR merges.")))
print("wrote ../flow-pipeline.svg")
