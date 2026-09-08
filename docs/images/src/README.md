# Diagram sources

The three flow diagrams in `docs/images/` are generated, not hand-drawn, so a change to the
pipeline is a one-line edit rather than a re-draw in some other tool.

| Script | Output | Used by |
|---|---|---|
| `flow_hero.py` | `../flow-hero.svg` | the top of `README.md` — four acts, big type, legible at GitHub's ~880px content width |
| `flow_pipeline.py` | `../flow-pipeline.svg` | `README.md` § How it works — the detailed pipeline; also the slide/print asset |
| `flow_control_plane.py` | `../flow-control-plane.svg` | `DESIGN.md` — control plane over the F5 data plane |

Regenerate (no dependencies beyond the standard library):

```bash
cd docs/images/src && python3 flow_hero.py && python3 flow_pipeline.py && python3 flow_control_plane.py
```

`svgkit.py` holds the shared primitives and the palette. Two constraints are deliberate and
worth keeping:

- **Presentation attributes only — no `<style>` block and no CSS classes.** GitHub sanitises
  SVG served through `<img>` and strips stylesheets on some paths; attributes always survive.
- **An explicit white background rect.** A transparent SVG is unreadable against GitHub's dark
  theme, and `prefers-color-scheme` inside an `<img>`-rendered SVG is not reliable.

Legibility is the binding constraint for anything destined for the README: GitHub renders it at
roughly 880px, so text below about 11px stops being readable. `flow-hero.svg` is sized for that;
`flow-pipeline.svg` is denser and is meant to be clicked through to full size.
