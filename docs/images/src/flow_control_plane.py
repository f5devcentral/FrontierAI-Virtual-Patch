"""Variant C — control plane over data plane. The copilot reaches down into the proxy that
already sits in the request path, with three named verbs."""
from svgkit import (
    BG, BIP, CARD, GREY, INK, LINE,
    MONO, MUTE, NGX, OK, RED, SOFT,
    XC, arrow, chip, kicker, line, path,
    rect, svg, text
)

W, H = 1560, 712
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
o.append(mark(40, 22, 30))
o.append(f'<text x="82" y="46" font-size="21" font-weight="800" fill="{INK}">'
         f'virtual-patch<tspan fill="{RED}">·</tspan>copilot</text>')
o.append(text(1520, 46, "an agent control plane for the F5 proxy already in your request path",
              size=13, fill=GREY, anchor="end"))
o.append(line(40, 68, 1520, 68, stroke=LINE, sw=1))

# ================================================================ CONTROL PLANE
o.append(rect(40, 88, 1480, 302, rx=16, fill="#fbfbfc", stroke=LINE, extra='stroke-dasharray="6 5"'))
o.append(kicker(64, 114, "control plane · what the copilot decides"))

for i, (a, b) in enumerate([("source repo", "any language"),
                            ("CVE / advisory id", "via OSV.dev"),
                            ("dependency manifests", "lockfiles, pom.xml"),
                            ("OpenAPI spec", "+ spec-vs-code drift")]):
    y = 134 + i * 42
    o.append(rect(64, y, 190, 36, rx=9, fill=BG, stroke=LINE))
    o.append(text(76, y + 16, a, size=11.5, weight="700", fill=INK))
    o.append(text(76, y + 29, b, size=9.5, fill=GREY))
o.append(text(64, 320, "read-only — a scan writes nothing,", size=10, fill=GREY))
o.append(text(64, 334, "anywhere", size=10, fill=GREY))
o.append(arrow(262, 208, 296, 208, stroke=GREY, sw=1.8))

# ---- the agents
o.append(rect(304, 128, 700, 240, rx=14, fill=CARD))
o.append(kicker(326, 156, "8 agents · one model each", fill=MUTE))
o.append(text(982, 156, "config/agents.yaml", size=10, fill="#6f7684", anchor="end", font=MONO))
XS, CWID = [326, 494, 662, 830], 152
for (lbl, sub), x in zip([("resolve", "advisory → exploit"), ("discover", "source → findings"),
                          ("verify", "refute the weak ones"), ("triage", "pick the control")], XS, strict=True):
    o.append(chip(x, 170, CWID, 54, lbl, sub=sub, size=13))
for x in XS[:-1]:
    o.append(arrow(x + CWID + 3, 197, x + 164, 197, stroke="#5c6373", sw=1.5, marker="ar-mute"))
o.append(text(654, 242, "each verified finding → a band-aid now, a code fix next", size=10,
              fill="#7c8493", weight="600", anchor="middle"))
o.append(path("M906 224 L906 250 L402 250 L402 268", stroke="#5c6373", sw=1.5, marker="ar-mute"))
o.append(path("M906 250 L906 268", stroke="#5c6373", sw=1.5, marker="ar-mute"))
for (lbl, sub), x in zip([("generate", "write the policy"), ("probe", "derive the exploit"),
                          ("refine", "fix what didn't block"), ("remediate", "write the code fix")],
                         XS, strict=True):
    o.append(chip(x, 268, CWID, 54, lbl, sub=sub, size=13))
for x in XS[:2]:
    o.append(arrow(x + CWID + 3, 295, x + 164, 295, stroke="#5c6373", sw=1.5, marker="ar-mute"))
o.append(line(814, 270, 814, 322, stroke="#3a3d47", sw=1, dash="3 3"))
o.append(path("M738 322 L738 340 L402 340 L402 324", stroke=RED, sw=1.5, dash="4 4", marker="ar-red"))
o.append(text(570, 357, "it didn't block → diagnose and retry until it does", size=10,
              fill="#c8556c", weight="600", anchor="middle"))

# ---- outputs
o.append(arrow(1012, 248, 1042, 248, stroke=GREY, sw=1.8))
o.append(path("M1046 248 L1058 248", stroke=GREY, sw=1.5))
o.append(line(1058, 166, 1058, 330, stroke=GREY, sw=1.5))
OUT = [("the cure", "a code-fix pull request for every finding", 134),
       ("the ledger", "found → mitigated → remediated → retired", 214),
       ("the evidence", "every LB change, signed and exportable", 294)]
for ttl, sub, y in OUT:
    o.append(arrow(1058, y + 32, 1082, y + 32, stroke=GREY, sw=1.5))
    o.append(rect(1086, y, 410, 64, rx=12, fill=BG, stroke=LINE))
    o.append(text(1104, y + 27, ttl, size=13.5, weight="800", fill=INK))
    o.append(text(1104, y + 46, sub, size=10.5, fill=GREY))

# ================================================================ the three verbs
VERBS = [(RED, 400, "apply", "gated by a human · snapshot first · rollback on failure"),
         (OK, 660, "validate", "re-fire the finding's own exploit at the live policy"),
         (GREY, 920, "retire", "the cure merged — detach the band-aid, close the ledger")]
for col, x, ttl, sub in VERBS:
    o.append(path(f"M{x} 392 L{x} 452", stroke=col, sw=2,
                  marker="ar-red" if col == RED else ("ar-ok" if col == OK else "ar")))
    o.append(text(x + 12, 412, ttl, size=13, weight="800", fill=col))
    o.append(text(x + 12, 428, sub, size=10, fill=GREY))

# ================================================================ DATA PLANE
o.append(rect(40, 456, 1480, 232, rx=16, fill=SOFT, stroke=LINE))
o.append(kicker(64, 482, "data plane · where the band-aid actually enforces"))

o.append(rect(64, 508, 176, 92, rx=12, fill=BG, stroke=LINE))
o.append(text(152, 542, "users", size=14, weight="800", fill=INK, anchor="middle"))
o.append(text(152, 562, "+ attackers", size=14, weight="800", fill=RED, anchor="middle"))
o.append(text(152, 582, "the open internet", size=9.5, fill=GREY, anchor="middle"))
o.append(arrow(248, 554, 292, 554, stroke=GREY, sw=2))

o.append(rect(300, 496, 764, 172, rx=14, fill=BG, stroke=LINE))
o.append(text(316, 518, "the F5 proxy you already run", size=12, weight="800", fill=INK))
o.append(text(1048, 518, "in priority order", size=10, fill=GREY, anchor="end", weight="600"))
PROX = [(XC, "F5 Distributed Cloud", "SaaS edge · the default target",
         ["service_policy · waf", "waf_data_guard · api_schema",
          "malicious_user · bot_defense", "rate_limit"], None),
        (NGX, "F5 WAF for NGINX", "App Protect · your own box",
         ["service_policy", "waf_data_guard · api_schema"],
         "the other four decline, each with its reason"),
        (BIP, "BIG-IP Advanced WAF", "your own appliance",
         ["service_policy", "waf_data_guard · api_schema"],
         "the other four decline, each with its reason")]
for i, (col, ttl, sub, forms, note) in enumerate(PROX):
    x = 312 + i * 248
    o.append(rect(x, 530, 236, 124, rx=11, fill=BG, stroke=LINE))
    o.append(rect(x, 530, 4, 124, rx=2, fill=col))
    o.append(f'<circle cx="{x+28}" cy="{554}" r="12" fill="{col}"/>')
    o.append(text(x + 28, 559, str(i + 1), size=12.5, weight="800", fill="#fff", anchor="middle"))
    o.append(text(x + 48, 552, ttl, size=12.5, weight="800", fill=INK))
    o.append(text(x + 48, 566, sub, size=9.5, fill=GREY))
    for j, f in enumerate(forms):
        o.append(text(x + 16, 590 + j * 13, f, size=8.5, fill=col, font=MONO, weight="600"))
    if note:
        o.append(text(x + 16, 644, note, size=8.5, fill=GREY))

o.append(arrow(1072, 554, 1112, 554, stroke=OK, sw=2, marker="ar-ok"))
o.append(text(1092, 540, "clean", size=9.5, fill=OK, weight="700", anchor="middle"))
o.append(rect(1120, 508, 376, 92, rx=12, fill=BG, stroke=LINE))
o.append(text(1308, 542, "your application", size=15, weight="800", fill=INK, anchor="middle"))
o.append(text(1308, 562, "the origin — never touched by the band-aid", size=10.5, fill=GREY,
              anchor="middle"))
o.append(text(1308, 580, "the code fix lands here, on your schedule", size=10.5, fill=GREY,
              anchor="middle"))

open("../flow-control-plane.svg", "w").write(svg(
    W, H, "".join(o),
    title="virtual-patch-copilot — an agent control plane over the F5 data plane",
    desc=("A control plane of eight agents turns scan input into a band-aid policy, a code-fix PR, "
          "a ledger and signed evidence. It applies, validates and retires that policy on the F5 "
          "proxy already sitting between the internet and the untouched origin.")))
print("wrote ../flow-control-plane.svg")
